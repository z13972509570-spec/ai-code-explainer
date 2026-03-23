"""测试可视化器"""
from src.visualizer import Visualizer


SAMPLE_PARSED = {
    "functions": [
        {"name": "hello", "lineno": 1, "args": [], "class": None, "is_async": False},
        {"name": "add", "lineno": 5, "args": ["a", "b"], "class": None, "is_async": False},
        {"name": "method", "lineno": 10, "args": ["self"], "class": "MyClass", "is_async": False},
    ],
    "classes": [
        {"name": "MyClass", "lineno": 8},
    ],
    "imports": ["os"],
}


class TestVisualizer:
    """测试 Visualizer"""

    def test_to_mermaid_contains_structure(self):
        result = Visualizer().to_mermaid(SAMPLE_PARSED)
        assert "```mermaid" in result
        assert "flowchart TD" in result
        assert "hello()" in result
        assert "MyClass" in result

    def test_to_mermaid_class_method_connected(self):
        """测试类和方法之间有连线"""
        result = Visualizer().to_mermaid(SAMPLE_PARSED)
        # 应该有 --> 连线
        assert "-->" in result

    def test_to_mermaid_async_prefix(self):
        """测试 async 函数有 ⚡ 前缀"""
        parsed = {
            "functions": [{"name": "fetch", "lineno": 1, "args": [], "class": None, "is_async": True}],
            "classes": [],
            "imports": [],
        }
        result = Visualizer().to_mermaid(parsed)
        assert "⚡" in result

    def test_to_plantuml_contains_structure(self):
        result = Visualizer().to_plantuml(SAMPLE_PARSED)
        assert "@startuml" in result
        assert "@enduml" in result
        assert "class MyClass" in result

    def test_to_plantuml_method_in_class(self):
        """测试类的方法正确出现在类图中"""
        result = Visualizer().to_plantuml(SAMPLE_PARSED)
        assert "method(self)" in result

    def test_to_plantuml_standalone_function(self):
        """测试独立函数以 note 形式出现"""
        result = Visualizer().to_plantuml(SAMPLE_PARSED)
        assert "hello" in result
        assert "add" in result

    def test_to_mermaid_empty(self):
        """测试空输入不报错"""
        result = Visualizer().to_mermaid({"functions": [], "classes": [], "imports": []})
        assert "```mermaid" in result

    def test_to_plantuml_empty(self):
        """测试空输入不报错"""
        result = Visualizer().to_plantuml({"functions": [], "classes": [], "imports": []})
        assert "@startuml" in result
        assert "@enduml" in result
