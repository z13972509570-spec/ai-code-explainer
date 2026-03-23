"""代码解析器"""
import ast
from typing import Dict, List, Optional


class CodeParser:
    """解析代码结构"""
    
    def __init__(self, language: str = "python"):
        self.language = language
    
    def parse(self, code: str) -> Dict:
        """解析代码"""
        if self.language == "python":
            return self._parse_python(code)
        return {"functions": [], "classes": [], "imports": []}
    
    def _parse_python(self, code: str) -> Dict:
        """解析 Python 代码"""
        try:
            tree = ast.parse(code)
            
            functions = []
            classes = []
            imports = []
            
            for node in ast.walk(tree):
                if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)):
                    functions.append({
                        "name": node.name,
                        "lineno": node.lineno,
                        "args": [a.arg for a in node.args.args],
                        "is_async": isinstance(node, ast.AsyncFunctionDef),
                    })
                elif isinstance(node, ast.ClassDef):
                    classes.append({
                        "name": node.name,
                        "lineno": node.lineno,
                    })
                elif isinstance(node, ast.Import):
                    imports.extend([a.name for a in node.names])
                elif isinstance(node, ast.ImportFrom):
                    if node.module:
                        imports.append(node.module)
            
            return {
                "functions": functions,
                "classes": classes,
                "imports": list(set(imports)),  # 去重
            }
        except SyntaxError as e:
            return {"functions": [], "classes": [], "imports": [], "error": str(e)}
