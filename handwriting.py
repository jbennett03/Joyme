from tkinter import * 
from tkinter import ttk 
from PIL import Image, ImageDraw
import pyautogui
import pytesseract 
from alphaapi import solver


root = Tk() 
root.title("Placeholder")
root.geometry("870x500")
root.attributes("-fullscreen", True)

width = 800 
height = 500

#mainframe = ttk.Frame(root, padding="3 3 12 12")
#mainframe.grid(column=0, row=0, sticky=(N, W, E, S))
white = (255, 255, 255) 
container = Frame(root)
container.pack(fill="both", expand=True)
container.grid_rowconfigure(0, weight=1)
container.grid_columnconfigure(0, weight=1)

inputScreen = Frame(container)
outputScreen = Frame(container)

for frame in (inputScreen, outputScreen):
    frame.grid(row=0, column=0, sticky="nsew")

canvas = Canvas(inputScreen, width=width, height=height, bg='white')
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

def screenShot(path="capture.png"): #remember this logic for the translation part 
    x = root.winfo_rootx() + canvas.winfo_x() 
    y = root.winfo_rooty() + canvas.winfo_y()
    w = canvas.winfo_width()
    h = canvas.winfo_height()

    screenshot = pyautogui.screenshot(region=(x, y, w, h))
    screenshot.save(path)

#translation logic comes after
#def translation():
pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'
imgTranslation = Image.open('capture.png')
customConfig = r'--psm 7 -c tessedit_char_whitelist=0123456789xX+-=*/= '
text = pytesseract.image_to_string(imgTranslation, config=customConfig)
print(text)

def switchFrame(frame):
    frame.tkraise()


def calculate(): #edit the logic for this as well
    screenShot("capture.png")
    explanation_label.config(text="Solving")
    switchFrame(outputScreen)
    root.update_idletasks()
    
    explanation = solver("capture.png")
    explanation_label.config(text=explanation)
    

mode_label = Label(inputScreen, text="Mode:Write")
mode_label.pack()

#input screen 
Button(inputScreen, text="Write Mode", command=setWriteMode).pack(side=LEFT, padx=10)
Button(inputScreen, text="Erase Mode", command=clear).pack(side=LEFT)
Button(inputScreen, text="Calculate", command=calculate).place(x=650, y=550) #placeholder code for the moment

#output screen 
Label(outputScreen, text="Here's the solution:", font=("Arial", 20)).pack(pady=20)

explanation_label = Label(outputScreen, text="", font=("Arial", 14), wraplength=800, justify=LEFT)
explanation_label.pack(pady=20)

Button(outputScreen, text="Back", font=("Arial", 14), command=lambda: switchFrame(inputScreen)).pack(pady=20)


switchFrame(inputScreen)
setWriteMode()

#Button(root, text="Save", command=save).pack()

root.mainloop()
