"""
AI算命核心模块
整合八字计算、人格对话、情感分析功能
"""
import os
from typing import Dict, List, Optional
from datetime import datetime
from openai import OpenAI
from dotenv import load_dotenv

from bazi_calculator import BaziCalculator
from personality_prompts import PersonalityPrompts
from emotion_engine import EmotionEngine


class AIFortuneTeller:
    """AI算命师核心类"""
    
    # 配置常量
    DEFAULT_TEMPERATURE = 0.8
    DEFAULT_MAX_TOKENS = 800
    DEFAULT_MAX_HISTORY = 20
    
    def __init__(self, personality_type: str = "rational"):
        """
        初始化AI算命师
        
        Args:
            personality_type: 人格类型 ('rational', 'gentle', 'sharp')
        """
        load_dotenv()
        
        # Try multiple sources for API key
        # 1. Try Streamlit secrets (for Streamlit Cloud deployment)
        self.api_key = None
        try:
            import streamlit as st
            if hasattr(st, 'secrets') and 'OPENAI_API_KEY' in st.secrets:
                self.api_key = st.secrets['OPENAI_API_KEY']
                self.model = st.secrets.get('OPENAI_MODEL', 'gpt-3.5-turbo')
                self.api_base = st.secrets.get('OPENAI_API_BASE', None)
        except (ImportError, FileNotFoundError, KeyError):
            pass
        
        # 2. Fall back to environment variables (including .env file)
        if not self.api_key:
            self.api_key = os.getenv("OPENAI_API_KEY")
            self.model = os.getenv("OPENAI_MODEL", "gpt-3.5-turbo")
            self.api_base = os.getenv("OPENAI_API_BASE")
        
        if not self.api_key:
            raise ValueError(
                "OPENAI_API_KEY未配置。请通过以下方式之一设置：\n"
                "1. Streamlit Cloud: 在应用设置中添加 secrets\n"
                "2. 本地运行: 在.env文件中设置OPENAI_API_KEY\n"
                "3. 环境变量: export OPENAI_API_KEY=your_key"
            )
        
        # 支持自定义API Base（如硅基流动平台）
        if self.api_base:
            self.client = OpenAI(api_key=self.api_key, base_url=self.api_base)
        else:
            self.client = OpenAI(api_key=self.api_key)
        self.personality_type = personality_type
        self.personality = PersonalityPrompts.get_personality(personality_type)
        self.emotion_engine = EmotionEngine()
        
        self.conversation_history: List[Dict] = []
        self.bazi_info: Optional[Dict] = None
        
    def set_user_bazi(self, year: int, month: int, day: int, hour: int):
        """
        设置用户八字信息
        
        Args:
            year: 出生年份
            month: 出生月份
            day: 出生日期
            hour: 出生时辰
        """
        calculator = BaziCalculator(year, month, day, hour)
        self.bazi_info = calculator.get_fortune_base()
        self.bazi_info['personality_traits'] = calculator.get_personality_traits()
        
    def generate_bazi_context(self) -> str:
        """生成八字上下文信息"""
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
    
    def chat(self, user_message: str) -> str:
        """
        与用户对话
        
        Args:
            user_message: 用户消息
            
        Returns:
            AI回复
        """
        # 分析用户情感
        emotion, intensity = self.emotion_engine.analyze_emotion(user_message)
        topics = self.emotion_engine.detect_topic(user_message)
        
        # 构建系统提示
        system_prompt = self.personality['system_prompt']
        if self.bazi_info:
            system_prompt += "\n\n" + self.generate_bazi_context()
        
        system_prompt += f"\n\n【当前对话分析】\n用户情感：{emotion}（强度：{intensity:.2f}）\n话题：{', '.join(topics)}"
        
        # 构建消息列表
        messages = [{"role": "system", "content": system_prompt}]
        
        # 添加历史对话（保留最近的对话）
        max_history = int(os.getenv("MAX_HISTORY_LENGTH", str(self.DEFAULT_MAX_HISTORY)))
        messages.extend(self.conversation_history[-max_history:])
        
        # 添加当前用户消息
        messages.append({"role": "user", "content": user_message})
        
        try:
            # 调用OpenAI API，使用可配置的参数
            temperature = float(os.getenv("OPENAI_TEMPERATURE", str(self.DEFAULT_TEMPERATURE)))
            max_tokens = int(os.getenv("OPENAI_MAX_TOKENS", str(self.DEFAULT_MAX_TOKENS)))
            
            response = self.client.chat.completions.create(
                model=self.model,
                messages=messages,
                temperature=temperature,
                max_tokens=max_tokens
            )
            
            ai_response = response.choices[0].message.content
            
            # 优化对话流畅性
            ai_response = self.emotion_engine.enhance_dialogue_fluency(ai_response, emotion)
            
            # 保存对话历史
            self.conversation_history.append({"role": "user", "content": user_message})
            self.conversation_history.append({"role": "assistant", "content": ai_response})
            
            return ai_response
            
        except Exception as e:
            return f"抱歉，处理您的请求时出现了问题：{str(e)}"
    
    def generate_fortune_report(self) -> str:
        """
        生成命理报告
        
        Returns:
            完整的命理分析报告
        """
        if not self.bazi_info:
            return "请先输入您的生辰信息。"
        
        report_prompt = f"""请根据以下八字信息，生成一份详细的命理分析报告：

{self.generate_bazi_context()}

报告应包含以下内容：
1. 基本命理特征
2. 性格分析
3. 事业运势
4. 感情运势
5. 财运分析
6. 健康建议
7. 整体建议

请用{self.personality['name']}的风格撰写报告。"""
        
        return self.chat(report_prompt)
    
    def generate_psychological_report(self) -> str:
        """
        生成心理分析报告
        
        Returns:
            心理维度分析报告
        """
        if not self.bazi_info:
            return "请先输入您的生辰信息。"
        
        if not self.conversation_history:
            return "请先进行一些对话，以便我更好地了解您。"
        
        # 分析对话历史中的情感和主题
        all_emotions = []
        all_topics = []
        
        for msg in self.conversation_history:
            if msg['role'] == 'user':
                emotion, intensity = self.emotion_engine.analyze_emotion(msg['content'])
                topics = self.emotion_engine.detect_topic(msg['content'])
                all_emotions.append((emotion, intensity))
                all_topics.extend(topics)
        
        psych_prompt = f"""基于我们的对话和你的八字信息，请生成一份心理维度分析报告：

{self.generate_bazi_context()}

【对话分析】
总对话轮次：{len(self.conversation_history) // 2}
关注话题：{', '.join(set(all_topics))}
整体情绪倾向：{self._analyze_overall_emotion(all_emotions)}

报告应包含：
1. 心理状态评估
2. 性格特质分析
3. 当前关注焦点
4. 心理建议
5. 成长方向

请用{self.personality['name']}的风格撰写报告。"""
        
        return self.chat(psych_prompt)
    
    def _analyze_overall_emotion(self, emotions: List[tuple]) -> str:
        """分析整体情绪倾向"""
        if not emotions:
            return "中性"
        
        positive_count = sum(1 for e, _ in emotions if e == "positive")
        negative_count = sum(1 for e, _ in emotions if e == "negative")
        
        if positive_count > negative_count:
            return "积极乐观"
        elif negative_count > positive_count:
            return "需要关注"
        else:
            return "平稳中性"
    
    def reset_conversation(self):
        """重置对话历史"""
        self.conversation_history = []
