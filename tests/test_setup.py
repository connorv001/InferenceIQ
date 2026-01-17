import openai
import anthropic
import pandas

def test_imports():
    assert openai.__version__ is not None
    assert anthropic.__version__ is not None
    assert pandas.__version__ is not None
