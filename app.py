"""
AI算命大师 - Streamlit前端应用
提供友好的用户界面和优化的交互体验
"""
import streamlit as st
from datetime import datetime, date
import time

from ai_fortune_teller import AIFortuneTeller
from personality_prompts import PersonalityPrompts
from analytics import UserAnalytics


# 页面配置
st.set_page_config(
    page_title="AI算命大师",
    page_icon="🔮",
    layout="wide",
    initial_sidebar_state="expanded"
)

# 自定义CSS样式
st.markdown("""
<style>
    .main-header {
        text-align: center;
        padding: 1rem;
        background: linear-gradient(120deg, #a1c4fd 0%, #c2e9fb 100%);
        border-radius: 10px;
        margin-bottom: 2rem;
    }
    .personality-card {
        padding: 1rem;
        border-radius: 8px;
        border: 2px solid #e0e0e0;
        margin: 0.5rem 0;
        cursor: pointer;
        transition: all 0.3s;
    }
    .personality-card:hover {
        border-color: #4CAF50;
        box-shadow: 0 4px 8px rgba(0,0,0,0.1);
    }
    .report-section {
        background-color: #f8f9fa;
        padding: 1.5rem;
        border-radius: 10px;
        margin: 1rem 0;
    }
    .chat-message {
        padding: 1rem;
        border-radius: 8px;
        margin: 0.5rem 0;
    }
    .user-message {
        background-color: #e3f2fd;
        text-align: right;
    }
    .ai-message {
        background-color: #f5f5f5;
    }
    .stats-box {
        background-color: #fff3e0;
        padding: 1rem;
        border-radius: 8px;
        text-align: center;
    }
</style>
""", unsafe_allow_html=True)


def init_session_state():
    """初始化会话状态"""
    if 'ai_fortune_teller' not in st.session_state:
        st.session_state.ai_fortune_teller = None
    if 'analytics' not in st.session_state:
        st.session_state.analytics = UserAnalytics()
    if 'bazi_set' not in st.session_state:
        st.session_state.bazi_set = False
    if 'chat_history' not in st.session_state:
        st.session_state.chat_history = []
    if 'session_started' not in st.session_state:
        st.session_state.session_started = False


def display_personality_selection():
    """显示人格选择界面"""
    st.markdown('<div class="main-header"><h1>🔮 AI算命大师</h1><p>选择您喜欢的大师风格，开启专属命理之旅</p></div>', unsafe_allow_html=True)
    
    personalities = PersonalityPrompts.get_all_personalities()
    
    st.subheader("选择您的专属大师")
    
    cols = st.columns(3)
    
    personality_icons = {
        'rational': '🧠',
        'gentle': '💕',
        'sharp': '⚡'
    }
    
    for idx, (key, personality) in enumerate(personalities.items()):
        with cols[idx]:
            st.markdown(f"""
            <div class="personality-card">
                <h3>{personality_icons[key]} {personality['name']}</h3>
                <p>{personality['description']}</p>
            </div>
            """, unsafe_allow_html=True)
            
            if st.button(f"选择{personality['name']}", key=f"btn_{key}", use_container_width=True):
                st.session_state.selected_personality = key
                st.session_state.ai_fortune_teller = AIFortuneTeller(key)
                st.session_state.analytics.start_session(key)
                st.session_state.session_started = True
                st.rerun()


def display_birth_info_input():
    """显示生辰信息输入界面"""
    st.markdown('<div class="main-header"><h2>📝 请输入您的生辰信息</h2></div>', unsafe_allow_html=True)
    
    col1, col2 = st.columns(2)
    
    with col1:
        birth_date = st.date_input(
            "出生日期",
            min_value=date(1900, 1, 1),
            max_value=date.today(),
            value=date(1990, 1, 1)
        )
    
    with col2:
        birth_hour = st.slider("出生时辰（时）", 0, 23, 12)
    
    if st.button("开始算命", type="primary", use_container_width=True):
        try:
            st.session_state.ai_fortune_teller.set_user_bazi(
                birth_date.year,
                birth_date.month,
                birth_date.day,
                birth_hour
            )
            st.session_state.bazi_set = True
            st.session_state.birth_info = {
                'year': birth_date.year,
                'month': birth_date.month,
                'day': birth_date.day,
                'hour': birth_hour
            }
            st.rerun()
        except Exception as e:
            st.error(f"处理生辰信息时出错：{str(e)}")


def display_bazi_summary():
    """显示八字摘要信息"""
    if st.session_state.ai_fortune_teller and st.session_state.ai_fortune_teller.bazi_info:
        bazi_info = st.session_state.ai_fortune_teller.bazi_info
        
        with st.expander("📊 您的八字信息", expanded=False):
            col1, col2, col3 = st.columns(3)
            
            with col1:
                st.write("**八字：**", bazi_info['八字']['八字'])
                st.write("**生肖：**", bazi_info['生肖'])
            
            with col2:
                st.write("**星座：**", bazi_info['星座'])
                st.write("**最强五行：**", bazi_info['最强五行'])
            
            with col3:
                st.write("**五行分布：**")
                for element, count in bazi_info['五行'].items():
                    st.write(f"{element}: {'●' * count}")


def display_chat_interface():
    """显示对话界面"""
    st.markdown('<div class="main-header"><h2>💬 与大师对话</h2></div>', unsafe_allow_html=True)
    
    # 显示八字摘要
    display_bazi_summary()
    
    # 对话历史
    chat_container = st.container()
    
    with chat_container:
        for message in st.session_state.chat_history:
            if message['role'] == 'user':
                st.markdown(f'<div class="chat-message user-message">👤 {message["content"]}</div>', unsafe_allow_html=True)
            else:
                st.markdown(f'<div class="chat-message ai-message">🔮 {message["content"]}</div>', unsafe_allow_html=True)
    
    # 输入框
    col1, col2 = st.columns([5, 1])
    
    with col1:
        user_input = st.text_input("请输入您的问题", key="user_input", label_visibility="collapsed", placeholder="例如：我的事业运势如何？")
    
    with col2:
        send_button = st.button("发送", type="primary", use_container_width=True)
    
    if send_button and user_input:
        # 记录交互
        topics = st.session_state.ai_fortune_teller.emotion_engine.detect_topic(user_input)
        st.session_state.analytics.record_interaction(topics[0] if topics else None)
        
        # 添加用户消息
        st.session_state.chat_history.append({
            'role': 'user',
            'content': user_input
        })
        
        # 获取AI回复
        with st.spinner('大师正在思考...'):
            ai_response = st.session_state.ai_fortune_teller.chat(user_input)
        
        # 添加AI回复
        st.session_state.chat_history.append({
            'role': 'assistant',
            'content': ai_response
        })
        
        st.rerun()


def display_reports():
    """显示报告生成界面"""
    st.markdown('<div class="main-header"><h2>📄 生成专属报告</h2></div>', unsafe_allow_html=True)
    
    col1, col2 = st.columns(2)
    
    with col1:
        if st.button("生成命理报告", type="primary", use_container_width=True):
            with st.spinner('正在生成命理报告...'):
                report = st.session_state.ai_fortune_teller.generate_fortune_report()
                st.session_state.fortune_report = report
                st.session_state.analytics.record_interaction("命理报告")
    
    with col2:
        if st.button("生成心理报告", type="primary", use_container_width=True):
            with st.spinner('正在生成心理报告...'):
                report = st.session_state.ai_fortune_teller.generate_psychological_report()
                st.session_state.psychological_report = report
                st.session_state.analytics.record_interaction("心理报告")
    
    # 显示命理报告
    if 'fortune_report' in st.session_state:
        st.markdown('<div class="report-section">', unsafe_allow_html=True)
        st.subheader("🔮 命理分析报告")
        st.write(st.session_state.fortune_report)
        st.markdown('</div>', unsafe_allow_html=True)
    
    # 显示心理报告
    if 'psychological_report' in st.session_state:
        st.markdown('<div class="report-section">', unsafe_allow_html=True)
        st.subheader("🧠 心理分析报告")
        st.write(st.session_state.psychological_report)
        st.markdown('</div>', unsafe_allow_html=True)


def display_rating():
    """显示评分界面"""
    st.markdown("---")
    st.subheader("💯 为您的体验评分")
    
    rating = st.slider("满意度评分", 1.0, 5.0, 4.5, 0.1)
    
    if st.button("提交评分"):
        st.session_state.analytics.end_session(rating)
        st.success("感谢您的反馈！")
        st.balloons()


def display_statistics():
    """在侧边栏显示统计信息"""
    stats = st.session_state.analytics.get_statistics()
    
    st.sidebar.markdown("---")
    st.sidebar.subheader("📊 平台统计")
    
    st.sidebar.markdown(f"""
    <div class="stats-box">
        <h3>{stats['total_sessions']}</h3>
        <p>总体验人数</p>
    </div>
    """, unsafe_allow_html=True)
    
    if stats['total_sessions'] > 0:
        st.sidebar.metric("平均停留时长", f"{stats['avg_duration_minutes']:.1f} 分钟")
        st.sidebar.metric("满意度评分", f"{stats['avg_rating']:.1f}/5.0")
        
        if stats['improvement_percentage'] > 0:
            st.sidebar.metric(
                "相比传统应用提升",
                f"{stats['improvement_percentage']:.1f}%",
                delta=f"{stats['improvement_percentage']:.1f}%"
            )
    
    # 人格统计
    personality_stats = st.session_state.analytics.get_personality_stats()
    if personality_stats:
        st.sidebar.markdown("**人格选择分布**")
        for personality, count in personality_stats.items():
            st.sidebar.write(f"{personality}: {count}次")


def main():
    """主函数"""
    init_session_state()
    
    # 侧边栏
    with st.sidebar:
        st.title("🔮 AI算命大师")
        st.markdown("融合传统命理与现代AI")
        
        # 显示统计信息
        display_statistics()
        
        # 功能按钮
        if st.session_state.bazi_set:
            st.markdown("---")
            st.subheader("功能导航")
            
            if st.button("🔄 重置对话", use_container_width=True):
                st.session_state.ai_fortune_teller.reset_conversation()
                st.session_state.chat_history = []
                st.rerun()
            
            if st.button("🆕 重新开始", use_container_width=True):
                st.session_state.clear()
                st.rerun()
    
    # 主界面
    if not st.session_state.session_started:
        # 人格选择阶段
        display_personality_selection()
    elif not st.session_state.bazi_set:
        # 生辰信息输入阶段
        display_birth_info_input()
    else:
        # 主要功能界面
        tab1, tab2 = st.tabs(["💬 对话咨询", "📄 报告生成"])
        
        with tab1:
            display_chat_interface()
        
        with tab2:
            display_reports()
        
        # 评分
        display_rating()


if __name__ == "__main__":
    main()
