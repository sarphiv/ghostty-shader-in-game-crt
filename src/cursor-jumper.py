import sys, time, shutil, colorsys, signal, random

ESC = "\x1b"
BEL = "\x07"

def cup(y, x):
    sys.stdout.write(f"{ESC}[{y};{x}H")

def set_cursor_color_rgb(r, g, b):
    sys.stdout.write(f"{ESC}]12;#{r:02x}{g:02x}{b:02x}{BEL}")

def reset_cursor_color():
    sys.stdout.write(f"{ESC}]112{BEL}")

def cleanup(*_):
    reset_cursor_color()
    sys.stdout.write(f"{ESC}[?25h")     # show cursor
    sys.stdout.write(f"{ESC}[?1049l")   # leave alt screen
    sys.stdout.flush()
    raise SystemExit(0)

signal.signal(signal.SIGINT, cleanup)
signal.signal(signal.SIGTERM, cleanup)

# enter alternate screen + clear
sys.stdout.write(f"{ESC}[?1049h")
sys.stdout.write(f"{ESC}[2J{ESC}[H")
sys.stdout.write(f"{ESC}[?25h")
sys.stdout.flush()

cols, rows = shutil.get_terminal_size((80, 24))
w = max(2, cols - 1)
h = max(2, rows - 1)

# Minimum jump length in character cells (l1 norm)
MIN_JUMP = 20
max_possible = (w - 1 - 1) + (h - 1 - 1)
min_jump = min(MIN_JUMP, max_possible)

x, y = 1, 1
nx, ny = x, y

while True:
    while abs(nx - x) + abs(ny - y) <= min_jump:
        nx = random.randint(1, w - 1)
        ny = random.randint(1, h - 1)

    # color = f(x,y) (HSV -> RGB), deterministic in position
    hue = (nx / max(1, (w - 1)) + ny / max(1, (h - 1))) % 1.0
    r, g, b = colorsys.hsv_to_rgb(hue, 1.0, 1.0)
    R, G, B = int(255*r), int(255*g), int(255*b)

    set_cursor_color_rgb(R, G, B)
    cup(ny, nx)
    sys.stdout.flush()

    x, y = nx, ny
    time.sleep(0.3)
