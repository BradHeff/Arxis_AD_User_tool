import datetime

# import threading
from signal import SIGINT, signal
import tkthread as tkt
import base64
import ttkbootstrap as ttk
from ttkbootstrap import Style
import Functions as f
from Gui import baseGUI

# Constants
WINDOW_TITLE = "Horizon AD Tool v{}"
DEFAULT_COMPANY = "Horizon"
DEFAULT_PASSWORD = "Horizon{}"
DEBUG_LDAP = "192.168.3.33"


class ADUnlocker(ttk.Window):
    """Main Class for AD Unlocker"""

    def __init__(self):
        super(ADUnlocker, self).__init__(themename="trinity-dark")
        self._initialize_attributes()
        self._setup_window()
        self._load_data()

    def _initialize_attributes(self):
        self.company = DEFAULT_COMPANY
        self.username = base64.b64decode(
            "Y249cHl0aG9uIHNlcnZpY2UgYWNjb3VudCxvdT1zZXJ2aWNlcyxvdT11c2VycyxvdT1ob3Jpem9uLGRjPWhvcml6b24sZGM9bG9jYWw="
        ).decode("UTF-8")
        self.password = str(base64.b64decode("Qm9vbURvZ2d5MTIz").decode("UTF-8"))

        self.isTeacher = False
        self.data = {}
        self.chkBtns = {}
        self.updateList = {}
        self.fullGroups = {}

        self.disName = []
        self.selItem = []
        self.selItem3 = []
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
        self.domains = {}
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

        self.date = datetime.datetime.now().date().strftime("%Y")

    def _setup_window(self):
        self.bind_all("<Control-c>", self.handler)
        signal(SIGINT, lambda x, y: print("") or self.handler())
        self.protocol("WM_DELETE_WINDOW", self.on_closing)

        baseGUI(self)

        f.ensure_directory_exists(f.settings_dir)

        self.title(WINDOW_TITLE.format(f.Version))

    def _load_data(self):
        f.safe_thread(self.fetchData)

    def fetchData(self):
        try:
            self.api_config = f.getStatus(self)
            # self.api_config = f.parseStatus(self, self.dataz)
            # print(wself.api_config)
            # Use get() method with default values to avoid KeyError
            self.server = (
                self.api_config.get("server", "") if not f.DEBUG else DEBUG_LDAP
            )
            self.jobTitle = self.api_config.get("title", [])
            self.disOU = self.api_config.get("expiredous", {})
            self.domains = self.api_config.get("domains", {})
            self.positions = self.api_config.get("positions", {})
            self.campus = self.api_config.get("campus", []).split(",")
            self.ou = self.api_config.get("userou", {})
            self.user_ou = self.api_config.get("users", "")
            self.domainName = self.api_config.get("domainname", [])
            self.groupOU = self.api_config.get("groupsou", {})
            self.groupPos = self.api_config.get("groups", {})
            self.positionsOU = self.api_config.get("positionsou", {})

            # Print for debugging
            # print("API Config:", self.api_config)

            self._setup_campus()
            self.comboLoad("")
        except Exception as e:
            print(f"Error fetching data: {e}")

    def on_closing(self):
        print("Thanks for using Arxis AD Tool!\n")
        self.destroy()
        self.quit()

    def alterButton(self, widget):
        index = self.tabControl.index(self.tabControl.select())
        if index == 0:
            self.btn_unlockAll.configure(text="Unlock All", state=ttk.NORMAL)
        elif index == 1:
            self.btn_unlockAll.configure(text="Create User", state=ttk.NORMAL)
            self.comboLoad("")
        elif index == 2:
            self.btn_unlockAll.configure(text="Update User", state=ttk.NORMAL)
            self.comboLoad("")
        else:
            print("ERROR!!! - Something went wrong!")

        if self.state:
            f.widgetStatusFailed(self, True)

    def selectItem(self, a):
        curItem = self.tree.focus()
        self.selItem = self.tree.item(curItem)["values"]

    def selectItem3(self, a):
        curItem = self.tree4.focus()
        if curItem:
            self.selItem3 = self.tree4.item(curItem)["values"]
            print(self.selItem3)
            self._options_clear()
            self.fetch_user_info_thread()

    def populate_user_fields(self, user_info):

        self.jobTitleEnt.delete(0, ttk.END)
        self.jobTitleEnt.insert(0, self.jobTitle[user_info])

        self.depEnt.delete(0, ttk.END)
        self.depEnt.insert(0, self.dep)

        self.orgCompEnt.delete(0, ttk.END)
        self.orgCompEnt.insert(0, self.org)

    def fetch_user_info_thread(self):
        def thread_function():
            try:
                self.entDomain["state"] = "normal"
                domain = str(self.updateList[self.selItem3[0]]["userPrincipalName"])
                print(domain)
                domain = f.clean_string(domain.split("@")[1])
                print(domain)
                self.entDomain.insert(0, domain)
            except Exception:
                pass
            try:
                self.entJobTitle.insert(
                    0,
                    str(self.updateList[self.selItem3[0]]["title"])
                    .strip()
                    .strip("{}")
                    .strip("[]")
                    .strip("'"),
                )
            except Exception:
                pass
            try:
                self.lname_entry.insert(0, self.updateList[self.selItem3[0]]["fname"])
            except Exception:
                pass
            try:
                self.fname_entry.insert(0, self.updateList[self.selItem3[0]]["lname"])
            except Exception:
                pass
            try:
                self.entSamname.insert(0, self.selItem3[0])
            except Exception:
                pass
            try:
                desc = self.updateList[self.selItem3[0]]["description"][0]
                self.entDesc.insert(
                    0, str(desc.strip().strip("{}").strip("[]").strip("'"))
                )
            except Exception:
                pass
            self.entDomain["state"] = "readonly"

        f.safe_thread(thread_function)

    def getCheck(self):
        grp = []
        for x in self.groups:
            grp.append(x)
        return grp

    def _options_clear(self):
        self.entDomain["state"] = "normal"
        self.entDesc.delete(0, "end")
        self.entJobTitle.delete(0, "end")
        self.entSamname.delete(0, "end")
        self.entDomain.delete(0, "end")
        self.lname_entry.delete(0, "end")
        self.fname_entry.delete(0, "end")
        self.entDomain["state"] = "readonly"

    def editOption(self):
        # self.clear_position_widgets(self.lbl_frame9)
        self.status["text"] = "Loading Users ...."
        self.updateList = f.listUsersEdit(self, self.positionsOU[self.var3.get()])
        self.tree4.delete(*self.tree4.get_children())
        self.progress["maximum"] = self.updateList.__len__()
        count = 0
        for i in self.updateList:
            count += 1
            self.progress["value"] = count
            name = str(self.updateList[i]["name"]).strip("{}").strip("[]").strip("'")
            ou = str(self.updateList[i]["ou"]).strip("{}").strip("[]").strip("'")
            self.tree4.insert(
                "",
                "end",
                values=(i, name, ou),
            )
        self.progress["value"] = 0
        self.status["text"] = "Idle..."

    def posSelectEdit(self):
        self._options_clear()
        print(self.var3.get())
        isBalak = "clare" not in self.EcampH.get().lower()
        if not isBalak:
            self._setup_clare_position(self.var3.get())
        else:
            self._setup_balaklava_position(self.var3.get())
        f.safe_thread(self.editOption)

    def posSelect(self):

        self.clear_group()
        self.dep = "Balaklava Campus"
        isBalak = "clare" not in self.campH.get().lower()

        self.dpass.delete(0, "end")
        self.dpass.insert(0, DEFAULT_PASSWORD.format(self.date))

        if not isBalak:
            self._setup_clare_position(self.var.get())
        else:
            self._setup_balaklava_position(self.var.get())

        self._setup_group_checkboxes()
        self.populate_user_fields(self.var.get())

    def _setup_clare_position(self, var):
        print(var)
        text = f"{var} - Clare {self.date}"
        if "Year" in var or "Found" in var:
            key = var.replace(" Clare", "").strip()
            self.posOU = f.safe_get(self.positionsOU, f"{key}-Clare")
        else:
            key = var.replace(" Clare", "").strip()
            self.posOU = f.safe_get(self.positionsOU, key)

        if not self.posOU:
            print(f"Error: No matching posOU found for key '{key}'")
        else:
            print(f"Updated posOU for Clare: {self.posOU}")

        self.groups = self.groupPos.get(key, [])
        self.dep = "Clare Campus"
        self.org = "Horizon Christian School Clare"
        self.desc.delete(0, "end")
        self.desc.insert(0, text)

    def _setup_balaklava_position(self, var):
        descDate = self.date
        print(var)
        key = var.strip()

        if key in self.positionsOU:
            self.posOU = self.positionsOU[key]
        else:
            print(f"Error: No matching posOU found for key '{key}' in Balaklava")
            self.posOU = ""

        if "Year" in var or "Found" in var:
            self.desc.delete(0, "end")
            self.desc.insert(0, f"{var} - {descDate}")
        else:
            self.desc.delete(0, "end")
            self.desc.insert(0, descDate)

        self.groups = self.groupPos.get(key, [])
        self.dep = "Balaklava Campus"
        self.org = "Horizon Christian School Balaklava"

    def _check_posiotion(self, position, value):
        if value == "E":
            if "Year" in position or "Found" in position:
                return True
            if "ESO" in position or "Student Support" in position:
                return True
            if "Admin" in position and "Temp" not in position:
                return True
        return False

    def _setup_group_checkboxes(self):
        style = Style()
        self.checkCount = 0
        self.checkRow = 0
        for x in self.groups:
            gn = x.split(",")[0].replace("CN=", "")
            self.chkBtns[gn] = ttk.IntVar()
            self.chkBtns[gn].set(1)

            cBtnY = ttk.Label(self.lbl_frame2, text=gn)
            cBtnY.configure(
                background=style.colors.primary, foreground=style.colors.bg, padding=10
            )
            cBtnY.grid(
                row=self.checkRow, column=self.checkCount, sticky="nsew", padx=5, pady=5
            )

            cBtn = ttk.Checkbutton(
                self.lbl_frame2, variable=self.chkBtns[gn], style="success-round-toggle"
            )
            cBtn.grid(
                row=self.checkRow,
                column=self.checkCount + 1,
                sticky="nsew",
                padx=5,
                pady=5,
            )

            self.checkCount += 2
            if self.checkCount > 3:
                self.checkCount = 0
                self.checkRow += 1

    def _setup_campus(self):
        if self.campus.__len__() > 0:
            print(self.campus)
            # self.clear_campus(self.frameC)
            # self.clear_campus(self.frameG)
            counter = 1
            for x in self.campus:
                balak = ttk.Radiobutton(
                    self.lbl_frameC,
                    text=x,
                    variable=self.campH,
                    value=x,
                    command=lambda: self.comboSelect("H"),
                )
                balak_edit = ttk.Radiobutton(
                    self.lbl_frameG,
                    text=x,
                    variable=self.EcampH,
                    value=x,
                    command=lambda: self.comboSelect("E"),
                )
                # balak_move = ttk.Radiobutton(
                #     self.lbl_frameF,
                #     text=x,
                #     variable=self.McampH,
                #     value=x,
                #     command=lambda: self.comboSelect("M"),
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
                #     command=lambda: self.comboSelect("D"),
                # )
                if counter == 1:
                    balak.pack(side="left", fill="y", expand=True, padx=10, pady=10)
                    balak_edit.pack(
                        side="left", fill="y", expand=True, padx=10, pady=10
                    )
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
                    balak.pack(side="right", fill="y", expand=True, padx=10, pady=10)
                    balak_edit.pack(
                        side="right", fill="y", expand=True, padx=10, pady=10
                    )
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

    def clear_position_widgets(self, lbl_positions):
        [widget.destroy() for widget in lbl_positions.grid_slaves()]

    def clear_group(self):
        [widget.destroy() for widget in self.lbl_frame2.grid_slaves()]

    def clear_campus(self, lbl_positions):
        [widget.destroy() for widget in lbl_positions.grid_slaves()]

    def comboSelect(self, value="H"):
        f.safe_thread(self.comboLoad, value)

    def comboLoad(self, value):  # noqa
        self.status["text"] = "Loading..."
        progress_value = 1
        if value == "H":
            self.clear_position_widgets(self.lbl_frame)
            self.clear_group()
            self.tree.delete(*self.tree.get_children())

            self.desc.delete(0, "end")
            self.dpass.delete(0, "end")
            self.jobTitleEnt.delete(0, "end")
            self.depEnt.delete(0, "end")
            self.orgCompEnt.delete(0, "end")
            self.desc.insert(0, self.date)

            for x in self.disOU:
                self.disName.append(x)
        elif value == "E":
            self.clear_position_widgets(self.lbl_frame9)
            self.tree4.delete(*self.tree4.get_children())
            self.entDomain["state"] = "normal"
            self.entDesc.delete(0, "end")
            self.entJobTitle.delete(0, "end")
            self.entSamname.delete(0, "end")
            self.entDomain.delete(0, "end")
            self.lname_entry.delete(0, "end")
            self.fname_entry.delete(0, "end")
            self.entDomain["state"] = "readonly"

        if not self.positions.__len__() <= 0:
            try:
                row = count = 0
                # row2 = count2 = 0

                self.progress["maximum"] = float(self.positions.__len__())

                self.var = ttk.StringVar(None, "1")
                self.var3 = ttk.StringVar(None, "1")
                for position_group, positions in self.positions.items():
                    for position in positions:
                        self.progress["value"] = progress_value
                        if value == "H" or value == "":
                            position_radio_button = ttk.Radiobutton(
                                self.lbl_frame,
                                text=position,
                                variable=self.var,
                                command=self.posSelect,
                                value=position,
                            )
                            position_radio_button.grid(
                                row=row, column=count, padx=10, pady=10
                            )
                        if value == "E" or value == "":
                            isClarePosition = self._check_posiotion(position, value)
                            edit_position_radio_button = ttk.Radiobutton(
                                self.lbl_frame9,
                                text=(
                                    position + " Clare" if isClarePosition else position
                                ),
                                variable=self.var3,
                                command=self.posSelectEdit,
                                value=(
                                    position + " Clare" if isClarePosition else position
                                ),
                            )

                            edit_position_radio_button.grid(
                                row=row, column=count, padx=10, pady=10
                            )

                        progress_value += 1
                        count += 1
                        if count > 3:
                            count = 0
                            row += 1

            except Exception as error:
                print(f"Error populating position selection: {error}")

        if hasattr(self, "domains") and isinstance(self.domains, dict):
            try:
                self.progress["value"] = 60
                self.pdomains = self.domains.get("Primary", [])
                print(self.domains)
                if self.pdomains:
                    self.combo_domain["values"] = self.pdomains
                    self.primary_domain.set("horizon.sa.edu.au")
                else:
                    # print("Warning: No primary domains found.")
                    self.combo_domain["values"] = ["horizon.sa.edu.au"]  # Default value
                    self.primary_domain.set("horizon.sa.edu.au")
                    # print(self.primary_domain.get())

            except Exception as e:
                print(f"ERROR DOMAIN: {e}")
                self.combo_domain["values"] = ["horizon.sa.edu.au"]  # Default value
                self.primary_domain.set("horizon.sa.edu.au")
        else:
            print("Warning: self.domains is not a dictionary or doesn't exist.")
            self.combo_domain["values"] = ["horizon.sa.edu.au"]  # Default value
            self.primary_domain.set("horizon.sa.edu.au")

        if not self.groupOU.__len__() <= 3:
            self.progress["value"] = progress_value
            progress_value = 0
        self.progress["value"] = progress_value
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

        f.safe_thread(f.resetPassword, self, self.selItem[2], newPass)

    def loadUsers(self):
        f.widgetStatus(self, ttk.DISABLED)
        self.tree.delete(*self.tree.get_children())
        f.safe_thread(self.loads)

    def loads(self):
        try:
            self.status["text"] = "Searching locked users ..."
            locked = f.listLocked(self)

            if not isinstance(locked, dict):
                raise ValueError("Expected a dictionary from listLocked function")

            if len(locked) <= 0:
                f.widgetStatus(self, ttk.NORMAL)
                self.status["text"] = "Idle..."
                return

            # Debugging: Print the locked users dictionary
            print("Locked users:", locked)

            for user, details in locked.items():
                print(f"User: {user}, Details: {details}")
                # Ensure details is a dictionary
                if not isinstance(details, dict):
                    raise ValueError(
                        f"Expected a dictionary for user details, got {type(details)}"
                    )

                # Add user to the tree view (assuming self.tree is a ttk.Treeview)
                self.tree.insert(
                    "", "end", text=user, values=(user, details["name"], details["ou"])
                )

            f.widgetStatus(self, ttk.NORMAL)
            self.status["text"] = "Idle..."
        except ValueError as ve:
            print(f"ValueError: {ve}")
            f.widgetStatus(self, ttk.NORMAL)
            self.status["text"] = "Idle..."
        except Exception as e:
            print(f"General Exception: {e}")
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
        f.safe_thread(self._unlock)

    def _unlock(self):
        f.unlockUser(self, self.selItem[2])
        selected_item = self.tree.selection()[0]
        self.tree.delete(selected_item)
        self.selItem = []
        self.status["text"] = "Idle..."
        tkt.call_nosync(f.Toast, "COMPLETE!", "Users Unlocked!", "happy")

    def global_button(self):
        f.widgetStatus(self, ttk.DISABLED)

        index = self.tabControl.index(self.tabControl.select())
        if index == 0:
            self._handle_unlock_all()
        elif index == 1:
            self._handle_create_user()
        elif index == 2:
            self._handle_update_user()
        else:
            print("")

    def _handle_unlock_all(self):
        if not self.tree.get_children():
            f.widgetStatus(self, ttk.NORMAL)
            tkt.call_nosync(self.messageBox, "ERROR!!", "List cannot be empty!")
            return

        self.data = {
            self.tree.item(line)["values"][0]: {
                "name": self.tree.item(line)["values"][1],
                "ou": self.tree.item(line)["values"][2],
            }
            for line in self.tree.get_children()
        }
        maxs = len(self.tree.get_children())
        self.progress["maximum"] = float(maxs)
        self.all = maxs
        f.safe_thread(f.unlockAll, self, self.data)

    def _handle_create_user(self):
        if not self._validate_create_user_input():
            return

        data = self._prepare_create_user_data()
        try:
            f.safe_thread(f.createUser, self, data)
        except Exception as e:
            print(f"ERROR: {e}")

    def _handle_update_user(self):
        if not self._validate_update_user_input():
            return
        self.progress["value"] = 30
        self.status["text"] = "Gathering User Data..."
        data = self._prepare_update_user_data()

        # print(data)
        f.safe_thread(f.update_user, self, data)

    def _validate_create_user_input(self):
        if self.fname.get().__len__() <= 1 and self.lname.get().__len__() <= 1:
            self.messageBox("ERROR!!", "Firstname and Lastname cannot be empty!")
            return False
        if self.dpass.get().__len__() < 8:
            self.messageBox(
                "ERROR!!", "Password must be at least 8 characters or empty!"
            )
            return False
        return True

    def _validate_update_user_input(self):
        if self.entPass.get().__len__() < 8 and self.entPass.get().__len__() != 0:
            self.messageBox(
                "ERROR!!", "Password must be at least 8 characters or empty!"
            )
            return False
        if not self.tree4.get_children():
            self.messageBox("ERROR!!", "Must select a position")
            return False
        if not self.selItem3:
            self.messageBox("ERROR!!", "Must select a user!")
            return False
        if len(self.fname_entry.get()) <= 1:
            self.messageBox("ERROR!!", "First Name cannot be empty!")
            return False
        return True

    def _prepare_create_user_data(self):
        if "flast" in self.samFormat.get():
            samname = "".join([self.fname.get().strip()[0:1], self.lname.get().strip()])
        elif "firstlast" in self.samFormat.get():
            samname = "".join([self.fname.get().strip(), self.lname.get().strip()])
        else:
            samname = "".join([self.fname.get().strip(), ".", self.lname.get().strip()])

        data = {
            "login": samname.lower(),
            "first": self.fname.get().capitalize(),
            "last": self.lname.get().capitalize(),
            "domain": self.primary_domain.get(),
            "description": self.desc.get(),
            "title": self.jobTitleEnt.get(),
            "password": self.dpass.get(),
            "department": self.depEnt.get(),
            "company": self.orgCompEnt.get(),
            "proxy": (
                self.domains["Secondary"] if len(self.domains["Secondary"]) > 3 else ""
            ),
            "groups": self.groups,
        }

        return data

    def _prepare_update_user_data(self):
        data = {
            "login": self.entSamname.get(),
            "first": self.fname_entry.get().capitalize(),
            "last": self.lname_entry.get().capitalize(),
            "domain": self.entDomain.get(),
            "description": self.entDesc.get(),
            "title": self.entJobTitle.get(),
            "ou": self.updateList[self.selItem3[0]]["ou"],
            "password": self.entPass.get(),
        }

        if self.updateList[self.selItem3[0]]["proxyAddresses"] is not None:
            for x in self.updateList[self.selItem3[0]]["proxyAddresses"]:
                if self.entDomain.get() not in x and len(x) > 5:
                    data["proxy"] = x.split("@")[1]
                    break
            else:
                data["proxy"] = (
                    self.domains["Secondary"]
                    if len(self.domains["Secondary"]) > 3
                    else ""
                )
        else:
            data["proxy"] = (
                self.domains["Secondary"] if len(self.domains["Secondary"]) > 3 else ""
            )

        return data

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


if __name__ == "__main__":
    root = ADUnlocker()
    root.mainloop()
