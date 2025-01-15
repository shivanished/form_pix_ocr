from wand.api import library
from wand.version import MAGICK_VERSION

print("MagickWand version:", MAGICK_VERSION)
print("Library loaded:", bool(library))