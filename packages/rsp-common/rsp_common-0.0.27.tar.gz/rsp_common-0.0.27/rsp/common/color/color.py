def bgr2rgb(color_bgr):
    return (color_bgr[2], color_bgr[1], color_bgr[0])

def rgb2bgr(color_rgb):
    return (color_rgb[2], color_rgb[1], color_rgb[0])

def as_float(color):
    return color / 255

def as_int(color):
    res = (int(color[0]*255), int(color[1]*255), int(color[2]*255))
    return res

BLACK = (0, 0, 0)
WHITE = (255, 255, 255)

LIGHT_GRAY = (204, 204, 204)
DARK_GRAY = (102, 102, 102)

LIGHT_BLUE = (165, 212, 250)
DARK_BLUE = (44, 74, 150)

LIGHT_GREEN = (78, 250, 75)
DARK_GREEN = (18, 99, 17)

LIGHT_RED = (95, 95, 255)
DARK_RED = (0, 0, 139)

CORNFLOWER_BLUE = (255, 153, 153)

FOCUSED = CORNFLOWER_BLUE
FOREGROUND = BLACK
FOREGROUND_DISABLED = DARK_GRAY