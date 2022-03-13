<div align="center">
<img src="https://i.imgur.com/5IFkzIf.png" width="128px">
<h1>typesplainer</h1>
 A Python type explainer!

Available [as a cli](https://pypi.org/project/typesplainer), [as a website](https://typesplainer.herokuapp.com), [as a vscode extension (WIP)](#)

[![PyPI](https://img.shields.io/pypi/v/typesplainer?label=cli)](https://pypi.org/project/typesplainer) [![Website](https://img.shields.io/website?url=https%3A%2F%2Ftypesplainer.herokuapp.com)](https://typesplainer.herokuapp.com) [![Visual Studio Marketplace Version](https://img.shields.io/visual-studio-marketplace/v/WasiMaster.typesplainer?label=vscode)](https://marketplace.visualstudio.com/items?itemName=WasiMaster.typesplainer)

</div>

## Usage

First, install the package with `pip install typesplainer`

Then like any other tool such a `black`, `isort`. run typesplainer on your desired files or directory. It will automatically find all types and then explain them for you. e.g.

```sh
python -m typesplainer my_file.py
python -m typesplainer my_directory
```

### Features

- Very performant! Takes 1.7 seconds (YMMV) to explain the entire [python rich library source code](https://github.com/Textualize/rich) consisting of around 50,000 lines!
- Colorized output. Output with colors is going to make sure your eyes feel refreshed.
- Intelligent explanation. Takes pluralization, pronoun usage, article usage, correct grammar into account.
- Best in class parser. It does not rely on some substandard AI based description generator, instead it parses the file using [mypy](https://github.com/mypy/mypy)'s custom parser and shows the most accurate description
