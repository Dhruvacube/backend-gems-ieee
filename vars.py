import configparser
import os
from pathlib import Path
from typing import Any

from sqlalchemy.orm import declarative_base

# only way to resolve the circular, yes this is the only way
class _MissingSentinel:
    __slots__ = ()

    def __eq__(self, other):
        return False

    def __bool__(self):
        return False

    def __hash__(self):
        return 0

    def __repr__(self):
        return "..."

    def __iter__(self):
        return iter([])

    def __len__(self):
        return 0


MISSING: Any = _MissingSentinel()

BASE_DIR = Path(__file__).resolve().parent  # In minato_namikaze/ folder
print(BASE_DIR)
CONFIG_FILE = BASE_DIR / ".ini"
DEFAULT_COMMAND_SELECT_LENGTH = 25
Base = declarative_base()


def token_get(tokenname: str = MISSING, all: bool = False) -> Any:
    """Helper function to get the credentials from the environment variables or from the configuration file

    :param tokenname: The token name to access
    :type tokenname: str
    :param all: Return all values from config filename, defaults to False
    :type all: bool, optional
    :raises RuntimeError: When all set :bool:`True` and `.ini` file is not found
    :return: The environment variables data requested if not found then None is returned
    :rtype: Any
    """
    if not all:
        if CONFIG_FILE.is_file():
            config = configparser.ConfigParser()
            config.read(CONFIG_FILE)
            sections = config.sections()
            for i in sections:
                for j in config:
                    if j.lower() == tokenname.lower():
                        return config[i][j]
            return
        return os.environ.get(tokenname, "False").strip("\n")
    if CONFIG_FILE.is_file():
        config = configparser.ConfigParser()
        config.read(CONFIG_FILE)
        return {i: config[i] for i in config.sections()}
    raise RuntimeError("Could not find .ini file")


class _envConfig:
    """A class which contains all token configuration"""

    def __init__(self):
        self.data: dict = token_get(all=True)
        for i in self.data:
            for j in self.data.get(i, MISSING):
                setattr(self, j.lower(), self.data[i].get(j))
                setattr(self, j.upper(), self.data[i].get(j))


envConfig: Any = _envConfig()