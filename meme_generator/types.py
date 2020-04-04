from typing import BinaryIO, Union

from PIL.Image import Image

ImageType = Union[Image, BinaryIO, str]

CoordType = Union[int, float]
