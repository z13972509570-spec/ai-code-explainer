"""可视化器"""
from typing import Dict


class Visualizer:
    """生成可视化图表"""
    
    def to_mermaid(self, parsed: Dict) -> str:
        """生成 Mermaid 图表"""
        lines = ["```mermaid", "flowchart TD"]
        
        for i, func in enumerate(parsed.get("functions", [])):
            lines.append(f"    F{i}[`{func['name']}()`]")
        
        for i, cls in enumerate(parsed.get("classes", [])):
            lines.append(f"    C{i}[(`{cls['name']}`)]")
        
        lines.append("```")
        return "\n".join(lines)
    
    def to_plantuml(self, parsed: Dict) -> str:
        """生成 PlantUML"""
        lines = ["@startuml"]
        
        for cls in parsed.get("classes", []):
            lines.append(f"class {cls['name']} {{")
            lines.append("    --")
            for func in parsed.get("functions", []):
                if func.get("class") == cls["name"]:
                    args = ", ".join(func["args"])
                    lines.append(f"    +{func['name']}({args})")
            lines.append("}")
        
        lines.append("@enduml")
        return "\n".join(lines)
