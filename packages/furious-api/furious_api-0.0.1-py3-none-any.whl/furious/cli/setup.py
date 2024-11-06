import site

from furious.cli.config import get_config_key

_is_set_up = False


def is_set_up():
    return _is_set_up


def set_up_furious():
    workdir = get_config_key("workdir")
    if workdir is not None:
        add_workdir_to_path(workdir)
    global _is_set_up
    _is_set_up = True


def add_workdir_to_path(workdir):
    """Adds workidr to sys.path"""
    site.addsitedir(workdir)
