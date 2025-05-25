from adafruit_display_shapes.line import Line
from adafruit_display_shapes.rect import Rect
import adafruit_ili9341
import board
import displayio
from fourwire import FourWire


# --- Data (Simulated for example) ---
def generate_candlestick_data():
    # Replace with real-time data fetching or your sample data
    return [
        [100, 105, 95, 102],  # Open, High, Low, Close
        [108, 108, 100, 106],
        [106, 112, 104, 109],
        [109, 115, 107, 111],
        [111, 117, 110, 114],
        [114, 120, 112, 118],
        [118, 125, 115, 123],
        [123, 130, 120, 128],
        [128, 135, 125, 132],
        [132, 140, 130, 130],
        [138, 145, 135, 142],
        [142, 150, 140, 148],
        [148, 155, 145, 152],
        [152, 160, 150, 158],
        [158, 165, 155, 162],
        [162, 170, 160, 168],
        [168, 175, 165, 172],
        [172, 180, 170, 178],
        [178, 185, 175, 182],
        [182, 190, 180, 188],
    ]


# --- Display ---
def draw_candlestick(splash, data, x_offset):
    y_offset = 300
    scale_factor = 2
    color_bullish = 0x00FF00  # Green
    color_bearish = 0xFF0000  # Red

    for i, candle in enumerate(data):
        x = x_offset + i * 30
        open_price = candle[0]
        high_price = candle[1]
        low_price = candle[2]
        close_price = candle[3]

        # --- Candle Body ---
        if close_price >= open_price:
            color = color_bullish
        else:
            color = color_bearish

        body_width = 10
        body_start_y = y_offset - (close_price * scale_factor)
        body_end_y = y_offset - (open_price * scale_factor)

        rect = Rect(
            x,
            body_start_y,
            body_width,
            abs(body_end_y - body_start_y),
            outline=color,
            fill=color,
        )
        splash.append(rect)

        # --- Wicks ---
        line = Line(
            x + body_width // 2,
            y_offset - (high_price * scale_factor),
            x + body_width // 2,
            y_offset - (low_price * scale_factor),
            color,
        )
        splash.append(line)


# Release any resources currently in use for the displays
displayio.release_displays()

spi = board.SPI()
tft_cs = board.D9
tft_dc = board.D10

display_bus = FourWire(spi, command=tft_dc, chip_select=tft_cs, reset=board.D6)
display = adafruit_ili9341.ILI9341(display_bus, width=320, height=240)

splash = displayio.Group()
display.root_group = splash

data = generate_candlestick_data()
draw_candlestick(splash, data, 0)  # x_offset = 0

while True:
    pass  # Keep the program running
