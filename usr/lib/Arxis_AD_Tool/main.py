# import datetime
from concurrent.futures import ThreadPoolExecutor
from signal import SIGINT, signal
import numpy as np
import tkthread as tkt
import base64
import ttkbootstrap as ttk

# from ttkbootstrap import Style
import Functions as func
import gui as Gui
from ttkbootstrap.dialogs.dialogs import Messagebox

# import webbrowser


class ActiveDirectoryTool(ttk.Window):
    """Main Class for Active Directory Management Tool"""

    def __init__(self):
        super(ActiveDirectoryTool, self).__init__(themename="trinity-dark")
        self.executor = ThreadPoolExecutor(
            max_workers=5
        )  # Thread pool for threading tasks
        self.bind_all("<Control-c>", self.exit_handler)
        signal(SIGINT, lambda x, y: print("") or self.exit_handler())
        self.protocol("WM_DELETE_WINDOW", self.on_application_close)

        # Initialize attributes
        self.status = ttk.StringVar(value="Idle...")
        self.progress = ttk.DoubleVar(value=0.0)

        # Company and Credentials
        self.company_name = "Horizon"
        self.username = base64.b64decode(
            "Y249cHl0aG9uIHNlcnZpY2UgYWNjb3VudCxvdT1zZXJ2aWNlcyxvdT11c2VycyxvdT1ob3Jpem9uLGRjPWhvcml6b24sZGM9bG9jYWw="
        ).decode("UTF-8")
        self.password = str(base64.b64decode("Qm9vbURvZ2d5MTIz").decode("UTF-8"))

        # User Interaction Data
        self.primary_domain = ttk.StringVar(value="Select Domain")
        self.domains = {"primary": [], "secondary": []}
        self.selItem = []  # Placeholder for selected item in treeview

        # Data Structures
        self.is_teacher = False
        self.ad_data = {}
        self.check_buttons = {}
        self.update_list = {}
        self.group_list = {}
        self.display_names = np.array([])
        self.selected_items = np.array([])
        self.groups = np.array([])
        self.api_config = {}
        self.api_updates = {}
        self.server_address = ""
        self.domain_list = np.array([])
        self.job_titles = np.array([])
        self.campus_list = np.array([])
        self.position_mappings = {}

        # Initialize Scaling and DPI detection
        scaling = self.tk.call("tk", "scaling")  # Get current scaling
        print(f"Current scaling: {scaling}")
        dpi = self.winfo_fpixels("1i")  # Get DPI
        print(f"Detected DPI: {dpi}")
        self.dpi = dpi

        # Initialize UI
        Gui.initialize_base_gui(self)
        Gui.adjust_scaling(self)
        func.verify_configuration(self)

        # Load initial data asynchronously
        self.executor.submit(self.load_initial_data)

    def load_initial_data(self):
        """Fetch initial data for application setup."""
        try:
            self.ad_data = func.get_status(self)
            self.update_list = func.get_update(self)
            self.api_config = func.parse_status(self, self.ad_data)
            self.api_updates = func.parse_status(self, self.update_list)
            self.server_address = self.api_config.get("server", "default_server")
            self.domain_list = np.array(self.api_config.get("domains", []))
            self.job_titles = np.array(self.api_config.get("title", []))
            self.campus_list = np.array(self.api_config.get("campus", []))
            self.position_mappings = self.api_config.get("positions", {})

            self.load_domains()
        except Exception as error:
            print(f"Error during data loading: {error}")
            self.status.set("Error loading data.")

    def handle_selected_domain(self):
        """
        Handle domain selection change.
        """
        selected_domain = self.primary_domain.get()
        if selected_domain == "Select Domain":
            tkt.call_nosync(
                self.messageBox, "ERROR!!", "You must select a valid domain!", "error"
            )
        else:
            print(f"Selected domain: {selected_domain}")
            # Continue processing with the selected domain

    def load_domains(self):
        """
        Populate the domain combobox with available domains.
        """
        try:
            # Populate domains dynamically
            self.domains["primary"] = (
                self.domain_list.tolist()
                if self.domain_list.size > 0
                else ["Select Domain"]
            )
            self.domains["secondary"] = "horizonsa.onmicrosoft.com"

            # Update the combobox with primary domains
            self.combo_domain["values"] = self.domains["primary"]
            self.primary_domain.set(
                self.domains["primary"][0]
                if self.domains["primary"]
                else "Select Domain"
            )
        except Exception as error:
            print(f"Error loading domains: {error}")
            self.primary_domain.set("Select Domain")

    def combo_select(self, selected_widget, selected_value="H"):
        """
        Handle selection in comboboxes or radio buttons and populate related widgets.
        """
        try:
            # Clear existing widgets in dynamic frames
            self.clear_campus_widgets()
            self.clear_position_widgets()
            self.clear_group_widgets()

            if "camp" not in str(selected_widget):
                if self.campus_list.size > 0:
                    self.populate_campus_selection()

            # Load data dynamically in a new thread
            self.executor.submit(self.combo_load, selected_value)
        except Exception as error:
            print(f"Error in combo_select: {error}")

    def combo_load(self, selected_value):  # noqa
        """
        Dynamically load and populate data based on the selected value.
        """
        self.status.set("Loading...")
        try:
            # Clear existing widgets and reset UI elements
            self.clear_position_widgets()
            self.clear_group_widgets()
            self.tree_locked_users.delete(*self.tree_locked_users.get_children())
            self.description_entry.delete(0, "end")
            self.password_entry.delete(0, "end")
            self.job_title_entry.delete(0, "end")
            self.department_entry.delete(0, "end")
            self.organization_entry.delete(0, "end")
            self.description_entry.insert(0, self.current_year)

            # Populate display names
            self.display_names = np.array(list(self.ad_data.keys()))

            # Populate positions
            if self.position_mappings:
                self.populate_position_selection()

            # Populate domains
            if "primary" in self.domain_list:
                self.primary_domains = self.domain_list.get("primary", [])
                self.combo_domain["values"] = self.primary_domains
                self.primary_domain.set("horizon.sa.edu.au")

            self.status.set("Idle...")
        except Exception as error:
            print(f"Error in combo_load: {error}")
            self.status.set("Error loading data.")

    def populate_campus_selection(self):
        """
        Populate campus selection dynamically in the GUI.
        """
        counter = 1
        for campus in self.campus_list:
            try:
                balak_radio_button = ttk.Radiobutton(
                    self.lbl_frameC,
                    text=campus,
                    variable=self.campus_selection,
                    value=counter,
                    command=lambda: self.combo_select("camp", "H"),
                )
                clare_radio_button = ttk.Radiobutton(
                    self.lbl_frameG,
                    text=campus,
                    variable=self.EcampH,
                    value=counter,
                    command=lambda: self.combo_select("camp", "E"),
                )

                if counter == 1:
                    balak_radio_button.pack(
                        side="left", fill="y", expand=True, padx=10, pady=10
                    )
                    clare_radio_button.pack(
                        side="left", fill="y", expand=True, padx=10, pady=10
                    )
                else:
                    balak_radio_button.pack(
                        side="right", fill="y", expand=True, padx=10, pady=10
                    )
                    clare_radio_button.pack(
                        side="right", fill="y", expand=True, padx=10, pady=10
                    )
                counter += 1
            except Exception as error:
                print(f"Error populating campus selection: {error}")

    def populate_position_selection(self):
        """
        Dynamically populate position selection widgets in the GUI.
        """
        try:
            row = column = 0
            for position_group, positions in self.position_mappings.items():
                for position in positions:
                    position_radio_button = ttk.Radiobutton(
                        self.lbl_frame,
                        text=position,
                        variable=self.position_selection,
                        command=lambda: self.position_selected(),
                        value=position,
                    )
                    position_radio_button.grid(row=row, column=column, padx=10, pady=10)
                    column += 1
                    if column > 3:
                        column = 0
                        row += 1
        except Exception as error:
            print(f"Error populating position selection: {error}")

    def clear_campus_widgets(self):
        """
        Clear dynamic widgets in the campus selection frame.
        """
        for widget in self.lbl_frameC.pack_slaves():
            widget.destroy()
        for widget in self.lbl_frameG.pack_slaves():
            widget.destroy()

    def clear_position_widgets(self):
        """
        Clear dynamic widgets in the position selection frame.
        """
        for widget in self.lbl_frame.grid_slaves():
            widget.destroy()

    def clear_group_widgets(self):
        """
        Clear dynamic widgets in the group selection frame.
        """
        for widget in self.lbl_frame2.grid_slaves():
            widget.destroy()

    def on_application_close(self):
        """Handle application closure."""
        print("Thanks for using Active Directory Tool!\n")
        self.destroy()
        self.quit()

    def exit_handler(self):
        """Handle Ctrl+C exit."""
        print("Ctrl+C was pressed. Exiting now...\n")
        self.destroy()

    def show_about_box(self):
        """Display the About box with application information."""
        Messagebox.show_info(
            title="About Active Directory Tool",
            message=(
                "Active Directory Tool is a comprehensive application designed for "
                "managing Active Directory operations.\n\n"
                "Purpose:\n"
                "The application helps in user creation, searching for locked accounts, "
                "and unlocking them.\n\n"
                f"Version: {func.Version}\n"
                "Company: Arxis Security Solutions\n"
                "Website: https://www.arxis.com.au\n"
            ),
        )

    def save_new_user(self):
        """
        Save a new user to Active Directory based on the input fields in the GUI.
        """
        try:
            # Validate user input
            if len(self.entry_fname.get()) < 2 or len(self.entry_lname.get()) < 2:
                tkt.call_nosync(
                    self.messageBox,
                    "ERROR!!",
                    "First and Last name must be filled!",
                    "error",
                )
                return

            if len(self.entry_password.get()) < 8:
                tkt.call_nosync(
                    self.messageBox,
                    "ERROR!!",
                    "Password must be at least 8 characters long!",
                    "error",
                )
                return

            if self.primary_domain.get() == "Select Domain":
                tkt.call_nosync(
                    self.messageBox, "ERROR!!", "You must select a domain!", "error"
                )
                return

            # Gather user data from GUI
            user_data = {
                "login": self.getSamName().lower(),
                "first": self.entry_fname.get().strip().capitalize(),
                "last": self.entry_lname.get().strip().capitalize(),
                "password": self.entry_password.get(),
                "domain": self.primary_domain.get(),
                "description": "",  # Description is not included in the current GUI; set as blank
                "title": "",  # Job title is not included in the current GUI; set as blank
                "department": "",  # Department is not included in the current GUI; set as blank
                "company": "",  # Company is not included in the current GUI; set as blank
                "groups": self.get_selected_groups(),  # Retrieve selected groups dynamically
            }

            # Submit the save task to the thread pool
            self.status_label["text"] = "Saving new user..."
            self.executor.submit(self._save_new_user_task, user_data)
        except Exception as e:
            print(f"Error in save_new_user: {e}")
            self.status_label["text"] = "Error occurred while saving new user."

    def _save_new_user_task(self, user_data):
        """
        Background task to save a new user to Active Directory.
        """
        try:
            func.createUser(self, user_data)  # Create the user in Active Directory
            tkt.call_nosync(
                func.Toast, "COMPLETE!", "New user saved successfully!", "happy"
            )
            self.status_label["text"] = "New user saved."
        except Exception as e:
            print(f"Error saving new user: {e}")
            tkt.call_nosync(
                self.messageBox, "ERROR!!", f"Failed to save user: {e}", "error"
            )
            tkt.call_nosync(
                func.Toast, "ERROR!", "An error occurred while saving user.", "angry"
            )
        finally:
            self.status_label["text"] = "Idle..."

    def get_selected_groups(self):
        """
        Retrieve selected groups from the 'Groups' frame.
        """
        selected_groups = []
        for child in self.group_frame.winfo_children():
            if isinstance(child, ttk.Checkbutton) and child.variable.get():
                selected_groups.append(child.cget("text"))
        return selected_groups

    def execute_threaded_task(self, target_function, *args):
        """Submit a task to the thread pool executor."""
        try:
            future = self.executor.submit(target_function, *args)
            return future.result()
        except Exception as error:
            print(f"Thread execution error: {error}")

    def unlock_selected_users(self):
        """Unlock selected users in the Active Directory."""
        if not self.tree.get_children():
            self.display_message("ERROR!!", "User list cannot be empty!", "error")
            return

        if len(self.selected_items) == 0:
            self.display_message("ERROR!!", "You must select a user!", "error")
            return

        func.update_widget_status(self, ttk.DISABLED)
        self.status["text"] = f"Unlocking {self.selected_items[1]}"

        def unlock_logic():
            try:
                func.unlock_user(self, self.selected_items[2])
                selected_item = self.tree.selection()[0]
                self.tree.delete(selected_item)
                self.selected_items = []
                self.status["text"] = "Idle..."
                tkt.call_nosync(
                    func.show_toast, "COMPLETE!", "Users Unlocked!", "happy"
                )
            except Exception as error:
                print(f"Error unlocking user: {error}")
                self.display_message(
                    "ERROR!!", f"Failed to unlock user: {error}", "error"
                )

        self.executor.submit(unlock_logic)

    def display_message(self, title, message, message_type):
        """Display message dialogs."""
        dialog_mapping = {
            "info": Messagebox.show_info,
            "warning": Messagebox.show_warning,
            "question": Messagebox.show_question,
            "error": Messagebox.show_error,
        }
        dialog_function = dialog_mapping.get(
            message_type, Messagebox.ok
        )  # Default to ok dialog
        return dialog_function(message, title=title, parent=self, alert=True)

    def reset_password(self):
        """Reset the password for the selected user."""
        if len(self.selected_items) == 0:
            self.display_message("ERROR!!", "You must select a user!", "error")
            return
        if len(self.password_entry.get()) < 8:
            self.display_message("ERROR!!", "Password Too Short!", "error")
            return

        func.update_widget_status(self, ttk.DISABLED)
        new_password = self.password_entry.get()

        def reset_password_logic():
            try:
                func.reset_password(self, self.selected_items[2], new_password)
            except Exception as error:
                print(f"Error resetting password: {error}")

        self.executor.submit(reset_password_logic)

    def update_button_state(self, event=None):
        """
        Update the function and text of the single button based on the currently active tab.
        This function is called when the tab changes.
        """
        active_tab = self.tabControl.select()  # Get the currently active tab

        if active_tab == self.tabControl.tab(0):  # Locked Users Tab
            self.btn_dynamic_action.configure(
                text="Unlock All", command=self.unlock_all_users
            )

        elif active_tab == self.tabControl.tab(1):  # New Users Tab
            self.btn_dynamic_action.configure(
                text="Create User", command=self.create_new_user
            )

        elif active_tab == self.tabControl.tab(2):  # Edit Users Tab
            self.btn_dynamic_action.configure(
                text="Update User", command=self.update_existing_user
            )

    def unlockUsers(self):
        if not self.tree.get_children():
            tkt.call_nosync(
                self.messageBox, "ERROR!!", "List cannot be empty!", "error"
            )
            return

        if not self.selItem:
            tkt.call_nosync(self.messageBox, "ERROR!!", "Must select a user!", "error")
            return

        func.widgetStatus(self, ttk.DISABLED)
        self.status["text"] = f"Unlocking {self.selItem[1]}"

        # Use the executor to submit the background task
        self.executor.submit(self.unlocker)

    def unlocker(self):
        try:
            func.unlockUser(self, self.selItem[2])
            selected_item = self.tree.selection()[0]
            self.tree.delete(selected_item)
            self.selItem = []
            self.status["text"] = "Idle..."
            tkt.call_nosync(func.Toast, "COMPLETE!", "Users Unlocked!", "happy")
        except Exception as e:
            print(f"Error unlocking user: {e}")
            self.status["text"] = "Error occurred!"

    def unlockAll(self):
        func.widgetStatus(self, ttk.DISABLED)
        data = {}

        index = self.tabControl.index(self.tabControl.select())
        if index == 0:
            self.handleTabIndexZero(data)
        elif index == 1:
            self.handleTabIndexOne(data)
        elif index == 2:
            self.handleTabIndexTwo(data)
        else:
            func.widgetStatus(self, ttk.NORMAL)
            self.messageBox("ERROR!!", "Your Settings are incomplete\nfor this TAB!")

    def handleTabIndexZero(self, data):
        if not self.tree.get_children():
            func.widgetStatus(self, ttk.NORMAL)
            tkt.call_nosync(
                self.messageBox, "ERROR!!", "List cannot be empty!", "error"
            )
            return

        for line in self.tree.get_children():
            values = self.tree.item(line)["values"]
            data[values[0]] = {"name": values[1], "ou": values[2]}

        maxs = len(self.tree.get_children())
        self.progress["maximum"] = float(maxs)
        self.all = maxs

        # Submit the unlockAll task to the executor
        self.executor.submit(self.unlockAllThread, data)

    def unlockAllThread(self, data):
        try:
            func.unlockAll(self, data)  # Function to handle unlocking all users
            tkt.call_nosync(func.Toast, "COMPLETE!", "All Users Unlocked!", "happy")
            self.status["text"] = "Idle..."
            self.progress["value"] = 100
        except Exception as e:
            print(f"Error unlocking all users: {e}")
            self.status["text"] = "Error occurred!"
            self.progress["value"] = 0

    def handleTabIndexOne(self, data):
        func.widgetStatus(self, ttk.DISABLED)

        if len(self.fname.get()) < 2 or len(self.lname.get()) < 2:
            self.showErrorAndReturn("First and Lastname must\nbe filled!")
            return

        if len(self.dpass.get()) < 8:
            self.showErrorAndReturn("Must enter Password\nor password 8 characters min")
            return

        if "Select" in self.primary_domain.get():
            self.showErrorAndReturn("You must select domain\nHomeDrive and HomePath")
            return

        self.progress["value"] = 10
        self.status["text"] = "Rebuilding groups..."
        groups = self.getCheck()

        self.status["text"] = "Setting login name..."
        samname = self.getSamName()

        self.status["text"] = "Rebuilding data..."
        self.populateDataForTabIndexOne(data, samname, groups)

        self.progress["value"] = 20
        try:
            # Submit the user creation task to the executor
            self.executor.submit(self.createUserThread, data)
        except Exception as e:
            print(f"Error creating user: {e}")
            self.status["text"] = "Error occurred!"

    def createUserThread(self, data):
        try:
            func.createUser(self, data)  # Function to handle user creation
            tkt.call_nosync(func.Toast, "COMPLETE!", "User Created!", "happy")
            self.status["text"] = "Idle..."
            self.progress["value"] = 100
        except Exception as e:
            print(f"Error creating user: {e}")
            self.status["text"] = "Error occurred!"
            self.progress["value"] = 0

    def handleTabIndexTwo(self, data):
        if len(self.entPass.get()) < 8 and len(self.entPass.get()) > 0:
            self.showErrorAndReturn("Password must be 8 characters long")
            return

        if not self.tree4.get_children():
            self.showErrorAndReturn("Must select a position")
            return

        if not self.selItem3:
            self.showErrorAndReturn("Must select a user!")
            return

        if len(self.fname_entry.get()) <= 1:
            self.showErrorAndReturn("First Name cannot be empty!")
            return

        func.widgetStatus(self, ttk.DISABLED)
        self.progress["value"] = 10
        self.status["text"] = "Gathering Information..."
        self.populateDataForTabIndexTwo(data)

        self.progress["value"] = 20
        try:
            # Submit the user update task to the executor
            self.executor.submit(self.updateUserThread, data)
        except Exception as e:
            print(f"Error updating user: {e}")
            self.status["text"] = "Error occurred!"

    def updateUserThread(self, data):
        try:
            func.update_user(self, data)  # Function to handle updating user
            tkt.call_nosync(func.Toast, "COMPLETE!", "User Updated!", "happy")
            self.status["text"] = "Idle..."
            self.progress["value"] = 100
        except Exception as e:
            print(f"Error updating user: {e}")
            self.status["text"] = "Error occurred!"
            self.progress["value"] = 0

    def showErrorAndReturn(self, message):
        func.widgetStatus(self, ttk.NORMAL)
        tkt.call_nosync(self.messageBox, "ERROR!!", message, "error")

    def getSamName(self):
        index2 = self.samFormat.get()
        if index2 == "flastname":
            return f"{self.fname.get().strip()[0:1]}{self.lname.get().strip()}"
        elif index2 == "firstlastname":
            return f"{self.fname.get().strip()}{self.lname.get().strip()}"
        else:
            return f"{self.fname.get().strip()}.{self.lname.get().strip()}"

    def populateDataForTabIndexOne(self, data, samname, groups):
        data.update(
            {
                "login": samname.lower(),
                "first": self.fname.get().strip().capitalize(),
                "last": self.lname.get().strip().capitalize(),
                "password": self.dpass.get(),
                "domain": self.primary_domain.get(),
                "proxy": self.domains["secondary".lower()],
                "groups": groups,
                "description": self.desc.get(),
                "title": self.jobTitleEnt.get(),
                "department": self.depEnt.get(),
                "company": self.orgCompEnt.get(),
            }
        )

    def populateDataForTabIndexTwo(self, data):
        data.update(
            {
                "login": self.entSamname.get(),
                "first": self.fname_entry.get().capitalize(),
                "last": self.lname_entry.get().capitalize(),
                "domain": self.entDomain.get(),
                "description": self.entDesc.get(),
                "title": self.entJobTitle.get(),
                "ou": self.updateList[self.selItem3[0]]["ou"],
                "password": self.entPass.get(),
            }
        )

        if self.updateList[self.selItem3[0]].get("proxyAddresses"):
            for x in self.updateList[self.selItem3[0]]["proxyAddresses"]:
                if self.entDomain.get() not in x and len(x) > 5:
                    data["proxy"] = x.split("@")[1]
                else:
                    data["proxy"] = (
                        self.domains["secondary".lower()]
                        if len(self.domains["secondary".lower()]) > 3
                        else ""
                    )
        else:
            data["proxy"] = (
                self.domains["secondary".lower()]
                if len(self.domains["secondary".lower()]) > 3
                else ""
            )

    def resetProgress(self):
        self.progress["value"] = 0

    def select_locked_user(self, event):
        """
        Handle selecting a user from the treeview.
        Updates the selected user information.
        """
        try:
            selected_item = self.tree_locked_users.selection()[0]
            self.selItem = self.tree_locked_users.item(selected_item)["values"]
            self.status["text"] = f"Selected: {self.selItem[1]}"
            self.btn_unlock_selected_user.configure(
                state=ttk.NORMAL
            )  # Enable the button
        except Exception as e:
            print(f"Error selecting user: {e}")
            self.status["text"] = "Error selecting user."

    def select_edit_user(self, event):
        """
        Handle selecting a user from the treeview in the Edit Users tab.
        Updates the selected user information for editing.
        """
        try:
            # Get the selected item from the treeview
            selected_item = self.tree_edit_users.selection()[0]
            self.selItem = self.tree_edit_users.item(selected_item)["values"]

            # Update status with the selected user's information
            self.status_label["text"] = f"Selected: {self.selItem[1]}"  # Display Name
            self.btn_unlock_user.configure(state=ttk.NORMAL)  # Enable the Unlock button
        except IndexError:
            # No item is selected
            self.status_label["text"] = "No user selected."
        except Exception as e:
            print(f"Error selecting edit user: {e}")
            self.status_label["text"] = "Error selecting user."

    def load_locked_users(self):
        """
        Load and display locked users in the treeview.
        This method retrieves the list of locked users and populates the treeview.
        """
        try:
            # Fetch the locked users data (replace with the actual function to get locked users)
            locked_users = (
                self.get_locked_users_data()
            )  # This is a placeholder for the actual data fetching function

            if not locked_users:
                tkt.call_nosync(
                    self.messageBox, "INFO", "No locked users found.", "info"
                )
                return

            # Clear existing treeview entries before loading new data
            for item in self.tree_locked_users.get_children():
                self.tree_locked_users.delete(item)

            # Populate the treeview with locked users data
            for user in locked_users:
                self.tree_locked_users.insert(
                    "",
                    "end",
                    values=(user["username"], user["display_name"], user["dn"]),
                )

            self.status["text"] = "Loaded locked users."

        except Exception as e:
            print(f"Error loading locked users: {e}")
            self.status["text"] = "Error occurred while loading locked users."

    def get_locked_users_data(self):
        """
        Fetch and populate the locked users in the treeview.
        Uses ThreadPoolExecutor for background task execution.
        """
        self.status["text"] = "Searching locked users ..."

        # Submit the task to the executor
        self.executor.submit(self._fetch_locked_users)

    def _fetch_locked_users(self):
        """
        Internal method to fetch and populate locked users in the treeview.
        Runs in a separate thread.
        """
        try:
            # Fetch the list of locked users
            locked_users = func.listLocked(self)

            # Check if the locked users list is empty
            if len(locked_users) == 0:
                tkt.call_nosync(func.Toast, "COMPLETE!", "No Locked Users!", "happy")
                self.status["text"] = "Idle..."
                func.widgetStatus(self, ttk.NORMAL)
                return

            # Update status and clear the treeview
            self.status["text"] = "Populating list..."
            tkt.call_nosync(
                self.tree_locked_users.delete, *self.tree_locked_users.get_children()
            )

            # Populate the treeview with locked users
            for username, user_data in locked_users.items():
                tkt.call_nosync(
                    self.tree_locked_users.insert,
                    "",
                    "end",
                    values=(username, user_data["name"], user_data["ou"]),
                )

            # Update status after completion
            self.status["text"] = "Locked users loaded successfully."
            tkt.call_nosync(func.Toast, "COMPLETE!", "Locked Users Loaded!", "happy")

        except Exception as e:
            print(f"ERROR LOADING USERS: {str(e)}")
            tkt.call_nosync(
                self.messageBox, "Error", f"An error occurred: {str(e)}", "error"
            )
            tkt.call_nosync(func.Toast, "ERROR!", "An error occurred", "angry")
        finally:
            # Re-enable widgets and reset the status
            func.widgetStatus(self, ttk.NORMAL)
            self.status["text"] = "Idle..."

    def unlock_selected_user(self):
        """
        Unlock the selected user from the treeview.
        """
        try:
            # Ensure a user is selected
            if not self.selItem:
                tkt.call_nosync(
                    self.messageBox,
                    "ERROR!!",
                    "You must select a user to unlock!",
                    "error",
                )
                return

            func.widgetStatus(self, ttk.DISABLED)
            self.status["text"] = f"Unlocking user: {self.selItem[1]}..."

            # Submit the unlock operation to the thread pool
            self.executor.submit(self._unlock_user_task, self.selItem)

        except Exception as e:
            print(f"Error in unlock_selected_user: {e}")
            self.status["text"] = "Error occurred!"
            func.widgetStatus(self, ttk.NORMAL)

    def _unlock_user_task(self, selected_user):
        """
        Background task to unlock the selected user.
        """
        try:
            func.unlockUser(
                self, selected_user[2]
            )  # Assuming selItem[2] contains the DN
            tkt.call_nosync(
                func.Toast,
                "COMPLETE!",
                f"User {selected_user[1]} unlocked successfully!",
                "happy",
            )
            tkt.call_nosync(
                self.tree_locked_users.delete, self.tree_locked_users.selection()[0]
            )
            self.status["text"] = "User unlocked."
            self.selItem = []  # Clear the selected user
        except Exception as e:
            print(f"Error unlocking user: {e}")
            tkt.call_nosync(
                self.messageBox, "ERROR!!", f"Failed to unlock user: {e}", "error"
            )
            tkt.call_nosync(func.Toast, "ERROR!", "An error occurred", "angry")
        finally:
            func.widgetStatus(self, ttk.NORMAL)
            self.status["text"] = "Idle..."

    def unlock_all_users(self):
        """
        Unlock all users that are currently listed in the Locked Users tab.
        This method will unlock each user and update the treeview and status accordingly.
        """
        try:
            if not self.tree_locked_users.get_children():
                tkt.call_nosync(
                    self.messageBox, "ERROR", "No locked users to unlock.", "error"
                )
                return

            # Disable the button and set status
            self.btn_dynamic_action.configure(state=ttk.DISABLED)
            self.status_label["text"] = "Unlocking all users..."

            # Get all users from the treeview and unlock them
            users_to_unlock = [
                self.tree_locked_users.item(item)["values"]
                for item in self.tree_locked_users.get_children()
            ]
            for user in users_to_unlock:
                self.executor.submit(
                    self._unlock_user_task, user[2]
                )  # Assuming user[2] is the user DN or identifier

            # Update status after unlocking
            tkt.call_nosync(func.Toast, "COMPLETE!", "All users unlocked.", "happy")
            self.status_label["text"] = "All users unlocked."

        except Exception as e:
            print(f"Error unlocking users: {e}")
            tkt.call_nosync(
                self.messageBox, "ERROR", f"An error occurred: {e}", "error"
            )
            self.status_label["text"] = "Error occurred while unlocking users."


if __name__ == "__main__":
    app = ActiveDirectoryTool()
    app.mainloop()
