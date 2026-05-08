"""Session 管理服务（内存存储）"""
from typing import Optional
from backend.core.bazi_calculator import BaziCalculator


class SessionState:
    def __init__(self, session_id: str):
        self.session_id = session_id
        self.bazi_info: Optional[dict] = None
        self.conversation_histories: dict[str, list[dict]] = {}

    def set_bazi(self, year: int, month: int, day: int, hour: int):
        calculator = BaziCalculator(year, month, day, hour)
        self.bazi_info = calculator.get_fortune_base()
        self.bazi_info["personality_traits"] = calculator.get_personality_traits()

    def get_bazi_context_string(self) -> str:
        if not self.bazi_info:
            return ""
        context = f"""
【用户八字信息】
八字：{self.bazi_info['八字']['八字']}
生肖：{self.bazi_info['生肖']}
星座：{self.bazi_info['星座']}
五行分布：{', '.join([f'{k}:{v}' for k, v in self.bazi_info['五行'].items()])}
最强五行：{self.bazi_info['最强五行']}
最弱五行：{self.bazi_info['最弱五行']}
性格特征：{', '.join(self.bazi_info['personality_traits'])}
"""
        return context

    def add_user_message(self, message: str):
        for agent_id in self.conversation_histories:
            self.conversation_histories[agent_id].append(
                {"role": "user", "content": message}
            )

    def add_agent_message(self, agent_id: str, content: str):
        if agent_id not in self.conversation_histories:
            self.conversation_histories[agent_id] = []
        self.conversation_histories[agent_id].append(
            {"role": "assistant", "content": content}
        )


class SessionService:
    def __init__(self):
        self._sessions: dict[str, SessionState] = {}

    def get_or_create(self, session_id: str) -> SessionState:
        if session_id not in self._sessions:
            self._sessions[session_id] = SessionState(session_id)
        return self._sessions[session_id]

    def delete(self, session_id: str):
        self._sessions.pop(session_id, None)
