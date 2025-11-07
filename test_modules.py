"""
Basic tests for core modules
"""

def test_personality_prompts():
    """Test personality prompts module"""
    from personality_prompts import PersonalityPrompts
    
    # Test get_personality
    rational = PersonalityPrompts.get_personality('rational')
    assert rational['name'] == "理性大师"
    assert 'system_prompt' in rational
    
    gentle = PersonalityPrompts.get_personality('gentle')
    assert gentle['name'] == "温柔大师"
    
    sharp = PersonalityPrompts.get_personality('sharp')
    assert sharp['name'] == "毒舌大师"
    
    # Test get_all_personalities
    all_personalities = PersonalityPrompts.get_all_personalities()
    assert len(all_personalities) == 3
    assert 'rational' in all_personalities
    assert 'gentle' in all_personalities
    assert 'sharp' in all_personalities
    
    print("✓ PersonalityPrompts tests passed")


def test_emotion_engine():
    """Test emotion engine module"""
    from emotion_engine import EmotionEngine
    
    engine = EmotionEngine()
    
    # Test emotion analysis
    emotion, intensity = engine.analyze_emotion("我很开心")
    assert emotion == "positive"
    
    emotion, intensity = engine.analyze_emotion("我很难过")
    assert emotion == "negative"
    
    emotion, intensity = engine.analyze_emotion("我想问一下")
    assert emotion == "neutral"
    
    # Test topic detection
    topics = engine.detect_topic("我想问问工作的事情")
    assert "事业" in topics
    
    topics = engine.detect_topic("我想问问恋爱的事情")
    assert "感情" in topics
    
    # Test empathy response
    response = engine.generate_empathy_response("positive", 0.8)
    assert len(response) > 0
    
    response = engine.generate_empathy_response("negative", 0.8)
    assert len(response) > 0
    
    # Test response quality validation
    assert engine.validate_response_quality("这是一个关于八字的详细分析，包含了五行和命理的建议。") == True
    assert engine.validate_response_quality("好的") == False
    
    print("✓ EmotionEngine tests passed")


def test_bazi_calculator():
    """Test BaZi calculator module (requires lunar-python)"""
    try:
        from bazi_calculator import BaziCalculator
        
        # Test with a sample date
        calculator = BaziCalculator(1990, 1, 1, 12)
        
        # Test calculate_bazi
        bazi = calculator.calculate_bazi()
        assert '八字' in bazi
        assert '年柱' in bazi
        assert '月柱' in bazi
        assert '日柱' in bazi
        assert '时柱' in bazi
        
        # Test analyze_wuxing
        wuxing = calculator.analyze_wuxing()
        assert len(wuxing) == 5
        assert '金' in wuxing
        assert '木' in wuxing
        assert '水' in wuxing
        assert '火' in wuxing
        assert '土' in wuxing
        
        # Test get_fortune_base
        fortune = calculator.get_fortune_base()
        assert '八字' in fortune
        assert '五行' in fortune
        assert '最强五行' in fortune
        assert '生肖' in fortune
        
        # Test get_personality_traits
        traits = calculator.get_personality_traits()
        assert isinstance(traits, list)
        assert len(traits) > 0
        
        print("✓ BaziCalculator tests passed")
    except ImportError:
        print("⚠ BaziCalculator tests skipped (lunar-python not installed)")


def test_analytics():
    """Test analytics module"""
    import os
    import tempfile
    from analytics import UserAnalytics
    
    # Use secure temporary file for testing
    temp_fd, temp_file = tempfile.mkstemp(suffix='.json')
    os.close(temp_fd)  # Close the file descriptor as we'll use the path
    
    try:
        analytics = UserAnalytics(temp_file)
        
        # Test start_session
        analytics.start_session('rational')
        assert analytics.current_session is not None
        assert analytics.current_session['personality_type'] == 'rational'
        
        # Test record_interaction
        analytics.record_interaction('事业')
        assert analytics.current_session['interactions'] == 1
        assert '事业' in analytics.current_session['topics_discussed']
        
        # Test end_session
        analytics.end_session(4.5)
        assert analytics.data['total_sessions'] == 1
        
        # Test get_statistics
        stats = analytics.get_statistics()
        assert stats['total_sessions'] == 1
        assert stats['avg_rating'] == 4.5
        
        # Test get_personality_stats
        personality_stats = analytics.get_personality_stats()
        assert 'rational' in personality_stats
        assert personality_stats['rational'] == 1
        
        print("✓ Analytics tests passed")
    finally:
        # Clean up
        if os.path.exists(temp_file):
            os.remove(temp_file)


if __name__ == "__main__":
    print("Running module tests...\n")
    
    test_personality_prompts()
    test_emotion_engine()
    test_bazi_calculator()
    test_analytics()
    
    print("\n✅ All available tests passed!")
