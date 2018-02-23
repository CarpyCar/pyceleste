from PIL import ImageDraw


COLORS = {
    'red': 'F44336',
    'blue': '2196F3',
}


def hex2rgb(hex_str):
    r = int(hex_str[0:2], 16)
    g = int(hex_str[2:4], 16)
    b = int(hex_str[4:6], 16)
    return r, g, b


def border(im, color='red'):
    if isinstance(color, str):
        color = hex2rgb(COLORS[color])
    draw = ImageDraw.Draw(im)
    w, h = im.size
    draw.line((0, 0, w - 1, 0, w - 1, h - 1, 0, h - 1, 0, 0), fill=color,
              width=1)
