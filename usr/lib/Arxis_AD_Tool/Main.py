import datetime
import threading
from signal import SIGINT, signal
import tkthread as tkt
import base64
import ttkbootstrap as ttk
from ttkbootstrap import Style
import Functions as f
import Gui
from ttkbootstrap.dialogs.dialogs import Messagebox
import webbrowser


class Mainz(ttk.Window):
    """Main Class for AD Unlocker"""

    def __init__(self):
        super(Mainz, self).__init__(themename="trinity-dark")
        self.bind_all("<Control-c>", self.handler)
        signal(SIGINT, lambda x, y: print("") or self.handler())
        # self.after(500, self.check)
        self.protocol("WM_DELETE_WINDOW", self.on_closing)

        self.company = "Horizon"
        self.username = base64.b64decode(
            "Y249cHl0aG9uIHNlcnZpY2UgYWNjb3VudCxvdT1zZXJ2aWNlcyxvdT11c2VycyxvdT1ob3Jpem9uLGRjPWhvcml6b24sZGM9bG9jYWw="
        ).decode("UTF-8")
        self.password = str(base64.b64decode("Qm9vbURvZ2d5MTIz").decode("UTF-8"))

        self.isTeacher = False
        self.data = dict()
        self.chkBtns = dict()
        self.updateList = dict()
        self.fullGroups = dict()

        self.disName = []
        self.selItem = []
        self.groups = []

        self.posOU = ""
        self.samFormat = ""
        self.department = ""

        self.servs = False
        self.isRunning = False
        self.loaded = False
        self.isExit = False
        self.data_file = False
        self.state = True

        self.checkCount = 0
        self.checkRow = 0

        self.load = ttk.BooleanVar(self, False)
        self.comp = "Select Company"

        self.dataz = {}
        self.updatez = {}
        self.api_config = {}
        self.api_updates = {}
        self.server = ""
        self.domains = []
        self.jobTitle = []
        self.disOU = {}
        self.positions = {}
        self.pdomains = {}
        self.campus = []
        self.ou = {}
        self.domainName = []
        self.groupOU = {}
        self.groupPos = {}
        self.positionsOU = {}

        t = threading.Thread(target=self.fetchData)
        t.daemon = True
        t.start()

        currentDateTime = datetime.datetime.now()
        date = currentDateTime.date()
        self.date = date.strftime("%Y")

        self.title("".join(["Arxis AD Tool v", f.Version[4 : f.Version.__len__()]]))

        scaling = self.tk.call("tk", "scaling")  # Get current scaling
        print(f"Current scaling: {scaling}")
        dpi = self.winfo_fpixels("1i")  # Get DPI
        print(f"Detected DPI: {dpi}")
        self.dpi = dpi
        Gui.baseGUI(self)
        Gui.adjust_scaling(self)

    def setLoad(self):
        print(f"Load state: {self.load.get()}")

    def fetchData(self):
        self.dataz = f.getStatus(self)
        self.updatez = f.getUpdate(self)
        self.api_config = f.parseStatus(self, self.dataz)
        self.api_updates = f.parseStatus(self, self.updatez)
        if f.DEBUG:
            self.server = "192.168.3.34"
        else:
            self.server = self.api_config["server"]  # f.getServer(self, self.company)
        print(self.server)
        self.domains = self.api_config["domains"]
        self.jobTitle = self.api_config["title"]
        self.disOU = self.api_config["expiredous"]
        self.positions = self.api_config["positions"]
        self.pdomains = self.api_config["domains"]
        self.campus = self.api_config["campus"]
        self.ou = self.api_config["userou"]
        self.domainName = self.api_config["domainname"]
        self.groupOU = self.api_config["groupsou"]
        self.groupPos = self.api_config["groups"]
        self.positionsOU = self.api_config["positionsou"]
        self.comboSelect("", "H")

    def on_closing(self):
        print("Thanks for using Arxis AD Tool!\n")
        self.destroy()
        self.quit()

    def alterButton(self, widget):
        index = self.tabControl.index(self.tabControl.select())
        if index == 0:
            self.btn_unlockAll.configure(text="Unlock All", state=ttk.NORMAL)
            if self.state:
                f.widgetStatusFailed(self, True)
        elif index == 1:
            self.btn_unlockAll.configure(text="Create User", state=ttk.NORMAL)
            if self.state:
                f.widgetStatusFailed(self, True)
            else:
                if self.state:
                    f.widgetStatusFailed(self, True)
        elif index == 2:
            self.btn_unlockAll.configure(text="Edit User", state=ttk.NORMAL)
            if self.state:
                f.widgetStatusFailed(self, True)
            else:
                if self.state:
                    f.widgetStatusFailed(self, True)
        else:
            print("ERROR!!! - Something went wrong!")
            # f.Toast("ERROR!!!", "Something went wrong!", "sad")

    def selectItem(self, a):
        curItem = self.tree.focus()
        self.selItem = self.tree.item(curItem)["values"]

    def selectItem3(self, a):
        curItem = self.tree4.focus()
        self.selItem3 = self.tree4.item(curItem)["values"]

    def getCheck(self):
        grp = []
        for x in self.groups:
            grp.append(x)
        return grp

    def posSelect(self):
        self.clear_group()
        camp = "Balaklava"
        self.dep = "Balaklava Campus"
        isBalak = False
        position_key = self.var.get()
        capitalized_position_key = position_key.lower()
        self.dpass.insert(
            0, "".join(["Horizon", datetime.datetime.now().strftime("%Y")])
        )
        if self.campH.get() == 0:
            isBalak = False
        else:
            isBalak = True
        print(isBalak)
        if not isBalak:
            print(self.positionsOU)
            if (
                "Year".lower() in capitalized_position_key
                or "Found".lower() in capitalized_position_key
            ):
                self.posOU = self.positionsOU[capitalized_position_key + "-clare"]
            elif (
                "ESO" in capitalized_position_key
                or "Student Support" in capitalized_position_key
            ):
                self.posOU = self.positionsOU["Student Support Clare".lower()]
            elif (
                "Admin" in capitalized_position_key
                and "Temp" not in capitalized_position_key
            ):
                self.posOU = self.positionsOU[
                    capitalized_position_key + " Clare".lower()
                ]
            self.groups = self.groupPos[capitalized_position_key]
            descDate = f"{self.date} Clare"
            camp = "Clare"
            self.dep = "Clare Campus"
            print(self.posOU)
        else:
            descDate = self.date
            if (
                "Year" in capitalized_position_key
                or "Found" in capitalized_position_key
            ):
                self.posOU = self.positionsOU[capitalized_position_key]
                self.desc.delete(0, "end")
                self.desc.insert(0, f"{capitalized_position_key} - {descDate}")
            else:
                self.posOU = self.positionsOU[capitalized_position_key]
                self.desc.delete(0, "end")
                self.desc.insert(0, descDate)

            self.groups = self.groupPos[capitalized_position_key]
        style = Style()
        self.checkCount = 0
        self.checkRow = 0
        print(self.groups)
        print(self.posOU)
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
            if self.checkCount > 2:
                self.checkCount = 0
                self.checkRow += 1

        if not self.jobTitle.__len__() <= 3:
            try:
                self.jobTitleEnt.delete(0, "end")
                self.jobTitleEnt.insert(0, self.jobTitle[capitalized_position_key])
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

    def comboSelect(self, widget, value="H"):
        if "camp" not in str(widget):
            if self.campus.split(",")[0].__len__() > 0:
                #     .__len__().__len__() <= 0:
                counter = 1
                for x in self.campus.split(","):
                    balak = ttk.Radiobutton(
                        self.lbl_frameC,
                        text=x,
                        variable=self.campH,
                        value=counter,
                        command=lambda: self.comboSelect("camp", "H"),
                    )
                    # balak_edit = ttk.Radiobutton(
                    #     self.lbl_frameG,
                    #     text=x,
                    #     variable=self.EcampH,
                    #     value=x,
                    #     command=lambda: self.comboSelect("camp", "E"),
                    # )
                    # balak_move = ttk.Radiobutton(
                    #     self.lbl_frameF,
                    #     text=x,
                    #     variable=self.McampH,
                    #     value=x,
                    #     command=lambda: self.comboSelect("camp", "M"),
                    # )
                    # balak_move2 = ttk.Radiobutton(
                    #     self.lbl_frameF2,
                    #     text=x,
                    #     variable=self.McampH2,
                    #     value=x,
                    # )
                    # balakB = ttk.Radiobutton(
                    #     self.lbl_frameC6,
                    #     text=x,
                    #     variable=self.McampH6,
                    #     value=x,
                    #     command=lambda: self.comboSelect("camp", "D"),
                    # )
                    if counter == 1:
                        balak.pack(side="left", fill="y", expand=True, padx=10, pady=10)
                        # balak_edit.pack(
                        #     side="left", fill="y", expand=True, padx=10, pady=10
                        # )
                        # balak_move.pack(
                        #     side="left", fill="y", expand=True, padx=10, pady=10
                        # )
                        # balak_move2.pack(
                        #     side="left", fill="y", expand=True, padx=10, pady=10
                        # )
                        # balakB.pack(
                        #     side="left", fill="y", expand=True, padx=10, pady=10
                        # )
                    else:
                        balak.pack(
                            side="right", fill="y", expand=True, padx=10, pady=10
                        )
                        # balak_edit.pack(
                        #     side="right", fill="y", expand=True, padx=10, pady=10
                        # )
                        # balak_move.pack(
                        #     side="right", fill="y", expand=True, padx=10, pady=10
                        # )
                        # balak_move2.pack(
                        #     side="right", fill="y", expand=True, padx=10, pady=10
                        # )
                        # balakB.pack(
                        #     side="right", fill="y", expand=True, padx=10, pady=10
                        # )
                    counter -= 1

        t = threading.Thread(target=self.comboLoad, args=(value))
        t.daemon = True
        t.start()

    def comboLoad(self, value):  # noqa
        self.status["text"] = "Loading..."
        self.clear_pos()
        self.clear_group()
        self.tree.delete(*self.tree.get_children())
        self.tree4.delete(*self.tree4.get_children())
        self.desc.delete(0, "end")
        self.dpass.delete(0, "end")
        self.jobTitleEnt.delete(0, "end")
        self.depEnt.delete(0, "end")
        self.orgCompEnt.delete(0, "end")
        self.desc.insert(0, self.date)

        for x in self.disOU:
            self.disName.append(x)

        if not self.positions.__len__() <= 0:
            try:
                self.progress["value"] = 20
                count = 0
                row = 0
                # count2 = 0
                # row2 = 0
                # count3 = 0
                # row3 = 0
                count4 = 0
                row4 = 0

                self.var = ttk.StringVar(None, "1")
                self.var4 = ttk.StringVar(None, "1")
                for x in self.positions:
                    for y in self.positions[x]:
                        prog = 1
                        self.progress["maximum"] = float(self.positions.__len__())
                        self.progress["value"] = prog

                        rbtn = ttk.Radiobutton(
                            self.lbl_frame,
                            text=y,
                            variable=self.var,
                            command=self.posSelect,
                            value=y,
                        )
                        rbtn.grid(row=row, column=count, padx=10, pady=10)
                        rbtn.selection_clear()

                        rbtn4 = ttk.Radiobutton(
                            self.lbl_frame9,
                            text=y,
                            variable=self.var4,
                            command=self.posSelect,
                            value=y,
                        )
                        rbtn4.grid(row=row4, column=count4, padx=10, pady=10)
                        rbtn4.selection_clear()

                        count += 1
                        count4 += 1
                        if count > 3:
                            count = 0
                            row += 1
                        if count4 > 2:
                            count4 = 0
                            row4 += 1
                        # else:
                        #     rbtn2 = ttk.Radiobutton(
                        #         self.lbl_frame4,
                        #         text=y,
                        #         variable=self.var,
                        #         command=lambda: self.posSelect(value),
                        #         value=y,
                        #     )
                        #     rbtn2.grid(row=row2, column=count2, padx=10, pady=10)
                        #     rbtn2.selection_clear()

                        #     rbtn3 = ttk.Radiobutton(
                        #         self.lbl_frame10,
                        #         text=y,
                        #         variable=self.var4,
                        #         command=lambda: self.posSelect(value),
                        #         value=y,
                        #     )
                        #     rbtn3.grid(row=row3, column=count3, padx=10, pady=10)
                        #     rbtn3.selection_clear()

                        #     count2 += 1
                        #     count3 += 1
                        #     if count2 > 6:
                        #         count2 = 0
                        #         row2 += 1
                        #     if count3 > 3:
                        #         count3 = 0
                        #         row3 += 1
                        prog += 1
            except Exception as e:
                print("ERROR POS")
                print(e)

        if not self.domains["primary"].__len__() <= 0:
            try:
                self.progress["value"] = 60
                self.pdomains = self.domains["primary"]
                self.combo_domain["values"] = self.pdomains
                self.primary_domain.set("horizon.sa.edu.au")
            except Exception as e:
                print("ERROR DOMAIN")
                print(e)
                pass

        if not self.groupOU.__len__() <= 3:
            self.progress["value"] = 80
            prog = 1
        self.progress["value"] = 0
        self.status["text"] = "Idle..."
        if f.path.isfile(f.settings_dir + "Config.ini") and not self.loaded:
            f.loadConfig(self)

    def resetPass(self):
        if self.selItem.__len__() <= 0:
            tkt.call_nosync(self.messageBox, "ERROR!!", "Must select a user!", "error")
            return
        if self.passBox.get().__len__() < 8:
            tkt.call_nosync(self.messageBox, "ERROR!!", "Password Too Short!", "error")
            return
        f.widgetStatus(self, ttk.DISABLED)
        newPass = self.passBox.get()

        t = threading.Thread(
            target=f.resetPassword, args=[self, self.selItem[2], newPass]
        )
        t.daemon = True
        t.start()

    def loadUsers(self):
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
            print("ERROR LOAD USERS, ", str(e))
            tkt.call_nosync(
                self.messageBox, "Error", "An error occurred, " + str(e), "error"
            )
            tkt.call_nosync(f.Toast, "ERROR!", "An error occurred", "angry")

        f.widgetStatus(self, ttk.NORMAL)
        self.status["text"] = "Idle..."

    def unlockUsers(self):
        if self.tree.get_children() == ():
            tkt.call_nosync(
                self.messageBox, "ERROR!!", "List cannot be empty!", "error"
            )
            return

        if self.selItem.__len__() <= 0:
            tkt.call_nosync(self.messageBox, "ERROR!!", "Must select a user!", "error")
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
        index = self.tabControl.index(self.tabControl.select())
        if index == 0:
            if self.tree.get_children() == ():
                f.widgetStatus(self, ttk.NORMAL)

                tkt.call_nosync(
                    self.messageBox, "ERROR!!", "List cannot be empty!", "error"
                )
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
        elif index == 1:
            f.widgetStatus(self, ttk.DISABLED)
            if self.fname.get().__len__() >= 2 and self.lname.get().__len__() >= 2:
                if self.dpass.get().__len__() < 8:
                    f.widgetStatus(self, ttk.NORMAL)

                    tkt.call_nosync(
                        self.messageBox,
                        "ERROR!!",
                        "Must enter Password\n\
                    or password 8 characters min",
                        "error",
                    )
                    return
                if "Select" in self.primary_domain.get():
                    f.widgetStatus(self, ttk.NORMAL)
                    self.status["text"] = "Idle..."

                    tkt.call_nosync(
                        self.messageBox,
                        "ERROR!!",
                        "You must select domain\n\
                                    HomeDrive and HomePath",
                        "error",
                    )
                    return
                self.progress["value"] = 10
                self.status["text"] = "Rebuilding groups..."
                groups = self.getCheck()
                self.status["text"] = "Setting login name..."
                index2 = self.samFormat.get()
                if index2 == "flastname":
                    samname = "".join(
                        [
                            self.fname.get().strip()[0:1],
                            self.lname.get().strip(),
                        ]
                    )
                elif index2 == "firstlastname":
                    samname = "".join(
                        [self.fname.get().strip(), self.lname.get().strip()]
                    )
                else:
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
                data["proxy"] = self.domains["secondary"]
                data["groups"] = groups
                data["description"] = self.desc.get()
                data["title"] = self.jobTitleEnt.get()
                data["department"] = self.depEnt.get()
                data["company"] = self.orgCompEnt.get()
                self.progress["value"] = 20
                try:
                    t = threading.Thread(target=f.createUser, args=(self, data))
                    t.daemon = True
                    t.start()
                except Exception as e:
                    print(f"ERROR: {e}")
            else:
                f.widgetStatus(self, ttk.NORMAL)

                tkt.call_nosync(
                    self.messageBox,
                    "ERROR!!",
                    "First and Lastname must\n\
                be filled!",
                    "error",
                )
        else:
            print("")

    def resetProgress(self):
        self.progress["value"] = 0

    def handler(self):
        msg = "Ctrl-c was pressed. Exiting now... "
        print(msg)
        print("")
        self.destroy()

    def messageBox(self, txttitle, message, typez):
        if typez == "info":
            Messagebox.show_info(
                message,
                title=txttitle,
                parent=self,
                alert=True,
            )
        elif typez == "warning":
            Messagebox.show_warning(
                message,
                title=txttitle,
                parent=self,
                alert=True,
            )
        elif typez == "question":
            return Messagebox.show_question(
                message,
                title=txttitle,
                parent=self,
                alert=True,
            )
        elif typez == "error":
            Messagebox.show_error(
                message,
                title=txttitle,
                parent=self,
                alert=True,
            )
        else:
            Messagebox.ok(
                message,
                title=txttitle,
                parent=self,
                alert=False,
            )

    def navGithub(self):
        webbrowser.open_new_tab("https://github.com/BradHeff/Arxis-Pentester")
        self.logger.info("Navigated to GitHub repository")

    def aboutBox(self):
        Messagebox.show_info(
            title="About Arxis AD Tool",
            message=(
                "Arxis AD Tool is a comprehensive application designed for Active Directory management.\n\n"
                "Purpose:\n"
                "The application helps create users, search for locked accounts, and list them for unlocking.\n\n"
                f"Version: {f.Version}\n"
                "Company: Arxis Security Solutions\n"
                "Website: https://www.arxis.com.au\n"
            ),
        )
        print("About box shown")


if __name__ == "__main__":
    root = Mainz()
    root.mainloop()
