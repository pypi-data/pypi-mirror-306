# ClickD
Adds a click-based decorator that allows you to specify the directory with all the files being the subcommands/groups; and allows nesting the decorator--in the subdirectories' init-files--to traverse a directory tree for a quicker and cleaner cli-code layout.

## Install
```
pip install clickd
```

## Usage

Decorate the top-level--and all directory-modules' \_\_init\_\_ under--with the `clickd` 
decorator.


```
# <package-root-folder>/<cli-interface-top-level-folder>

./clickd/tests/cli  # <- this is the real test/example directory in this repo.
│   a.py
│   b.py
│   __init__.py
│
├───c
│   │   d.py
│   │   __init__.py
│   │
│   └───__pycache__
│           e.cpython-312.pyc
│           __init__.cpython-312.pyc
│
├───e
│   │   f.py
│   │   __init__.py
│   │
│   ├───g
│   │       j.py
│   │       __init__.py
│   │
│   └───h
│           k.py
│           __init__.py
│
└───__pycache__
        a.cpython-312.pyc
        b.cpython-312.pyc
        __init__.cpython-311.pyc
        __init__.cpython-312.pyc
```

The `__init__.py` files will contain `@clickd(dirp=./clickd/tests/cli/<folder>)`; for e.g.,
`h/__init__.py` will have:
```
from clickd import clickd

@clickd(dpath="./clickd/tests/cli/e/h")
def h():
    pass
```

And all the init-files in `./clickd/tests/cli/e/h` (and `./clickd/tests/cli/e`, and `./clickd/tests/cli`, for that matter) will have this set-up; every `click.Group` that I want to automatically load
subcommands as individual files from. 

The subcommands will, for e.g., look like this (in this case `./clickd/tests/cli/e/h/k.py`):
```
import click

@click.command()
def k():
    print("k")
```

Click can be used interoperably; the only thing that won't work is the `@clickd` groups
don't allow the use of `.add_command()`; I can use `@click.group()` as long as it is in
a file found by the `@clickd(dirpath=<path-to-folder-containing-file-with-group>)` or 
it is chained by a regular instance of `click.Group` that eventually parents-back to 
the `@clickd()`, which is a `click.MultiCommand` subclass called `ClickD`.  

I can use `@click.command(cls=ClickD, dirp=<path>)` above my group, instead--as a note.