import threading
import time
import Login
import ttkbootstrap as ttk
import io
from signal import SIGINT, signal
from PIL import Image, ImageDraw, ImageTk
import subprocess as sp
from os import remove, rmdir, mkdir, _exit
import usr.lib.Arxis_AD_Tool.Functions as fn
import requests
from packaging import version

from usr.lib.Arxis_AD_Tool.icon import loading

# from GifLabel import GifLabel

loadedMain = False
# versionFile = "https://trincloud.cc/programs/hcs_ad_tool.txt"
newProg = "https://trincloud.cc/programs/release/TrinityCloud%20AD%20User%20Tool"
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
xcopy \"TrinityCloud AD User Tool.exe\" \"%folder%\\\" /E /R /S /Y

echo \"%folder%\\%nameComplete%\"
start \"TrinityCloud AD User Tool\" \"%folder%\\TrinityCloud AD User Tool.exe\"

endlocal
pause
goto :EOF
"""


def decode_base64_image(base64_string):
    """
    Decode a Base64 string and return a PIL image.
    """
    image_data = fn.base64.b64decode(base64_string)
    image = Image.open(io.BytesIO(image_data))
    return image


def create_rounded_image(image, radius):
    """
    Create an image with rounded corners.
    """
    # Create a mask
    mask = Image.new("L", image.size, 0)
    draw = ImageDraw.Draw(mask)
    draw.rounded_rectangle((0, 0) + image.size, radius, fill=255)

    # Apply mask to the image
    rounded_image = Image.new("RGBA", image.size)
    rounded_image.paste(image, (0, 0), mask)
    return rounded_image


def start_move(event):
    root.x = event.x
    root.y = event.y


def stop_move(event):
    root.x = None
    root.y = None


def do_move(event):
    x = event.x_root - root.x
    y = event.y_root - root.y
    root.geometry(f"+{x}+{y}")


class Splash(ttk.Toplevel):
    """Splash Screen displayed before the program starts"""

    def __init__(self, original, themename="trinity-dark"):
        super().__init__()
        global photo, root

        self.bind_all("<Control-c>", self.handler)
        signal(SIGINT, lambda x, y: print("") or self.handler(0))
        self.original_frame = original
        self.original_frame.hide()
        W, H = 504, 250
        x, y = self.centerWindow(W, H)
        self.geometry("%dx%d%+d%+d" % (W, H, x, y))
        self.attributes("-fullscreen", False)
        self.attributes("-topmost", True)
        self.resizable(False, False)
        self.title(
            "".join(
                [
                    "TrinityCloud AD User Tool v",
                    fn.Version[4 : fn.Version.__len__()],
                ]
            )
        )
        if fn.name == "nt":
            self.attributes("-toolwindow", True)
            self.attributes("-transparentcolor", "green")
        else:
            self.attributes("-type", "splash")
        self.configure(background="green")
        self.overrideredirect(True)
        self.update()
        image = decode_base64_image(loading)
        rounded_image = create_rounded_image(image, 20)
        photo = ImageTk.PhotoImage(rounded_image)
        self.canvas = ttk.Canvas(
            self,
            bg="green",
            width=W,
            height=H,
            highlightthickness=0,
        )
        self.canvas.pack(fill="both", expand=True)

        self.canvas.create_image(0, 0, image=photo, anchor="nw")

        self.count = 1
        self.text = self.canvas.create_text(
            20.2,
            206,
            text="Checking for Update...",
            fill="white",
            font=("Poppins", 12),
            anchor="nw",
        )
        self.prog = ttk.Progressbar(self, length=460.5, maximum=100)
        self.prog.place(x=20.2, y=235)
        self.cleanUpRun()

        t = threading.Thread(target=self.checkUpdate, args=("ADTools",))
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

    def checkUpdate(self, tool):
        try:
            time.sleep(2)
            # r = requests.get(versionFile)
            jsn = self.original_frame.updatez.get(tool)
            if "version" in jsn:
                # print(r.text)
                if version.parse(str(jsn["version"])) > version.parse(
                    str(fn.Version.replace("v", ""))
                ):
                    self.canvas.itemconfig(
                        self.text,
                        text="Downloading new version v%s" % str(jsn["version"]),
                    )
                    self.cleanUp()
                    t = threading.Thread(
                        target=self.startUpdate,
                        args=(str(jsn["version"]),),
                    )
                    t.daemon = True
                    t.start()
                else:
                    self.canvas.itemconfig(
                        self.text,
                        text="You are on the latest version %s" % str(fn.Version),
                    )

                    time.sleep(2)
                    self.cleanUpRun()
                    self.onClose()
            else:
                print(jsn)
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

                        print(
                            "MAX = %s | VAL = %s"
                            % (
                                float((total_size) / (5 * 1024 * 1024)),
                                float((total_size - tsize) / (5 * 1024 * 1024)),
                            )
                        )
                        if tsize > chunk_size:
                            j += 1
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

    def onClose(self):
        self.cleanUpRun()
        self.destroy()
        Login.Login(self.original_frame)

    def handler(self, handle):
        msg = "Ctrl-c was pressed. Exiting now... "
        self.cleanUp()
        print(msg)
        print("")
        self.original_frame.destroy()
