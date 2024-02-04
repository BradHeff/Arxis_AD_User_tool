import threading
import time

import ttkbootstrap as ttk

from Functions import clear_console
from icon import hsplashbg

loadedMain = False


class Splash(ttk.Toplevel):
    """Splash Screen displayed before the program starts"""

    def __init__(self, original, themename="heffelhoffui"):
        super().__init__()
        global photo, root
        self.original_frame = original
        self.original_frame.hide()
        W, H = 504, 250
        screen_width = self.winfo_screenwidth()
        screen_height = self.winfo_screenheight()
        center_x = int(screen_width / 2 - W / 2)
        center_y = int(screen_height / 2 - H / 2)
        self.geometry(f"{W}x{H}+{center_x}+{center_y}")
        self.attributes("-fullscreen", False)
        self.attributes("-toolwindow", True)
        self.attributes("-topmost", True)
        self.attributes("-transparentcolor", "grey15")
        self.overrideredirect(True)

        canvas = ttk.Canvas(
            self,
            bg="grey15",
            width=W - 4,
            height=H - 4,
            highlightthickness=0,
        )
        canvas.pack()
        photo = ttk.PhotoImage(data=hsplashbg)
        canvas.create_image(1, 1.5, image=photo, anchor="nw")

        self.count = 1

        self.prog = ttk.Progressbar(self, length=500.5, maximum=100)
        self.prog.place(x=1.5, y=240)
        print(self.ConsoleWelcome())
        # self.prog["value"] = 100
        t = threading.Thread(target=self.startSplash)
        t.daemon = True
        t.start()

    def ConsoleWelcome(self):
        clear_console()
        message = "====================================\n"
        message += "    ======TRINITY CLOUD======\n"
        message += "====================================\n"
        message += "Author: Brad Heffernan\n"
        message += "-----------\n"
        message += "Libraries:\n"
        message += "    ttkbootstrap\n"
        message += "    ldap3\n"
        message += "    flask\n"
        message += "    pyOpenSSL\n"
        message += "    configparser_crypt\n"
        message += "    pywin32\n"
        message += "    tinyaes\n"
        message += "    tkthread\n"
        message += "===================================="

        return message

    def startSplash(self):
        while self.count < 99:
            self.count += 10
            if loadedMain is True:
                self.count = 100

            self.prog["value"] = self.count
            time.sleep(0.7)
        self.onClose()

    def onClose(self):
        self.destroy()
        self.original_frame.show()
