"""测试可视化器"""
import pytest
from src.visualizer import Visualizer


class TestVisualizer:
    """测试 Visualizer"""
    
    def test_to_mermaid(self):
        """测试 Mermaid 图表生成"""
        parsed = {
            "functions": [
                {"name": "hello", "lineno": 1, "args": []},
                {"name": "add", "lineno": 5, "args": ["a", "b"]},
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
    
    def test_to_plantuml(self):
        """测试 PlantUML 图表生成"""
        parsed = {
            "functions": [
                {"name": "hello", "lineno": 1, "args": []},
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