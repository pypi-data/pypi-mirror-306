import ast
import pathlib
import typing

import typer

import zeropython.ast_cleaner
import zeropython.report

app = typer.Typer(pretty_exceptions_enable=False)


def _code_to_ast(
    file: pathlib.Path,
) -> tuple[typing.Union[ast.AST, None], zeropython.report.Report]:
    report = zeropython.report.Report()
    try:
        return zeropython.ast_cleaner.ast_clean(file.read_text(encoding="utf-8"), report)
    except UnicodeDecodeError as e:
        raise ValueError(f"{file.stem} is not a valid python file") from e


@app.command()
def check(file: pathlib.Path) -> None:
    _, report = _code_to_ast(file)
    print(report)


@app.command()
def clean(file: pathlib.Path, inplace: bool = False) -> None:
    clean_ast, _ = _code_to_ast(file)
    if clean_ast is None:
        return
    clean_code = ast.unparse(clean_ast)
    if inplace:
        file.write_text(clean_code)
        return

    print(clean_code)


@app.command()
def run(file: pathlib.Path) -> None:
    clean_ast, report = _code_to_ast(file)
    print(report)
    if clean_ast is None:
        return

    code = ast.unparse(clean_ast)
    exec(code, globals())


if __name__ == "__main__":
    app()
