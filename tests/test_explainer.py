"""测试解释器"""
from src.explainer import Explainer


class TestExplainer:
    """测试 Explainer"""

    def test_explain_simple_code(self):
        code = "def hello():\n    pass"
        result = Explainer().explain(code)
        assert "explanations" in result
        assert "summary" in result
        assert result["language"] == "python"

    def test_explain_with_class(self):
        code = """
class MyClass:
    def method(self):
        pass
"""
        result = Explainer().explain(code)
        assert len(result["classes"]) == 1
        assert len(result["functions"]) == 1
        explanations_text = " ".join(result["explanations"])
        assert "MyClass" in explanations_text

    def test_explain_summary(self):
        code = """
import os

def func1():
    pass

def func2():
    pass
"""
        result = Explainer().explain(code)
        assert "2 个函数" in result["summary"]
        assert "1 个导入" in result["summary"]

    def test_explain_language_passed_to_parser(self):
        """测试 language 参数正确传递给 CodeParser"""
        explainer = Explainer(language="python")
        assert explainer.parser.language == "python"

    def test_explain_async_function(self):
        """测试 async def 被标记为异步函数"""
        code = "async def fetch(url):\n    pass"
        result = Explainer().explain(code)
        assert len(result["functions"]) == 1
        assert result["functions"][0]["is_async"] is True
        assert "异步函数" in result["explanations"][0]

    def test_explain_empty_code(self):
        """测试空代码不报错"""
        result = Explainer().explain("")
        assert result["summary"] == "发现 0 个函数，0 个类，0 个导入"
        assert result["explanations"] == []
