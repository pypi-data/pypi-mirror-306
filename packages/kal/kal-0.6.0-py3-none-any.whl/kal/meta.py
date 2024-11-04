import importlib.metadata
import tomllib

from kal import path

try:
    with open(path.PROJECT_DIR / "pyproject.toml", "rb") as f:
        pyproject = tomllib.load(f)
    __version__ = pyproject["tool"]["poetry"]["version"]
except Exception as e:
    __version__ = importlib.metadata.version('kal')
