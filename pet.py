import random
import tkinter as tk

TRANSPARENT ="#010101"
PET_W, PET_H = 100, 110

INK = "#2b2d42"
LENS_CALM = "#4cc9f0"
LENS_LOCKED = "#f72585"

root = tk.Tk()
root.overrideredirect(True)
root.attributes("-topmost", True)
try:
    root.attributes("-transparentcolor", TRANSPARENT)
except tk.TclError:
    pass
root.config(bg=TRANSPARENT)

canvas = tk.Canvas(root, width=PET_W, height=PET_H, bg=TRANSPARENT, highlightthickness=0)
canvas.pack()

def oval(cx, cy, rx, ry):
    """Turn a center and two radii into four numbers tkinter wants"""
    return (cx - rx, cy - ry, cx + rx, cy + ry)

canvas.create_line(50, 24, 50, 10, fill=INK, width=3)
bulb = canvas.create_oval(44, 2, 56, 14, fill=LENS_CALM, outline=INK, width=2)

canvas.create_rectangle(18, 24, 50, 88, fill="#ffd7b5", outline="")
canvas.create_rectangle(50, 24, 82, 88, fill="#8d99ae", outline="")
canvas.create_rectangle(18, 24, 82, 88, outline=INK, width=3)
canvas.create_line(50, 24, 46, 36, 54, 48, 46, 60, 54, 72, 50, 88, fill=INK, width=2)
canvas.create_oval(*oval(74, 31, 2, 2), fill=INK, outline="")
canvas.create_oval(*oval(74, 81, 2, 2), fill=INK, outline="")
canvas.create_oval(22, 62, 34, 72, fill="#ffb3c7", outline="")

LEFT = (34, 50)
RIGHT = (66, 50)
eye = canvas.create_oval(*oval(LEFT[0], LEFT[1], 5, 6), fill="black")
eye_shine = canvas.create_oval(*oval(LEFT[0] - 1.5, LEFT[1] - 2.5, 1.5, 1.5), fill="white", outline="")
canvas.create_oval(*oval(RIGHT[0], RIGHT[1], 9, 9), fill=LENS_CALM, outline="")
lens = canvas.create_oval(*oval(RIGHT[0], RIGHT[1], 6, 6), fill=LENS_CALM, outline="")
lens_dot = canvas.create_oval(*oval(RIGHT[0], RIGHT[1], 2, 2), fill="white", outline="")

canvas.create_arc(40, 62, 60, 78, start=200, extent=140, style="arc", outline=INK, width=2)
x = root.winfo_screenwidth() // 2
y = root.winfo_screenheight() - PET_H - 60
root.geometry(f"{PET_W}x{PET_H}+{x}+{y}")

EYE_PARTS = (eye, eye_shine,  lens, lens_dot)
def look():
    """Slide the eyes a few pixel towards the mouse cursor."""
    cx = root.winfo_x() + PET_W // 2
    cy = root.winfo_y() + 50
    dx = root.winfo_pointerx() - cx
    dy = root.winfo_pointery() - cy
    dist = max(1, (dx * dx + dy * dy) ** 0.5)
    ox = dx / dist * 3
    oy = dy / dist * 3
    canvas.coords(eye, *oval(LEFT[0] + ox, LEFT[1] + oy, 5, 6))
    canvas.coords(eye_shine, *oval(LEFT[0] + ox - 1.5, LEFT[1] + oy - 2.5, 1.5, 1.5))
    canvas.coords(lens, *oval(RIGHT[0] + ox, RIGHT[1] + oy, 2, 2))
    canvas.coords(lens_dot, *oval(RIGHT[0] + ox, RIGHT[1] + oy, 2, 2))
    canvas.itemconfig(lens, fill=LENS_LOCKED if dist < 140 else LENS_CALM)
    root.after(50, look)

def blink():
    for part in EYE_PARTS:
        canvas.itemconfig(part, state="hidden")
    root.after(130, open_eyes)

def open_eyes():
    for part in EYE_PARTS:
        canvas.itemconfig(part, state="normal")
    root.after(random.randint(2000, 5000), blink)

def pulse():
    """The antenna light flips between cyan and pink"""
    now = canvas.itemcget(bulb, "fill")
    canvas.itemconfig(bulb, fill=LENS_LOCKED if now == LENS_CALM else LENS_CALM)
    root.after(700, pulse)


root.bind("<Button-3>", lambda event: root.destroy())
look()
root.after(2000, blink)
root.mainloop()