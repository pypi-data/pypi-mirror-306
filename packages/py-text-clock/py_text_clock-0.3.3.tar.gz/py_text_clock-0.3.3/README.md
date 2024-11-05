# Py-Clock
![Pipeline](https://github.com/manojmanivannan/py-clock/actions/workflows/test.yml/badge.svg)
[![latest tag](https://img.shields.io/github/v/tag/manojmanivannan/py-clock.svg?label=latest%20tag&sort=semver)](https://pypi.org/project/py-text-clock/)

A verbose clock which prints the time in words in a matrix

```bash

Usage: py-clock [OPTIONS]

Options:
    -s, --show    Show the current time
    -m, --matrix  Show time as matrix
    -d, --debug   Run in debug mode
    -h, --help    Show this message and exit.
```

py-clock can print the current time in words format.

For example: if the time is 13:50, it prints 
        
**I T** L **I S** A S T H **T E N**\
A C F I F T E E N D C O\
T W E N T Y X F I V E W\
T H I R T Y F T E N O S\
**M I N U T E S** E **T O** U R\
P A S T O R U F O U R T\
S E V E N X T W E L V E\
N I N E D I V E C **T W O** \
E I G H T F E L E V E N\
S I X T H R E E O N E G\
T E N S E Z O' C L O C K


## Setup Env
Make sure you have Python and the `poetry` package install. From inside the project directory
- `poetry shell` ( this will create a new virtual env and activate it)
- `poetry install` ( this will install dependencies)

## Install from PyPI
- `pip install py-text-clock`


# Use the tool
After activating the virtual env,
```bash
(venv) C:\Users\manoj\Documents\MANOJ\Github\py-clock>py-clock -s -m
```
**I T** L **I S** A S T H T E N\
A C F I F T E E N D C O\
**T W E N T Y** X **F I V E** W\
T H I R T Y F T E N O S\
**M I N U T E S** E T O U R\
**P A S T** O R U F O U R T\
S E V E N X T W E L V E\
N I N E D I V E C T W O\
E I G H T F E L E V E N\
S I X T H R E E **O N E** G\
T E N S E Z O' C L O C K\
```
