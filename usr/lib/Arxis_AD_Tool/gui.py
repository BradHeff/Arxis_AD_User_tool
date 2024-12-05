import io
import base64
import ttkbootstrap as ttk
from PIL import Image, ImageTk
import tkinter.font as tkFont
from Functions import Version, loadConfig, saveConfig
from icon import image


def window_setup(self):
    """Configure window size, position, and attributes."""
    if self.dpi >= 96.015:
        self.width, self.height = 1355, 785
    else:
        self.width, self.height = 1855, 980

    screen_width = self.winfo_screenwidth() / 2
    screen_center_x = screen_width + (screen_width / 2)
    screen_height = self.winfo_screenheight()
    center_x = int(screen_center_x - (self.width / 2))
    center_y = int(screen_height / 2 - (self.height / 2))
    self.geometry(f"{self.width}x{self.height}+{center_x}+{center_y}")
    self.attributes("-fullscreen", False)


def set_icon(self):
    """Set the window icon using a base64-encoded image."""
    try:
        b64_img = io.BytesIO(base64.b64decode(image))
        img = Image.open(b64_img, mode="r")
        photo = ImageTk.PhotoImage(image=img)
        self.wm_iconphoto(False, photo)
    except Exception as error:
        print(f"Error setting icon: {error}")


def adjust_scaling(self):
    """Adjust the UI scaling dynamically based on DPI."""
    try:
        if self.dpi > 96:  # Higher DPI (e.g., 150% scaling)
            self.tk.call("tk", "scaling", self.dpi / 96)
        else:
            self.tk.call("tk", "scaling", 1.0)
    except Exception as error:
        print(f"Error adjusting scaling: {error}")


def initialize_base_gui(self):
    """Initialize the base GUI setup."""
    window_setup(self)
    set_icon(self)

    default_font = tkFont.nametofont("TkDefaultFont")
    default_font.configure(size=9, family="Poppins")
    self.option_add("*Font", default_font)

    # Menu Bar Setup
    menubar = ttk.Menu(self, background="#4a4a59", fg="#ededef")

    self.load_config = ttk.BooleanVar(menubar, value=True)
    self.file_menu = ttk.Menu(menubar, tearoff=1, background="#060607", fg="#ededef")
    self.about_menu = ttk.Menu(menubar, tearoff=0, background="#060607", fg="#ededef")

    self.file_menu.add_checkbutton(label="Auto Load", variable=self.load_config)
    self.file_menu.add_command(
        label="Load Config", command=lambda: loadConfig(self, True)
    )
    self.file_menu.add_command(label="Save Config", command=lambda: saveConfig(self))
    self.file_menu.add_separator()
    self.file_menu.add_command(label="Exit", command=self.quit)

    menubar.add_cascade(label="File", menu=self.file_menu)
    self.config(menu=menubar, background="#4a4a59")
    menubar.add_cascade(label="Help", menu=self.about_menu)

    self.about_menu.add_command(label="Github", command=lambda: self.nav_github())
    self.about_menu.add_command(label="About", command=lambda: self.about_box())

    # Notebook (Tab) Setup
    self.tabControl = ttk.Notebook(self, style="long.TNotebook")

    tab_locked_users = ttk.Frame(self.tabControl, padding=(0, 0, 5, 0))
    tab_new_users = ttk.Frame(self.tabControl)
    tab_edit_users = ttk.Frame(self.tabControl)

    tab_locked_users.rowconfigure(1, weight=1)
    tab_locked_users.columnconfigure(0, weight=1)
    tab_new_users.rowconfigure(1, weight=0, pad=30)

    self.tabControl.add(tab_locked_users, text="Locked Users")
    self.tabControl.add(tab_new_users, text="New Users")
    self.tabControl.add(tab_edit_users, text="Edit Users")
    self.tabControl.bind("<<NotebookTabChanged>>", self.update_button_state)
    self.tabControl.grid(sticky=ttk.NSEW, columnspan=4, row=0)

    Tab1(self, tab_locked_users)
    Tab2(self, tab_new_users)
    Tab5(self, tab_edit_users)

    # Footer Section
    footer_frame = ttk.Frame(self)
    footer_frame.grid(sticky="sew", columnspan=4, row=5)
    footer_frame.rowconfigure(0, weight=0, pad=32)
    footer_frame.columnconfigure(0, weight=1)

    # This is your dynamic button that will change text and function
    self.btn_dynamic_action = ttk.Button(
        footer_frame,
        text="Unlock All",  # Initial text
        width=20,
        command=self.unlock_all_users,  # Initial command
    )
    self.btn_dynamic_action.grid(sticky="e", column=3, row=0, padx=10, pady=5)

    self.status_label = ttk.Label(footer_frame, text="Idle...")
    self.status_label.grid(sticky="w", column=0, row=1, padx=10, pady=2)
    version_label = ttk.Label(footer_frame, text=f"v{Version}")
    version_label.grid(sticky="e", column=3, row=1, padx=10, pady=2)

    self.progress_bar = ttk.Progressbar(footer_frame)
    self.progress_bar.grid(sticky="wes", columnspan=4, row=2, pady=5)


def Tab1(self, tab_locked_users):
    """Tab for managing locked users."""
    tab_locked_users.rowconfigure(4, weight=0, pad=8)
    lbl_title = ttk.Label(tab_locked_users, text="Active Directory Locked Users")
    lbl_title.grid(sticky="n", columnspan=4, padx=10, pady=5)

    self.tree_locked_users = ttk.Treeview(
        tab_locked_users, column=("c1", "c2", "c3"), show="headings"
    )
    vertical_scrollbar = ttk.Scrollbar(tab_locked_users, orient=ttk.VERTICAL)
    horizontal_scrollbar = ttk.Scrollbar(tab_locked_users, orient=ttk.HORIZONTAL)

    vertical_scrollbar.config(command=self.tree_locked_users.yview)
    horizontal_scrollbar.config(command=self.tree_locked_users.xview)

    self.tree_locked_users.config(
        yscrollcommand=vertical_scrollbar.set, xscrollcommand=horizontal_scrollbar.set
    )
    self.tree_locked_users.column("# 1", anchor=ttk.CENTER)
    self.tree_locked_users.heading("# 1", text="USERNAME")
    self.tree_locked_users.column("# 2", anchor=ttk.CENTER)
    self.tree_locked_users.heading("# 2", text="DISPLAY NAME")
    self.tree_locked_users.column("# 3", anchor=ttk.CENTER)
    self.tree_locked_users.heading("# 3", text="USER DN")
    self.tree_locked_users.bind("<ButtonRelease-1>", self.select_locked_user)
    self.tree_locked_users.grid(sticky=ttk.NSEW, row=1, columnspan=4, padx=8, pady=5)

    self.btn_load_locked_users = ttk.Button(
        tab_locked_users, text="Load", width=20, command=self.load_locked_users
    )
    self.btn_load_locked_users.grid(sticky="e", row=3, column=3, padx=10, pady=10)

    self.btn_unlock_user = ttk.Button(
        tab_locked_users,
        text="Unlock User",
        width=20,
        command=self.unlock_selected_user,
    )
    self.btn_unlock_user.grid(sticky="w", row=3, column=0, padx=10, pady=10)


def Tab2(self, tab_new_users):
    """Tab for adding new Active Directory users."""
    # Title
    lbl_title = ttk.Label(tab_new_users, text="Add New Active Directory Users")
    lbl_title.grid(sticky="n", columnspan=4, padx=10, pady=5)

    # Left and Right Frames
    left_frame = ttk.Frame(tab_new_users)
    right_frame = ttk.Frame(tab_new_users)
    left_frame.grid(sticky="nsew", column=0, row=1, columnspan=2, pady=10, padx=5)
    right_frame.grid(sticky="nsew", column=2, row=1, columnspan=2, pady=10, padx=5)

    # Left Frame Configuration
    left_frame.rowconfigure(0, weight=1)
    left_frame.columnconfigure(0, weight=1)

    # User Info Inputs
    lbl_fname = ttk.Label(left_frame, text="First Name:")
    lbl_fname.grid(sticky="w", row=0, column=0, padx=10, pady=5)

    self.entry_fname = ttk.Entry(left_frame, width=30)
    self.entry_fname.grid(sticky="w", row=0, column=1, padx=10, pady=5)

    lbl_lname = ttk.Label(left_frame, text="Last Name:")
    lbl_lname.grid(sticky="w", row=1, column=0, padx=10, pady=5)

    self.entry_lname = ttk.Entry(left_frame, width=30)
    self.entry_lname.grid(sticky="w", row=1, column=1, padx=10, pady=5)

    # Campus Selection
    self.lbl_campus = ttk.LabelFrame(left_frame, text="Campus")
    self.lbl_campus.grid(sticky="ew", column=0, columnspan=2, row=2, padx=10, pady=5)

    # Position Selection
    self.lbl_positions = ttk.LabelFrame(left_frame, text="Positions")
    self.lbl_positions.grid(sticky="ew", column=0, columnspan=2, row=3, padx=10, pady=5)

    # Right Frame Configuration
    right_frame.rowconfigure(0, weight=1)
    right_frame.columnconfigure(0, weight=1)

    lbl_domains = ttk.Label(right_frame, text="Domain:")
    lbl_domains.grid(sticky="w", row=0, column=0, padx=10, pady=5)

    self.combo_domain = ttk.Combobox(
        self,
        textvariable=self.primary_domain,
        state="readonly",
        values=[],  # Empty initially; will be populated with domain data
        width=29,
    )
    self.combo_domain.bind(
        "<<ComboboxSelected>>", lambda e: self.handle_selected_domain()
    )

    self.combo_domain.grid(sticky="w", row=0, column=1, padx=10, pady=5)

    lbl_password = ttk.Label(right_frame, text="Password:")
    lbl_password.grid(sticky="w", row=1, column=0, padx=10, pady=5)

    self.entry_password = ttk.Entry(right_frame, show="*", width=30)
    self.entry_password.grid(sticky="w", row=1, column=1, padx=10, pady=5)

    lbl_groups = ttk.LabelFrame(right_frame, text="Groups")
    lbl_groups.grid(sticky="ew", column=0, columnspan=2, row=2, padx=10, pady=5)
    self.group_frame = lbl_groups

    # Save Button
    btn_save_user = ttk.Button(
        right_frame, text="Save User", width=20, command=self.save_new_user
    )
    btn_save_user.grid(sticky="e", row=3, column=1, padx=10, pady=5)


def Tab5(self, tab_edit_users):
    """Tab for editing existing Active Directory users."""
    # Title
    lbl_title5 = ttk.Label(tab_edit_users, text="Edit Active Directory Users")
    lbl_title5.grid(sticky="n", columnspan=4, padx=10, pady=5)

    # Left and Right Frames
    left_frame = ttk.Frame(tab_edit_users)
    right_frame = ttk.Frame(tab_edit_users)
    left_frame.grid(sticky="nsew", column=0, row=1, columnspan=2, pady=10, padx=5)
    right_frame.grid(sticky="nsew", column=2, row=1, columnspan=2, pady=10, padx=5)

    # Configure Left and Right Frames
    left_frame.rowconfigure([0, 1, 2], weight=1)
    left_frame.columnconfigure(0, weight=1)

    right_frame.rowconfigure(0, weight=1)  # Treeview row stretches vertically
    right_frame.columnconfigure(0, weight=1)  # Treeview column stretches horizontally

    # Campus Selection
    self.lbl_campus_edit = ttk.LabelFrame(left_frame, text="Campus")
    self.lbl_campus_edit.grid(
        sticky="ew", column=0, columnspan=2, row=0, padx=10, pady=5
    )

    # User OU Selection
    self.lbl_user_ou = ttk.LabelFrame(left_frame, text="User OU")
    self.lbl_user_ou.grid(sticky="ew", column=0, columnspan=2, row=1, padx=10, pady=5)

    # Attributes Section
    self.lbl_attributes = ttk.LabelFrame(left_frame, text="Attributes")
    self.lbl_attributes.grid(
        sticky="ew", column=0, columnspan=2, row=2, padx=10, pady=5
    )

    lbl_fname = ttk.Label(self.lbl_attributes, text="First Name:")
    lbl_fname.grid(sticky="w", row=0, column=0, padx=10, pady=5)

    self.entry_edit_fname = ttk.Entry(self.lbl_attributes, width=25)
    self.entry_edit_fname.grid(sticky="w", row=0, column=1, padx=10, pady=5)

    lbl_lname = ttk.Label(self.lbl_attributes, text="Last Name:")
    lbl_lname.grid(sticky="w", row=1, column=0, padx=10, pady=5)

    self.entry_edit_lname = ttk.Entry(self.lbl_attributes, width=25)
    self.entry_edit_lname.grid(sticky="w", row=1, column=1, padx=10, pady=5)

    lbl_password = ttk.Label(self.lbl_attributes, text="Password:")
    lbl_password.grid(sticky="w", row=2, column=0, padx=10, pady=5)

    self.entry_edit_password = ttk.Entry(self.lbl_attributes, show="*", width=25)
    self.entry_edit_password.grid(sticky="w", row=2, column=1, padx=10, pady=5)

    lbl_description = ttk.Label(self.lbl_attributes, text="Description:")
    lbl_description.grid(sticky="w", row=3, column=0, padx=10, pady=5)

    self.entry_edit_description = ttk.Entry(self.lbl_attributes, width=50)
    self.entry_edit_description.grid(
        sticky="w", row=3, column=1, columnspan=2, padx=10, pady=5
    )

    # Treeview for Selecting Users
    self.tree_edit_users = ttk.Treeview(
        right_frame, column=("c1", "c2"), show="headings"
    )
    self.tree_edit_users.column("# 1", anchor=ttk.CENTER, width=150)
    self.tree_edit_users.heading("# 1", text="USERNAME")
    self.tree_edit_users.column("# 2", anchor=ttk.CENTER, width=250)
    self.tree_edit_users.heading("# 2", text="DISPLAY NAME")
    self.tree_edit_users.bind("<ButtonRelease-1>", self.select_edit_user)

    # Scrollbars
    scrollbar_v = ttk.Scrollbar(
        right_frame, orient=ttk.VERTICAL, command=self.tree_edit_users.yview
    )
    scrollbar_h = ttk.Scrollbar(
        right_frame, orient=ttk.HORIZONTAL, command=self.tree_edit_users.xview
    )

    self.tree_edit_users.configure(yscroll=scrollbar_v.set, xscroll=scrollbar_h.set)

    # Position Treeview and Scrollbars
    self.tree_edit_users.grid(sticky="nsew", column=0, row=0, padx=10, pady=5)
    scrollbar_v.grid(sticky="ns", column=1, row=0, pady=5)
    scrollbar_h.grid(sticky="ew", column=0, row=1, padx=10)

    right_frame.columnconfigure(0, weight=1)  # Ensure Treeview stretches horizontally
    right_frame.rowconfigure(0, weight=1)  # Ensure Treeview stretches vertically
