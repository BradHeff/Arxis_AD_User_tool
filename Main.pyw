import datetime
import threading
from signal import SIGINT, signal
import tkthread as tkt

import ttkbootstrap as ttk
from ttkbootstrap import Style
import Functions as f
import Gui

import splash


class Main(ttk.Window):
    """Main Class for AD Unlocker"""

    def __init__(self):
        super(Main, self).__init__(themename="trinity-dark")
        self.bind_all("<Control-c>", self.handler)
        signal(SIGINT, lambda x, y: print("") or self.handler())
        # self.after(500, self.check)
        self.protocol("WM_DELETE_WINDOW", self.on_closing)
        self.company = "Horizon"
        self.server = f.getServer(self, self.company)
        splash.Splash(self)
        self.data = dict()
        self.domains = dict()
        self.chkBtns = dict()
        self.jobTitle = dict()
        self.updateList = dict()
        self.fullGroups = dict()

        self.selItem = []
        self.selItem2 = []
        self.selItem3 = []
        self.options = []
        self.groups = []
        self.positions = []
        self.pdomains = []
        self.homePaths = []
        self.campus = []
        self.username = ""
        self.password = ""
        self.ou = ""
        self.posOU = ""
        self.domainName = ""
        self.samFormat = ""
        self.groupPos = ""
        self.editPosOU = ""
        self.movePosOU = ""
        self.moveNewPosOU = ""
        self.department = ""
        self.servs = False
        self.isRunning = False
        self.loaded = False
        self.isExit = False
        self.data_file = False

        self.checkCount = 0
        self.checkRow = 0

        self.load = ttk.BooleanVar(self, False)
        self.comp = "Select Company"

        currentDateTime = datetime.datetime.now()
        date = currentDateTime.date()
        self.date = date.strftime("%Y")

        Gui.baseGUI(self)

        self.title(
            "".join(["TrinityCloud AD User Tool v", f.Version[4 : f.Version.__len__()]])
        )

        self.options.set("Horizon")
        self.comboSelect("", "H")

        self.combobox["state"] = ttk.NORMAL

        if not f.DEBUG:
            self.combobox["state"] = ttk.DISABLED

        splash.loadedMain = True

    def on_closing(self):
        print("Thanks for using Trinity AD User Tool!\n")
        self.destroy()
        self.quit()

    def hide(self):
        self.withdraw()

    def show(self):
        self.update()
        self.deiconify()

    def setLoad(self):
        if f.path.isfile(f.settings_dir + "Config.ini"):
            parser = f.cCrypt.ConfigParserCrypt()
            parser.read(f.settings_dir + "Config.ini")
            parser.set("config", "autoload", str(self.load.get()))
            with open(f.settings_dir + "Config.ini", "w+") as w:
                parser.write(w)
        else:
            f.saveConfig(self)

    def alterButton(self, widget):
        match self.tabControl.index(self.tabControl.select()):
            case 0:
                self.btn_unlockAll.configure(text="Unlock All", state=ttk.NORMAL)
                if self.state and self.servs:
                    f.widgetStatusFailed(self, False)
            case 1:
                self.btn_unlockAll.configure(text="Create User", state=ttk.NORMAL)
                if "Select" not in self.options.get():
                    if not self.compFail:
                        if self.domains["Primary"].__len__() <= 0:
                            f.widgetStatusFailed(self, True)

                            tkt.call_nosync(
                                self.messageBox,
                                "ERROR!!",
                                "Domains Settings is not complete!",
                            )
                            return
                        if self.groupPos.__len__() <= 0:
                            f.widgetStatusFailed(self, True)

                            tkt.call_nosync(
                                self.messageBox,
                                "ERROR!!",
                                "Group Settings is not complete!",
                            )
                            return
                        if self.positions.__len__() <= 0:
                            f.widgetStatusFailed(self, True)

                            tkt.call_nosync(
                                self.messageBox,
                                "ERROR!!",
                                "Positions Settings is not complete!",
                            )

                            return
                    else:
                        if self.state:
                            f.widgetStatusFailed(self, True)
            case 2:
                self.btn_unlockAll.configure(text="Move User", state=ttk.NORMAL)

                if not self.compFail:
                    pass
                else:
                    if self.state:
                        f.widgetStatusFailed(self, True)
            case 3:
                self.btn_unlockAll.configure(text="Update User", state=ttk.NORMAL)
                if not self.compFail:
                    pass
                else:
                    if self.state:
                        f.widgetStatusFailed(self, True)
            case 4:
                self.btn_unlockAll.configure(text="????")
                if not self.compFail:
                    pass
                else:
                    if self.state:
                        f.widgetStatusFailed(self, True)

            case _:
                f.Toast("ERROR!!!", "Something went wrong!", "sad")

    def driveSelect(self, el):
        pass

    def selectItem(self, a):
        curItem = self.tree.focus()
        self.selItem = self.tree.item(curItem)["values"]

    def selectItem2(self, a):
        curItem = self.tree3.focus()
        self.selItem2 = self.tree3.item(curItem)["values"]

    def selectItem3(self, a):
        curItem = self.tree4.focus()
        self.selItem3 = self.tree4.item(curItem)["values"]
        self.entDomain["state"] = "normal"
        self.entDesc.delete(0, "end")
        self.entJobTitle.delete(0, "end")
        self.entSamname.delete(0, "end")
        self.entDomain.delete(0, "end")
        self.lname_entry.delete(0, "end")
        self.fname_entry.delete(0, "end")
        try:
            domain = str(self.updateList[self.selItem3[0]]["userPrincipalName"])
            domain = domain.split("@")[1].strip()
            self.entDomain.insert(0, domain)
        except Exception as e:
            print(e)
            pass
        try:
            self.entJobTitle.insert(0, self.updateList[self.selItem3[0]]["title"])
        except Exception as e:
            print(e)
            pass
        try:
            self.lname_entry.insert(0, self.updateList[self.selItem3[0]]["lname"])
        except Exception as e:
            print(e)
            pass
        try:
            self.fname_entry.insert(0, self.updateList[self.selItem3[0]]["fname"])
        except Exception as e:
            print(e)
            pass
        try:
            self.entSamname.insert(0, self.selItem3[0])
        except Exception as e:
            print(e)
            pass
        try:
            desc = self.updateList[self.selItem3[0]]["description"][0]
            self.entDesc.insert(0, str(desc))
        except Exception as e:
            print(e)
            pass
        self.entDomain["state"] = "readonly"

    def getCheck(self):
        grp = []
        for x in self.groups:
            grp.append(x)
        return grp

    def posSelect(self, value):
        self.clear_group()
        camp = "Balaklava"
        self.dep = "Balaklava Campus"
        isBalak = False

        if "clare" in self.campH.get():
            isBalak = False
        else:
            isBalak = True

        if not isBalak:
            if "Year" in self.var.get() or "Found" in self.var.get():
                self.posOU = self.positionsOU[self.var.get() + "-Clare"]
            elif "ESO" in self.var.get() or "Student Support" in self.var.get():
                self.posOU = self.positionsOU["Student Support Clare"]
            elif "Admin" in self.var.get() and "Temp" not in self.var.get():
                self.posOU = self.positionsOU[self.var.get() + " Clare"]
            self.groups = self.groupPos[self.var.get()]
            descDate = f"{self.date} Clare"
            camp = "Clare"
            self.dep = "Clare Campus"
        else:
            descDate = self.date
            if "Year" in self.var.get() or "Found" in self.var.get():
                self.posOU = self.positionsOU[self.var.get()]
                self.desc.delete(0, "end")
                self.desc.insert(0, f"{self.var.get()} - {descDate}")
            else:
                self.posOU = self.positionsOU[self.var.get()]
                self.desc.delete(0, "end")
                self.desc.insert(0, descDate)

            self.groups = self.groupPos[self.var.get()]
        style = Style()
        self.checkCount = 0
        self.checkRow = 0
        print(self.groups)
        for x in self.groups:
            gn = x.split(",")[0].replace("CN=", "")
            self.chkBtns[gn] = ttk.IntVar()
            self.chkBtns[gn].set(1)

            cBtnY = ttk.Label(self.lbl_frame2, text=gn)
            cBtnY.configure(
                background=style.colors.primary, foreground=style.colors.bg, padding=10
            )
            cBtnY.grid(row=self.checkRow, column=self.checkCount, padx=10, pady=10)
            self.checkCount += 1
            if self.checkCount > 3:
                self.checkCount = 0
                self.checkRow += 1

        if not self.jobTitle.__len__() <= 3:
            try:
                self.jobTitleEnt.delete(0, "end")
                self.jobTitleEnt.insert(0, self.jobTitle[self.var.get()])
            except Exception as e:
                print(e)

        if not self.dep.__len__() <= 3:
            try:
                self.depEnt.delete(0, "end")
                self.depEnt.insert(0, f"{camp} Campus")
                self.orgCompEnt.delete(0, "end")
                self.orgCompEnt.insert(0, f"Horizon Christian School {camp}")
            except Exception as e:
                print(e)

    def editSelect(self, value):
        self.entDomain["state"] = "normal"
        self.entDesc.delete(0, "end")
        self.entJobTitle.delete(0, "end")
        self.entSamname.delete(0, "end")
        self.entDomain.delete(0, "end")
        self.lname_entry.delete(0, "end")
        self.fname_entry.delete(0, "end")
        self.entDomain["state"] = "readonly"
        t = threading.Thread(target=self.editOption)
        t.daemon = True
        t.start()

    def editOption(self):
        self.tree3.delete(*self.tree3.get_children())
        self.var2.set(None)
        self.var.set(None)
        list = self.lbl_frame8.grid_slaves()
        for lx in list:
            lx.destroy()
        self.status["text"] = "Loading Users ...."
        if "clare" in self.EcampH.get():
            if "Year" in self.var3.get() or "Found" in self.var3.get():
                self.updateList = f.listUsers2(
                    self, self.positionsOU[self.var3.get() + "-Clare"]
                )
                self.editPosOU = self.positionsOU[self.var3.get() + "-Clare"]
            elif "ESO" in self.var3.get() or "Student Support" in self.var3.get():
                self.updateList = f.listUsers2(
                    self, self.positionsOU["Student Support Clare"]
                )
                self.editPosOU = self.positionsOU["Student Support Clare"]
            elif "Admin" in self.var3.get() and "Temp" not in self.var3.get():
                self.updateList = f.listUsers2(
                    self, self.positionsOU[self.var3.get() + " Clare"]
                )
                self.editPosOU = self.positionsOU[self.var3.get() + " Clare"]
            else:
                self.updateList = f.listUsers2(self, self.positionsOU[self.var3.get()])
                self.editPosOU = self.positionsOU[self.var3.get()]
        else:
            self.updateList = f.listUsers2(self, self.positionsOU[self.var3.get()])
            self.editPosOU = self.positionsOU[self.var3.get()]
        self.tree4.delete(*self.tree4.get_children())
        self.progress["maximum"] = self.updateList.__len__()
        count = 0
        for i in self.updateList:
            count += 1
            self.progress["value"] = count
            self.tree4.insert(
                "",
                "end",
                values=(i, self.updateList[i]["name"], self.updateList[i]["ou"]),
            )
        self.progress["value"] = 0
        self.status["text"] = "Idle..."

    def moveSelect(self, value):
        t = threading.Thread(target=self.movePosSelect, args=(value,))
        t.daemon = True
        t.start()

    def moveNewPosSelect(self, value=None):
        if "clare" in self.McampH2.get():
            if "Year" in self.var2.get() or "Found" in self.var2.get():
                self.moveNewPosOU = self.positionsOU[self.var2.get() + "-Clare"]
                print("CLARE!!@")
            elif "ESO" in self.var2.get() or "Student Support" in self.var2.get():
                self.moveNewPosOU = self.positionsOU["Student Support Clare"]
                print("CLARE!!@@")
            elif "Admin" in self.var2.get() and "Temp" not in self.var2.get():
                self.moveNewPosOU = self.positionsOU[self.var2.get() + " Clare"]
                print("CLARE!!@@#")
            else:
                self.moveNewPosOU = self.positionsOU[self.var2.get()]
                print("CLARE!!@@##")
        else:
            self.moveNewPosOU = self.positionsOU[self.var2.get()]
            print("BALAK")

    def movePosSelect(self, value=None):
        self.tree4.delete(*self.tree4.get_children())
        self.tree3.delete(*self.tree3.get_children())
        self.var3.set(None)
        self.var.set(None)
        self.entDomain["state"] = "normal"
        self.entDesc.delete(0, "end")
        self.entJobTitle.delete(0, "end")
        self.entSamname.delete(0, "end")
        self.entDomain.delete(0, "end")
        self.lname_entry.delete(0, "end")
        self.fname_entry.delete(0, "end")
        self.entDomain["state"] = "readonly"
        self.status["text"] = "Loading Users ...."

        if "clare" in self.McampH.get():
            if "Year" in self.var2.get() or "Found" in self.var2.get():
                self.updateList = f.listUsers2(
                    self, self.positionsOU[self.var2.get() + "-Clare"]
                )
                self.movePosOU = self.positionsOU[self.var2.get() + "-Clare"]

            elif "ESO" in self.var2.get() or "Student Support" in self.var2.get():
                self.updateList = f.listUsers2(
                    self, self.positionsOU["Student Support Clare"]
                )
                self.movePosOU = self.positionsOU["Student Support Clare"]

            elif "Admin" in self.var2.get() and "Temp" not in self.var2.get():
                self.updateList = f.listUsers2(
                    self, self.positionsOU[self.var2.get() + " Clare"]
                )
                self.movePosOU = self.positionsOU[self.var2.get() + " Clare"]

            else:
                self.updateList = f.listUsers2(self, self.positionsOU[self.var2.get()])
                self.movePosOU = self.positionsOU[self.var2.get()]

        else:
            self.updateList = f.listUsers2(self, self.positionsOU[self.var2.get()])
            self.movePosOU = self.positionsOU[self.var2.get()]

        usersList = f.listUsers(self, self.movePosOU)
        self.progress["maximum"] = float(usersList.__len__())
        progCount = 1
        for i in usersList:
            self.progress["value"] = progCount
            self.tree3.insert(
                "", "end", values=(i, usersList[i]["name"], usersList[i]["ou"])
            )
            progCount += 1

        self.status["text"] = "Idle..."
        self.progress["value"] = 0

    def clear_group(self):
        list = self.lbl_frame2.grid_slaves()
        for la in list:
            la.destroy()

    def clear_campus(self):
        list = self.lbl_frameC.pack_slaves()
        # listF = self.lbl_frameF.pack_slaves()
        listG = self.lbl_frameG.pack_slaves()
        for la in list:
            la.destroy()
        # for l in listF:
        #     l.destroy()
        for la in listG:
            la.destroy()

    def clear_pos(self):
        list = self.lbl_frame.grid_slaves()
        for la in list:
            la.destroy()
        list = self.lbl_frame4.grid_slaves()
        for la in list:
            la.destroy()

    def clear_exp(self):
        list = self.lbl_frame5.grid_slaves()
        for lx in list:
            lx.destroy()

    def clear_move(self):
        list = self.lbl_frame6.grid_slaves()
        for lx in list:
            lx.destroy()
        list = self.lbl_frame7.grid_slaves()
        for lxx in list:
            lxx.destroy()
        list = self.lbl_frame8.grid_slaves()
        for lxxx in list:
            lxxx.destroy()

    def clear_edit(self):
        list = self.lbl_frame9.grid_slaves()
        for la in list:
            la.destroy()
        list = self.lbl_frame10.grid_slaves()
        for la in list:
            la.destroy()

    def expSelect(self):
        self.expiredOU = self.expiredOUs[self.exOU.get()]
        self.tree2.delete(*self.tree2.get_children())

    def comboSelect(self, widget, value="H"):
        if "camp" not in str(widget):
            f.getConfig(self, self.options.get())
            self.clear_campus()
            if (
                not f.base64.b64decode(self.campus)
                .decode("UTF-8")
                .split(",")[0]
                .__len__()
                <= 0
            ):
                counter = 1
                for x in f.base64.b64decode(self.campus).decode("UTF-8").split(","):
                    balak = ttk.Radiobutton(
                        self.lbl_frameC,
                        text=x,
                        variable=self.campH,
                        value=x,
                        command=lambda: self.comboSelect("camp", "H"),
                    )
                    balak_edit = ttk.Radiobutton(
                        self.lbl_frameG,
                        text=x,
                        variable=self.EcampH,
                        value=x,
                        command=lambda: self.comboSelect("camp", "E"),
                    )
                    balak_move = ttk.Radiobutton(
                        self.lbl_frameF,
                        text=x,
                        variable=self.McampH,
                        value=x,
                        command=lambda: self.comboSelect("camp", "M"),
                    )
                    balak_move2 = ttk.Radiobutton(
                        self.lbl_frameF2,
                        text=x,
                        variable=self.McampH2,
                        value=x,
                    )
                    if counter == 1:
                        balak.pack(side="left", fill="y", expand=True, padx=10, pady=10)
                        balak_edit.pack(
                            side="left", fill="y", expand=True, padx=10, pady=10
                        )
                        balak_move.pack(
                            side="left", fill="y", expand=True, padx=10, pady=10
                        )
                        balak_move2.pack(
                            side="left", fill="y", expand=True, padx=10, pady=10
                        )
                    else:
                        balak.pack(
                            side="right", fill="y", expand=True, padx=10, pady=10
                        )
                        balak_edit.pack(
                            side="right", fill="y", expand=True, padx=10, pady=10
                        )
                        balak_move.pack(
                            side="right", fill="y", expand=True, padx=10, pady=10
                        )
                        balak_move2.pack(
                            side="right", fill="y", expand=True, padx=10, pady=10
                        )
                    counter -= 1

        t = threading.Thread(target=self.comboLoad, args=(value))
        t.daemon = True
        t.start()

    def comboLoad(self, value):  # noqa
        # print(self.positions)
        # f.pythoncom.CoInitialize()
        self.status["text"] = "Loading..."
        self.clear_pos()
        self.clear_group()
        # self.clear_exp()
        self.clear_move()
        self.clear_edit()
        self.tree4.delete(*self.tree4.get_children())
        self.tree3.delete(*self.tree3.get_children())
        # self.tree2.delete(*self.tree2.get_children())
        self.tree.delete(*self.tree.get_children())
        self.desc.delete(0, "end")
        self.dpass.delete(0, "end")
        self.jobTitleEnt.delete(0, "end")
        self.depEnt.delete(0, "end")
        self.orgCompEnt.delete(0, "end")
        self.desc.insert(0, self.date)

        if self.compFail and self.state and self.servs:
            f.widgetStatusFailed(self, False)

            tkt.call_nosync(self.messageBox, "ERROR!!", "Some settings are incomplete")
            return

        if self.compFail:
            f.widgetStatusFailed(self, True)

            tkt.call_nosync(
                self.messageBox, "ERROR!!", "Server settings are incomplete"
            )
            return

        if not self.positions.__len__() <= 0:
            try:
                self.progress["value"] = 20
                count = 0
                row = 0
                count2 = 0
                row2 = 0

                count11 = 0
                row11 = 0

                self.chkValue = ttk.StringVar(self.lbl_frame8, "1")
                self.var = ttk.StringVar(None, "1")
                self.var2 = ttk.StringVar(None, "1")
                self.var3 = ttk.StringVar(None, "1")
                for x in self.positions:
                    for y in self.positions[x]:
                        prog = 1
                        self.progress["maximum"] = float(self.positions.__len__())
                        self.progress["value"] = prog

                        if not x == "Students":
                            rbtn = ttk.Radiobutton(
                                self.lbl_frame,
                                text=y,
                                variable=self.var,
                                command=lambda: self.posSelect(value),
                                value=y,
                            )
                            rbtn.grid(row=row, column=count, padx=10, pady=10)
                            rbtn.selection_clear()
                            rbtn3 = ttk.Radiobutton(
                                self.lbl_frame6,
                                text=y,
                                variable=self.var2,
                                command=lambda: self.moveSelect(value),
                                value=y,
                            )
                            rbtn3.grid(row=row, column=count, padx=10, pady=10)
                            rbtn3.selection_clear()
                            rbtn11 = ttk.Radiobutton(
                                self.lbl_frame8,
                                text=y,
                                variable=self.chkValue,
                                command=lambda: self.moveNewPosSelect(value),
                                value=y,
                            )
                            rbtn11.grid(row=row11, column=count11, padx=10, pady=10)
                            rbtn11.selection_clear()
                            count11 += 1
                            if count11 > 4:
                                count11 = 0
                                row11 += 1
                            rbtn5 = ttk.Radiobutton(
                                self.lbl_frame9,
                                text=y,
                                variable=self.var3,
                                command=lambda: self.editSelect(value),
                                value=y,
                            )
                            rbtn5.grid(row=row, column=count, padx=10, pady=10)
                            rbtn5.selection_clear()
                            count += 1
                            if count > 3:
                                count = 0
                                row += 1
                        else:
                            rbtn2 = ttk.Radiobutton(
                                self.lbl_frame4,
                                text=y,
                                variable=self.var,
                                command=lambda: self.posSelect(value),
                                value=y,
                            )
                            rbtn2.grid(row=row2, column=count2, padx=10, pady=10)
                            rbtn2.selection_clear()
                            rbtn4 = ttk.Radiobutton(
                                self.lbl_frame7,
                                text=y,
                                variable=self.var2,
                                command=lambda: self.moveSelect(value),
                                value=y,
                            )
                            rbtn4.grid(row=row2, column=count2, padx=10, pady=10)
                            rbtn4.selection_clear()
                            rbtn12 = ttk.Radiobutton(
                                self.lbl_frame8,
                                text=y,
                                variable=self.chkValue,
                                command=lambda: self.moveNewPosSelect(value),
                                value=y,
                            )
                            rbtn12.grid(row=row11, column=count11, padx=10, pady=10)
                            rbtn12.selection_clear()
                            count11 += 1
                            if count11 > 4:
                                count11 = 0
                                row11 += 1
                            rbtn6 = ttk.Radiobutton(
                                self.lbl_frame10,
                                text=y,
                                variable=self.var3,
                                command=lambda: self.editSelect(value),
                                value=y,
                            )
                            rbtn6.grid(row=row2, column=count2, padx=10, pady=10)
                            rbtn6.selection_clear()
                            count2 += 1
                            if count2 > 6:
                                count2 = 0
                                row2 += 1
                        prog += 1
            except Exception as e:
                print("ERROR POS")
                print(e)

        # if not self.expiredOUs.__len__() <= 0:
        #     try:
        #         self.progress['maximum'] = float(self.expiredOUs.\
        #       __len__())
        #         prog = 1
        #         count3 = 0
        #         row3 = 0
        #         self.exOU = ttk.StringVar(None,"1")
        #         for i in self.expiredOUs:
        #             self.progress['value'] = prog
        #             rbtn3 = ttk.Radiobutton(self.lbl_frame5,
        #               text=i, variable=self.exOU,
        #               command=self.expSelect, value=i)
        #             rbtn3.grid(row=row3, column=count3, padx=10, pady=10)
        #             rbtn3.selection_clear()
        #             count3 += 1
        #             if count3 > 3:
        #                 count3 = 0
        #                 row3 += 1
        #             prog += 1
        #     except:
        #         pass
        print(self.domains["Primary"])
        if not self.domains["Primary"].__len__() <= 0:
            try:
                self.progress["value"] = 60
                self.pdomains = self.domains["Primary"]
                self.combo_domain["values"] = self.pdomains
                self.primary_domain.set("Select Domain")
            except Exception as e:
                print("ERROR DOMAIN")
                print(e)
                pass
        if (
            not f.base64.b64decode(self.homePaths).decode("UTF-8").split(",").__len__()
            <= 0
        ):
            try:
                self.progress["value"] = 70
                self.homePath["values"] = (
                    f.base64.b64decode(self.homePaths).decode("UTF-8").split(",")
                )
                self.paths.set("Select Homepath")
                self.hdrive.set("Select Drive")
            except Exception as e:
                print("ERROR DRIVE")
                print(e)
                pass
        if not f.base64.b64decode(self.groupOU).decode("UTF-8").__len__() <= 3:
            self.progress["value"] = 80
            prog = 1
        self.progress["value"] = 0
        self.status["text"] = "Idle..."
        if f.path.isfile(f.settings_dir + "Config.ini") and not self.loaded:
            f.loadConfig(self)

    def resetPass(self):
        if self.selItem.__len__() <= 0:
            tkt.call_nosync(self.messageBox, "ERROR!!", "Must select a user!")
            return
        if self.passBox.get().__len__() < 8:
            tkt.call_nosync(self.messageBox, "ERROR!!", "Password Too Short!")
            return
        f.widgetStatus(self, ttk.DISABLED)
        newPass = self.passBox.get()
        t = threading.Thread(
            target=f.resetPassword, args=[self, self.selItem[2], newPass]
        )
        t.daemon = True
        t.start()

    def moveUser(self):
        pass

    def loadUsers(self):
        if "Select" in self.options.get():
            tkt.call_nosync(self.messageBox, "ERROR!!", "You must select a company!")
            return
        f.widgetStatus(self, ttk.DISABLED)
        self.tree.delete(*self.tree.get_children())
        t = threading.Thread(target=self.loads, args=[])
        t.daemon = True
        t.start()

    def loads(self):
        try:
            self.status["text"] = "Searching locked users ..."
            locked = f.listLocked(self)
            if locked.__len__() <= 0:
                f.widgetStatus(self, ttk.NORMAL)
                self.status["text"] = "Idle..."
                tkt.call_nosync(f.Toast, "COMPLETE!", "No Locked Users!", "happy")
                return
            else:
                self.status["text"] = "Populating list..."
                for x in locked:
                    self.tree.insert(
                        "", "end", values=(x, locked[x]["name"], locked[x]["ou"])
                    )
        except Exception as e:
            tkt.call_nosync(self.messageBox, "Error", "An error occurred, " + str(e))
            tkt.call_nosync(f.Toast, "ERROR!", "An error occurred", "angry")

        f.widgetStatus(self, ttk.NORMAL)
        self.status["text"] = "Idle..."

    def unlockUsers(self):
        if self.tree.get_children() == ():
            tkt.call_nosync(self.messageBox, "ERROR!!", "List cannot be empty!")
            return

        if self.selItem.__len__() <= 0:
            tkt.call_nosync(self.messageBox, "ERROR!!", "Must select a user!")
            return

        f.widgetStatus(self, ttk.DISABLED)
        self.status["text"] = "".join(["Unlocking ", self.selItem[1]])
        t = threading.Thread(target=self.unlocker, args=[])
        t.daemon = True
        t.start()

    def unlocker(self):
        f.unlockUser(self, self.selItem[2])
        selected_item = self.tree.selection()[0]
        self.tree.delete(selected_item)
        self.selItem = []
        self.status["text"] = "Idle..."
        tkt.call_nosync(f.Toast, "COMPLETE!", "Users Unlocked!", "happy")

    def unlockAll(self):
        f.widgetStatus(self, ttk.DISABLED)
        data = dict()
        if self.compFail:
            f.widgetStatus(self, ttk.NORMAL)

            tkt.call_nosync(
                self.messageBox,
                "ERROR!!",
                "Your Settings are incomplete\n\
            for this TAB!",
            )
            return
        match self.tabControl.index(self.tabControl.select()):
            case 0:
                if self.tree.get_children() == ():
                    f.widgetStatus(self, ttk.NORMAL)

                    tkt.call_nosync(self.messageBox, "ERROR!!", "List cannot be empty!")
                    return

                for line in self.tree.get_children():
                    self.data[self.tree.item(line)["values"][0]] = {
                        "name": self.tree.item(line)["values"][1],
                        "ou": self.tree.item(line)["values"][2],
                    }
                maxs = self.tree.get_children().__len__()
                self.progress["maximum"] = float(maxs)
                self.all = maxs
                t = threading.Thread(target=f.unlockAll, args=[self, self.data])
                t.daemon = True
                t.start()
            case 1:
                f.widgetStatus(self, ttk.DISABLED)
                if self.fname.get().__len__() >= 2 and self.lname.get().__len__() >= 2:
                    if self.dpass.get().__len__() < 8:
                        f.widgetStatus(self, ttk.NORMAL)

                        tkt.call_nosync(
                            self.messageBox,
                            "ERROR!!",
                            "Must enter Password\n\
                        or password 8 characters min",
                        )
                        return
                    if (
                        "Select" in self.primary_domain.get()
                        or "Select" in self.hdrive.get()
                        or self.paths.get().__len__() <= 0
                    ):
                        f.widgetStatus(self, ttk.NORMAL)
                        self.status["text"] = "Idle..."

                        tkt.call_nosync(
                            self.messageBox,
                            "ERROR!!",
                            "You must select domain\n\
                                        HomeDrive and HomePath",
                        )
                        return
                    self.progress["value"] = 10
                    self.status["text"] = "Rebuilding groups..."
                    groups = self.getCheck()
                    self.status["text"] = "Setting login name..."
                    match (self.samFormat.get()):
                        case "flastname":
                            samname = "".join(
                                [
                                    self.fname.get().strip()[0:1],
                                    self.lname.get().strip(),
                                ]
                            )
                        case "firstlastname":
                            samname = "".join(
                                [self.fname.get().strip(), self.lname.get().strip()]
                            )
                        case _:
                            samname = "".join(
                                [
                                    self.fname.get().strip(),
                                    ".",
                                    self.lname.get().strip(),
                                ]
                            )
                    self.status["text"] = "Rebuilding data..."
                    data["login"] = samname.lower()
                    data["first"] = self.fname.get().strip().capitalize()
                    data["last"] = self.lname.get().strip().capitalize()
                    data["password"] = self.dpass.get()
                    data["domain"] = self.primary_domain.get()
                    data["proxy"] = self.domains["Secondary"]
                    data["groups"] = groups
                    data["homeDirectory"] = self.paths.get() + "\\" + samname.lower()
                    data["homeDrive"] = self.hdrive.get() + ":"
                    data["description"] = self.desc.get()
                    data["title"] = self.jobTitleEnt.get()
                    data["department"] = self.depEnt.get()
                    data["company"] = self.orgCompEnt.get()
                    self.progress["value"] = 20
                    # print(data["groups"])
                    t = threading.Thread(target=f.createUser, args=(self, data))
                    t.daemon = True
                    t.start()
                else:
                    f.widgetStatus(self, ttk.NORMAL)

                    tkt.call_nosync(
                        self.messageBox,
                        "ERROR!!",
                        "First and Lastname must\n\
                    be filled!",
                    )
            # case 2:
            #     print("PRINTERD")
            case 2:
                if self.compFail:
                    f.widgetStatus(self, ttk.NORMAL)

                    tkt.call_nosync(
                        self.messageBox,
                        "ERROR!!",
                        "Your Settings are incomplete\n\
                    for this TAB!",
                    )
                    return
                if self.var2.get().__len__() <= 2 or self.movePosOU.__len__() <= 1:
                    tkt.call_nosync(
                        self.messageBox, "ERROR!!", "You must select a position!"
                    )
                    return
                if self.selItem2.__len__() <= 0:
                    tkt.call_nosync(
                        self.messageBox, "ERROR!!", "You must select a user!"
                    )
                    return
                self.status["text"] = "Moving " + str(self.selItem2[1]) + "..."
                f.widgetStatus(self, ttk.DISABLED)
                self.progress["max"] = 100
                self.progress["value"] = 30
                t = threading.Thread(
                    target=f.moveUser, args=[self, self.selItem2[2], self.moveNewPosOU]
                )
                t.daemon = True
                t.start()
            case 3:
                if self.compFail:
                    f.widgetStatus(self, ttk.NORMAL)

                    tkt.call_nosync(
                        self.messageBox,
                        "ERROR!!",
                        "Your Settings are incomplete\n\
                    for this TAB!",
                    )
                    return

                if (
                    self.entPass.get().__len__() >= 8
                    or self.entPass.get().__len__() == 0
                ):
                    if self.tree4.get_children() == ():
                        tkt.call_nosync(
                            self.messageBox, "ERROR!!", "Must select a position"
                        )
                        return

                    if self.selItem3.__len__() <= 0:
                        tkt.call_nosync(
                            self.messageBox, "ERROR!!", "Must select a user!"
                        )
                        return

                    if self.fname_entry.get().__len__() <= 1:
                        tkt.call_nosync(
                            self.messageBox,
                            "ERROR!!",
                            "First Name\
                        cannot be empty!",
                        )
                        return

                    data = dict()
                    f.widgetStatus(self, ttk.DISABLED)
                    self.progress["value"] = 10
                    self.status["text"] = "Gathering Information..."

                    data["login"] = self.entSamname.get()
                    data["first"] = self.fname_entry.get().capitalize()
                    data["last"] = self.lname_entry.get().capitalize()
                    data["domain"] = self.entDomain.get()
                    data["description"] = self.entDesc.get()
                    data["title"] = self.entJobTitle.get()
                    data["ou"] = self.updateList[self.selItem3[0]]["ou"]
                    data["password"] = self.entPass.get()
                    data["proxy"] = None

                    self.progress["value"] = 20
                    lists = self.updateList[self.selItem3[0]]
                    if lists["proxyAddresses"] is not None:
                        for x in lists["proxyAddresses"]:
                            if self.entDomain.get() not in x and x.__len__() > 5:
                                data["proxy"] = x.split("@")[1]
                            else:
                                if not self.domains["Secondary"].__len__() <= 3:
                                    data["proxy"] = self.domains["Secondary"]

                    else:
                        if not self.domains["Secondary"].__len__() <= 3:
                            data["proxy"] = self.domains["Secondary"]

                    t = threading.Thread(target=f.update_user, args=[self, data])
                    t.daemon = True
                    t.start()
                else:
                    f.widgetStatus(self, ttk.NORMAL)

                    tkt.call_nosync(
                        self.messageBox,
                        "ERROR!!",
                        "Password must be 8\
                    characters long",
                    )

            case _:
                print("")

        # elif self.tabControl.index(self.tabControl.select()) == 2:
        #     if not self.compFail:
        #         if not self.expiredOU == None:
        #             f.widgetStatus(self, ttk.DISABLED)
        #             t = threading.Thread(target=f.remove_groups, args=[self])
        #             t.start()
        #         else:
        #             f.widgetStatus(self, ttk.NORMAL)
        #             tkt.call_nosync(self.messageBox,"ERROR!!", "You must select an OU!")
        #     else:
        #         f.widgetStatus(self, ttk.NORMAL)
        #         tkt.call_nosync(self.messageBox,"ERROR!!", "Your Settings are\
        #           incomplete\nfor this TAB!")
        # elif self.tabControl.index(self.tabControl.select()) == 3:
        #     f.widgetStatus(self, ttk.NORMAL)
        #     tkt.call_nosync(self.messageBox,"MAINTENANCE!!", "This Option is still\
        #       being\ndeveloped.")

    def resetProgress(self):
        self.progress["value"] = 0

    def handler(self):
        msg = "Ctrl-c was pressed. Exiting now... "
        print(msg)
        print("")
        self.destroy()

    def check(self):
        self.after(500, self.check)  # time in ms.

    def messageBox(self, txttitle, message):
        geo = self.winfo_geometry()
        posX = geo.split("+")[1]
        posY = geo.split("+")[2]
        W, H = 300, 100
        center_x = int(int(posX) + (self.W / 2) - (W / 2))
        center_y = int(int(posY) + (self.H / 2) - (H / 2))

        mb = ttk.Toplevel(title=txttitle)
        mb.geometry(f"{W}x{H}+{center_x}+{center_y}")
        mb.attributes("-toolwindow", True)
        mb.attributes("-topmost", True)

        messages = ttk.Label(
            mb, text=message, wraplength=250, justify=ttk.CENTER, style="color:black"
        )
        btn = ttk.Button(
            mb, text="OK", width=20, command=mb.destroy, style="bgcolor: black"
        )

        messages.pack(side="top", fill="x", expand=True, padx=10, pady=10)
        btn.pack(side="bottom", expand=True, padx=10, pady=10)


root = Main()


def thread_run(func):
    threading.Thread(target=func).start()


@thread_run
def func():
    @tkt.main(root)
    @tkt.current(root)
    def runthread():
        root.update()


root.mainloop()
