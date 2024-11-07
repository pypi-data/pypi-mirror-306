import enum
import tomllib
from functools import cache
from pathlib import Path

from pydantic import BaseModel, ConfigDict, Field, field_validator

from furious.cli.exceptions import FuriousException


class REPLs(enum.StrEnum):
    """
    Supported REPLs to use with `> furious shell` command
    """

    PT: str = "ptpython"
    B: str = "bpython"
    I: str = "ipython"  # noqa

    @classmethod
    def values(cls):
        return [i.value for i in cls]


class Config(BaseModel):
    model_config = ConfigDict(frozen=True)

    app: str | None = None
    workdir: Path = Field(
        default_factory=lambda: Path(""), validate_default=True
    )
    shell: REPLs = REPLs.PT
    host: str = "0.0.0.0"
    port: int = 8001

    @field_validator("workdir")
    @classmethod
    def workdir_to_abspath(cls, value: Path):
        return value.resolve()


def get_config_key(key):
    return getattr(get_config(), key)


@cache
def get_config():
    config_data = _read_config()
    return Config(**config_data)


def _read_config():
    try:
        f = open("pyproject.toml", "rb")
    except FileNotFoundError:
        print("pyproject.toml is not found. Using default configuration")
        return {}

    try:
        data = tomllib.load(f)
    except Exception:
        raise FuriousException("Cannot parse pyproject.toml")
    finally:
        f.close()
    try:
        return data["tool"]["furious"]
    except KeyError:
        raise FuriousException(
            "section [tool.furios] is missing in pyproject.toml"
        )
