from importlib import import_module

from fastapi import FastAPI

from furious.cli.config import get_config_key
from furious.cli.exceptions import FuriousException
from furious.cli.setup import is_set_up


def guess_and_import_module():
    workdir = get_config_key("workdir")
    package_name = workdir.name
    potential_modules = (
        "main",
        "app",
        "main.main",
        "main.app",
        "app.main",
        "app.app",
        f"{package_name}.main",
        f"{package_name}.app",
    )
    for m in potential_modules:
        try:
            module = import_module(m)
        except ImportError:
            continue

        if module.__file__:  # return if not a package.
            return module  # otherwise, continue

    raise FuriousException(
        "Module with the FastAPI application cannot be found. "
        "Please specify it explicitly in pyproject.toml under [tools.furious]"
        " e.g. app = 'main.app:app'"
    )


def get_app_import_string() -> str:
    assert is_set_up()
    app_path = get_config_key("app")
    if app_path:
        return app_path

    module = guess_and_import_module()
    app_name, _ = find_app(module)
    return f"{module.__name__}:{app_name}"


def import_app():
    assert is_set_up()
    app_path = get_config_key("app")

    if app_path is None:
        module = guess_and_import_module()
        _, app = find_app(module)
        return app
    else:
        module_name, app_name = app_path.rsplit(":", 1)
        module = import_module(module_name)
        return getattr(module, app_name)


def find_app(module):
    for name, obj in module.__dict__.items():
        if isinstance(obj, FastAPI):
            return name, obj
    raise FuriousException(
        "ASGI application cannot be discovered.\n"
        "You have to specify application path explicitly in pyproject.toml"
    )
