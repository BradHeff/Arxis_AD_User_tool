import threading

# import time
import tkthread as tkt
import io
import ttkbootstrap as ttk
import Functions as f
from signal import SIGINT, signal
from PIL import Image, ImageTk
from Functions import Version, base64
from icon import image
from ldap3.core.exceptions import LDAPBindError

# import subprocess as sp
# from os import remove, rmdir, mkdir, _exit
# import Functions as fn

import splash
import Main


class Login(ttk.Window):
    """
    A class to represent the login window of the Trinity AD User Tool.

    Attributes:
    - themename: The theme name for the window.
    - handle: The handle for the Ctrl-c signal.

    Methods:
    - __init__(): Initializes the login window.
    - centerWindow(width, height): Calculates the coordinates to center the window.
    - on_closing(): Handles the closing event of the window.
    - handler(handle): Handles the Ctrl-c signal.
    - hide(): Hides the window.
    - show(): Shows the window.
    """

    def __init__(self):
        super(Login, self).__init__(themename="trinity-dark")
        self.bind_all("<Control-c>", self.handler)
        signal(SIGINT, lambda x, y: print("") or self.handler(0))

        # splash.Splash(self)
        W, H = 504, 250
        x, y = self.centerWindow(W, H)
        self.geometry("%dx%d%+d%+d" % (W, H, x, y))
        self.attributes("-fullscreen", False)
        self.attributes("-topmost", True)
        self.protocol("WM_DELETE_WINDOW", self.on_closing)
        self.Icon()
        self.columnconfigure(0, weight=1)
        self.columnconfigure(1, weight=1)
        self.rowconfigure(1, weight=0, pad=26)
        print(f.getSettings(self))
        self.company = "Horizon"
        self.server = f.getServer(self, self.company)
        self.title(
            "".join(["TrinityCloud AD User Tool v", Version[4 : Version.__len__()]])
        )
        print(self.company)
        print(self.server)
        lbltitle = ttk.Label(self, text="TrinityCloud AD User Tool")
        lbltitle.grid(row=0, column=0, columnspan=2, pady=5)

        lbluser = ttk.Label(self, text="Username:")
        lblpass = ttk.Label(self, text="Password:")

        self.userBox = ttk.Entry(self)
        self.passBox = ttk.Entry(self, show="*")

        lbluser.grid(sticky="NW", row=1, column=0, pady=10, padx=20)
        self.userBox.grid(sticky="SEW", row=1, column=0, pady=10, padx=20)

        lblpass.grid(sticky="NW", row=1, column=1, pady=10, padx=20)
        self.passBox.grid(sticky="SEW", row=1, column=1, pady=10, padx=20)

        loginBtn = ttk.Button(
            self,
            text="Login",
            command=lambda: self.login(self.userBox.get(), self.passBox.get()),
        )
        loginBtn.grid(sticky="SE", row=2, columnspan=2, pady=10, padx=10)
        cancelBtn = ttk.Button(self, text="Cancel", command=self.on_closing)
        cancelBtn.grid(sticky="SW", row=2, columnspan=2, pady=10, padx=10)

        splash.loadedMain = True

    def Icon(self):
        b64_img = io.BytesIO(base64.b64decode(image))
        img = Image.open(b64_img, mode="r")
        photo = ImageTk.PhotoImage(image=img)
        self.wm_iconphoto(False, photo)

    def login(self, username, password):
        print("Username: ", username)
        print("Password: ", password)
        try:
            conn = f.ldap_login(self, username, password)
            if self.company.upper() in conn.extend.standard.who_am_i():
                self.hide()
                Main.Main(self)
            else:
                print("Login Failed")
        except LDAPBindError as e:
            print("Login Failed: ", str(e))
        # self.hide()
        # Main.Main(root)

    def centerWindow(self, width, height):  # Return 4 values needed to center Window
        screen_width = self.winfo_screenwidth()  # Width of the screen
        screen_height = self.winfo_screenheight()  # Height of the screen
        x = (screen_width / 2) - (width / 2)
        y = (screen_height / 2) - (height / 2)
        return int(x), int(y)

    def on_closing(self):
        print("Thanks for using Trinity AD User Tool!\n")
        root.destroy()

    def handler(self, handle):
        msg = "Ctrl-c was pressed. Exiting now... "
        print(msg)
        print("")

    def hide(self):
        self.withdraw()

    def show(self):
        self.update()
        self.deiconify()


root = Login()


def thread_run(func):
    threading.Thread(target=func).start()


@thread_run
def func():
    @tkt.main(root)
    @tkt.current(root)
    def runthread():
        root.update()


root.mainloop()
