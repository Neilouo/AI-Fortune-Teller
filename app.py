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

# 自定义CSS样式 - 整体美化
st.markdown("""
<link href="https://fonts.googleapis.com/css2?family=Noto+Serif+SC:wght@400;600;700&family=Inter:wght@400;500;600&display=swap" rel="stylesheet">
<style>
    /* 全局：背景与主内容区 */
    .stApp {
        background: linear-gradient(160deg, #0f0d1a 0%, #1a1625 40%, #151220 100%);
    }
    .main .block-container {
        max-width: 900px;
        padding-top: 2rem;
        padding-bottom: 3rem;
    }
    h1, h2, h3 { font-family: 'Noto Serif SC', serif !important; }
    p, span, div, label { font-family: 'Inter', 'Noto Serif SC', sans-serif !important; }

    /* 隐藏 Streamlit 默认多余元素 */
    #MainMenu { visibility: hidden; }
    footer { visibility: hidden; }
    header { background: transparent !important; }
    /* 修复侧边栏折叠按钮图标显示为 keyboard_double 的 bug */
    [data-testid="collapsedControl"],
    [data-testid="collapsedControl"] *,
    button[aria-label*="sidebar"],
    button[aria-label*="collapse"],
    [class*="sidebarCollapse"],
    [class*="SidebarCollapse"] { display: none !important; visibility: hidden !important; }

    /* 主头部 - 神秘感 */
    .main-header {
        text-align: center;
        padding: 2.5rem 1.5rem;
        background: linear-gradient(145deg, rgba(62,39,83,0.95) 0%, rgba(40,25,55,0.98) 100%);
        border-radius: 20px;
        margin-bottom: 2rem;
        box-shadow: 0 20px 50px rgba(0,0,0,0.4), inset 0 1px 0 rgba(255,255,255,0.06);
        color: white;
        border: 1px solid rgba(255,255,255,0.06);
    }
    .main-header h1 {
        color: #ffffff;
        font-size: 2rem;
        font-weight: 700;
        margin-bottom: 0.3rem;
        letter-spacing: 0.04em;
    }
    .main-header p, .main-header .tagline {
        color: #ffffff;
        font-size: 0.95rem;
        margin-top: 0.2rem;
    }

    /* 人格卡片 - 玻璃拟态，高对比文字 */
    .personality-card {
        padding: 1.5rem;
        border-radius: 16px;
        margin: 0.6rem 0;
        cursor: pointer;
        transition: all 0.25s ease;
        background: rgba(255,255,255,0.06);
        backdrop-filter: blur(12px);
        border: 1px solid rgba(255,255,255,0.15);
        box-shadow: 0 8px 24px rgba(0,0,0,0.2);
        min-height: 160px;
    }
    .personality-card:hover {
        border-color: var(--card-accent);
        box-shadow: 0 12px 32px rgba(0,0,0,0.3), 0 0 0 1px var(--card-accent);
        transform: translateY(-2px);
    }
    .personality-card h3 {
        margin: 0 0 0.4rem 0;
        color: #ffffff;
        font-size: 1.2rem;
        font-weight: 600;
    }
    .personality-card .slogan {
        font-size: 0.8rem;
        color: #f0ecf5;
        font-style: italic;
        margin-bottom: 0.5rem;
        line-height: 1.45;
    }
    .personality-card p {
        margin: 0;
        line-height: 1.5;
        font-size: 0.88rem;
        color: #ffffff;
        -webkit-line-clamp: 2;
    }
    .personality-card .tag {
        display: inline-block;
        margin-top: 0.6rem;
        padding: 0.28rem 0.65rem;
        border-radius: 999px;
        font-size: 0.72rem;
        background: rgba(255,255,255,0.12);
        color: #f5f2fa;
    }

    /* 报告区域 */
    .report-section {
        background: rgba(255,255,255,0.03);
        padding: 2rem;
        border-radius: 16px;
        margin: 1rem 0;
        border: 1px solid rgba(255,255,255,0.08);
        box-shadow: 0 8px 24px rgba(0,0,0,0.2);
    }
    .report-summary-card {
        background: linear-gradient(135deg, rgba(62,39,83,0.9) 0%, rgba(40,25,55,0.95) 100%);
        color: #ffffff;
        padding: 1.2rem 1.5rem;
        border-radius: 12px;
        margin-bottom: 1rem;
        font-size: 0.95rem;
        line-height: 1.6;
        border: 1px solid rgba(255,255,255,0.06);
    }
    .report-summary-card strong { color: #ffffff; }
    .share-line {
        background: rgba(255,255,255,0.08);
        padding: 0.85rem 1rem;
        border-radius: 10px;
        font-size: 0.9rem;
        color: #f5f2fa;
        margin-top: 0.8rem;
        border: 1px solid rgba(255,255,255,0.1);
    }
    .question-group-title {
        font-size: 0.8rem;
        color: #ffffff;
        font-weight: 600;
        margin: 1rem 0 0.5rem 0;
        letter-spacing: 0.03em;
    }
    /* 人格选择页标题与说明：高对比度 */
    .personality-section-title {
        font-size: 1.35rem !important;
        font-weight: 700 !important;
        color: #ffffff !important;
        margin: 0 0 0.4rem 0 !important;
    }
    .personality-section-hint {
        font-size: 0.95rem !important;
        color: #f0f0f0 !important;
        margin: 0 0 1rem 0 !important;
        line-height: 1.5 !important;
    }

    /* 对话气泡 */
    .chat-message {
        padding: 1rem 1.25rem;
        border-radius: 16px;
        margin: 0.75rem 0;
        animation: fadeIn 0.35s ease;
    }
    @keyframes fadeIn {
        from { opacity: 0; transform: translateY(8px); }
        to { opacity: 1; transform: translateY(0); }
    }
    .user-message {
        background: linear-gradient(135deg, rgba(88,65,120,0.9) 0%, rgba(62,45,90,0.95) 100%);
        color: #ffffff;
        margin-left: 18%;
        border: 1px solid rgba(255,255,255,0.08);
        box-shadow: 0 6px 20px rgba(0,0,0,0.25);
    }
    .ai-message {
        background: rgba(255,255,255,0.08);
        border: 1px solid rgba(255,255,255,0.15);
        color: #ffffff;
        margin-right: 18%;
        box-shadow: 0 6px 20px rgba(0,0,0,0.2);
    }

    /* ========== 侧边栏整体 ========== */
    [data-testid="stSidebar"] {
        background: linear-gradient(180deg, #0f0c14 0%, #0a0810 100%) !important;
        border-right: 1px solid rgba(255,255,255,0.08) !important;
    }
    [data-testid="stSidebar"] > div {
        padding: 1.25rem 1rem 1.5rem !important;
        background: transparent !important;
    }
    [data-testid="stSidebar"] .stMarkdown, [data-testid="stSidebar"] p { color: #f0eef5 !important; }
    [data-testid="stSidebar"] h3 { color: #ffffff !important; font-size: 0.9rem !important; margin-bottom: 0.6rem !important; }
    [data-testid="stSidebar"] hr { border-color: rgba(255,255,255,0.08) !important; margin: 1rem 0 !important; }

    .sidebar-brand {
        text-align: center;
        padding: 1.25rem 0.75rem 1.5rem;
        margin-bottom: 1rem;
        border-radius: 14px;
        background: rgba(255,255,255,0.04);
        border: 1px solid rgba(255,255,255,0.08);
    }
    .sidebar-brand .icon { font-size: 2rem; display: block; margin-bottom: 0.35rem; }
    .sidebar-brand .title { font-size: 1.1rem; font-weight: 700; color: #ffffff; margin: 0; letter-spacing: 0.02em; }
    .sidebar-brand .tagline { font-size: 0.75rem; color: rgba(240,238,245,0.7); margin: 0.35rem 0 0; }

    .sidebar-section-title {
        font-size: 0.7rem;
        font-weight: 600;
        color: rgba(255,255,255,0.6);
        text-transform: uppercase;
        letter-spacing: 0.08em;
        margin: 1.25rem 0 0.6rem;
    }
    .sidebar-card {
        background: rgba(255,255,255,0.05);
        border: 1px solid rgba(255,255,255,0.08);
        border-radius: 12px;
        padding: 1rem;
        margin-bottom: 0.75rem;
    }
    .sidebar-card .value { font-size: 1.5rem; font-weight: 700; color: #ffffff; line-height: 1.2; }
    .sidebar-card .label { font-size: 0.75rem; color: rgba(240,238,245,0.75); margin-top: 0.25rem; }
    .sidebar-metric-row { display: flex; gap: 0.5rem; margin-top: 0.5rem; }
    .sidebar-metric-item { flex: 1; background: rgba(255,255,255,0.04); border-radius: 8px; padding: 0.6rem; text-align: center; border: 1px solid rgba(255,255,255,0.06); }
    .sidebar-metric-item .val { font-size: 0.95rem; font-weight: 600; color: #ffffff; }
    .sidebar-metric-item .lbl { font-size: 0.65rem; color: rgba(240,238,245,0.7); margin-top: 0.15rem; }
    .sidebar-personality-item { font-size: 0.8rem; color: #f0eef5; padding: 0.4rem 0; border-bottom: 1px solid rgba(255,255,255,0.05); display: flex; justify-content: space-between; }
    .sidebar-personality-item:last-child { border-bottom: none; }
    .sidebar-footer {
        margin-top: 1.5rem;
        padding-top: 1rem;
        border-top: 1px solid rgba(255,255,255,0.08);
        text-align: center;
        font-size: 0.72rem;
        color: rgba(220,215,235,0.65);
        line-height: 1.6;
    }
    [data-testid="stSidebar"] .stButton > button {
        width: 100%;
        margin-bottom: 0.5rem;
        background: rgba(255,255,255,0.10) !important;
        color: #ffffff !important;
        border: 1px solid rgba(255,255,255,0.18) !important;
        opacity: 1 !important;
    }
    [data-testid="stSidebar"] .stButton > button,
    [data-testid="stSidebar"] .stButton > button * {
        color: #ffffff !important;
        -webkit-text-fill-color: #ffffff !important;
        fill: #ffffff !important;
        opacity: 1 !important;
    }
    [data-testid="stSidebar"] .stButton > button:disabled {
        background: rgba(255,255,255,0.06) !important;
        color: rgba(255,255,255,0.65) !important;
        border-color: rgba(255,255,255,0.10) !important;
        opacity: 1 !important;
    }
    [data-testid="stSidebar"] .stButton > button:disabled,
    [data-testid="stSidebar"] .stButton > button:disabled * {
        color: rgba(255,255,255,0.65) !important;
        -webkit-text-fill-color: rgba(255,255,255,0.65) !important;
        fill: rgba(255,255,255,0.65) !important;
    }
    [data-testid="stSidebar"] .stButton > button:hover {
        background: rgba(255,255,255,0.16) !important;
        border-color: rgba(255,255,255,0.26) !important;
    }

    /* 侧边栏统计（保留兼容） */
    .stats-box {
        background: rgba(255,255,255,0.05);
        padding: 1rem;
        border-radius: 12px;
        text-align: center;
        border: 1px solid rgba(255,255,255,0.08);
    }
    .stats-box h2, .stats-box .value { color: #ffffff !important; }
    .stats-box p, .stats-box .label { color: rgba(240,238,245,0.8) !important; }
    .element-bar { display: flex; align-items: center; margin: 0.5rem 0; }
    .element-name { width: 60px; font-weight: 600; color: #ffffff; }
    .element-progress {
        flex: 1; height: 18px;
        background: rgba(255,255,255,0.1);
        border-radius: 10px;
        overflow: hidden;
        margin-left: 10px;
    }

    /* 按钮统一 */
    .stButton>button {
        border-radius: 10px;
        font-weight: 500;
        transition: all 0.25s ease;
        border: 1px solid rgba(255,255,255,0.15);
    }
    .stButton>button:hover {
        transform: translateY(-1px);
        box-shadow: 0 6px 20px rgba(88,65,120,0.35);
    }
    .stButton>button[kind="primary"] {
        background: linear-gradient(135deg, #5a3d7a 0%, #4a2d6a 100%);
        color: #f5f0fa;
    }

    /* 输入框、滑块等与深色背景协调 */
    .stTextInput>div>div>input,
    .stTextInput input,
    [data-testid="stTextInput"] input,
    [data-baseweb="input"] input,
    [data-baseweb="base-input"] input,
    [data-baseweb="textarea"] textarea,
    .stSelectbox>div {
        background: rgba(255,255,255,0.12) !important;
        border: 1px solid rgba(255,255,255,0.25) !important;
        color: #ffffff !important;
        -webkit-text-fill-color: #ffffff !important;
        text-shadow: none !important;
        border-radius: 10px;
    }
    /* 更高优先级：防止被 Streamlit/BaseWeb 覆盖成黑色 */
    .main [data-testid="stTextInput"] input,
    .main [data-testid="stTextInput"] textarea,
    .main [data-baseweb="input"] input,
    .main [data-baseweb="base-input"] input,
    .main [data-baseweb="textarea"] textarea {
        color: #ffffff !important;
        -webkit-text-fill-color: #ffffff !important;
        caret-color: #ffffff !important;
    }
    .stTextInput input::placeholder,
    [data-testid="stTextInput"] input::placeholder {
        color: rgba(255,255,255,0.7) !important;
        -webkit-text-fill-color: rgba(255,255,255,0.7) !important;
    }
    [data-testid="stTextInput"] input:focus { border-color: rgba(255,255,255,0.4) !important; box-shadow: 0 0 0 1px rgba(255,255,255,0.2) !important; }
    .stTextInput input { caret-color: #ffffff !important; }
    /* 表单语义：输入框采用浅底黑字（你要求黑色文字） */
    :root { color-scheme: dark; }
    /* 输入框：浅底 + 黑字，更清晰 */
    .stTextInput>div>div>input,
    .stTextInput input,
    [data-testid="stTextInput"] input,
    [data-baseweb="input"] input,
    [data-baseweb="base-input"] input,
    [data-baseweb="textarea"] textarea {
        background: rgba(255,255,255,0.92) !important;
        border: 1px solid rgba(255,255,255,0.45) !important;
        color: #0b0b0f !important;
        -webkit-text-fill-color: #0b0b0f !important;
        caret-color: #0b0b0f !important;
    }
    .stTextInput input::placeholder,
    [data-testid="stTextInput"] input::placeholder,
    textarea::placeholder {
        color: rgba(20,20,28,0.55) !important;
        -webkit-text-fill-color: rgba(20,20,28,0.55) !important;
    }
    [data-testid="stTextInput"] input:focus,
    [data-baseweb="input"] input:focus,
    [data-baseweb="base-input"] input:focus,
    [data-baseweb="textarea"] textarea:focus {
        border-color: rgba(255,255,255,0.7) !important;
        box-shadow: 0 0 0 2px rgba(255,255,255,0.18) !important;
    }
    /* 自动填充：保持浅底黑字 */
    input:-webkit-autofill,
    input:-webkit-autofill:hover,
    input:-webkit-autofill:focus,
    textarea:-webkit-autofill,
    textarea:-webkit-autofill:hover,
    textarea:-webkit-autofill:focus {
        -webkit-text-fill-color: #0b0b0f !important;
        box-shadow: 0 0 0px 1000px rgba(255,255,255,0.92) inset !important;
        transition: background-color 9999s ease-in-out 0s;
        caret-color: #0b0b0f !important;
    }
    /* 解决浏览器自动填充导致的“白底白字/灰字” */
    input:-webkit-autofill,
    input:-webkit-autofill:hover,
    input:-webkit-autofill:focus,
    textarea:-webkit-autofill,
    textarea:-webkit-autofill:hover,
    textarea:-webkit-autofill:focus {
        -webkit-text-fill-color: #ffffff !important;
        box-shadow: 0 0 0px 1000px rgba(255,255,255,0.12) inset !important;
        transition: background-color 9999s ease-in-out 0s;
        caret-color: #ffffff !important;
    }
    .stSlider label { color: #f5f5f5 !important; }
    .stSelectbox label { color: #f5f5f5 !important; }
    .stDateInput label { color: #f5f5f5 !important; }
    .stExpander {
        background: rgba(255,255,255,0.05);
        border: 1px solid rgba(255,255,255,0.1);
        border-radius: 12px;
    }
    .stExpander label, .stExpander summary, [data-testid="stExpander"] label { color: #ffffff !important; }
    .stExpander .stCaption, [data-testid="stExpander"] .stCaption { color: #f5f5f5 !important; }
    /* 隐藏 Streamlit 未渲染的 Material 图标（显示为 keyboard_arrow_right、arrow、down、right 等文字） */
    [data-testid="stIconMaterial"] { display: none !important; visibility: hidden !important; font-size: 0 !important; line-height: 0 !important; overflow: hidden !important; }
    [data-testid="stDateInput"] label { color: #ffffff !important; }
    /* 出生日期与时辰区块：标题和标签都用纯白，提高可读性 */
    .birth-section-title { color: #ffffff !important; font-size: 1.25rem !important; }
    .main [data-testid="stDateInput"] label, .main [data-testid="stDateInput"] div { color: #ffffff !important; }
    .main [data-testid="stSlider"] label { color: #ffffff !important; }
    /* 标题与正文：高对比度白/浅色 */
    .main h2 { color: #ffffff !important; }
    .main h3 { color: #ffffff !important; }
    .main p, .main .stMarkdown, .main div[data-testid="stMarkdown"] { color: #f5f5f5 !important; }
    .main .stMarkdown p { color: #f5f5f5 !important; }
    .stCaption { color: #f0f0f0 !important; }
    .report-section .stMarkdown, .report-section p { color: #ffffff !important; }
    /* 信息框与 Tab */
    .stAlert {
        background: rgba(50,35,70,0.7) !important;
        border: 1px solid rgba(255,255,255,0.12) !important;
        border-radius: 12px;
        color: #ffffff !important;
    }
    .stAlert p { color: #ffffff !important; }
    [data-baseweb="tab-list"] {
        background: rgba(255,255,255,0.06) !important;
        border-radius: 12px;
        padding: 4px;
        border: 1px solid rgba(255,255,255,0.1);
    }
    [data-baseweb="tab"] { color: #ffffff !important; }
    .stTabs [data-baseweb="tab-highlight"] { background: rgba(88,65,120,0.5) !important; }
    /* 更多组件高对比度 */
    .stExpander label { color: #ffffff !important; }
    .stExpander .stMarkdown { color: #f5f5f5 !important; }
    [data-testid="stMetricValue"] { color: #ffffff !important; }
    [data-testid="stMetricLabel"] { color: #e8e8e8 !important; }
    .stSlider [data-baseweb="slider"] { color: #f5f5f5; }
    .main label { color: #f5f5f5 !important; }
    /* 对话/提问/评分等区块标题：纯白加粗，确保看清 */
    .section-title-strong,
    .main p.section-title-strong,
    p.section-title-strong {
        color: #ffffff !important;
        font-size: 1.25rem !important;
        font-weight: 700 !important;
        margin: 0.8rem 0 0.5rem 0 !important;
        text-shadow: 0 0 1px rgba(0,0,0,0.5);
    }
    .question-group-title { color: #ffffff !important; font-weight: 600 !important; }
</style>
""", unsafe_allow_html=True)

# 推荐问题按场景分组，便于用户快速找到想问的
QUESTION_GROUPS = {
    "事业与财运": [
        "我的事业运势如何？",
        "我适合从事什么职业？",
        "如何提升我的财运？",
        "从命理角度分析我的职业规划",
    ],
    "感情与人际": [
        "最近感情方面有什么建议吗？",
        "我和什么样的人最合得来？",
        "今年桃花运怎么样？",
    ],
    "自我与健康": [
        "我的性格有哪些优势和劣势？",
        "我的健康方面需要注意什么？",
        "今年我需要注意什么？",
    ],
    "更多话题": [
        "我的五行缺什么？如何平衡？",
        "我最近很迷茫，能给我一些鼓励吗？",
        "直接告诉我，我最大的问题是什么？",
    ],
}


def get_recommended_questions(personality_type: str = "") -> List[str]:
    """获取推荐问题列表（扁平化，供随机等使用）"""
    all_q = []
    for qs in QUESTION_GROUPS.values():
        all_q.extend(qs)
    return all_q


def get_random_question(personality_type: str = "") -> str:
    """随机返回一个推荐问题，用于「随机一问」"""
    questions = get_recommended_questions(personality_type)
    return random.choice(questions) if questions else "我的事业运势如何？"


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


# 人格展示增强：金句 + 适合人群
PERSONALITY_SLOGANS = {
    'rational': '「三分天注定，七分靠打拼」—— 用逻辑帮你把命理讲清楚',
    'gentle': '「你值得被温柔以待」—— 像知心朋友一样陪你说说话',
    'sharp': '「别自欺欺人，听我一句真话」—— 犀利但为你好的那种',
}
PERSONALITY_TAGS = {
    'rational': '适合：需要理性分析、职业规划、想听依据的人',
    'gentle': '适合：压力大、需要安慰、想被理解的人',
    'sharp': '适合：想听真话、不怕被怼、需要被点醒的人',
}


def display_personality_selection():
    """显示人格选择界面"""
    st.markdown(
        '<div class="main-header">'
        '<h1>🔮 AI算命大师</h1>'
        '<p>选一位合眼缘的大师，开启你的专属命理之旅</p>'
        '<p class="tagline">传统八字 × 现代AI × 三种人格，总有一款懂你</p>'
        '</div>',
        unsafe_allow_html=True
    )
    st.markdown(
        '<p class="personality-section-title">✨ 三位大师，三种风格</p>'
        '<p class="personality-section-hint">点击卡片下方按钮即可选择，选错也没关系，随时可以「重新开始」换一位。</p>',
        unsafe_allow_html=True
    )
    st.write("---")

    personalities = PersonalityPrompts.get_all_personalities()
    personality_icons = {'rational': '🧠', 'gentle': '💕', 'sharp': '⚡'}
    personality_colors = {'rational': '#4A6FA5', 'gentle': '#B84D6B', 'sharp': '#C17F3D'}
    cols = st.columns(3)
    for idx, (key, personality) in enumerate(personalities.items()):
        with cols[idx]:
            icon = personality_icons[key]
            color = personality_colors[key]
            slogan = PERSONALITY_SLOGANS.get(key, '')
            tag = PERSONALITY_TAGS.get(key, '')
            st.markdown(
                f'<div class="personality-card" style="--card-accent: {color};">'
                f'<h3 style="color: {color};">{icon} {personality["name"]}</h3>'
                f'<div class="slogan">{slogan}</div>'
                f'<p>{personality["description"]}</p>'
                f'<span class="tag">{tag}</span>'
                f'</div>',
                unsafe_allow_html=True
            )
            if st.button(f"就选 TA → {personality['name']}", key=f"btn_{key}", use_container_width=True):
                st.session_state.selected_personality = key
                st.session_state.ai_fortune_teller = AIFortuneTeller(key)
                st.session_state.analytics.start_session(key)
                st.session_state.session_started = True
                st.rerun()

    st.markdown("---")
    st.info("💡 **小提示**：不同大师说话风格差别很大，可以按你此刻的心情选——想被安慰选温柔，想听真话选毒舌，想理性分析选理性。")


def display_birth_info_input():
    """显示生辰信息输入界面"""
    st.markdown(
        '<div class="main-header">'
        '<h1>📝 输入生辰信息</h1>'
        '<p>用于计算八字与五行，越准确分析越有参考价值</p>'
        '</div>',
        unsafe_allow_html=True
    )
    
    st.markdown('<p class="birth-section-title">🎂 出生日期与时辰</p>', unsafe_allow_html=True)
    
    col1, col2 = st.columns(2)
    with col1:
        birth_date = st.date_input(
            "出生日期（阳历）📅",
            min_value=date(1900, 1, 1),
            max_value=date.today(),
            value=date(1990, 1, 1),
            help="请选择您的阳历出生日期"
        )
    with col2:
        birth_hour = st.slider(
            "出生时辰⏰",
            0, 23, 12,
            help="0–23 点。不确定可先选 12 点，对整体分析影响有限"
        )
    
    # 时辰说明改为折叠，减少首屏信息量
    with st.expander("📖 不确定时辰？点这里看对照表"):
        time_periods = {
            "子时": "23:00-01:00", "丑时": "01:00-03:00",
            "寅时": "03:00-05:00", "卯时": "05:00-07:00",
            "辰时": "07:00-09:00", "巳时": "09:00-11:00",
            "午时": "11:00-13:00", "未时": "13:00-15:00",
            "申时": "15:00-17:00", "酉时": "17:00-19:00",
            "戌时": "19:00-21:00", "亥时": "21:00-23:00"
        }
        cols = st.columns(4)
        for idx, (period, time_range) in enumerate(time_periods.items()):
            with cols[idx % 4]:
                st.caption(f"**{period}**: {time_range}")
        st.caption("💡 记不清的话选 12 点即可，后续对话中也可以再问大师「时辰不准会怎样」。")
    
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
                    try:
                        st.toast("八字已算好，正在进入对话～")
                    except Exception:
                        pass
                    st.rerun()
            except Exception as e:
                st.error(f"❌ 处理生辰信息时出错：{str(e)}")
    
    st.markdown("---")
    st.info("🔒 **隐私说明**：生辰仅用于本次会话的八字与对话分析，不会被保存或分享。")


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
    st.markdown(
        '<div class="main-header">'
        '<h1>💬 与大师对话</h1>'
        '<p>想问什么就问什么，事业、感情、财运、健康都可以</p>'
        '</div>',
        unsafe_allow_html=True
    )
    
    display_bazi_summary()
    
    # 推荐问题：分组展示 + 随机一问
    if len(st.session_state.chat_history) == 0:
        st.markdown('<p class="section-title-strong">💡 不知道问啥？点下面任意一句开始</p>', unsafe_allow_html=True)
        
        # 随机一问
        if st.button("🎲 随机一问", help="随机选一个问题帮你开场"):
            q = get_random_question(st.session_state.ai_fortune_teller.personality_type)
            st.session_state.selected_question = q
            st.rerun()
        
        for group_name, questions in QUESTION_GROUPS.items():
            st.markdown(f'<p class="question-group-title">{group_name}</p>', unsafe_allow_html=True)
            cols = st.columns(2)
            for idx, question in enumerate(questions[:4]):  # 每组最多展示 4 个
                col_idx = idx % 2
                with cols[col_idx]:
                    if st.button(f"💭 {question}", key=f"rec_{group_name}_{idx}", use_container_width=True):
                        st.session_state.selected_question = question
                        st.rerun()
        
        st.markdown("---")
    
    # 对话历史
    chat_container = st.container()
    with chat_container:
        if len(st.session_state.chat_history) == 0:
            st.info("👋 大师已就位，选一个问题或自己输入，开始你的第一问吧～")
        
        for message in st.session_state.chat_history:
            if message['role'] == 'user':
                st.markdown(f'<div class="chat-message user-message">👤 {message["content"]}</div>', unsafe_allow_html=True)
            else:
                st.markdown(f'<div class="chat-message ai-message">🔮 {message["content"]}</div>', unsafe_allow_html=True)
    
    st.markdown('<p class="section-title-strong">💬 提问</p>', unsafe_allow_html=True)
    
    if 'selected_question' in st.session_state:
        user_input = st.session_state.selected_question
        del st.session_state.selected_question
        process_user_input(user_input)
        st.rerun()
    
    if len(st.session_state.chat_history) == 0:
        placeholder_text = f"💭 例如：{st.session_state.default_question}"
    else:
        placeholder_text = "💭 继续问下一句..."
    
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
    
    if send_button:
        if user_input.strip():
            process_user_input(user_input)
            st.rerun()
        elif len(st.session_state.chat_history) == 0:
            process_user_input(st.session_state.default_question)
            st.rerun()
        else:
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


def _report_summary(report: str, max_len: int = 200) -> str:
    """从报告中截取前一段作为摘要，避免截断句中"""
    if not report or len(report) <= max_len:
        return report.strip()
    s = report[:max_len]
    for sep in ["。", "！", "？", "\n", "；"]:
        idx = s.rfind(sep)
        if idx > max_len // 2:
            return s[: idx + 1].strip()
    return s.strip() + "…"


def _share_line(report_type: str) -> str:
    """生成可复制的分享文案"""
    return f"我刚在 🔮 AI算命大师 生成了{report_type}，既有八字又有心理分析，挺好玩的～（仅供娱乐）"


def display_reports():
    """显示报告生成界面"""
    st.markdown(
        '<div class="main-header">'
        '<h1>📄 生成专属报告</h1>'
        '<p>命理 + 心理双维度，一份报告看懂自己</p>'
        '</div>',
        unsafe_allow_html=True
    )
    
    st.info("💡 先多聊几句再生成报告，内容会更贴你。")
    
    col1, col2 = st.columns(2)
    with col1:
        st.markdown("### 🔮 命理报告")
        st.caption("八字、五行、事业/感情/财运/健康综合解读")
        if st.button("🎯 生成命理报告", type="primary", use_container_width=True, key="btn_fortune"):
            with st.spinner('正在生成命理报告...'):
                report = st.session_state.ai_fortune_teller.generate_fortune_report()
                st.session_state.fortune_report = report
                st.session_state.analytics.record_interaction("命理报告")
                st.success("✅ 命理报告已生成，可下载或复制分享文案。")
    
    with col2:
        st.markdown("### 🧠 心理报告")
        st.caption("基于对话内容的心理状态与成长建议")
        if st.button("🎯 生成心理报告", type="primary", use_container_width=True, key="btn_psych"):
            with st.spinner('正在生成心理报告...'):
                report = st.session_state.ai_fortune_teller.generate_psychological_report()
                st.session_state.psychological_report = report
                st.session_state.analytics.record_interaction("心理报告")
                st.success("✅ 心理报告已生成，可下载或复制分享文案。")
    
    st.markdown("---")
    
    if 'fortune_report' in st.session_state:
        report = st.session_state.fortune_report
        summary = _report_summary(report)
        st.markdown(
            f'<div class="report-summary-card">'
            f'<strong>📌 命理报告摘要</strong><br>{summary}'
            f'</div>',
            unsafe_allow_html=True
        )
        st.markdown('<div class="report-section">', unsafe_allow_html=True)
        st.markdown("## 🔮 命理分析报告")
        st.markdown(report)
        report_text = f"命理分析报告\n生成时间：{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n{report}"
        st.download_button(
            label="📥 下载报告",
            data=report_text,
            file_name=f"命理报告_{datetime.now().strftime('%Y%m%d')}.txt",
            mime="text/plain",
            key="dl_fortune"
        )
        share_msg = _share_line("命理报告")
        st.markdown(f'<div class="share-line">📤 分享文案（可复制）：<br>{share_msg}</div>', unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)
    
    if 'psychological_report' in st.session_state:
        report = st.session_state.psychological_report
        summary = _report_summary(report)
        st.markdown(
            f'<div class="report-summary-card">'
            f'<strong>📌 心理报告摘要</strong><br>{summary}'
            f'</div>',
            unsafe_allow_html=True
        )
        st.markdown('<div class="report-section">', unsafe_allow_html=True)
        st.markdown("## 🧠 心理分析报告")
        st.markdown(report)
        report_text = f"心理分析报告\n生成时间：{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n{report}"
        st.download_button(
            label="📥 下载报告",
            data=report_text,
            file_name=f"心理报告_{datetime.now().strftime('%Y%m%d')}.txt",
            mime="text/plain",
            key="dl_psych"
        )
        share_msg = _share_line("心理报告")
        st.markdown(f'<div class="share-line">📤 分享文案（可复制）：<br>{share_msg}</div>', unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)


def display_rating():
    """显示评分界面"""
    st.markdown("---")
    st.markdown('<p class="section-title-strong">💯 体验如何？给我们打个分吧</p>', unsafe_allow_html=True)
    st.caption("你的反馈会帮助我们越做越好～")
    
    col1, col2 = st.columns([3, 1])
    with col1:
        rating = st.select_slider(
            "满意度",
            options=[1.0, 2.0, 3.0, 4.0, 5.0],
            value=5.0,
            format_func=lambda x: f"{'⭐' * int(x)} {x} 分",
            help="1 分=很不满意，5 分=非常满意"
        )
    with col2:
        if st.button("✅ 提交评分", type="primary", use_container_width=True):
            st.session_state.analytics.end_session(rating)
            st.success("感谢你的反馈！🙏")
            st.balloons()


def display_statistics():
    """在侧边栏显示统计信息"""
    stats = st.session_state.analytics.get_statistics()
    
    st.sidebar.markdown('<p class="sidebar-section-title">📊 平台统计</p>', unsafe_allow_html=True)
    st.sidebar.markdown(f"""
    <div class="sidebar-card">
        <div class="value">{stats['total_sessions']}</div>
        <div class="label">总体验人数</div>
    </div>
    """, unsafe_allow_html=True)
    
    if stats['total_sessions'] > 0:
        # 分块输出 HTML，避免嵌套 f-string 导致内层被转义成纯文本
        dur = f"{stats['avg_duration_minutes']:.1f}"
        rating = f"{stats['avg_rating']:.1f}"
        card1 = (
            '<div class="sidebar-card">'
            '<div class="sidebar-metric-row">'
            '<div class="sidebar-metric-item"><div class="val">⏱️ ' + dur + ' 分钟</div><div class="lbl">平均时长</div></div>'
            '<div class="sidebar-metric-item"><div class="val">⭐ ' + rating + '/5</div><div class="lbl">满意度</div></div>'
            '</div></div>'
        )
        st.sidebar.markdown(card1, unsafe_allow_html=True)
        if stats['improvement_percentage'] > 0:
            pct = f"{stats['improvement_percentage']:.1f}"
            card2 = (
                '<div class="sidebar-card">'
                '<div class="sidebar-metric-item">'
                '<div class="val">📈 +' + pct + '%</div><div class="lbl">体验提升</div>'
                '</div></div>'
            )
            st.sidebar.markdown(card2, unsafe_allow_html=True)
    
    personality_stats = st.session_state.analytics.get_personality_stats()
    if personality_stats:
        personality_names = {
            'rational': '🧠 理性大师',
            'gentle': '💕 温柔大师',
            'sharp': '⚡ 毒舌大师'
        }
        st.sidebar.markdown('<p class="sidebar-section-title">🎭 人格分布</p>', unsafe_allow_html=True)
        items_html = "".join(
            f'<div class="sidebar-personality-item"><span>{personality_names.get(p, p)}</span><span>{c} 次</span></div>'
            for p, c in personality_stats.items()
        )
        st.sidebar.markdown(f'<div class="sidebar-card">{items_html}</div>', unsafe_allow_html=True)


def main():
    """主函数"""
    init_session_state()
    
    # 侧边栏
    with st.sidebar:
        st.markdown("""
        <div class="sidebar-brand">
            <span class="icon">🔮</span>
            <p class="title">AI算命大师</p>
            <p class="tagline">传统八字 × 现代AI</p>
        </div>
        """, unsafe_allow_html=True)
        
        display_statistics()
        
        if st.session_state.bazi_set:
            st.sidebar.markdown('<p class="sidebar-section-title">功能</p>', unsafe_allow_html=True)
            if st.sidebar.button("💬 清空对话", use_container_width=True, help="清空当前对话记录"):
                st.session_state.ai_fortune_teller.reset_conversation()
                st.session_state.chat_history = []
                st.success("对话已清空！")
                st.rerun()
            if st.sidebar.button("🔄 重新开始", use_container_width=True, help="重新选择大师和输入生辰"):
                st.session_state.clear()
                st.success("已重置！")
                st.rerun()
        
        st.sidebar.markdown("""
        <div class="sidebar-footer">
            <p>💡 仅供娱乐，理性看待</p>
            <p>📧 有问题可提 Issue</p>
            <p style="margin-top: 0.75rem;">© AI算命大师</p>
        </div>
        """, unsafe_allow_html=True)
    
    # 主界面
    if not st.session_state.session_started:
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
