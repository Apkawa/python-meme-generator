from enum import Enum, Flag, auto

from gi.repository import Pango as pango


class TextAlignment(Enum):
    LEFT = pango.Alignment.LEFT
    CENTER = pango.Alignment.CENTER
    RIGHT = pango.Alignment.RIGHT


class TextStyle(Flag):
    NORMAL = pango.Style.NORMAL
    ITALIC = pango.Style.ITALIC
    OBLIQUE = pango.Style.OBLIQUE


class Align(Flag):
    LEFT = auto()
    RIGHT = auto()
    TOP = auto()
    CENTER = auto()
    BOTTOM = auto()

    # def __init__(self, *args):
    #     cls = self.__class__
    #     VERTICAL = cls.TOP | cls.BOTTOM
    #     HORIZONTAL = cls.LEFT | cls.RIGHT
    #     if self.value in [VERTICAL, HORIZONTAL]:
    #         raise ValueError("Invalid combination")
