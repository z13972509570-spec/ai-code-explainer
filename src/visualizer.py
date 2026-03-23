"""可视化器"""
from typing import Dict


class Visualizer:
    """生成可视化图表"""

    def to_mermaid(self, parsed: Dict) -> str:
        """生成 Mermaid 流程图，类与其方法之间有连线"""
        lines = ["```mermaid", "flowchart TD"]

        # 渲染类节点
        for i, cls in enumerate(parsed.get("classes", [])):
            lines.append(f'    C{i}["`**{cls["name"]}**`"]')

        # 渲染函数节点，并连接到所属类
        class_index = {cls["name"]: i for i, cls in enumerate(parsed.get("classes", []))}
        standalone_funcs = []

        for i, func in enumerate(parsed.get("functions", [])):
            prefix = "⚡ " if func.get("is_async") else ""
            lines.append(f'    F{i}["{prefix}{func["name"]}()"]')
            parent = func.get("class")
            if parent and parent in class_index:
                lines.append(f"    C{class_index[parent]} --> F{i}")
            else:
                standalone_funcs.append(i)

        lines.append("```")
        return "\n".join(lines)

    def to_plantuml(self, parsed: Dict) -> str:
        """生成 PlantUML 类图，正确渲染类的方法"""
        lines = ["@startuml"]

        # 按类分组函数
        class_methods: Dict[str, list] = {}
        for func in parsed.get("functions", []):
            parent = func.get("class")
            if parent:
                class_methods.setdefault(parent, []).append(func)

        for cls in parsed.get("classes", []):
            lines.append(f'class {cls["name"]} {{')
            for func in class_methods.get(cls["name"], []):
                args = ", ".join(func["args"])
                async_prefix = "{abstract} " if func.get("is_async") else ""
                lines.append(f"    +{async_prefix}{func['name']}({args})")
            lines.append("}")

        # 独立函数（不属于任何类）
        standalone = [f for f in parsed.get("functions", []) if not f.get("class")]
        if standalone:
            lines.append("")
            for func in standalone:
                args = ", ".join(func["args"])
                lines.append(f'note "func: {func["name"]}({args})" as N_{func["name"]}')

        lines.append("@enduml")
        return "\n".join(lines)
