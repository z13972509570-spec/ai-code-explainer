"""代码解释器"""
from typing import Dict
from .parser import CodeParser


class Explainer:
    """AI 代码解释器"""
    
    def __init__(self, language: str = "python"):
        self.parser = CodeParser(language=language)
        self.language = language
    
    def explain(self, code: str, language: Optional[str] = None) -> Dict:
        """解释代码
        
        Args:
            code: 要解释的代码字符串
            language: 编程语言，默认为 python
            
        Returns:
            包含解析结果、解释和摘要的字典
        """
        if language:
            self.parser = CodeParser(language=language)
        
        parsed = self.parser.parse(code)
        parsed["language"] = language or self.language
        
        # 生成解释
        explanations = []
        
        for func in parsed.get("functions", []):
            prefix = "异步函数" if func.get("is_async") else "函数"
            explanations.append(
                f"{prefix} `{func['name']}`: "
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
