import os, sys
import re

import rich
from mypy.version import __version__ as mypy_version
from rich.highlighter import RegexHighlighter
from rich.text import Text

from .__init__ import __version__
from .core import describe, parse_code, get_json

class TypeHighlighter(RegexHighlighter):
    base_style = "type."
    highlights = [
        r"(?:^|[\[\s,])(?P<screaming_snake_case>([A-Z0-9]{3,}(?:_[A-Z0-9]+)*))[^a-z]",
        r"(?:^|[\[\s,])(?P<snake_case>([a-z0-9]{3,}(?:_[a-z0-9]+)*))",
        r"(?P<camelCase>([a-z]+[A-Z]+\w+)+)",
        r"(?P<PascalCase>([A-Z][a-z0-9]+)+)",
        r"(?P<brace>[\{\[\(\)\]\}])",
        r"(?P<string>[\"\'].*[\"\'])",
    ]


def format_location(def_, typehint_text, file_name):
    line = def_.line
    end_line = def_.end_line
    column = def_.column + 1
    end_column = column + len(typehint_text)

    return f"[red]({file_name}:{line}{f'-{end_line}' if end_line else ''}:{column})[/red]"


def print_description(source_code: str, file_name: str, highlighter=TypeHighlighter()):
    defs = parse_code(source_code)
    typelist_regex = re.compile(r"<TypeList ([^>]+)>")
    format_typelist = lambda x: "[" + x.group(1) + "]"
    for def_ in defs:
        if def_ is None:
            continue
        typehint_text = str(def_).replace("?", "")
        if "<TypeList" in typehint_text:
            typehint_text = re.sub(typelist_regex, format_typelist,typehint_text)
        text = Text(typehint_text)
        highlighter.highlight(text)
        console.print(text, format_location(def_, typehint_text, file_name), ":", describe(def_))


if __name__ == "__main__":
    import argparse
    from pathlib import Path

    from rich.console import Console
    from rich.theme import Theme

    theme = Theme(
        {
            "type.brace": "bold magenta",
            "type.camelCase": "magenta",
            "type.PascalCase": "cyan",
            "type.snake_case": "green",
            "type.screaming_snake_case": "bold green",
            "type.string": "yellow",
        }
    )
    console = Console(highlight=False, theme=theme, emoji=False)
    v_info =  sys.version_info
    parser = argparse.ArgumentParser()
    parser.add_argument("file_or_directory")
    parser.add_argument("-j", "--json", action="store_true")
    parser.add_argument("-d", "--debug", action="store_true")
    parser.add_argument("-e", "--encoding", default="utf-8")
    parser.add_argument(
        "-v",
        "--version",
        action="version",
        version=f"typesplainer {__version__} running on mypy {mypy_version} on python {v_info.major}.{v_info.minor}.{v_info.micro}"
    )
    args = parser.parse_args()

    if args.debug:
        from rich.traceback import install

        install(show_locals=True)

    path = Path(sys.argv[1])

    if os.path.isdir(path):
        files = []
        for python_file in path.rglob("*.py"):
            files.append(python_file)
    else:
        files = [path]

    for file in files:
        with open(file, encoding=args.encoding) as f:
            if args.json:
                console.print_json(data=get_json(parse_code(f.read())))
            else:
                print_description(f.read(), file_name=file)
