"""OH MY GOD package built upon rich console interface"""

__version__ = "0.1.1"


from .main import OhMyGod
from .message import Message as HolyMessage
from .format import Color as HolyColor

__all__ = ["OhMyGod", "HolyMessage", "HolyColor"]
