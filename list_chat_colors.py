from construct import *
from recipe import *


colors_list = dict(
    white = 0x00,
    red = 0x01,
    green = 0x02,
    blue = 0x03,
    beige = 0x04,
    gray = 0x05,
    black = 0x06,
    br_beige = 0x07,
    gold = 0x08,
    br_gold = 0x09,
    darkest_green = 0x0a,
    purple = 0x0b,
    dark_green = 0x0c,
    br_white = 0x12,
    dark_red = 0x13,
    silver = 0x15
)
rcolors_list = dict(map(reversed, colors_list.items()))

class ColorAdapter(Adapter):
    def _encode(self, obj, context):
        return colors_list.get(obj, obj)

    def _decode(self, obj, context):
        return rcolors_list.get(obj, obj)

def Color(name):
    return ColorAdapter(ULInt8(name))

