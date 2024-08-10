import threading
import time
import os
import io
import ttkbootstrap as ttk
import Functions as f
import tkthread as tkt
import configparser_crypt as cCrypt
import base64
from PIL import Image, ImageTk
from Functions import Version, creds, settings_dir, key
from icon import himage, shield
from ldap3.core.exceptions import LDAPBindError, LDAPPasswordIsMandatoryError


class Login(ttk.Toplevel):
    """
    A class to represent the login window of the Trinity AD User Tool.
    """

    def __init__(self, original, themename="trinity-dark"):
        super().__init__()
        self.MainFrame = original
        W, H = 534, 280

        self.attributes("-fullscreen", False)
        self.attributes("-topmost", True)
        self.protocol("WM_DELETE_WINDOW", self.on_closing)
        self.Icon()
        self.columnconfigure(0, weight=1)
        self.columnconfigure(2, weight=1)
        self.rowconfigure(0, weight=0, pad=26)
        self.rowconfigure(1, weight=0, pad=16)
        self.rowconfigure(2, weight=0, pad=16)
        # self.rowconfigure(4, weight=0, pad=16)
        self.resizable(False, False)

        self.title(
            "".join(
                [
                    "TrinityCloud AD User Tool v",
                    Version[4 : Version.__len__()],
                ]
            )
        )
        print(self.MainFrame.company)
        print(self.MainFrame.server)
        lbltitle = ttk.Label(self, text="TrinityCloud AD User Tool")
        lbltitle.grid(row=0, columnspan=4, pady=5)

        lbluser = ttk.Label(self, text="Username:")
        lblpass = ttk.Label(self, text="Password:")

        self.userBox = ttk.Entry(self, textvariable="flastname")
        self.passBox = ttk.Entry(self, show="*")
        self.userBox.bind("<Return>", self.loginForm)
        self.passBox.bind("<Return>", self.loginForm)
        lbluser.grid(sticky="NW", row=1, column=0, pady=10, padx=20)
        self.userBox.grid(sticky="SEW", row=1, column=0, pady=20, padx=20)

        lblpass.grid(sticky="NW", row=1, column=2, pady=10, padx=20)
        self.passBox.grid(sticky="SEW", row=1, column=2, pady=20, padx=20)

        self.loginBtn = ttk.Button(
            self,
            text="Login",
            command=self.loginForm,
            width=22,
        )
        self.cancelBtn = ttk.Button(
            self, text="Cancel", command=self.on_closing, width=22
        )
        self.cancelBtn.grid(row=2, column=0, columnspan=2, padx=20)
        self.loginBtn.grid(row=2, column=2, columnspan=2, padx=20)

        self.sLogin = ttk.IntVar(self, 0)
        self.saveLogin = ttk.Checkbutton(
            self,
            text="Remember Me",
            variable=self.sLogin,
            onvalue=1,
            offvalue=0,
            bootstyle="round-toggle",
        )
        self.saveLogin.grid(row=3, column=2, padx=20, pady=10)
        b64_img = base64.b64decode(shield)
        img = Image.open(io.BytesIO(b64_img))
        new_size = (70, 70)  # width, height
        img = img.resize(new_size, Image.ANTIALIAS)
        photo = ImageTk.PhotoImage(img)

        lblImage = ttk.Label(self, image=photo)
        lblImage.grid(sticky=ttk.NW, row=3, rowspan=2, column=0, padx=10, pady=10)
        lblImage.photo = photo
        self.lblstatus = ttk.Label(self, text="")
        self.lblstatus.grid(row=4, columnspan=4, padx=20)

        x, y = self.centerWindow(W, H)
        self.geometry("%dx%d%+d%+d" % (W, H, x, y))
        if os.path.isfile(settings_dir + "\\" + creds):
            print("LOADED")
            parser = cCrypt.ConfigParserCrypt()
            parser.aes_key = key
            parser.read_encrypted(settings_dir + "\\" + creds)
            if parser.has_section("login"):
                print("Loaded Config")
                if parser.has_option("login", "autoload"):
                    if parser.get("login", "autoload") == "1":
                        print("Loaded Config3")
                        if parser.has_option("login", "autoload"):
                            self.sLogin.set(eval(parser.get("login", "autoload")))
                        if parser.has_option("login", "username"):
                            self.userBox.insert(0, parser.get("login", "username"))
                        if parser.has_option("login", "password"):
                            self.passBox.insert(0, parser.get("login", "password"))

    def saveConfig(self):
        conf_file = cCrypt.ConfigParserCrypt()
        conf_file.aes_key = key
        conf_file.add_section("login")
        if self.sLogin.get() == 1:
            conf_file["login"]["username"] = str(self.userBox.get())
            conf_file["login"]["password"] = str(self.passBox.get())
        else:
            conf_file["login"]["username"] = ""
            conf_file["login"]["password"] = ""
        conf_file["login"]["autoload"] = str(self.sLogin.get())
        with open(settings_dir + "\\" + creds, "wb") as file_handle:
            conf_file.write_encrypted(file_handle)

    def disElements(self, state):
        self.userBox["state"] = state
        self.passBox["state"] = state
        self.loginBtn["state"] = state
        self.cancelBtn["state"] = state

    def Icon(self):
        b64_img = io.BytesIO(base64.b64decode(himage))
        img = Image.open(b64_img, mode="r")
        photo = ImageTk.PhotoImage(image=img)
        self.wm_iconphoto(False, photo)

    def loginForm(self, optional=None):
        username = self.userBox.get()
        password = self.passBox.get()
        self.lblstatus.config(bootstyle="warning", font=("Poppins", 14))
        self.lblstatus["text"] = "Logging in..."
        self.disElements(ttk.DISABLED)
        tt = threading.Thread(target=self.login, args=(username, password))
        tt.daemon = True
        tt.start()

    def login(self, username, password):
        print("Username: ", username)
        print("Password: ", password)
        try:

            conn = f.ldap_login(self.MainFrame, username, password)
            if self.MainFrame.company.upper() in conn.extend.standard.who_am_i():
                # if f.isTeacher(
                #     self.MainFrame,
                #     username,
                # ):
                #     tkt.call_nosync(
                #         self.lblstatus.config,
                #         bootstyle="success",
                #         font=("Poppins", 14),
                #         text="Login Success",
                #     )

                if (
                    username in f.ICT_Admins["IT"]
                    or username in f.ICT_Admins["Management"]
                ):
                    tkt.call_nosync(
                        self.lblstatus.config,
                        bootstyle="success",
                        font=("Poppins", 14),
                        text="Authorized",
                    )
                    self.saveConfig()
                    self.MainFrame.loginUser = username
                    self.MainFrame.lbl_login.config(
                        bootstyle="success",
                        font=("Poppins", 12),
                        text="Authorized",
                    )
                else:
                    tkt.call_nosync(
                        self.lblstatus.config,
                        bootstyle="danger",
                        font=("Poppins", 14),
                        text="Not Authorized to access this system",
                    )
                    tkt.call_nosync(self.disElements, ttk.NORMAL)
                self.MainFrame.state = f.checkConnection(self.MainFrame)
                
                time.sleep(2)
                f.widgetStatusFailed(self.MainFrame, True)
                self.destroy()
                self.MainFrame.show()

            else:
                tkt.call_nosync(
                    self.lblstatus.config,
                    bootstyle="danger",
                    font=("Poppins", 14),
                    text="Login Failed",
                )
                tkt.call_nosync(self.disElements, ttk.NORMAL)
                print("Login Failed")
        except LDAPBindError as e:
            tkt.call_nosync(
                self.lblstatus.config,
                bootstyle="danger",
                font=("Poppins", 14),
                text="Incorrect Username or Password",
            )
            tkt.call_nosync(self.disElements, ttk.NORMAL)
            print("Login Failed: ", str(e))
        except LDAPPasswordIsMandatoryError as e:
            print("Login Failed: ", str(e))
            tkt.call_nosync(
                self.lblstatus.config,
                bootstyle="danger",
                font=("Poppins", 14),
                text="Login Failed: Password is mandatory",
            )
            tkt.call_nosync(self.disElements, ttk.NORMAL)

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
