"""CLI 入口"""
import json
import click
from src import Explainer, Visualizer


@click.command()
@click.argument("file_path", type=click.Path(exists=True))
@click.option(
    "--format", "-f",
    type=click.Choice(["text", "json", "mermaid", "plantuml"]),
    default="text",
    help="输出格式",
)
@click.option(
    "--language", "-l",
    default="python",
    help="代码语言（默认 python）",
)
def main(file_path: str, format: str, language: str):
    """解释代码文件并生成分析报告"""
    with open(file_path, "r", encoding="utf-8") as f:
        code = f.read()

    explainer = Explainer(language=language)
    result = explainer.explain(code)

    if format == "json":
        click.echo(json.dumps(result, indent=2, ensure_ascii=False))
    elif format == "mermaid":
        viz = Visualizer()
        click.echo(viz.to_mermaid(result))
    elif format == "plantuml":
        viz = Visualizer()
        click.echo(viz.to_plantuml(result))
    else:
        click.echo(f"# 📊 代码分析报告: {file_path}\n")
        click.echo("## 📝 概览")
        click.echo(result.get("summary", ""))
        click.echo("")
        click.echo("## 🔧 详情\n")
        for exp in result.get("explanations", []):
            click.echo(f"- {exp}")


if __name__ == "__main__":
    main()
