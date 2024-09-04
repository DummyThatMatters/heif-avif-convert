from dataclasses import dataclass
import re

DEFAULT_EXTENSIONS = 'jpg, jpeg, png, bmp'
EXT_RE = re.compile('[ ;,.|]+')
DEFAULT_QUALITY = 50


@dataclass
class Format:
    name: str
    ext: str


class Formats:
    HEIF = Format('HEIF', '.heic')
    AVIF = Format('AVIF', '.avif')


