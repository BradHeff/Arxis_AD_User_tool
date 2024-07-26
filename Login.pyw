import threading
import time

# import time
# import tkthread as tkt
import io
import ttkbootstrap as ttk
import Functions as f

# from signal import SIGINT, signal
from PIL import Image, ImageTk
from Functions import Version, base64
from icon import image
from ldap3.core.exceptions import LDAPBindError, LDAPPasswordIsMandatoryError

# import subprocess as sp
# from os import remove, rmdir, mkdir, _exit
# import Functions as fn


class Login(ttk.Toplevel):
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

    def __init__(self, original, themename="trinity-dark"):
        super().__init__()
        # self.bind_all("<Control-c>", self.handler)
        # signal(SIGINT, lambda x, y: print("") or self.handler(0))
        self.MainFrame = original
        # self.MainFrame.hide()
        # splash.Splash(self)
        W, H = 504, 250

        self.attributes("-fullscreen", False)
        self.attributes("-topmost", True)
        self.protocol("WM_DELETE_WINDOW", self.on_closing)
        self.Icon()
        self.columnconfigure(0, weight=1)
        self.columnconfigure(2, weight=1)
        self.rowconfigure(0, weight=0, pad=26)
        self.rowconfigure(1, weight=0, pad=16)
        self.rowconfigure(2, weight=0, pad=16)
        self.rowconfigure(3, weight=1)
        # print(f.getSettings(self))

        self.title(
            "".join(["TrinityCloud AD User Tool v", Version[4 : Version.__len__()]])
        )
        print(self.MainFrame.company)
        print(self.MainFrame.server)
        lbltitle = ttk.Label(self, text="TrinityCloud AD User Tool")
        lbltitle.grid(row=0, columnspan=4, pady=5)

        lbluser = ttk.Label(self, text="Username:")
        lblpass = ttk.Label(self, text="Password:")

        self.userBox = ttk.Entry(self)
        self.passBox = ttk.Entry(self, show="*")

        lbluser.grid(sticky="NW", row=1, column=0, pady=10, padx=20)
        self.userBox.grid(sticky="SEW", row=1, column=0, pady=20, padx=20)

        lblpass.grid(sticky="NW", row=1, column=2, pady=10, padx=20)
        self.passBox.grid(sticky="SEW", row=1, column=2, pady=20, padx=20)

        loginBtn = ttk.Button(
            self,
            text="Login",
            command=self.loginForm,
            width=32,
        )
        cancelBtn = ttk.Button(self, text="Cancel", command=self.on_closing, width=32)
        cancelBtn.grid(sticky="W", row=2, column=0, columnspan=2, padx=20)
        loginBtn.grid(sticky="E", row=2, column=2, columnspan=2, padx=20)

        self.lblstatus = ttk.Label(self, text="")
        self.lblstatus.grid(row=3, columnspan=4, padx=20)

        x, y = self.centerWindow(W, H)
        self.geometry("%dx%d%+d%+d" % (W, H, x, y))

    def Icon(self):
        b64_img = io.BytesIO(base64.b64decode(image))
        img = Image.open(b64_img, mode="r")
        photo = ImageTk.PhotoImage(image=img)
        self.wm_iconphoto(False, photo)

    def loginForm(self):
        username = self.userBox.get()
        password = self.passBox.get()
        self.lblstatus.config(bootstyle="warning", font=("Poppins", 14))
        self.lblstatus["text"] = "Logging in..."
        self.login(username, password)

    def login(self, username, password):
        print("Username: ", username)
        print("Password: ", password)
        try:
            conn = f.ldap_login(self.MainFrame, username, password)
            if self.MainFrame.company.upper() in conn.extend.standard.who_am_i():
                if (
                    username in f.ICT_Admins["IT"]
                    or username in f.ICT_Admins["Management"]
                ):
                    self.lblstatus.config(bootstyle="success", font=("Poppins", 14))
                    self.lblstatus["text"] = "Login Successful"
                    # time.sleep(1)
                    t = threading.Thread(target=self.showMain)
                    t.daemon = True
                    t.start()

                else:
                    self.lblstatus.config(bootstyle="danger", font=("Poppins", 14))
                    self.lblstatus["text"] = "Not Authorized to access this system"
            else:
                self.lblstatus.config(bootstyle="danger", font=("Poppins", 14))
                self.lblstatus["text"] = "Login Failed"
                print("Login Failed")
        except LDAPBindError as e:
            self.lblstatus.config(bootstyle="danger", font=("Poppins", 14))
            self.lblstatus["text"] = "Incorrect Username or Password"
            print("Login Failed: ", str(e))
        except LDAPPasswordIsMandatoryError as e:
            print("Login Failed: ", str(e))
            self.lblstatus.config(bootstyle="danger", font=("Poppins", 14))
            self.lblstatus["text"] = "Login Failed: Password is mandatory"
        # self.hide()
        # Main.Main(root)

    def showMain(self):
        time.sleep(3)
        self.destroy()
        self.MainFrame.show()

    def centerWindow(self, width, height):  # Return 4 values needed to center Window
        screen_width = self.winfo_screenwidth()  # Width of the screen
        screen_height = self.winfo_screenheight()  # Height of the screen
        x = (screen_width / 2) - (width / 2)
        y = (screen_height / 2) - (height / 2)
        return int(x), int(y)

    def on_closing(self):
        print("Thanks for using Trinity AD User Tool!\n")
        self.destroy()
        self.MainFrame.destroy()

    def handler(self, handle):
        msg = "Ctrl-c was pressed. Exiting now... "
        print(msg)
        print("")
