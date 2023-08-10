import io

import ttkbootstrap as ttk
from PIL import Image, ImageTk

from Functions import Version, base64, loadConfig, saveConfig
from icon import EDIT, image


def Window(self):
    self.W, self.H = 1480, 800
    screen_width = self.winfo_screenwidth()
    screen_height = self.winfo_screenheight()
    center_x = int(screen_width / 2 - self.W / 2)
    center_y = int(screen_height / 2 - self.H / 2)
    self.geometry(f"{self.W}x{self.H}+{center_x}+{center_y}")
    # self.resizable(0, 0)
    self.attributes("-fullscreen", False)


def Icon(self):
    b64_img = io.BytesIO(base64.b64decode(image))
    img = Image.open(b64_img, mode="r")
    photo = ImageTk.PhotoImage(image=img)
    self.wm_iconphoto(False, photo)


def baseGUI(self):
    Window(self)
    # Icon(self)

    menubar = ttk.Menu(self)
    self.file = ttk.Menu(menubar, tearoff=0)
    self.file.add_checkbutton(
        label="Auto Load", variable=self.load, command=self.setLoad
    )
    self.file.add_command(label="Load", command=lambda: loadConfig(self, True))
    self.file.add_command(label="Save", command=lambda: saveConfig(self))
    self.file.add_separator()
    # # self.file.add_command(label="Import", command=self.importConfig,
    #                         state=ttk.DISABLED)
    # self.file.add_separator()
    self.file.add_command(label="Exit", command=self.quit)
    # # self.theme = tk.Menu(menubar, tearoff=0)
    # # self.theme.add_command(label="Light",command=lambda: setTheme(self,
    #                                                                 "light"))
    # # self.theme.add_command(label="Dark", command=lambda: setTheme(self,
    #                                                                 "dark"))

    menubar.add_cascade(label="File", menu=self.file)
    self.config(menu=menubar)

    # b64_create = io.BytesIO(base64.b64decode(CREATE))
    # img_create = Image.open(b64_create, mode='r')
    # create = ImageTk.PhotoImage(image=img_create)

    # b64_move = io.BytesIO(base64.b64decode(MOVE))
    # img_move = Image.open(b64_move, mode='r')
    # move = ImageTk.PhotoImage(image=img_move)

    b64_edit = io.BytesIO(base64.b64decode(EDIT))
    img_edit = Image.open(b64_edit, mode="r")
    edit = ImageTk.PhotoImage(image=img_edit)

    # b64_lock = io.BytesIO(base64.b64decode(LOCK))
    # img_lock = Image.open(b64_lock, mode='r')
    # lock = ImageTk.PhotoImage(image=img_lock)

    self.tabControl = ttk.Notebook(self)

    tab1 = ttk.Frame(self.tabControl)
    self.tab2 = ttk.Frame(self.tabControl)
    # tab3 = ttk.Frame(self.tabControl)
    # tab4 = ttk.Frame(self.tabControl)
    tab5 = ttk.Frame(self.tabControl)

    # self.tab2.columnconfigure(0, weight=1)
    # self.tab2.columnconfigure(1, weight=1)
    # self.tab2.columnconfigure(2, weight=0)
    self.tab2.rowconfigure(1, weight=0, pad=30)

    tab1.rowconfigure(1, weight=1)
    tab1.columnconfigure(0, weight=1)

    # tab3.rowconfigure(5, weight=1)
    # tab3.columnconfigure(0, weight=1)

    # tab4.rowconfigure(4, weight=1)
    # tab4.columnconfigure(0, weight=1)

    # tab5.rowconfigure(4, weight=1)
    # tab5.columnconfigure(0, weight=1)
    # tab5.rowconfigure(1, weight=0, pad=25)

    self.columnconfigure(1, weight=1)
    self.columnconfigure(0, weight=0, pad=70)
    self.rowconfigure(0, weight=1)

    self.tabControl.add(tab1, text="Lock", image=edit, compound="top")
    self.tabControl.add(self.tab2, text="New Users")
    # self.tabControl.add(tab3, text ='Disabled User')
    # self.tabControl.add(tab4, text ='Move User')
    self.tabControl.add(tab5, text="Edit User")
    self.tabControl.bind("<<NotebookTabChanged>>", self.alterButton)
    self.tabControl.grid(sticky="nsew", columnspan=4, row=0)

    Tab1(self, tab1)
    Tab2(self, self.tab2)
    # Tab3(self, tab3)
    # Tab4(self, tab4)
    Tab5(self, tab5)

    frmbtn = ttk.Frame(self)
    frmbtn.grid(sticky="sew", columnspan=4, row=5)
    frmbtn.rowconfigure(0, weight=0, pad=26)
    frmbtn.columnconfigure(0, weight=1)
    self.btn_unlockAll = ttk.Button(
        frmbtn, text="Unlock All", width=20, command=self.unlockAll
    )
    self.btn_unlockAll.grid(sticky="e", column=3, row=0, padx=10, pady=5)
    self.btn_unlockAll.configure(state=ttk.DISABLED)

    lbl_company = ttk.Label(frmbtn, text="Company:")
    lbl_company.grid(sticky="wns", column=0, row=0, padx=10, pady=5)

    self.options = ttk.StringVar(frmbtn)
    value = base64.b64decode(self.company).decode("UTF-8").split(",")
    self.combobox = ttk.Combobox(frmbtn, textvariable=self.options, width=32)
    self.combobox["values"] = value
    self.combobox["state"] = "readonly"
    self.combobox.set("Select Company")
    self.combobox.bind("<<ComboboxSelected>>", self.comboSelect)
    self.combobox.grid(sticky="w", column=0, row=0, padx=10, pady=5)

    self.status = ttk.Label(frmbtn, text="Idle...")
    self.status.grid(sticky="w", column=0, row=1, padx=10, pady=2)
    version = ttk.Label(frmbtn, text=Version)
    version.grid(sticky="e", column=3, row=1, padx=10, pady=2)
    self.progress = ttk.Progressbar(frmbtn)
    self.progress.grid(sticky="wes", columnspan=4, row=2, pady=5)


def Tab1(self, tab1):
    lbl_title = ttk.Label(tab1, text="Active Directory Locked Users")
    lbl_title.grid(sticky="n", columnspan=4, padx=10, pady=5)

    self.tree = ttk.Treeview(tab1, column=("c1", "c2", "c3"), show="headings")
    scrollbars = ttk.Scrollbar(tab1, orient=ttk.VERTICAL)
    scrollbars.config(command=self.tree.yview)
    scrollbars.grid(sticky=ttk.NSEW, row=1, column=4)
    scrollbar2s = ttk.Scrollbar(tab1, orient=ttk.HORIZONTAL)
    scrollbar2s.config(command=self.tree.xview)
    scrollbar2s.grid(sticky=ttk.EW, row=2, columnspan=4)

    self.tree.config(yscrollcommand=scrollbars.set, xscrollcommand=scrollbar2s.set)
    self.tree.column("# 1", anchor=ttk.CENTER)
    self.tree.heading("# 1", text="USERNAME")
    self.tree.column("# 2", anchor=ttk.CENTER)
    self.tree.heading("# 2", text="DISPLAY NAME")
    self.tree.column("# 3", anchor=ttk.CENTER)
    self.tree.heading("# 3", text="OU")
    self.tree.bind("<ButtonRelease-1>", self.selectItem)
    self.tree.grid(sticky=ttk.NSEW, row=1, columnspan=4, padx=10)

    self.btn_search = ttk.Button(tab1, text="Load", width=20, command=self.loadUsers)
    self.btn_search.grid(sticky="e", row=3, column=3, padx=10, pady=10)
    self.btn_search.configure(state=ttk.DISABLED)

    self.btn_userUnlock = ttk.Button(
        tab1, text="Unlock User", width=20, command=self.unlockUsers
    )
    self.btn_userUnlock.grid(sticky="w", row=3, column=0, padx=10, pady=10)
    self.btn_userUnlock.configure(state=ttk.DISABLED)

    lbl_password = ttk.Label(tab1, text="Password:")
    lbl_password.grid(sticky="wn", row=4, column=0, padx=10)

    self.passBox = ttk.Entry(tab1, width=30)
    self.passBox.grid(sticky="ws", row=4, column=0, padx=10, pady=1)

    self.btn_reset = ttk.Button(
        tab1, text="Reset Password", width=20, command=self.resetPass
    )
    self.btn_reset.grid(sticky="es", row=4, column=3, padx=10, pady=13)
    self.btn_reset.configure(state=ttk.DISABLED)


def Tab2(self, tab2):
    lbl_title = ttk.Label(tab2, text="Active Directory New Users")
    lbl_title.grid(sticky="n", columnspan=4, padx=10, pady=5)

    lframe = ttk.Frame(tab2)
    rframe = ttk.Frame(tab2)

    lframe.grid(sticky="nsw", column=0, row=1, pady=10)
    rframe.grid(sticky="nse", column=2, row=1, pady=10)

    # lframe.columnconfigure(0, weight=1)
    # lframe.columnconfigure(1, weight=1)
    # lframe.columnconfigure(0, weight=0)
    # lframe.columnconfigure(1, weight=0)
    lframe.rowconfigure(1, weight=0, pad=26)
    lframe.rowconfigure(6, weight=0, pad=26)

    rframe.rowconfigure(0, weight=0, pad=26)

    lbl_fname = ttk.Label(lframe, text="Firstname:")
    lbl_fname.grid(sticky="wn", column=0, row=1, padx=10, pady=5)
    self.fname = ttk.Entry(lframe, width=39)
    self.fname.grid(sticky="ws", column=0, row=1, padx=10)
    lbl_lname = ttk.Label(lframe, text="Lastname:")
    lbl_lname.grid(sticky="wn", column=1, row=1, padx=10, pady=5)
    self.lname = ttk.Entry(lframe, width=39)
    self.lname.grid(sticky="ws", column=1, row=1, padx=10)

    self.frame = ttk.Frame(lframe)
    self.frame.grid(sticky="sew", columnspan=4, row=2, padx=10)
    self.frame.columnconfigure(0, weight=1)

    self.samFormat = ttk.StringVar(lframe, "flastname")
    f_last = ttk.Radiobutton(
        self.frame, text="flastname", variable=self.samFormat, value="flastname"
    )
    f_last.grid(sticky="se", row=0, padx=10, pady=10)

    f_dot_last = ttk.Radiobutton(
        self.frame, text="first.last", variable=self.samFormat, value="first.lastname"
    )
    f_dot_last.grid(sticky="sn", row=0, padx=10, pady=10)

    first_last = ttk.Radiobutton(
        self.frame, text="firstlast", variable=self.samFormat, value="firstlastname"
    )
    first_last.grid(sticky="sw", row=0, padx=10, pady=10)

    self.lbl_frameC = ttk.LabelFrame(lframe, text="Campus")
    self.lbl_frameC.grid(sticky="ew", columnspan=4, row=3, padx=10, pady=5)

    self.lbl_frame = ttk.LabelFrame(lframe, text="Staff Position")
    self.lbl_frame.grid(sticky="ew", columnspan=4, row=4, padx=10, pady=5)

    self.lbl_frame4 = ttk.LabelFrame(lframe, text="Students Position")
    self.lbl_frame4.grid(sticky="ew", columnspan=4, row=5, padx=10, pady=5)

    lbl_groups = ttk.Label(lframe, text="Add Groups")
    lbl_groups.grid(sticky="wn", column=0, row=6, padx=10, pady=5)

    self.add_groups = ttk.StringVar(lframe, "Select Group")
    self.ex_groups = ttk.Combobox(lframe, textvariable=self.add_groups, width=35)
    self.ex_groups["state"] = "readonly"
    self.ex_groups.grid(sticky="ws", column=0, row=6, padx=10, pady=5)

    self.addGroup = ttk.Button(
        lframe, text="Add Group", width=20, command=self.addToGroups
    )
    self.addGroup["state"] = ttk.DISABLED
    self.addGroup.grid(sticky="e", column=1, row=6, padx=10, pady=5)

    self.lbl_frame2 = ttk.LabelFrame(rframe, text="Groups")
    self.lbl_frame2.grid(sticky="ew", columnspan=4, row=7, padx=10, pady=5)

    self.lbl_domains = ttk.Label(rframe, text="Domains:")
    self.lbl_domains.grid(sticky="wn", column=0, row=0, padx=10, pady=5)

    self.primary_domain = ttk.StringVar(rframe, "Select Domain")
    self.combo_domain = ttk.Combobox(rframe, textvariable=self.primary_domain, width=37)
    self.combo_domain["state"] = "readonly"
    self.combo_domain.grid(sticky="ws", column=0, row=0, padx=10, pady=5)

    lbl_dpass = ttk.Label(rframe, text="Password:")
    lbl_dpass.grid(sticky="wn", column=1, row=0, padx=10, pady=5)

    self.dpass = ttk.Entry(rframe, width=30)
    self.dpass.grid(sticky="ws", column=1, row=0, padx=10, pady=5)

    self.lbl_frame3 = ttk.LabelFrame(rframe, text="Profile")
    self.lbl_frame3.grid(sticky="ew", columnspan=2, row=1, padx=10, pady=2)

    lbl_homeDrive = ttk.Label(self.lbl_frame3, text="Home Drive:")
    lbl_homeDrive.grid(sticky="wns", column=0, row=0, padx=10, pady=10)

    self.hdrive = ttk.StringVar(self.lbl_frame3, "Select Drive")
    self.combo_hdrive = ttk.Combobox(
        self.lbl_frame3, textvariable=self.hdrive, width=15
    )
    self.combo_hdrive["values"] = [
        "A",
        "B",
        "C",
        "D",
        "E",
        "F",
        "G",
        "H",
        "I",
        "J",
        "K",
        "L",
        "M",
        "N",
        "O",
        "P",
        "Q",
        "R",
        "S",
        "T",
        "U",
        "V",
        "W",
        "X",
        "Y",
        "Z",
    ]
    self.combo_hdrive["state"] = "readonly"
    self.combo_hdrive.bind("<<ComboboxSelected>>", self.driveSelect)
    self.combo_hdrive.grid(sticky="en", column=1, row=0, padx=10, pady=10)

    lbl_homePath = ttk.Label(self.lbl_frame3, text="Home Path:")
    lbl_homePath.grid(sticky="wsn", column=2, row=0, padx=10, pady=10)

    self.paths = ttk.StringVar(self.lbl_frame3, "Select Homepath")
    self.homePath = ttk.Combobox(self.lbl_frame3, textvariable=self.paths, width=40)
    self.homePath["state"] = "readonly"
    self.homePath.grid(sticky="en", column=3, row=0, padx=10, pady=10)

    lbl_desc = ttk.Label(self.lbl_frame3, text="Description:")
    lbl_desc.grid(sticky="wsn", column=0, row=1, padx=10, pady=10)

    self.desc = ttk.Entry(self.lbl_frame3, width=18)
    self.desc.insert(0, self.date)
    self.desc.grid(sticky="es", column=1, row=1, padx=10, pady=10)

    lbl_dep = ttk.Label(self.lbl_frame3, text="Department:")
    lbl_dep.grid(sticky="wsn", column=0, row=2, padx=10, pady=10)

    self.depEnt = ttk.Entry(self.lbl_frame3, width=18)
    self.depEnt.grid(sticky="es", column=1, row=2, padx=10, pady=10)

    lbl_jobTitle = ttk.Label(self.lbl_frame3, text="Job Title:")
    lbl_jobTitle.grid(sticky="wsn", column=2, row=1, padx=10, pady=10)

    self.jobTitleEnt = ttk.Entry(self.lbl_frame3, width=43)
    self.jobTitleEnt.grid(sticky="en", column=3, row=1, padx=10, pady=10)

    lbl_orCampTitle = ttk.Label(self.lbl_frame3, text="Company:")
    lbl_orCampTitle.grid(sticky="wsn", column=2, row=2, padx=10, pady=10)

    self.orgCompEnt = ttk.Entry(self.lbl_frame3, width=43)
    self.orgCompEnt.grid(sticky="en", column=3, row=2, padx=10, pady=10)

    self.campH = ttk.StringVar(self.lbl_frameC, "balaklava")

    # clare = tk.Radiobutton(self.lbl_frameC, text="Clare",
    #                        variable=self.campH, value=0,
    #                        command=lambda:self.comboSelect(""))
    # balak.pack(side="left", fill=ttk.BOTH, expand=True)
    # clare.pack(side="right", fill=ttk.BOTH, expand=True)


def Tab3(self, tab3):
    lbl_title = ttk.Label(tab3, text="Disabled User Group Cleanup")
    lbl_title.grid(sticky="n", columnspan=4, padx=10, pady=5)

    self.lbl_frame5 = ttk.Labelframe(tab3, text="Disabled User OU's")
    self.lbl_frame5.grid(sticky="new", columnspan=4, row=1, padx=10, pady=5)

    self.tree2 = ttk.Treeview(tab3, column=("c1", "c2", "c3"), show="headings")
    scrollbar = ttk.Scrollbar(tab3)
    scrollbar.config(command=self.tree2.yview)
    scrollbar.grid(sticky=ttk.NSEW, row=2, column=4)
    scrollbar2 = ttk.Scrollbar(tab3)
    scrollbar2.config(command=self.tree2.xview, orient=ttk.HORIZONTAL)
    scrollbar2.grid(sticky=ttk.NSEW, row=3, columnspan=4)

    self.tree2.column("# 1", anchor=ttk.CENTER)
    self.tree2.heading("# 1", text="USERNAME")
    self.tree2.column("# 2", anchor=ttk.CENTER)
    self.tree2.heading("# 2", text="DISPLAY NAME")
    self.tree2.column("# 3", anchor=ttk.CENTER)
    self.tree2.heading("# 3", text="OU")
    self.tree2.grid(sticky="nsew", row=2, columnspan=4, padx=5)


def Tab4(self, tab4):
    lbl_title4 = ttk.Label(tab4, text="Active Directory Move Users")
    lbl_title4.grid(sticky="n", columnspan=4, padx=10)

    lframe4 = ttk.Frame(tab4)
    rframe4 = ttk.Frame(tab4)

    lframe4.grid(sticky="nsw", column=0, row=1, pady=10)
    rframe4.grid(sticky="nse", column=2, row=1, pady=10)

    self.lbl_frameF = ttk.Labelframe(rframe4, text="Campus")
    self.lbl_frameF.grid(sticky="new", columnspan=2, row=1, padx=10, pady=5)

    self.lbl_frame6 = ttk.Labelframe(rframe4, text="Staff User OU's")
    self.lbl_frame6.grid(sticky="new", columnspan=2, row=2, padx=10, pady=5)

    self.lbl_frame7 = ttk.Labelframe(rframe4, text="Student User OU's")
    self.lbl_frame7.grid(sticky="new", columnspan=2, row=3, padx=10, pady=5)

    self.tree3 = ttk.Treeview(lframe4, column=("c1", "c2", "c3"), show="headings")
    scrollbar = ttk.Scrollbar(lframe4)
    scrollbar.config(command=self.tree3.yview)
    scrollbar.grid(sticky=ttk.NSEW, row=1, column=4)
    scrollbar2 = ttk.Scrollbar(lframe4, orient=ttk.HORIZONTAL)
    scrollbar2.config(command=self.tree3.xview)
    scrollbar2.grid(sticky=ttk.NSEW, row=2, columnspan=2)

    self.tree3.column("# 1", anchor=ttk.CENTER)
    self.tree3.heading("# 1", text="USERNAME")
    self.tree3.column("# 2", anchor=ttk.CENTER)
    self.tree3.heading("# 2", text="DISPLAY NAME")
    self.tree3.column("# 3", anchor=ttk.CENTER)
    self.tree3.heading("# 3", text="OU")
    self.tree3.bind("<ButtonRelease-1>", self.selectItem2)
    self.tree3.grid(sticky="nsew", row=1, columnspan=2, padx=10)

    self.lbl_frame8 = ttk.Labelframe(rframe4, text="Move To OU")
    self.lbl_frame8.grid(sticky="new", columnspan=2, row=4, padx=10, pady=5)

    self.move_btn = ttk.Button(
        rframe4, text="Move User", width=20, command=self.moveUser
    )
    self.move_btn.configure(state=ttk.DISABLED)
    self.move_btn.grid(sticky="w", column=0, row=7, padx=10, pady=10)


def Tab5(self, tab5):
    lbl_title5 = ttk.Label(tab5, text="Active Directory Edit Users")
    lbl_title5.grid(sticky="n", columnspan=4, padx=10)

    tab5.columnconfigure(0, weight=1)
    tab5.columnconfigure(2, weight=1)

    lframe5 = ttk.Frame(tab5)
    rframe5 = ttk.Frame(tab5)

    rframe5.rowconfigure(0, weight=1)
    rframe5.columnconfigure(0, weight=1)

    lframe5.grid(sticky="nsew", column=0, row=1, pady=10)
    rframe5.grid(sticky="nsew", column=2, row=1, pady=10)

    self.lbl_frameG = ttk.Labelframe(lframe5, text="Campus")
    self.lbl_frameG.grid(sticky="new", columnspan=2, row=1, padx=10, pady=5)

    self.lbl_frame9 = ttk.Labelframe(lframe5, text="Staff User OU's")
    self.lbl_frame9.grid(sticky="new", columnspan=2, row=2, padx=10, pady=5)

    self.lbl_frame10 = ttk.Labelframe(lframe5, text="Student User OU's")
    self.lbl_frame10.grid(sticky="new", columnspan=2, row=3, padx=10, pady=5)

    self.tree4 = ttk.Treeview(rframe5, column=("c1", "c2", "c3"), show="headings")
    self.tree4.column("# 1", anchor=ttk.CENTER)
    self.tree4.heading("# 1", text="USERNAME")
    self.tree4.column("# 2", anchor=ttk.CENTER)
    self.tree4.heading("# 2", text="DISPLAY NAME")
    self.tree4.column("# 3", anchor=ttk.CENTER)
    self.tree4.heading("# 3", text="OU")
    self.tree4.bind("<ButtonRelease-1>", self.selectItem3)
    scrollbar = ttk.Scrollbar(rframe5)
    scrollbar.config(command=self.tree4.yview)
    scrollbar.grid(sticky=ttk.NSEW, row=0, column=2)
    scrollbar2 = ttk.Scrollbar(rframe5, orient=ttk.HORIZONTAL)
    scrollbar2.config(command=self.tree4.xview)
    scrollbar2.grid(sticky=ttk.NSEW, row=1, columnspan=2)
    self.tree4.grid(sticky=ttk.NSEW, row=0, columnspan=2, padx=10)

    lbl_frame11 = ttk.Labelframe(rframe5, text="Attributes")
    lbl_frame11.grid(sticky="new", row=3, columnspan=2, padx=10, pady=5)

    lbl_frame11.rowconfigure(0, weight=0, pad=20)
    lbl_frame11.rowconfigure(1, weight=0, pad=20)
    lbl_frame11.rowconfigure(2, weight=0, pad=20)

    lblfname = ttk.Label(lbl_frame11, text="Firstname")
    lblfname.grid(sticky="nw", column=0, row=0, padx=10, pady=5)

    lbllname = ttk.Label(lbl_frame11, text="Lastname")
    lbllname.grid(sticky="nw", column=1, row=0, padx=10, pady=5)

    lbldomain = ttk.Label(lbl_frame11, text="Domain")
    lbldomain.grid(sticky="nw", column=2, row=0, padx=10, pady=5)

    self.fname_entry = ttk.Entry(lbl_frame11, width=28)
    self.fname_entry.grid(sticky="sew", column=0, row=0, padx=10, pady=5)

    self.lname_entry = ttk.Entry(lbl_frame11, width=28)
    self.lname_entry.grid(sticky="sew", column=1, row=0, padx=10, pady=5)

    self.entDomain = ttk.Entry(lbl_frame11, width=28)
    self.entDomain["state"] = "readonly"
    self.entDomain.grid(sticky="sew", column=2, row=0, padx=10, pady=5)

    lbllsname = ttk.Label(lbl_frame11, text="Login")
    lbllsname.grid(sticky="nw", column=0, row=1, padx=10, pady=5)

    self.entSamname = ttk.Entry(lbl_frame11, width=28)
    self.entSamname.grid(sticky="sew", column=0, row=1, padx=10, pady=5)

    lbltitle = ttk.Label(lbl_frame11, text="Title")
    lbltitle.grid(sticky="nw", column=1, row=1, padx=10, pady=5)

    self.entJobTitle = ttk.Entry(lbl_frame11, width=28)
    self.entJobTitle.grid(sticky="sew", column=1, row=1, padx=10, pady=5)

    lbllDesc = ttk.Label(lbl_frame11, text="Description")
    lbllDesc.grid(sticky="nw", column=2, row=1, padx=10, pady=5)

    self.entDesc = ttk.Entry(lbl_frame11, width=28)
    self.entDesc.grid(sticky="sew", column=2, row=1, padx=10, pady=5)

    lbllPass = ttk.Label(lbl_frame11, text="Password")
    lbllPass.grid(sticky="nw", column=0, row=2, padx=10, pady=5)

    self.entPass = ttk.Entry(lbl_frame11, width=28)
    self.entPass.grid(sticky="sew", column=0, row=2, padx=10, pady=5)
