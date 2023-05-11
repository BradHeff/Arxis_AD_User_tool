import threading
import time

import ttkbootstrap as ttk

from Functions import clear_console
from icon import splashbg

# from PIL import Image, ImageTk
# from ttkbootstrap.constants import *


class Splash(ttk.Toplevel):
    """docstring for Splash."""

    def __init__(self, original, themename="heffelhoffui"):
        super().__init__()
        global photo, root
        self.original_frame = original
        # ttk.Toplevel.__init__(self)

        self.W, self.H = 504, 250
        screen_width = self.winfo_screenwidth()
        screen_height = self.winfo_screenheight()
        center_x = int(screen_width / 2 - self.W / 2)
        center_y = int(screen_height / 2 - self.H / 2)
        self.geometry(f"{self.W}x{self.H}+{center_x}+{center_y}")
        self.attributes("-fullscreen", False)
        self.attributes("-toolwindow", True)
        self.attributes("-topmost", True)
        self.attributes("-transparentcolor", "grey15")
        self.overrideredirect(True)

        canvas = ttk.Canvas(
            self,
            bg="grey15",
            width=self.W - 2,
            height=self.H - 2,
            highlightthickness=0,
        )
        canvas.pack()
        # convert image to PhotoImage for `tkinter` to understand
        photo = ttk.PhotoImage(data=splashbg)
        # put the image on canvas because canvas supports transparent bg
        canvas.create_image(1, 1, image=photo, anchor="nw")

        # ttk.Label(self, image=photo).place(x=0,y=0)

        self.count = 1

        self.prog = ttk.Progressbar(self, length=501, maximum=100)
        self.prog.place(x=1, y=240)
        print(self.ConsoleWelcome())
        t = threading.Thread(target=self.runProg)
        t.daemon = True
        t.start()

    def ConsoleWelcome(self):
        clear_console()
        message = "====================================\n"
        message += "======HORIZON CHRISTIAN SCHOOL======\n"
        message += "====================================\n"
        message += "Author: Brad Heffernan\n"
        message += "-----------\n"
        message += "Libraries:\n"
        message += "    tkinter\n"
        message += "    ttkbootstrap\n"
        message += "    configparser_crypt\n"
        message += "    pythoncom\n"
        message += "    win32security\n"
        message += "    pyad\n"
        message += "    pathlib\n"
        message += "===================================="

        return message

    def runProg(self):
        while self.count < 99:
            self.count += 10
            self.prog["value"] = self.count
            time.sleep(0.7)
        self.onClose()

    def onClose(self):
        self.destroy()
        self.original_frame.show()
