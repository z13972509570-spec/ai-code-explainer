"""测试解析器"""
import pytest
from src.parser import CodeParser


class TestCodeParser:
    """测试 CodeParser"""
    
    def test_parse_simple_function(self):
        """测试解析简单函数"""
        code = "def hello():\n    pass"
        parser = CodeParser()
        result = parser.parse(code)
        
        assert len(result["functions"]) == 1
        assert result["functions"][0]["name"] == "hello"
    
    def test_parse_function_with_args(self):
        """测试解析带参数的函数"""
        code = "def add(a, b):\n    return a + b"
        parser = CodeParser()
        result = parser.parse(code)
        
        assert len(result["functions"]) == 1
        assert result["functions"][0]["args"] == ["a", "b"]
    
    def test_parse_class(self):
        """测试解析类"""
        code = "class MyClass:\n    pass"
        parser = CodeParser()
        result = parser.parse(code)
        
        assert len(result["classes"]) == 1
        assert result["classes"][0]["name"] == "MyClass"
    
    def test_parse_imports(self):
        """测试解析导入"""
        code = "import os\nimport sys\nfrom typing import Dict"
        parser = CodeParser()
        result = parser.parse(code)
        
        assert "os" in result["imports"]
        assert "sys" in result["imports"]
        assert "typing" in result["imports"]
    
    def test_parse_complex_code(self):
        """测试解析复杂代码"""
        code = """
import os
from typing import List

class DataProcessor:
    def process(self, data: List):
        return [x for x in data]

def transform(item):
    return item * 2
"""
        parser = CodeParser()
        result = parser.parse(code)
        
        assert len(result["functions"]) == 2
        assert len(result["classes"]) == 1
        assert len(result["imports"]) >= 2
    
    def test_parse_invalid_code(self):
        """测试解析无效代码"""
        code = "def invalid(\n    pass"
        parser = CodeParser()
        result = parser.parse(code)
        
        assert "error" in result