from tkinter import * 
from tkinter import ttk 
from PIL import Image, ImageDraw, ImageTk
import pyautogui
import pytesseract 
from backend.alphaapi import solver
from matplotlib import pyplot as plt 



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
    if "$" in explanation or "\\" in explanation:
        img = renderToLatex(explanation)
        explanation_label.config(image=img, text="")
        explanation_label.image = img
    else:
        explanation_label.config(text=explanation)
    

mode_label = Label(inputScreen, text="Mode:Write")
mode_label.pack()

#input screen 
Button(inputScreen, text="Write Mode", command=setWriteMode).pack(side=LEFT, padx=10)
Button(inputScreen, text="Erase Mode", command=clear).pack(side=LEFT)
Button(inputScreen, text="Calculate", command=calculate).place(x=650, y=550) 

#output screen 

outputScreen = Frame(container)
outputScreen.grid(row=0, column=0, sticky="nsew")

output_canvas = Canvas(outputScreen)
scrollbar = Scrollbar(outputScreen, orient="vertical", command=output_canvas.yview)
scrollable_frame = Frame(output_canvas)

#define functions here 
def mouseScrolling(event):
    output_canvas.yview_scroll(int(-1 * (event.delta / 120)), "units")
output_canvas.bind_all("<MouseWheel>", mouseScrolling)

def renderToLatex(latex_text):
    """
    Converts a LaTeX-formatted string to a Tkinter-compatible image.
    """
    fig, ax = plt.subplots(figsize=(8, 0.01))  # width controls line width
    ax.axis("off")

    # Display the LaTeX text
    ax.text(0.05, 0.95, latex_text, fontsize=10, va="top", ha="left", wrap=True)

    # Save as transparent PNG
    fig.savefig("latex_render.png", dpi=200, bbox_inches="tight", transparent=True)
    plt.close(fig)

    # Convert to Tkinter PhotoImage
    return ImageTk.PhotoImage(Image.open("latex_render.png"))


scrollable_frame.bind(
    "<Configure>",
    lambda e: output_canvas.configure(scrollregion=output_canvas.bbox("all"))
)
output_canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
output_canvas.configure(yscrollcommand=scrollbar.set)

output_canvas.pack(side="left", fill="both", expand=True)
scrollbar.pack(side="right", fill="y")


Label(scrollable_frame, text="Here's the solution:", font=("Arial", 20)).pack(pady=20)


explanation_label = Label(
    scrollable_frame,
    text="",
    font=("Arial", 14),
    wraplength=800,
    justify=LEFT,
    anchor="w"
)
explanation_label.pack(pady=20, padx=20, fill="x")

Button(
    scrollable_frame,
    text="Back",
    font=("Arial", 14),
    command=lambda: switchFrame(inputScreen)
).pack(pady=20)


switchFrame(inputScreen)
setWriteMode()

#Button(root, text="Save", command=save).pack()

root.mainloop()

