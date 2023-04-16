import sys
from PIL import Image, ImageTk

if sys.version_info[0] == 2:
    import Tkinter
    tkinter = Tkinter
else:
    import tkinter


def showPIL(pilImage):
    """
    Function for showing the images in full screen

    :param pilImage: The image to show
    :return: Tkinter window
    """
    root = tkinter.Tk()
    w, h = root.winfo_screenwidth(), root.winfo_screenheight()

    # Change to 1 to get images on full screen
    root.overrideredirect(0)

    root.geometry("%dx%d+0+0" % (w, h))
    root.focus_set()
    root.bind("<Escape>", lambda e: (e.widget.withdraw(), e.widget.quit()))
    canvas = tkinter.Canvas(root,width=w,height=h)
    canvas.pack()
    canvas.configure(background='black')
    imgWidth, imgHeight = pilImage.size
    if imgWidth > w or imgHeight > h:
        ratio = min(w/imgWidth, h/imgHeight)
        imgWidth = int(imgWidth*ratio)
        imgHeight = int(imgHeight*ratio)
        pilImage = pilImage.resize((imgWidth,imgHeight), Image.ANTIALIAS)
    image = ImageTk.PhotoImage(pilImage)
    imagesprite = canvas.create_image(w/2,h/2,image=image)
    root.update()
    return root


def destroyPIL(root):
    root.destroy()
