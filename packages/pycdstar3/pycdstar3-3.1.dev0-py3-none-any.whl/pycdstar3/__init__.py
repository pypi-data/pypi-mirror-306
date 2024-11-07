__version__ = "3.1-dev"
__url__ = "https://cdstar.gwdg.de/"

from .api import *  # noqa: F403 F401
from . import api

__all__ = api.__all__
