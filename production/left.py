print("Starting")

import board, busio

from kmk.kmk_keyboard import KMKKeyboard
from kmk.keys import KC
from kmk.scanners import DiodeOrientation
from kmk.modules.layers import Layers
from kmk.modules.split import Split, SplitType, SplitSide
from kmk.extensions.rgb import RGB
from kmk.hid import HIDModes
from kmk.extensions.display import Display, TextEntry, ImageEntry
from kmk.extensions.display.ssd1306 import SSD1306
from kmk.modules.encoder import EncoderHandler
from kmk.extensions.media_keys import MediaKeys
from kmk.scanners import gpio

keyboard = KMKKeyboard()

layers = Layers()
split = Split(split_type=SplitType.BLE, split_side=SplitSide.LEFT)
rgb = RGB(pixel_pin=board.GP18, num_pixels=26)

i2c_bus = busio.I2C(board.GP17, board.GP16)

driver = SSD1306(
    i2c=i2c_bus,
    device_address=0x3C,
)

display = Display(
    display=driver,
    width=128
    height=64,
    brightness=0.8,
    brightness_step=0.1,
    dim_time=60,
    dim_target=0.1,
    off_time=180,
    powersave_dim_time=30,
    powersave_dim_target=0.1,
    powersave_off_time=90
)

display.entries = [
    TextEntry(text="the best keyboard", x=0, y=0)
]

keyboard.extensions.append(rgb)
keyboard.modules.append(layers)
keyboard.extensions.append(display)
keyboard.extensions.append(MediaKeys())

encoder_handler = EncoderHandler()
encoder_handler.pins = [(board.GP13, board.GP14, board.GP15),]
encoder_handler.map = [((KC.AUDIO_VOL_DOWN,KC.AUDIO_VOL_UP,KC.AUDIO_MUTE),),(KC.BRIGHTNESS_DOWN,KC.BRIGHTNESS_UP,KC.NO)]
keyboard.extensions.append(encoder_handler)
keyboard.modules.append(split)

keyboard.col_pins = (
    board.GP7, board.GP8, board.GP9, board.GP10, board.GP11
)

keyboard.row_pins = (
    board.GP2, board.GP21, board.GP4, board.GP5, board.GP6
)

keyboard.diode_orientation = DiodeOrientation.COL2ROW

MO1 = KC.MO(1)

keyboard.keymap = [
    [
        KC.N1, KC.N2, KC.N3, KC.N4, KC.N5,
        KC.Q, KC.W, KC.E, KC.R, KC.T,
        KC.A, KC.S, KC.D, KC.F, KC.G,
        KC.LSHIFT, KC.Z, KC.X, KC.C, KC.V,
        KC.LCTL, KC.LGUI, KC.LALT, MO1, KC.FN,
    ],
    [
        KC.ESC, KC.NO, KC.NO, KC.NO, KC.GRAVE,
        KC.TAB, KC.NO, KC.NO, KC.NO, KC.DEL,
        KC.CAPS, KC.NO, KC.NO, KC.NO, KC.PGUP,
        KC.NO, KC.NO, KC.NO, KC.NO, KC.PGDN,
        KC.NO, KC.NO, KC.NO, KC.NO, KC.END,
    ]
]

thumb = gpio.GPIOInputPin(12)
keyboard.coord_mapping = {
    thumb: KC.SPACE
}

if __name__ == '__main__':
    keyboard.go()
    keyboard.go(hid_type=HIDModes.BLE, ble_name='hrid\'s split keyboard')