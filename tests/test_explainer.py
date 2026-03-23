"""测试解释器"""
import pytest
from src.explainer import Explainer


class TestExplainer:
    """测试 Explainer"""
    
    def test_explain_simple_code(self):
        """测试解释简单代码"""
        code = "def hello():\n    pass"
        explainer = Explainer()
        result = explainer.explain(code)
        
        assert "explanations" in result
        assert "summary" in result
        assert "functions" in result
        assert result["language"] == "python"
    
    def test_explain_async_function(self):
        """测试解释异步函数"""
        code = "async def fetch():\n    pass"
        explainer = Explainer()
        result = explainer.explain(code)
        
        assert len(result["functions"]) == 1
        assert "异步函数" in result["explanations"][0]
    
    def test_explain_with_class(self):
        """测试解释包含类的代码"""
        code = """
class MyClass:
    def method(self):
        pass
"""
        explainer = Explainer()
        result = explainer.explain(code)
        
        assert len(result["classes"]) == 1
        assert len(result["functions"]) == 1
        explanations_text = " ".join(result["explanations"])
        assert "MyClass" in explanations_text
    
    def test_explain_summary(self):
        """测试摘要生成"""
        code = """
import os

def func1():
    pass

def func2():
    pass
"""
        explainer = Explainer()
        result = explainer.explain(code)
        
        assert "2 个函数" in result["summary"]
        assert "1 个导入" in result["summary"]
    
    def test_explain_language_parameter(self):
        """测试 language 参数传递"""
        code = "def hello():\n    pass"
        explainer = Explainer()
        result = explainer.explain(code, language="python")
        
        assert result["language"] == "python"
    
    def test_explain_empty_code(self):
        """测试解释空代码"""
        code = ""
        explainer = Explainer()
        result = explainer.explain(code)
        
        assert result["summary"] == "发现 0 个函数，0 个类，0 个导入"
