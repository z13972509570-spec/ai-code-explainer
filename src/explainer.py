"""代码解释器"""
from typing import Dict
from .parser import CodeParser


class Explainer:
    """AI 代码解释器"""

    def __init__(self, language: str = "python"):
        self.language = language
        self.parser = CodeParser(language=language)

    def explain(self, code: str, language: str = None) -> Dict:
        """解释代码，language 可覆盖初始化时的设置"""
        if language and language != self.language:
            parser = CodeParser(language=language)
        else:
            parser = self.parser
            language = self.language

        parsed = parser.parse(code)
        parsed["language"] = language

        # 生成解释
        explanations = []

        for func in parsed.get("functions", []):
            prefix = "异步函数" if func.get("is_async") else "函数"
            args_str = ", ".join(func["args"]) or "无"
            explanations.append(
                f"{prefix} `{func['name']}`: "
                f"接收参数 {args_str}，"
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
