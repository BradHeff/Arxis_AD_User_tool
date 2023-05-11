import configparser
import csv
import tkinter
from configparser import ExtendedInterpolation

from Functions import data_dir, settings_dir

logWindowExists = False
csvfile2 = None


def convertCSV(file, setting):
    data = dict()
    with open(data_dir + file, "r", newline='\n') as csvfile2:
        reader = csv.DictReader(csvfile2, dialect='excel')
        has_rows = False
        for x in reader:
            if setting == "groups":
                has_rows = True
                data[x['positions']] = x['groups'].split(",")
            elif setting == "positionsOU":
                has_rows = True
                data[x['positions']] = x['ou']
            elif setting == "title":
                has_rows = True
                data[x['positions']] = x['title']
            elif setting == "positions":
                has_rows = True
                data[x['category']] = x['positions'].split(",")
            else:
                has_rows = False
        if not has_rows:
            data = "{}"
        csvfile2.close()
    return str(data).replace("\'", "\"")


def updateSettings(data, title, option):
    parser = configparser.ConfigParser(interpolation=ExtendedInterpolation(),
                                       inline_comment_prefixes=('#', ';'),
                                       comment_prefixes=('#', ';'))
    parser.read(settings_dir + "Settings.ini")
    if not parser.has_section(title):
        parser.add_section(title)
    parser.set(title, option, ''.join(["\'", str(data), "\'"]))
    val = parser.get('Settings', 'Company').replace("\'", "").replace("\"", "")
    if title not in val:
        parser.set('Settings', 'Company', ''.join(["'", val, ',', title, "'"]))
    with open(settings_dir + "\\Settings.ini", "w") as w:
        parser.write(w)


def inputBox(self):
    # logWindowExists = True

    geo = self.winfo_geometry()
    posX = geo.split("+")[1]
    posY = geo.split("+")[2]

    center_x = int(int(posX) + (self.W / 2) - 100)
    center_y = int(int(posY) + (self.H / 2) - 75)

    app = tkinter.Tk()
    app.title("Company Title")
    app.geometry(f'200x150+{center_x}+{center_y}')
    app.attributes("-fullscreen", False)
    app.attributes("-toolwindow", True)
    app.attributes("-topmost", True)

    message = tkinter.Label(app, text="Title: ")
    ent = tkinter.Entry(app, width=80)
    ent.insert(0, self.newTitle)
    btn = tkinter.Button(app, text="Ok", width=20,
                         command=lambda: on_closing_yes(self))

    message.pack(fill='x', expand=True, padx=10)
    ent.pack(fill='x', expand=True, padx=10)
    btn.pack(fill='x', expand=True, padx=10, pady=5)

    def on_closing(self):
        self.isExit = True
        # logWindowExists = False
        app.destroy()
        app.quit()

    def on_closing_yes(self):
        self.isExit = False
        # logWindowExists = False
        self.newTitle = ent.get()
        app.destroy()
        app.quit()

    app.protocol("WM_DELETE_WINDOW", lambda: on_closing(self))
    app.mainloop()


def getTitleWindow(self):
    if not logWindowExists:
        inputBox(self)
