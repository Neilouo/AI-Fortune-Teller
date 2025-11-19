"""
AI算命大师 - Streamlit前端应用
提供友好的用户界面和优化的交互体验
"""
import streamlit as st
from datetime import datetime, date
from typing import List
import time
import random

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
        padding: 2rem 1rem;
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        border-radius: 15px;
        margin-bottom: 2rem;
        box-shadow: 0 8px 20px rgba(0,0,0,0.15);
        color: white;
    }
    .main-header h1 {
        color: white;
        font-size: 2.5rem;
        margin-bottom: 0.5rem;
        text-shadow: 2px 2px 4px rgba(0,0,0,0.2);
    }
    .main-header p {
        color: rgba(255,255,255,0.95);
        font-size: 1.1rem;
    }
    .personality-card {
        padding: 1.5rem;
        border-radius: 12px;
        border: 2px solid #e0e0e0;
        margin: 0.5rem 0;
        cursor: pointer;
        transition: all 0.3s ease;
        background: white;
        box-shadow: 0 2px 8px rgba(0,0,0,0.08);
        height: 150px;
        display: flex;
        flex-direction: column;
        justify-content: flex-start;
    }
    .personality-card:hover {
        border-color: #667eea;
        box-shadow: 0 6px 16px rgba(102,126,234,0.3);
        transform: translateY(-3px);
    }
    .personality-card h3 {
        margin: 0 0 0.8rem 0;
        color: #333;
        font-size: 1.2rem;
        font-weight: 600;
    }
    .personality-card p {
        margin: 0;
        line-height: 1.5;
        font-size: 0.95rem;
        color: #666;
        overflow: hidden;
        text-overflow: ellipsis;
        display: -webkit-box;
        -webkit-line-clamp: 2;
        -webkit-box-orient: vertical;
    }
    .report-section {
        background: linear-gradient(135deg, #f5f7fa 0%, #c3cfe2 100%);
        padding: 2rem;
        border-radius: 15px;
        margin: 1rem 0;
        box-shadow: 0 4px 12px rgba(0,0,0,0.1);
    }
    .chat-message {
        padding: 1.2rem;
        border-radius: 12px;
        margin: 0.8rem 0;
        animation: fadeIn 0.3s ease;
    }
    @keyframes fadeIn {
        from { opacity: 0; transform: translateY(10px); }
        to { opacity: 1; transform: translateY(0); }
    }
    .user-message {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        margin-left: 20%;
        box-shadow: 0 3px 10px rgba(102,126,234,0.3);
    }
    .ai-message {
        background-color: #ffffff;
        border: 1px solid #e0e0e0;
        margin-right: 20%;
        box-shadow: 0 3px 10px rgba(0,0,0,0.08);
    }
    .stats-box {
        background: linear-gradient(135deg, #ffecd2 0%, #fcb69f 100%);
        padding: 1.2rem;
        border-radius: 12px;
        text-align: center;
        box-shadow: 0 4px 12px rgba(0,0,0,0.1);
    }
    .question-chip {
        display: inline-block;
        padding: 0.6rem 1.2rem;
        margin: 0.3rem;
        background: linear-gradient(135deg, #f093fb 0%, #f5576c 100%);
        color: white;
        border-radius: 20px;
        cursor: pointer;
        transition: all 0.3s ease;
        font-size: 0.9rem;
        box-shadow: 0 2px 8px rgba(245,87,108,0.3);
    }
    .question-chip:hover {
        transform: translateY(-2px);
        box-shadow: 0 4px 12px rgba(245,87,108,0.5);
    }
    .bazi-info-card {
        background: linear-gradient(135deg, #e0c3fc 0%, #8ec5fc 100%);
        padding: 1.5rem;
        border-radius: 12px;
        margin: 1rem 0;
        box-shadow: 0 4px 12px rgba(0,0,0,0.1);
    }
    .element-bar {
        display: flex;
        align-items: center;
        margin: 0.5rem 0;
    }
    .element-name {
        width: 60px;
        font-weight: bold;
    }
    .element-progress {
        flex: 1;
        height: 20px;
        background-color: rgba(255,255,255,0.3);
        border-radius: 10px;
        overflow: hidden;
        margin-left: 10px;
    }
    .stButton>button {
        border-radius: 8px;
        font-weight: 500;
        transition: all 0.3s ease;
    }
    .stButton>button:hover {
        transform: translateY(-2px);
        box-shadow: 0 4px 12px rgba(0,0,0,0.2);
    }
</style>
""", unsafe_allow_html=True)


def get_recommended_questions(personality_type: str = "") -> List[str]:
    """获取推荐问题列表"""
    base_questions = [
        "我的事业运势如何？",
        "最近感情方面有什么建议吗？",
        "我适合从事什么职业？",
        "如何提升我的财运？",
        "我的性格有哪些优势和劣势？",
        "今年我需要注意什么？",
        "我和什么样的人最合得来？",
        "我的健康方面需要注意什么？"
    ]
    
    # 根据人格类型添加特定问题
    if personality_type == "rational":
        base_questions.extend([
            "从命理角度分析我的职业规划",
            "我的五行缺什么？如何平衡？"
        ])
    elif personality_type == "gentle":
        base_questions.extend([
            "我最近很迷茫，能给我一些鼓励吗？",
            "如何让自己变得更好？"
        ])
    elif personality_type == "sharp":
        base_questions.extend([
            "直接告诉我，我最大的问题是什么？",
            "我需要改变什么才能成功？"
        ])
    
    return base_questions


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
    if 'default_question' not in st.session_state:
        # 随机选择一个默认问题
        default_questions = [
            "我的事业运势如何？",
            "最近感情方面有什么建议吗？",
            "我适合从事什么职业？",
            "如何提升我的财运？",
            "我的性格有哪些优势和劣势？",
            "今年我需要注意什么？"
        ]
        st.session_state.default_question = random.choice(default_questions)


def display_personality_selection():
    """显示人格选择界面"""
    st.markdown('<div class="main-header"><h1>🔮 AI算命大师</h1><p>选择您喜欢的大师风格，开启专属命理之旅</p></div>', unsafe_allow_html=True)
    
    st.markdown("### ✨ 三位大师，三种风格，总有一款适合您")
    st.write("---")
    
    personalities = PersonalityPrompts.get_all_personalities()
    
    personality_icons = {
        'rational': '🧠',
        'gentle': '💕',
        'sharp': '⚡'
    }
    
    personality_colors = {
        'rational': '#4A90E2',
        'gentle': '#E91E63',
        'sharp': '#FF9800'
    }
    
    cols = st.columns(3)
    
    for idx, (key, personality) in enumerate(personalities.items()):
        with cols[idx]:
            icon = personality_icons[key]
            color = personality_colors[key]
            
            st.markdown(f"""
            <div class="personality-card" style="border-color: {color};">
                <h3 style="color: {color};">{icon} {personality['name']}</h3>
                <p style="color: #666; line-height: 1.6;">{personality['description']}</p>
            </div>
            """, unsafe_allow_html=True)
            
            if st.button(f"选择 {personality['name']}", key=f"btn_{key}", use_container_width=True):
                st.session_state.selected_personality = key
                st.session_state.ai_fortune_teller = AIFortuneTeller(key)
                st.session_state.analytics.start_session(key)
                st.session_state.session_started = True
                st.success(f"✅ 已选择 {personality['name']}！")
                time.sleep(0.5)
                st.rerun()
    
    # 添加说明
    st.markdown("---")
    st.info("💡 **小提示**：不同的大师风格会带来不同的对话体验，建议根据您当前的心情和需求选择合适的大师。")


def display_birth_info_input():
    """显示生辰信息输入界面"""
    st.markdown('<div class="main-header"><h1>📝 请输入您的生辰信息</h1><p>准确的生辰信息将帮助我们为您提供更精准的分析</p></div>', unsafe_allow_html=True)
    
    st.markdown("### 🎂 基本信息")
    
    col1, col2 = st.columns(2)
    
    with col1:
        birth_date = st.date_input(
            "出生日期 📅",
            min_value=date(1900, 1, 1),
            max_value=date.today(),
            value=date(1990, 1, 1),
            help="请选择您的阳历出生日期"
        )
    
    with col2:
        birth_hour = st.slider(
            "出生时辰（时） ⏰", 
            0, 23, 12,
            help="请选择您的出生小时（0-23），如果不确定可选择12点"
        )
    
    # 时辰说明
    time_periods = {
        "子时": "23:00-01:00", "丑时": "01:00-03:00",
        "寅时": "03:00-05:00", "卯时": "05:00-07:00",
        "辰时": "07:00-09:00", "巳时": "09:00-11:00",
        "午时": "11:00-13:00", "未时": "13:00-15:00",
        "申时": "15:00-17:00", "酉时": "17:00-19:00",
        "戌时": "19:00-21:00", "亥时": "21:00-23:00"
    }
    
    st.markdown("#### 📖 时辰参考")
    cols = st.columns(4)
    for idx, (period, time_range) in enumerate(time_periods.items()):
        with cols[idx % 4]:
            st.caption(f"**{period}**: {time_range}")
    
    st.markdown("---")
    
    col_btn1, col_btn2, col_btn3 = st.columns([1, 2, 1])
    with col_btn2:
        if st.button("🎯 开始算命", type="primary", use_container_width=True):
            try:
                with st.spinner("正在计算您的八字..."):
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
                    st.success("✅ 八字计算完成！")
                    time.sleep(0.5)
                    st.rerun()
            except Exception as e:
                st.error(f"❌ 处理生辰信息时出错：{str(e)}")
    
    st.markdown("---")
    st.info("🔒 **隐私保护**：您的所有信息仅用于本次算命，不会被保存或分享。")


def display_bazi_summary():
    """显示八字摘要信息"""
    if st.session_state.ai_fortune_teller and st.session_state.ai_fortune_teller.bazi_info:
        bazi_info = st.session_state.ai_fortune_teller.bazi_info
        
        with st.expander("📊 您的八字信息", expanded=False):
            # 基本信息
            col1, col2, col3 = st.columns(3)
            
            with col1:
                st.markdown("### 基本信息")
                st.write(f"**八字：** {bazi_info['八字']['八字']}")
                st.write(f"**生肖：** {bazi_info['生肖']}")
            
            with col2:
                st.markdown("### 星象信息")
                st.write(f"**星座：** {bazi_info['星座']}")
                st.write(f"**最强五行：** {bazi_info['最强五行']}")
                st.write(f"**最弱五行：** {bazi_info['最弱五行']}")
            
            with col3:
                st.markdown("### 性格特征")
                for trait in bazi_info.get('personality_traits', [])[:3]:
                    st.write(f"✨ {trait}")
            
            # 五行分布可视化
            st.markdown("### 五行能量分布")
            element_colors = {
                '金': '#FFD700',
                '木': '#228B22', 
                '水': '#1E90FF',
                '火': '#FF4500',
                '土': '#8B4513'
            }
            
            for element, count in bazi_info['五行'].items():
                percentage = (count / 5) * 100
                color = element_colors.get(element, '#999999')
                st.markdown(f"""
                <div class="element-bar">
                    <div class="element-name">{element}</div>
                    <div class="element-progress">
                        <div style="width: {percentage}%; height: 100%; background-color: {color}; border-radius: 10px;"></div>
                    </div>
                    <div style="margin-left: 10px; font-weight: bold;">{count}</div>
                </div>
                """, unsafe_allow_html=True)


def display_chat_interface():
    """显示对话界面"""
    st.markdown('<div class="main-header"><h1>💬 与大师对话</h1><p>诚心提问，用心解答</p></div>', unsafe_allow_html=True)
    
    # 显示八字摘要
    display_bazi_summary()
    
    # 推荐问题区域
    if len(st.session_state.chat_history) == 0:
        st.markdown("### 💡 推荐问题")
        st.markdown("*点击下方问题快速开始对话*")
        
        recommended = get_recommended_questions(st.session_state.ai_fortune_teller.personality_type)
        
        # 创建问题按钮网格
        cols = st.columns(2)
        for idx, question in enumerate(recommended[:6]):
            col_idx = idx % 2
            with cols[col_idx]:
                if st.button(f"💭 {question}", key=f"rec_q_{idx}", use_container_width=True):
                    # 使用推荐问题
                    st.session_state.selected_question = question
                    st.rerun()
        
        st.markdown("---")
    
    # 对话历史
    chat_container = st.container()
    
    with chat_container:
        if len(st.session_state.chat_history) == 0:
            st.info("👋 您好！我是您的专属算命大师，请随时向我提问。")
        
        for message in st.session_state.chat_history:
            if message['role'] == 'user':
                st.markdown(f'<div class="chat-message user-message">👤 {message["content"]}</div>', unsafe_allow_html=True)
            else:
                st.markdown(f'<div class="chat-message ai-message">🔮 {message["content"]}</div>', unsafe_allow_html=True)
    
    # 输入框
    st.markdown("### 💬 提问区")
    
    # 检查是否有选中的推荐问题
    if 'selected_question' in st.session_state:
        user_input = st.session_state.selected_question
        del st.session_state.selected_question
        process_user_input(user_input)
        st.rerun()
    
    # 根据对话历史动态生成placeholder
    if len(st.session_state.chat_history) == 0:
        placeholder_text = f"💭 例如：{st.session_state.default_question}"
    else:
        placeholder_text = "💭 继续提问..."
    
    col1, col2 = st.columns([5, 1])
    
    with col1:
        user_input = st.text_input(
            "请输入您的问题", 
            key="user_input", 
            label_visibility="collapsed", 
            placeholder=placeholder_text
        )
    
    with col2:
        send_button = st.button("发送 📤", type="primary", use_container_width=True)
    
    # 如果点击发送但没有输入内容，使用默认问题
    if send_button:
        if user_input.strip():
            # 用户有输入，使用用户输入
            process_user_input(user_input)
            st.rerun()
        elif len(st.session_state.chat_history) == 0:
            # 用户没有输入且是首次对话，使用默认问题
            process_user_input(st.session_state.default_question)
            st.rerun()
        else:
            # 用户没有输入且不是首次对话，提示用户
            st.warning("⚠️ 请输入您的问题")


def process_user_input(user_input: str):
    """处理用户输入"""
    # 记录交互
    topics = st.session_state.ai_fortune_teller.emotion_engine.detect_topic(user_input)
    st.session_state.analytics.record_interaction(topics[0] if topics else None)
    
    # 添加用户消息
    st.session_state.chat_history.append({
        'role': 'user',
        'content': user_input
    })
    
    # 获取AI回复
    ai_response = st.session_state.ai_fortune_teller.chat(user_input)
    
    # 添加AI回复
    st.session_state.chat_history.append({
        'role': 'assistant',
        'content': ai_response
    })


def display_reports():
    """显示报告生成界面"""
    st.markdown('<div class="main-header"><h1>📄 生成专属报告</h1><p>深度分析，洞察未来</p></div>', unsafe_allow_html=True)
    
    st.info("💡 提示：生成报告前建议先进行一些对话，这样报告会更加准确和个性化。")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("### 🔮 命理报告")
        st.write("全面分析您的命理特征，包括事业、感情、财运、健康等多个维度。")
        if st.button("🎯 生成命理报告", type="primary", use_container_width=True):
            with st.spinner('正在生成命理报告...'):
                report = st.session_state.ai_fortune_teller.generate_fortune_report()
                st.session_state.fortune_report = report
                st.session_state.analytics.record_interaction("命理报告")
                st.success("✅ 报告生成成功！")
    
    with col2:
        st.markdown("### 🧠 心理报告")
        st.write("基于对话内容分析您的心理状态，提供专业的心理洞察和建议。")
        if st.button("🎯 生成心理报告", type="primary", use_container_width=True):
            with st.spinner('正在生成心理报告...'):
                report = st.session_state.ai_fortune_teller.generate_psychological_report()
                st.session_state.psychological_report = report
                st.session_state.analytics.record_interaction("心理报告")
                st.success("✅ 报告生成成功！")
    
    st.markdown("---")
    
    # 显示命理报告
    if 'fortune_report' in st.session_state:
        st.markdown('<div class="report-section">', unsafe_allow_html=True)
        st.markdown("## 🔮 命理分析报告")
        st.markdown(st.session_state.fortune_report)
        
        # 下载按钮
        report_text = f"命理分析报告\n生成时间：{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n{st.session_state.fortune_report}"
        st.download_button(
            label="📥 下载报告",
            data=report_text,
            file_name=f"命理报告_{datetime.now().strftime('%Y%m%d')}.txt",
            mime="text/plain"
        )
        st.markdown('</div>', unsafe_allow_html=True)
    
    # 显示心理报告
    if 'psychological_report' in st.session_state:
        st.markdown('<div class="report-section">', unsafe_allow_html=True)
        st.markdown("## 🧠 心理分析报告")
        st.markdown(st.session_state.psychological_report)
        
        # 下载按钮
        report_text = f"心理分析报告\n生成时间：{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n{st.session_state.psychological_report}"
        st.download_button(
            label="📥 下载报告",
            data=report_text,
            file_name=f"心理报告_{datetime.now().strftime('%Y%m%d')}.txt",
            mime="text/plain"
        )
        st.markdown('</div>', unsafe_allow_html=True)


def display_rating():
    """显示评分界面"""
    st.markdown("---")
    st.markdown("### 💯 为您的体验评分")
    st.write("您的反馈对我们非常重要，帮助我们不断改进服务质量。")
    
    col1, col2 = st.columns([3, 1])
    
    with col1:
        rating = st.slider("满意度评分", 1.0, 5.0, 4.5, 0.1, 
                          help="1星=非常不满意，5星=非常满意")
    
    with col2:
        if st.button("✅ 提交评分", type="primary", use_container_width=True):
            st.session_state.analytics.end_session(rating)
            st.success("感谢您的反馈！🙏")
            st.balloons()


def display_statistics():
    """在侧边栏显示统计信息"""
    stats = st.session_state.analytics.get_statistics()
    
    st.sidebar.markdown("---")
    st.sidebar.markdown("### 📊 平台统计")
    
    st.sidebar.markdown(f"""
    <div class="stats-box">
        <h2 style="margin: 0; color: #FF6B6B;">{stats['total_sessions']}</h2>
        <p style="margin: 0.5rem 0 0 0; color: #666;">总体验人数</p>
    </div>
    """, unsafe_allow_html=True)
    
    if stats['total_sessions'] > 0:
        st.sidebar.markdown("<br>", unsafe_allow_html=True)
        
        col1, col2 = st.sidebar.columns(2)
        with col1:
            st.metric("⏱️ 平均时长", f"{stats['avg_duration_minutes']:.1f}分钟")
        with col2:
            st.metric("⭐ 满意度", f"{stats['avg_rating']:.1f}/5.0")
        
        if stats['improvement_percentage'] > 0:
            st.sidebar.metric(
                "📈 体验提升",
                f"{stats['improvement_percentage']:.1f}%",
                delta=f"+{stats['improvement_percentage']:.1f}%",
                help="相比传统算命应用的提升"
            )
    
    # 人格统计
    personality_stats = st.session_state.analytics.get_personality_stats()
    if personality_stats:
        st.sidebar.markdown("---")
        st.sidebar.markdown("### 🎭 人格选择分布")
        
        personality_names = {
            'rational': '🧠 理性大师',
            'gentle': '💕 温柔大师',
            'sharp': '⚡ 毒舌大师'
        }
        
        for personality, count in personality_stats.items():
            name = personality_names.get(personality, personality)
            st.sidebar.write(f"{name}: **{count}** 次")


def main():
    """主函数"""
    init_session_state()
    
    # 侧边栏
    with st.sidebar:
        st.markdown("""
        <div style="text-align: center; padding: 1rem;">
            <h1 style="color: #667eea;">🔮</h1>
            <h2 style="margin: 0;">AI算命大师</h2>
            <p style="color: #888; margin: 0.5rem 0;">融合传统命理与现代AI</p>
        </div>
        """, unsafe_allow_html=True)
        
        # 显示统计信息
        display_statistics()
        
        # 功能按钮
        if st.session_state.bazi_set:
            st.sidebar.markdown("---")
            st.sidebar.markdown("### ⚙️ 功能菜单")
            
            if st.sidebar.button("💬 清空对话", use_container_width=True, help="清空当前对话记录"):
                st.session_state.ai_fortune_teller.reset_conversation()
                st.session_state.chat_history = []
                st.success("对话已清空！")
                st.rerun()
            
            if st.sidebar.button("🔄 重新开始", use_container_width=True, help="重新选择大师和输入生辰"):
                st.session_state.clear()
                st.success("已重置！")
                st.rerun()
        
        # 底部信息
        st.sidebar.markdown("---")
        st.sidebar.markdown("""
        <div style="text-align: center; color: #888; font-size: 0.8rem;">
            <p>💡 AI算命仅供娱乐参考</p>
            <p>📧 反馈建议请联系客服</p>
            <p style="margin-top: 1rem;">© 2024 AI算命大师</p>
        </div>
        """, unsafe_allow_html=True)
    
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
