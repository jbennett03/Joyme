from tkinter import * 
from tkinter import ttk 
from PIL import Image, ImageDraw

root = Tk() 
root.title("Placeholder")
root.geometry("870x500")
width = 800 
height = 500
root.attributes("-fullscreen", True)
#mainframe = ttk.Frame(root, padding="3 3 12 12")
#mainframe.grid(column=0, row=0, sticky=(N, W, E, S))
white = (255, 255, 255)
canvas = Canvas(root, width=width, height=height, bg='white')
canvas.pack()

image = Image.new("RGB", (width, height), white)
draw = ImageDraw.Draw(image)
def paint(event):
    x1, y1 = (event.x - 2), (event.y - 2)
    x2, y2 = (event.x + 2), (event.y + 2)
    canvas.create_oval([x1, y1, x2, y2], fill='black')
    draw.ellipse([x1, y1, x2, y2], fill='black')

def clear():
    canvas.delete("all")
    global image, draw 
    image = Image.new("RGB", (width, height), white)
    draw = ImageDraw.Draw(image)
    mode_label.config(text="Cleared Canvas")

#canvas.bind("<B1-Motion>", paint)

def setWriteMode():
    canvas.bind("<B1-Motion>", paint)
    mode_label.config(text="Mode: Write")

#def setEraseMode():
    #canvas.bind("<B1-Motion>", erase)
    #mode_label.config(text="Mode: Erase")

mode_label = Label(root, text="Mode:Write")
mode_label.pack()

Button(root, text="Write Mode", command=setWriteMode).pack(side=LEFT, padx=10)
Button(root, text="Erase Mode", command=clear).pack(side=LEFT)

#when erase button is pressed, activate def erase(event) function


def save():
    image.save("input.png")

Button(root, text="Save", command=save).pack()

root.mainloop()
