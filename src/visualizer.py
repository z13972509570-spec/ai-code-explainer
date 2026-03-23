"""可视化器"""
from typing import Dict, List, Tuple


class Visualizer:
    """生成可视化图表"""
    
    def to_mermaid(self, parsed: Dict) -> str:
        """生成 Mermaid 流程图
        
        Args:
            parsed: 解析结果字典
            
        Returns:
            Mermaid 格式的流程图代码
        """
        lines = ["```mermaid", "flowchart TD"]
        
        # 添加函数节点
        func_ids = {}
        for i, func in enumerate(parsed.get("functions", [])):
            func_id = f"F{i}"
            func_ids[func["name"]] = func_id
            prefix = "async " if func.get("is_async") else ""
            lines.append(f"    {func_id}[`{prefix}{func['name']}()`]")
        
        # 添加类节点
        class_ids = {}
        for i, cls in enumerate(parsed.get("classes", [])):
            class_id = f"C{i}"
            class_ids[cls["name"]] = class_id
            lines.append(f"    {class_id}[(`{cls['name']}`)]")
        
        # 添加连线（类到其方法）
        # 注：这里需要更复杂的 AST 分析来确定方法归属
        # 暂时保持简单实现
        
        lines.append("```")
        return "\n".join(lines)
    
    def to_plantuml(self, parsed: Dict) -> str:
        """生成 PlantUML 类图
        
        Args:
            parsed: 解析结果字典
            
        Returns:
            PlantUML 格式的类图代码
        """
        lines = ["@startuml"]
        
        # 添加类定义
        for cls in parsed.get("classes", []):
            lines.append(f"class {cls['name']} {{")
            lines.append("    --")
            lines.append("}")
        
        # 注：完整的方法关联需要在 parser 中记录方法所属的类
        # 当前 parser 没有这个信息，所以暂时只显示类定义
        
        lines.append("@enduml")
        return "\n".join(lines)
