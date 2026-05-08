"""聊天 API - 多 Agent 并行响应"""
from fastapi import APIRouter
from fastapi.responses import StreamingResponse
import asyncio
import json

from backend.models.schemas import ChatRequest, ChatResponse, AgentInfo
from backend.agents.orchestrator import AgentOrchestrator
from backend.services.session_service import SessionService
from backend.services.openai_service import OpenAIService
from backend.core.emotion_engine import EmotionEngine

router = APIRouter(prefix="/api", tags=["chat"])

# 延迟初始化的全局单例
_orchestrator: AgentOrchestrator | None = None
_session_service: SessionService | None = None


def get_orchestrator() -> AgentOrchestrator:
    global _orchestrator
    if _orchestrator is None:
        openai_service = OpenAIService()
        emotion_engine = EmotionEngine()
        _orchestrator = AgentOrchestrator(openai_service, emotion_engine)
    return _orchestrator


def get_session_service() -> SessionService:
    global _session_service
    if _session_service is None:
        _session_service = SessionService()
    return _session_service


@router.get("/agents", response_model=list[AgentInfo])
async def list_agents():
    """获取所有可用的 Agent 列表"""
    return get_orchestrator().get_agent_list()


@router.post("/chat", response_model=ChatResponse)
async def chat(request: ChatRequest):
    """多 Agent 并行回答用户问题"""
    session = get_session_service().get_or_create(request.session_id)
    bazi_context = session.get_bazi_context_string()

    response = await get_orchestrator().dispatch(
        user_message=request.message,
        selected_agents=request.selected_agents,
        bazi_context=bazi_context,
        conversation_histories=session.conversation_histories,
    )

    # 更新 session 对话历史
    session.add_user_message(request.message)
    for agent_resp in response.responses:
        if not agent_resp.error:
            session.add_agent_message(agent_resp.agent_id, agent_resp.content)

    return response


@router.post("/chat/stream")
async def chat_stream(request: ChatRequest):
    """SSE 流式响应 - 每个 Agent 完成后立即推送"""
    orchestrator = get_orchestrator()
    session_svc = get_session_service()
    session = session_svc.get_or_create(request.session_id)
    bazi_context = session.get_bazi_context_string()

    emotion, intensity = orchestrator.emotion_engine.analyze_emotion(request.message)
    topics = orchestrator.emotion_engine.detect_topic(request.message)
    topic = topics[0] if topics else "综合"

    async def event_generator():
        # 先发送元数据
        meta = {
            "type": "meta",
            "user_message": request.message,
            "emotion": emotion,
            "emotion_intensity": intensity,
            "topic": topic,
        }
        yield f"data: {json.dumps(meta, ensure_ascii=False)}\n\n"

        # 并行调度所有 Agent
        async def _call_one(agent_id: str):
            agent = orchestrator.agents.get(agent_id)
            if not agent:
                return {"agent_id": agent_id, "error": f"Agent {agent_id} not found"}
            history = session.conversation_histories.get(agent_id, [])
            try:
                text = await agent.chat(
                    user_message=request.message,
                    bazi_context=bazi_context,
                    conversation_history=history,
                    emotion=emotion,
                    intensity=intensity,
                    topic=topic,
                )
                return {
                    "agent_id": agent_id,
                    "display_name": agent.display_name,
                    "icon": agent.icon,
                    "content": text,
                    "error": None,
                }
            except Exception as e:
                return {
                    "agent_id": agent_id,
                    "display_name": agent.display_name,
                    "icon": agent.icon,
                    "content": "",
                    "error": str(e),
                }

        tasks = [
            _call_one(aid)
            for aid in request.selected_agents
            if aid in orchestrator.agents
        ]

        # 每个 Agent 完成后立即推送
        for coro in asyncio.as_completed(tasks):
            result = await coro
            yield f"data: {json.dumps({'type': 'response', 'data': result}, ensure_ascii=False)}\n\n"

            # 更新 session
            if not result.get("error"):
                session.add_agent_message(result["agent_id"], result["content"])

        session.add_user_message(request.message)
        yield f"data: {json.dumps({'type': 'done'}, ensure_ascii=False)}\n\n"

    return StreamingResponse(
        event_generator(),
        media_type="text/event-stream",
        headers={"Cache-Control": "no-cache", "X-Accel-Buffering": "no"},
    )


@router.post("/session/create")
async def create_session():
    """创建新 session"""
    import uuid
    session_id = str(uuid.uuid4)[:8]
    get_session_service().get_or_create(session_id)
    return {"session_id": session_id}


@router.delete("/session/{session_id}")
async def delete_session(session_id: str):
    """删除 session"""
    get_session_service().delete(session_id)
    return {"ok": True}
