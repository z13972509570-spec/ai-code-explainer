"""代码解释器"""
from typing import Dict
from .parser import CodeParser


class Explainer:
    """AI 代码解释器"""
    
    def __init__(self):
        self.parser = CodeParser()
    
    def explain(self, code: str, language: str = "python") -> Dict:
        """解释代码"""
        parsed = self.parser.parse(code)
        parsed["language"] = language
        
        # 生成解释
        explanations = []
        
        for func in parsed.get("functions", []):
            explanations.append(
                f"函数 `{func['name']}`: "
                f"接收参数 {', '.join(func['args']) or '无'}，"
                f"位于第 {func['lineno']} 行"
            )
        
        for cls in parsed.get("classes", []):
            explanations.append(
                f"类 `{cls['name']}`: "
                f"定义在第 {cls['lineno']} 行"
            )
        
        parsed["explanations"] = explanations
        parsed["summary"] = (
            f"发现 {len(parsed['functions'])} 个函数，"
            f"{len(parsed['classes'])} 个类，"
            f"{len(parsed['imports'])} 个导入"
        )
        
        return parsed
