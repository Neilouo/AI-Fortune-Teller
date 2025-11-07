"""
八字（BaZi）计算模块
基于中国传统命理学计算生辰八字
"""
from lunar_python import Lunar, Solar
from datetime import datetime


class BaziCalculator:
    """八字计算器"""
    
    # 天干
    TIANGAN = ["甲", "乙", "丙", "丁", "戊", "己", "庚", "辛", "壬", "癸"]
    # 地支
    DIZHI = ["子", "丑", "寅", "卯", "辰", "巳", "午", "未", "申", "酉", "戌", "亥"]
    # 五行
    WUXING = {
        "甲": "木", "乙": "木", "丙": "火", "丁": "火", "戊": "土",
        "己": "土", "庚": "金", "辛": "金", "壬": "水", "癸": "水",
        "子": "水", "丑": "土", "寅": "木", "卯": "木", "辰": "土",
        "巳": "火", "午": "火", "未": "土", "申": "金", "酉": "金",
        "戌": "土", "亥": "水"
    }
    
    def __init__(self, year: int, month: int, day: int, hour: int):
        """
        初始化八字计算器
        
        Args:
            year: 出生年份
            month: 出生月份
            day: 出生日期
            hour: 出生时辰（0-23）
        """
        self.solar = Solar.fromYmdHms(year, month, day, hour, 0, 0)
        self.lunar = self.solar.getLunar()
        
    def calculate_bazi(self) -> dict:
        """
        计算八字
        
        Returns:
            包含年柱、月柱、日柱、时柱的字典
        """
        year_gan_zhi = self.lunar.getYearInGanZhi()
        month_gan_zhi = self.lunar.getMonthInGanZhi()
        day_gan_zhi = self.lunar.getDayInGanZhi()
        hour_gan_zhi = self.lunar.getTimeInGanZhi()
        
        return {
            "年柱": year_gan_zhi,
            "月柱": month_gan_zhi,
            "日柱": day_gan_zhi,
            "时柱": hour_gan_zhi,
            "八字": f"{year_gan_zhi} {month_gan_zhi} {day_gan_zhi} {hour_gan_zhi}"
        }
    
    def analyze_wuxing(self) -> dict:
        """
        分析五行分布
        
        Returns:
            五行统计字典
        """
        bazi = self.calculate_bazi()
        wuxing_count = {"金": 0, "木": 0, "水": 0, "火": 0, "土": 0}
        
        for pillar in ["年柱", "月柱", "日柱", "时柱"]:
            gan_zhi = bazi[pillar]
            for char in gan_zhi:
                if char in self.WUXING:
                    element = self.WUXING[char]
                    wuxing_count[element] += 1
        
        return wuxing_count
    
    def get_fortune_base(self) -> dict:
        """
        获取命理基础信息
        
        Returns:
            包含基础命理信息的字典
        """
        bazi = self.calculate_bazi()
        wuxing = self.analyze_wuxing()
        
        # 找出最强和最弱的五行
        strongest = max(wuxing.items(), key=lambda x: x[1])
        weakest = min(wuxing.items(), key=lambda x: x[1])
        
        return {
            "八字": bazi,
            "五行": wuxing,
            "最强五行": strongest[0],
            "最弱五行": weakest[0],
            "农历": f"{self.lunar.getYearInChinese()}年{self.lunar.getMonthInChinese()}月{self.lunar.getDayInChinese()}",
            "生肖": self.lunar.getYearShengXiao(),
            "星座": self.solar.getXingZuo()
        }
    
    def get_personality_traits(self) -> list:
        """
        根据五行分析性格特征
        
        Returns:
            性格特征列表
        """
        wuxing = self.analyze_wuxing()
        traits = []
        
        if wuxing["金"] >= 2:
            traits.append("果断坚毅，具有领导力")
        if wuxing["木"] >= 2:
            traits.append("仁慈善良，富有同情心")
        if wuxing["水"] >= 2:
            traits.append("聪明灵活，善于思考")
        if wuxing["火"] >= 2:
            traits.append("热情积极，充满活力")
        if wuxing["土"] >= 2:
            traits.append("稳重踏实，值得信赖")
            
        return traits if traits else ["性格平衡，五行调和"]
