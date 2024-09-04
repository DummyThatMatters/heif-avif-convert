from dataclasses import dataclass
import re

DEFAULT_EXTENSIONS = 'jpg, jpeg, png, bmp'
EXT_RE = re.compile('[ ;,.|]+')
DEFAULT_QUALITY = 50

QUALITY_KEY = '-q'
RECURSIVE_KEY = '-r'
INPUT_KEY = '-i'
OUTPUT_KEY = '-o'
EXTENSION_KEY = '-e'
DIR_TREE_KEY = '-d'
SKIP_STAT_KEY = '-n'
AVIF_KEY = '-a'
SILENT_MODE_KEY = '-s'

@dataclass
class Format:
    name: str
    ext: str


class Formats:
    HEIF = Format('HEIF', '.heic')
    AVIF = Format('AVIF', '.avif')


