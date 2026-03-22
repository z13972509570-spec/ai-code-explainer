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
        # 检查类是否在解释中（任意位置）
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