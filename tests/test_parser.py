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
        assert result["functions"][0]["is_async"] is False
    
    def test_parse_async_function(self):
        """测试解析异步函数"""
        code = "async def fetch():\n    pass"
        parser = CodeParser()
        result = parser.parse(code)
        
        assert len(result["functions"]) == 1
        assert result["functions"][0]["name"] == "fetch"
        assert result["functions"][0]["is_async"] is True
    
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
    
    def test_parse_duplicate_imports(self):
        """测试导入去重"""
        code = "import os\nimport os\nfrom os import path"
        parser = CodeParser()
        result = parser.parse(code)
        
        # 应该去重
        assert result["imports"].count("os") == 1
    
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
        assert len(result["imports"]) == 2
    
    def test_parse_invalid_code(self):
        """测试解析无效代码"""
        code = "def invalid(\n    pass"
        parser = CodeParser()
        result = parser.parse(code)
        
        assert "error" in result
    
    def test_parse_empty_code(self):
        """测试解析空代码"""
        code = ""
        parser = CodeParser()
        result = parser.parse(code)
        
        assert result["functions"] == []
        assert result["classes"] == []
        assert result["imports"] == []
    
    def test_parse_unsupported_language(self):
        """测试不支持的语言"""
        parser = CodeParser(language="javascript")
        result = parser.parse("function hello() {}")
        
        assert result["functions"] == []
        assert result["classes"] == []
