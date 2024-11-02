from enum import Enum
from typing import Dict, List
from colorama import Fore


class Color(Enum):
	DEFAULT = "default"
	BLACK = "black"
	RED = "red"
	YELLOW = "yellow"
	BLUE = "blue"
	CYAN = "cyan"

_COLOR_MAP: Dict[Color, str] = {
	Color.DEFAULT: Fore.RESET,
	Color.BLACK: Fore.BLACK,
	Color.RED: Fore.RED,
	Color.YELLOW: Fore.YELLOW,
	Color.BLUE: Fore.MAGENTA,
	Color.CYAN: Fore.CYAN,
    # BLACK           = 30
    #   RED             = 31
    #   GREEN           = 32
    #   YELLOW          = 33
    #   BLUE            = 34
    #   MAGENTA         = 35
    #   CYAN            = 36
    #   WHITE           = 37
}

def get_colored_message(message: str | List[str], highlight: Color, default: Color = Color.DEFAULT) -> str:
	"""Color a message with the given colors."""
	highlight_color = _COLOR_MAP.get(highlight)
	default_color = _COLOR_MAP.get(default)

	if not highlight_color or not default_color:
		raise ValueError("Invalid color")
	return _color_message(message, highlight_color, default_color)

def get_plain_message(message: str | List[str]) -> str:
	"""Convert colorizable message to a plain message."""
	return _color_message(message, "", "")

def _color_message(message: str | List[str], hightlight: str, default: str) -> str:
	"""Format a message with the given colors."""
	def color(message: str):
		return message.format(hightlight, default)

	if type(message) is list:
		return "".join([format(chunk) for chunk in message])
	return color(message)


def get_animated_messages(message: str, animations: List[str]) -> List[str]:
	"""Apply a series of animation to a message."""
	return [message.format(animation=anm) for anm in animations]
