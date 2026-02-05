"""
Test API key loading from multiple sources
"""
import os
import sys

def test_api_key_from_env():
    """Test loading API key from environment variable"""
    print("Testing API key loading from environment variable...")
    
    # Set environment variable
    os.environ['OPENAI_API_KEY'] = 'test_key_from_env'
    os.environ['OPENAI_MODEL'] = 'gpt-4'
    
    try:
        from ai_fortune_teller import AIFortuneTeller
        teller = AIFortuneTeller()
        assert teller.api_key == 'test_key_from_env'
        assert teller.model == 'gpt-4'
        print("✓ Successfully loaded API key from environment variable")
        return True
    except Exception as e:
        print(f"✗ Failed to load API key from environment: {e}")
        return False
    finally:
        # Clean up
        if 'OPENAI_API_KEY' in os.environ:
            del os.environ['OPENAI_API_KEY']
        if 'OPENAI_MODEL' in os.environ:
            del os.environ['OPENAI_MODEL']

def test_api_key_missing():
    """Test error message when API key is missing"""
    print("\nTesting error message when API key is missing...")
    
    # Make sure no API key is set
    if 'OPENAI_API_KEY' in os.environ:
        del os.environ['OPENAI_API_KEY']
    
    try:
        from ai_fortune_teller import AIFortuneTeller
        # Force module reload to pick up environment changes
        import importlib
        import ai_fortune_teller
        importlib.reload(ai_fortune_teller)
        from ai_fortune_teller import AIFortuneTeller
        
        teller = AIFortuneTeller()
        print("✗ Should have raised ValueError")
        return False
    except ValueError as e:
        error_msg = str(e)
        # Check that error message includes helpful information
        if "Streamlit Cloud" in error_msg and ".env" in error_msg:
            print(f"✓ Correct error message: {error_msg}")
            return True
        else:
            print(f"✗ Error message doesn't include helpful information: {error_msg}")
            return False
    except Exception as e:
        print(f"✗ Unexpected error: {e}")
        return False

def test_streamlit_secrets_fallback():
    """Test that code handles missing streamlit gracefully"""
    print("\nTesting Streamlit secrets fallback...")
    
    # Set environment variable as fallback
    os.environ['OPENAI_API_KEY'] = 'test_key_from_env_fallback'
    
    try:
        from ai_fortune_teller import AIFortuneTeller
        teller = AIFortuneTeller()
        # Should fall back to env variable when streamlit secrets not available
        assert teller.api_key == 'test_key_from_env_fallback'
        print("✓ Successfully fell back to environment variable when Streamlit not available")
        return True
    except Exception as e:
        print(f"✗ Failed to handle Streamlit fallback: {e}")
        return False
    finally:
        if 'OPENAI_API_KEY' in os.environ:
            del os.environ['OPENAI_API_KEY']

if __name__ == "__main__":
    print("Testing API key loading mechanisms...\n")
    
    results = []
    results.append(test_api_key_from_env())
    results.append(test_api_key_missing())
    results.append(test_streamlit_secrets_fallback())
    
    if all(results):
        print("\n✅ All API key loading tests passed!")
        sys.exit(0)
    else:
        print("\n❌ Some tests failed")
        sys.exit(1)
