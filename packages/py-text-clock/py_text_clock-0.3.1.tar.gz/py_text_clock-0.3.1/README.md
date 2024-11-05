# Py-Clock
![Pipeline](https://github.com/manojmanivannan/py-clock/actions/workflows/release.yml/badge.svg?branch=main)
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
The version used is Python 3.11.0
- `python -m venv venv`
- `source ./ven/bin/activate` for linux or `.\venv\Scripts\activate` for windows

## Install the tool
- `python setup.py install`

## Install from PyPI
- `pip install py-clock`

## Run tests
This requires `pytest` to be installed.
- `python -m pytest -v tests`

# Use the tool
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
