"""
Test API key loading from Streamlit secrets
"""
import os
import sys
from unittest.mock import Mock, patch

def test_streamlit_secrets_priority():
    """Test that Streamlit secrets take priority over env vars"""
    print("Testing Streamlit secrets priority...")
    
    # Set both environment variable and mock Streamlit secrets
    os.environ['OPENAI_API_KEY'] = 'env_key'
    os.environ['OPENAI_MODEL'] = 'env_model'
    
    # Mock streamlit module
    mock_st = Mock()
    mock_st.secrets = {
        'OPENAI_API_KEY': 'streamlit_key',
        'OPENAI_MODEL': 'streamlit_model',
        'OPENAI_API_BASE': 'https://api.example.com'
    }
    
    with patch.dict('sys.modules', {'streamlit': mock_st}):
        # Force reload to pick up mocked streamlit
        import importlib
        if 'ai_fortune_teller' in sys.modules:
            del sys.modules['ai_fortune_teller']
        
        from ai_fortune_teller import AIFortuneTeller
        teller = AIFortuneTeller()
        
        # Streamlit secrets should take priority
        assert teller.api_key == 'streamlit_key', f"Expected 'streamlit_key', got '{teller.api_key}'"
        assert teller.model == 'streamlit_model', f"Expected 'streamlit_model', got '{teller.model}'"
        assert teller.api_base == 'https://api.example.com', f"Expected 'https://api.example.com', got '{teller.api_base}'"
        
        print("✓ Streamlit secrets correctly take priority over environment variables")
        return True
    
    # Clean up
    if 'OPENAI_API_KEY' in os.environ:
        del os.environ['OPENAI_API_KEY']
    if 'OPENAI_MODEL' in os.environ:
        del os.environ['OPENAI_MODEL']

def test_streamlit_secrets_partial():
    """Test fallback when only API key is in Streamlit secrets"""
    print("\nTesting partial Streamlit secrets configuration...")
    
    os.environ['OPENAI_MODEL'] = 'env_model_fallback'
    
    # Create a custom mock secrets dict that supports .get()
    class MockSecrets(dict):
        def __contains__(self, key):
            return dict.__contains__(self, key)
    
    # Mock streamlit with only API key
    mock_st = Mock()
    mock_st.secrets = MockSecrets({'OPENAI_API_KEY': 'streamlit_key_only'})
    
    with patch.dict('sys.modules', {'streamlit': mock_st}):
        # Force reload
        if 'ai_fortune_teller' in sys.modules:
            del sys.modules['ai_fortune_teller']
        
        from ai_fortune_teller import AIFortuneTeller
        teller = AIFortuneTeller()
        
        assert teller.api_key == 'streamlit_key_only'
        # Model should use default since not in secrets
        assert teller.model == 'gpt-3.5-turbo', f"Expected default model, got '{teller.model}'"
        assert teller.api_base is None
        
        print("✓ Correctly handles partial Streamlit secrets configuration")
        return True
    
    # Clean up
    if 'OPENAI_MODEL' in os.environ:
        del os.environ['OPENAI_MODEL']

if __name__ == "__main__":
    print("Testing Streamlit secrets integration...\n")
    
    try:
        results = []
        results.append(test_streamlit_secrets_priority())
        results.append(test_streamlit_secrets_partial())
        
        if all(results):
            print("\n✅ All Streamlit secrets tests passed!")
            sys.exit(0)
        else:
            print("\n❌ Some tests failed")
            sys.exit(1)
    except Exception as e:
        print(f"\n❌ Test error: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
