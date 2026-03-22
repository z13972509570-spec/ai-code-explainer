# AI Code Explainer

> 💡 一键解释任意代码，生成可视化分析图

## 功能

- 🔍 代码语法分析
- 📝 函数/变量解释
- 📊 控制流可视化
- 🔗 调用关系图
- 💬 多语言支持

## 使用

```bash
pip install -e .
python -m ai_code_explainer explain "path/to/code.py"
```

## API

```python
from ai_code_explainer import CodeExplainer

explainer = CodeExplainer()
result = explainer.explain(code)
print(result["explanation"])
```
