import importlib
from importlib.machinery import ModuleSpec
import importlib.util
import os
import sys
from types import ModuleType
from rich.pretty import pprint

import click

from pathlib import Path, WindowsPath, PureWindowsPath, PosixPath, PurePosixPath

import functools

class ClickD(click.MultiCommand):
    def __init__(
        self, 
        *args, 
        dpath: str, 
        ignore=[None], 
        **kwargs
    ):
        super().__init__(*args, **kwargs)

        self.ignore = ignore

        self.subcmds_dir = Path(dpath).resolve()


    def list_commands(self, ctx):
        all_cmds = []

        for name in os.listdir(self.subcmds_dir):
            if name in self.ignore:
                continue

            elif name.endswith(".py") and not name.startswith('__'):
                all_cmds.append(name[0:-3])

            elif (self.subcmds_dir / Path(name)).is_dir() and (self.subcmds_dir / Path(name) / "__init__.py").exists():
                all_cmds.append(name)
        
        all_cmds.sort()

        return all_cmds


    def get_command(self, ctx, cmd_name):
        ns = {}

        path = self.subcmds_dir / Path(cmd_name)

        if path.exists() and path.is_dir():
            path = path / "__init__.py"
        else:
            path = Path(str(path) + ".py")

        with open(path) as f:
            code = compile(f.read(), cmd_name + ".py", "exec")

            eval(code, ns, ns)

            return ns[cmd_name]            

def clickd(
    func=None,
    *,
    dpath: str | Path = ".",
    ignore: list[str | Path | None] = [None]
):
    @functools.wraps(func)
    def clickd_(*args, **kwargs):
        return click.command(*args, cls=ClickD, dpath=dpath, ignore=ignore, **kwargs)
    return clickd_()

def dev():
    print("YOLO")