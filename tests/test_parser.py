"""测试解析器"""
from src.parser import CodeParser


class TestCodeParser:
    """测试 CodeParser"""

    def test_parse_simple_function(self):
        code = "def hello():\n    pass"
        result = CodeParser().parse(code)
        assert len(result["functions"]) == 1
        assert result["functions"][0]["name"] == "hello"

    def test_parse_function_with_args(self):
        code = "def add(a, b):\n    return a + b"
        result = CodeParser().parse(code)
        assert result["functions"][0]["args"] == ["a", "b"]

    def test_parse_class(self):
        code = "class MyClass:\n    pass"
        result = CodeParser().parse(code)
        assert len(result["classes"]) == 1
        assert result["classes"][0]["name"] == "MyClass"

    def test_parse_imports(self):
        code = "import os\nimport sys\nfrom typing import Dict"
        result = CodeParser().parse(code)
        assert "os" in result["imports"]
        assert "sys" in result["imports"]
        assert "typing" in result["imports"]

    def test_parse_complex_code(self):
        code = """
import os
from typing import List

class DataProcessor:
    def process(self, data: List):
        return [x for x in data]

def transform(item):
    return item * 2
"""
        result = CodeParser().parse(code)
        assert len(result["functions"]) == 2
        assert len(result["classes"]) == 1
        assert len(result["imports"]) == 2

    def test_parse_invalid_code(self):
        code = "def invalid(\n    pass"
        result = CodeParser().parse(code)
        assert "error" in result

    def test_parse_async_function(self):
        """测试解析 async def"""
        code = "async def fetch(url: str):\n    pass"
        result = CodeParser().parse(code)
        assert len(result["functions"]) == 1
        assert result["functions"][0]["name"] == "fetch"
        assert result["functions"][0]["is_async"] is True

    def test_parse_empty_code(self):
        """测试空代码"""
        result = CodeParser().parse("")
        assert result["functions"] == []
        assert result["classes"] == []
        assert result["imports"] == []

    def test_parse_method_belongs_to_class(self):
        """测试方法正确归属到类"""
        code = """
class MyClass:
    def my_method(self):
        pass
"""
        result = CodeParser().parse(code)
        method = next(f for f in result["functions"] if f["name"] == "my_method")
        assert method["class"] == "MyClass"

    def test_parse_standalone_function_has_no_class(self):
        """测试独立函数没有 class 字段"""
        code = "def standalone():\n    pass"
        result = CodeParser().parse(code)
        assert result["functions"][0]["class"] is None
