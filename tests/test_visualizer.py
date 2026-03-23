"""测试可视化器"""
import pytest
from src.visualizer import Visualizer


class TestVisualizer:
    """测试 Visualizer"""
    
    def test_to_mermaid(self):
        """测试 Mermaid 图表生成"""
        parsed = {
            "functions": [
                {"name": "hello", "lineno": 1, "args": [], "is_async": False},
                {"name": "add", "lineno": 5, "args": ["a", "b"], "is_async": False},
            ],
            "classes": [
                {"name": "MyClass", "lineno": 10},
            ],
            "imports": ["os"],
        }
        
        viz = Visualizer()
        result = viz.to_mermaid(parsed)
        
        assert "```mermaid" in result
        assert "flowchart TD" in result
        assert "hello()" in result
        assert "MyClass" in result
    
    def test_to_mermaid_async(self):
        """测试 Mermaid 异步函数标记"""
        parsed = {
            "functions": [
                {"name": "fetch", "lineno": 1, "args": [], "is_async": True},
            ],
            "classes": [],
            "imports": [],
        }
        
        viz = Visualizer()
        result = viz.to_mermaid(parsed)
        
        assert "async fetch()" in result
    
    def test_to_plantuml(self):
        """测试 PlantUML 图表生成"""
        parsed = {
            "functions": [
                {"name": "hello", "lineno": 1, "args": [], "is_async": False},
            ],
            "classes": [
                {"name": "MyClass", "lineno": 5},
            ],
            "imports": [],
        }
        
        viz = Visualizer()
        result = viz.to_plantuml(parsed)
        
        assert "@startuml" in result
        assert "@enduml" in result
        assert "class MyClass" in result
    
    def test_to_plantuml_empty(self):
        """测试空代码的 PlantUML"""
        parsed = {
            "functions": [],
            "classes": [],
            "imports": [],
        }
        
        viz = Visualizer()
        result = viz.to_plantuml(parsed)
        
        assert "@startuml" in result
        assert "@enduml" in result
