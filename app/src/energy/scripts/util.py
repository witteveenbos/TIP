import os
import sys
import django
from pathlib import Path
from jinja2 import Template, Environment, FileSystemLoader, meta


def django_setup():
    """small uitility to setup django in a script, alows for interactive developement"""
    src = (Path("/workspace") / "src").resolve().absolute()
    os.chdir(src)
    sys.path.insert(0, src)
    django.setup()


def open_template(fp: Path) -> Template:
    with open(fp) as file_:
        return Template(file_.read())


def get_variables(fp: Path) -> set[str]:
    env = Environment()
    with open(fp) as file_:
        return meta.find_undeclared_variables(env.parse(file_.read()))


def substitute_jinja2_variables(fp: Path) -> str:
    t = open_template(fp)
    t_args = {}
    for var in get_variables(fp):
        t_args[var] = {"key": var}
    return t.render(**t_args)
