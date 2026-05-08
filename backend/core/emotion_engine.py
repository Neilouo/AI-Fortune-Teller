"""
情感词典和规则引擎
用于情绪识别、情感反馈和对话流畅性优化
"""
import jieba
import re
from typing import Dict, List, Tuple


class EmotionEngine:
    """情感分析引擎"""
    
    # 情感词典 - 分为积极、消极、中性三类
    POSITIVE_WORDS = {
        "开心", "快乐", "高兴", "幸福", "满意", "喜欢", "爱", "好", "棒", "优秀",
        "成功", "顺利", "如意", "美好", "温暖", "感动", "期待", "希望", "憧憬",
        "感谢", "幸运", "完美", "欣慰", "放心", "舒心", "安心"
    }
    
    NEGATIVE_WORDS = {
        "难过", "伤心", "痛苦", "失望", "沮丧", "焦虑", "担心", "害怕", "恐惧",
        "压力", "困难", "问题", "麻烦", "失败", "不顺", "倒霉", "糟糕", "郁闷",
        "烦恼", "迷茫", "无助", "孤独", "寂寞", "委屈", "愤怒", "生气", "不满"
    }
    
    NEUTRAL_WORDS = {
        "想", "问", "了解", "知道", "查", "看", "算", "测", "分析", "说说",
        "如何", "怎么", "什么", "为什么", "可以", "能", "会", "是", "吗"
    }
    
    # 话题关键词
    TOPIC_KEYWORDS = {
        "事业": ["工作", "事业", "职业", "升职", "加薪", "跳槽", "创业", "生意"],
        "感情": ["爱情", "恋爱", "结婚", "婚姻", "分手", "复合", "桃花", "对象", "伴侣"],
        "财运": ["财运", "钱", "财富", "投资", "理财", "赚钱", "收入", "发财"],
        "健康": ["健康", "身体", "疾病", "养生", "医疗", "体检"],
        "学业": ["学习", "考试", "学业", "成绩", "升学", "考研", "留学"],
        "家庭": ["家庭", "父母", "孩子", "子女", "家人", "亲人", "家族"]
    }
    
    def __init__(self):
        """初始化情感引擎"""
        # 加载自定义词典
        for words in [self.POSITIVE_WORDS, self.NEGATIVE_WORDS, self.NEUTRAL_WORDS]:
            for word in words:
                jieba.add_word(word)
    
    def analyze_emotion(self, text: str) -> Tuple[str, float]:
        """
        分析文本情感
        
        Args:
            text: 输入文本
            
        Returns:
            (情感类型, 情感强度) - 情感类型为 'positive', 'negative', 'neutral'
        """
        words = jieba.lcut(text)
        
        positive_count = sum(1 for word in words if word in self.POSITIVE_WORDS)
        negative_count = sum(1 for word in words if word in self.NEGATIVE_WORDS)
        
        total_emotion = positive_count + negative_count
        
        if total_emotion == 0:
            return "neutral", 0.5
        
        if positive_count > negative_count:
            intensity = min(positive_count / len(words) * 10, 1.0)
            return "positive", intensity
        elif negative_count > positive_count:
            intensity = min(negative_count / len(words) * 10, 1.0)
            return "negative", intensity
        else:
            return "neutral", 0.5
    
    def detect_topic(self, text: str) -> List[str]:
        """
        检测文本主题
        
        Args:
            text: 输入文本
            
        Returns:
            检测到的主题列表
        """
        topics = []
        for topic, keywords in self.TOPIC_KEYWORDS.items():
            if any(keyword in text for keyword in keywords):
                topics.append(topic)
        
        return topics if topics else ["综合"]
    
    def generate_empathy_response(self, emotion: str, intensity: float) -> str:
        """
        根据情感生成共鸣回应
        
        Args:
            emotion: 情感类型
            intensity: 情感强度
            
        Returns:
            共鸣回应文本
        """
        if emotion == "positive":
            if intensity > 0.7:
                return "看得出来你现在心情很不错！"
            else:
                return "很高兴看到你保持着积极的心态。"
        elif emotion == "negative":
            if intensity > 0.7:
                return "我能感受到你现在的困扰和压力。"
            else:
                return "听起来你遇到了一些烦恼。"
        else:
            return "我明白了你的情况。"
    
    def enhance_dialogue_fluency(self, response: str, user_emotion: str) -> str:
        """
        优化对话流畅性
        
        Args:
            response: AI生成的原始回应
            user_emotion: 用户情感类型
            
        Returns:
            优化后的回应
        """
        # 根据用户情感调整语气
        if user_emotion == "negative":
            # 为消极情绪添加安慰性过渡
            if not any(word in response for word in ["理解", "别担心", "会好的"]):
                response = "我理解你的感受。" + response
        
        # 确保回应有适当的结尾
        if not response.endswith(("。", "！", "？", "~")):
            response += "。"
        
        return response
    
    def validate_response_quality(self, response: str) -> bool:
        """
        验证回应质量
        
        Args:
            response: AI生成的回应
            
        Returns:
            是否通过质量检查
        """
        # 检查长度
        if len(response) < 20:
            return False
        
        # 检查是否包含实质内容（不只是客套话）
        substantive_words = ["八字", "五行", "命理", "建议", "分析", "运势", "性格"]
        if not any(word in response for word in substantive_words):
            return False
        
        return True
