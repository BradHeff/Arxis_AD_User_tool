import threading
import time
import Login
import ttkbootstrap as ttk
from signal import SIGINT, signal

import subprocess as sp
from os import remove, rmdir, mkdir, _exit
import Functions as fn
import requests
from packaging import version

from icon import loading

# from GifLabel import GifLabel

loadedMain = False
versionFile = "https://trincloud.cc/programs/hcs_ad_tool.txt"
newProg = "https://trincloud.cc/programs/release/Horizon%20AD%20User%20Tool"

# data_dir = ''.join([exe_dir, '\\Data\\'])
dwnld = """
@echo off

setlocal enabledelayedexpansion

:DownloadAndExtractZip
setlocal
set destination=%1

powershell -command \"Expand-Archive -Path '%destination%\\package.zip' -DestinationPath '%destination%' -Force\"
cd \"%destination%\"
del \"package.zip\"

for %%i in ("%~dp0..") do set "folder=%%~fi"
echo %folder%

xcopy \"Settings\\Settings.dat\" \"%folder%\\Settings\\\" /E /R /S /Y
xcopy \"Horizon AD User Tool.exe\" \"%folder%\\\" /E /R /S /Y

echo \"%folder%\\Horizon AD User Tool.exe\"
start \"Horizon AD User Tool\" \"%folder%\\Horizon AD User Tool.exe\"

endlocal
pause
goto :EOF
"""


class Splash(ttk.Toplevel):
    """Splash Screen displayed before the program starts"""

    def __init__(self, original, themename="trinity-dark"):
        super().__init__()
        global photo, root
        self.bind_all("<Control-c>", self.handler)
        signal(SIGINT, lambda x, y: print("") or self.handler(0))
        self.original_frame = original
        self.original_frame.hide()
        # self.withdraw()
        W, H = 504, 250
        x, y = self.centerWindow(W, H)
        self.geometry("%dx%d%+d%+d" % (W, H, x, y))
        self.attributes("-fullscreen", False)
        self.attributes("-topmost", True)

        if fn.name == "nt":
            self.attributes("-toolwindow", True)
            self.attributes("-transparentcolor", "grey15")
        else:
            self.attributes("-type", "splash")

        self.overrideredirect(True)
        self.update()

        self.canvas = ttk.Canvas(
            self,
            bg="grey15",
            width=W - 4,
            height=H - 4,
            highlightthickness=0,
        )
        self.canvas.pack()
        photo = ttk.PhotoImage(data=loading)
        self.canvas.create_image(1, 1.5, image=photo, anchor="nw")

        self.count = 1
        self.text = self.canvas.create_text(
            10,
            216,
            text="Checking for Update...",
            fill="white",
            font=("Poppins", 12),
            anchor="nw",
        )
        # self.updt = ttk.Label(
        #     self,
        #     text="Checking for Update...",
        #     background="grey15",
        #     foreground="dark green",
        # )

        self.prog = ttk.Progressbar(self, length=500.5, maximum=100)
        self.prog.place(x=1.5, y=240)
        # self.updt.place(x=1.5, y=224)
        # print(self.ConsoleWelcome())
        self.cleanUpRun()

        t = threading.Thread(target=self.checkUpdate)
        t.daemon = True
        t.start()

    def animate(self, frames, gif):
        ind = 0
        frame = frames[ind]
        ind += 1
        if ind > 78:
            ind = 0
        gif.configure(image=frame)

    def centerWindow(self, width, height):  # Return 4 values needed to center Window
        screen_width = self.winfo_screenwidth()  # Width of the screen
        screen_height = self.winfo_screenheight()  # Height of the screen
        x = (screen_width / 2) - (width / 2)
        y = (screen_height / 2) - (height / 2)
        return int(x), int(y)

    def checkUpdate(self):
        try:
            time.sleep(2)
            r = requests.get(versionFile)
            if r.status_code == 200:
                # print(r.text)
                if version.parse(str(r.text)) > version.parse(
                    str(fn.Version.replace("v", ""))
                ):
                    # print("New version available")
                    self.canvas.itemconfig(
                        self.text, text="Downloading new version v%s" % str(r.text)
                    )
                    # self.updt["text"] = "Downloading new version v%s" % str(r.text)
                    self.cleanUp()
                    t = threading.Thread(target=self.startUpdate, args=(r.text,))
                    t.daemon = True
                    t.start()
                else:
                    self.canvas.itemconfig(
                        self.text,
                        text="You are on the latest version %s" % str(fn.Version),
                    )

                    # self.updt["text"] = "You are on the latest version %s" % str(
                    #     fn.Version
                    # )
                    time.sleep(2)
                    self.cleanUpRun()
                    self.onClose()
            else:
                print(r.status_code)
                self.onClose()

        except Exception as e:
            print("ERROR ", e)

    def cleanUp(self):
        try:
            if fn.path.exists(fn.temp_dir + "Settings\\"):
                for x in fn.Path(fn.temp_dir + "Settings\\").iterdir():
                    remove(x)
            if fn.path.exists(fn.temp_dir):
                for x in fn.Path(fn.temp_dir).iterdir():
                    if fn.path.isdir(x):
                        rmdir(x)
                    remove(x)
                rmdir(fn.temp_dir)
        except:  # noqa: E722
            try:
                for x in fn.Path(fn.temp_dir).iterdir():
                    if fn.path.isdir(x):
                        rmdir(x)
                    remove(x)
                rmdir(fn.temp_dir)
            except:  # noqa: E722
                pass

        if not fn.path.exists(fn.temp_dir):
            mkdir(fn.temp_dir)

    def cleanUpRun(self):
        try:
            if fn.path.exists(fn.temp_dir + "Settings\\"):
                for x in fn.Path(fn.temp_dir + "Settings\\").iterdir():
                    remove(x)
            if fn.path.exists(fn.temp_dir):
                for x in fn.Path(fn.temp_dir).iterdir():
                    if fn.path.isdir(x):
                        rmdir(x)
                    remove(x)
                rmdir(fn.temp_dir)
        except:  # noqa: E722
            try:
                for x in fn.Path(fn.temp_dir).iterdir():
                    if fn.path.isdir(x):
                        rmdir(x)
                    remove(x)
                rmdir(fn.temp_dir)
            except:  # noqa: E722
                pass

    def ConsoleWelcome(self):
        fn.clear_console()
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

    def startUpdate(self, versionz):
        with open("".join([fn.temp_dir, "updater.bat"]), "w") as batch:
            batch.write(dwnld)
            batch.close()
        # start = time.perf_counter()
        # print("".join([newProg, "-", versionz, ".zip"]))
        with requests.get(
            "".join([newProg, "-", versionz, ".zip"]),
            stream=True,
        ) as r:

            total_size = int(r.headers.get("Content-Length"))
            # print(total_size / (5 * 1024 * 1024))
            self.prog["maximum"] = 100
            with open("".join([fn.temp_dir, "package.zip"]), "wb") as f:
                if total_size is None:  # no content length header
                    f.write(r.content)
                else:
                    chunk_size = 5 * 1024 * 1024
                    tsize = 0
                    obj = bytearray()
                    t0 = time.time()
                    j = 0
                    # dl = 0
                    for i, chunk in enumerate(r.iter_content(chunk_size=chunk_size)):
                        # for chunk in response.iter_content(chunk_size=1024):
                        # dl += len(chunk)
                        tsize += len(chunk)
                        c = i * tsize / total_size * 100
                        obj.extend(chunk)
                        self.prog["value"] = float(
                            c
                        )  # (total_size - tsize) / (5 * 1024 * 1024))
                        t2 = time.time()
                        tt = t2 - t0
                        speedz = round(5 / tt, 2)
                        self.canvas.itemconfig(
                            self.text,
                            text="Downloading... %s MB/s (%.2f%%)"
                            % (
                                str(speedz),
                                float(c),
                            ),
                        )
                        # self.updt["text"] = "Downloading... %s MB/s (%.2f%%)" % (
                        #     str(speedz),
                        #     float(c),
                        # )

                        print(
                            "MAX = %s | VAL = %s"
                            % (
                                float((total_size) / (5 * 1024 * 1024)),
                                float((total_size - tsize) / (5 * 1024 * 1024)),
                            )
                        )
                        if tsize > chunk_size:
                            j += 1
                            ## Calculate the speed.. this is in MB/s,
                            ## but you can easily change to KB/s, or Blocks/s
                            t1 = time.time()
                            t = t1 - t0
                            speed = round(5 / t, 2)

                            f.write(obj)
                            print("got", j * 5, "MB ", "block", j, " @", speed, "MB/s")

                            obj = bytearray()
                            tsize = 0
                            t0 = time.time()
                    f.write(obj)
        self.onCloseUpdate()

    def onCloseUpdate(self):
        process = sp.Popen(
            [fn.temp_dir + "updater.bat", fn.temp_dir],
            shell=True,
            creationflags=sp.CREATE_NEW_CONSOLE,
        )
        subprocess_pid = process.pid
        print(subprocess_pid)
        _exit(0)
        # self.destroy()
        # self.original_frame.destroy()

    def onClose(self):
        self.cleanUpRun()
        self.destroy()
        Login.Login(self.original_frame)
        # self.original_frame.show()

    def handler(self, handle):
        msg = "Ctrl-c was pressed. Exiting now... "
        self.cleanUp()
        print(msg)
        print("")
        self.original_frame.destroy()
