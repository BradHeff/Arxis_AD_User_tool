import io
import base64
import ttkbootstrap as ttk
from PIL import Image, ImageTk
import tkinter.font as tkFont
from Functions import Version
from icon import image


def Window(self):
    self.W, self.H = 1395, 780
    screen_width = self.winfo_screenwidth()
    screen_height = self.winfo_screenheight()
    center_x = int(screen_width / 2 - self.W / 2)
    center_y = int(screen_height / 2 - self.H / 2)
    self.geometry(f"{self.W}x{self.H}+{center_x}+{center_y}")
    self.minsize(1240, 710)
    self.attributes("-fullscreen", False)
    # self.resizable(False, False)


def Icon(self):
    b64_img = io.BytesIO(base64.b64decode(image))
    img = Image.open(b64_img, mode="r")
    photo = ImageTk.PhotoImage(image=img)
    self.wm_iconphoto(False, photo)


def baseGUI(self):
    Window(self)
    Icon(self)
    # self.config(font=("Poppins", 12))
    default_font = tkFont.nametofont("TkDefaultFont")
    default_font.configure(size=7, family="Poppins")
    self.option_add("*Font", default_font)
    # menubar = ttk.Menu(self, background="#4a4a59", fg="#ededef")
    # self.file = ttk.Menu(menubar, tearoff=0, background="#4a4a59", fg="#ededef")
    # self.file.add_checkbutton(
    #     label="Auto Load", variable=self.load, command=self.setLoad
    # )
    # self.file.add_command(label="Load", command=lambda: loadConfig(self, True))
    # self.file.add_command(label="Save", command=lambda: saveConfig(self))
    # self.file.add_separator()
    # self.file.add_command(label="Exit", command=self.quit)

    # menubar.add_cascade(label="File", menu=self.file)
    # self.config(menu=menubar, background="#4a4a59")
    self.columnconfigure(1, weight=1)
    self.columnconfigure(0, weight=0, pad=70)
    self.rowconfigure(0, weight=1)

    self.tabControl = ttk.Notebook(self)

    tab1 = ttk.Frame(self.tabControl, padding=(0, 0, 5, 0))
    self.tab2 = ttk.Frame(self.tabControl)
    # tab3 = ttk.Frame(self.tabControl)
    # tab4 = ttk.Frame(self.tabControl)
    tab5 = ttk.Frame(self.tabControl)
    # tab6 = ttk.Frame(self.tabControl, padding=(0, 0, 5, 0))

    self.tab2.rowconfigure(1, weight=0, pad=30)

    tab1.rowconfigure(1, weight=1)
    tab1.columnconfigure(0, weight=1)

    # tab3.rowconfigure(5, weight=1)
    # tab3.columnconfigure(0, weight=1)

    # tab4.rowconfigure(4, weight=1)
    # tab4.columnconfigure(0, weight=1)
    # tab4.columnconfigure(2, weight=1)

    self.tabControl.add(tab1, text="Lock", compound="top")
    self.tabControl.add(self.tab2, text="New Users")
    # self.tabControl.add(tab3, text="Disabled User")
    # self.tabControl.add(tab4, text="Move User")
    self.tabControl.add(tab5, text="Edit User")
    # self.tabControl.add(tab6, text="Disable User")
    self.tabControl.bind("<<NotebookTabChanged>>", self.alterButton)
    self.tabControl.grid(sticky=ttk.NSEW, columnspan=4, row=0)

    Tab1(self, tab1)
    Tab2(self, self.tab2)
    # Tab3(self, tab3)
    # Tab4(self, tab4)
    Tab5(self, tab5)
    # Tab6(self, tab6)

    frmbtn = ttk.Frame(self)
    frmbtn.grid(sticky="sew", columnspan=4, row=5)
    frmbtn.rowconfigure(0, weight=0, pad=26)
    frmbtn.columnconfigure(0, weight=1)
    self.btn_unlockAll = ttk.Button(
        frmbtn, text="Unlock All", width=20, command=self.global_button
    )
    self.btn_unlockAll.grid(sticky="e", column=3, row=0, padx=10, pady=5)
    self.btn_unlockAll.configure(state=ttk.DISABLED)

    # self.lbl_login = ttk.Label(frmbtn, text="Not Authorized")
    # self.lbl_login.grid(sticky="w", column=0, row=0, padx=10, pady=5)
    # self.lbl_login.config(
    #     bootstyle="danger",
    #     font=("Poppins", 12),
    #     text="No Access",
    # )
    # self.options = ttk.StringVar(frmbtn)
    # self.combobox = ttk.Combobox(frmbtn, textvariable=self.options, width=32)
    # self.combobox["values"] = ["Horizon"]
    # self.combobox["state"] = "readonly"
    # self.combobox.set("Select Company")
    # self.combobox.bind("<<ComboboxSelected>>", self.comboSelect)
    # self.combobox.grid(sticky="w", column=0, row=0, padx=10, pady=5)

    self.status = ttk.Label(frmbtn, text="Idle...")
    self.status.grid(sticky="w", column=0, row=1, padx=10, pady=2)
    version = ttk.Label(frmbtn, text="v{}".format(Version))
    version.grid(sticky="e", column=3, row=1, padx=10, pady=2)
    self.progress = ttk.Progressbar(frmbtn)
    self.progress.grid(sticky="wes", columnspan=4, row=2, pady=5)


def Tab1(self, tab1):
    lbl_title = ttk.Label(tab1, text="Active Directory Locked Users")
    lbl_title.grid(sticky="n", columnspan=4, padx=10, pady=5)

    self.tree = ttk.Treeview(tab1, column=("c1", "c2", "c3"), show="headings")
    scrollbars = ttk.Scrollbar(tab1, orient=ttk.VERTICAL, bootstyle="primary-round")
    scrollbars.config(command=self.tree.yview)
    scrollbars.grid(sticky=ttk.NSEW, row=1, column=4, pady=5)
    scrollbar2s = ttk.Scrollbar(tab1, orient=ttk.HORIZONTAL, bootstyle="primary-round")
    scrollbar2s.config(command=self.tree.xview)
    scrollbar2s.grid(sticky=ttk.EW, row=2, columnspan=4, padx=10)

    self.tree.config(yscrollcommand=scrollbars.set, xscrollcommand=scrollbar2s.set)
    self.tree.column("# 1", anchor=ttk.CENTER)
    self.tree.heading("# 1", text="USERNAME")
    self.tree.column("# 2", anchor=ttk.CENTER)
    self.tree.heading("# 2", text="DISPLAY NAME")
    self.tree.column("# 3", anchor=ttk.CENTER)
    self.tree.heading("# 3", text="USER DN")
    self.tree.bind("<ButtonRelease-1>", self.selectItem)
    self.tree.grid(sticky=ttk.NSEW, row=1, columnspan=4, padx=8, pady=5)

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

    tab2.columnconfigure(0, weight=1)
    tab2.columnconfigure(2, weight=1)

    tab2.rowconfigure(1, weight=1)

    lframe = ttk.Frame(tab2)
    rframe = ttk.Frame(tab2)

    lframe.grid(sticky="nsew", column=0, row=1, columnspan=2, pady=10)
    rframe.grid(sticky="nsew", column=2, row=1, columnspan=2, pady=10, padx=5)

    lframe.rowconfigure(1, weight=0, pad=26)
    lframe.columnconfigure(10, weight=1)

    rframe.rowconfigure(0, weight=0, pad=26)
    rframe.columnconfigure(1, weight=1)

    lbl_fname = ttk.Label(lframe, text="Firstname:")
    lbl_fname.grid(sticky="wn", column=0, row=1, padx=10, pady=5)

    self.fname = ttk.Entry(lframe, width=42)
    self.fname.grid(sticky="ws", column=0, row=1, padx=10)

    lbl_lname = ttk.Label(lframe, text="Lastname:")
    lbl_lname.grid(sticky="wn", column=1, row=1, padx=10, pady=5)

    self.lname = ttk.Entry(lframe, width=42)
    self.lname.grid(sticky="ws", column=1, row=1, padx=10)

    self.frame = ttk.Frame(lframe)
    self.frame.grid(sticky="ew", column=0, columnspan=4, row=2, padx=10)
    self.frame.columnconfigure(0, weight=1)

    self.samFormat = ttk.StringVar(lframe, "flastname")
    f_last = ttk.Radiobutton(
        self.frame,
        text="flastname",
        variable=self.samFormat,
        value="flastname",
        bootstyle="primary",
    )
    f_last.grid(sticky="se", row=0, padx=10, pady=10)

    f_dot_last = ttk.Radiobutton(
        self.frame,
        text="first.last",
        variable=self.samFormat,
        value="first.lastname",
        bootstyle="primary",
    )
    f_dot_last.grid(sticky="sn", row=0, padx=10, pady=10)

    first_last = ttk.Radiobutton(
        self.frame,
        text="firstlast",
        variable=self.samFormat,
        value="firstlastname",
        bootstyle="primary",
    )
    first_last.grid(sticky="sw", row=0, padx=10, pady=10)

    self.lbl_frameC = ttk.LabelFrame(lframe, text="Campus")
    self.lbl_frameC.grid(sticky="ew", column=0, columnspan=4, row=3, padx=10, pady=5)

    self.lbl_frame = ttk.LabelFrame(lframe, text="Staff Position")
    self.lbl_frame.grid(sticky="ew", columnspan=4, row=4, padx=10, pady=5)

    # self.lbl_frame4 = ttk.LabelFrame(lframe, text="Students Position")
    # self.lbl_frame4.grid(sticky="ew", columnspan=4, row=5, padx=10, pady=5)

    self.lbl_frame3 = ttk.LabelFrame(rframe, text="Profile")
    self.lbl_frame3.columnconfigure(2, weight=1)
    self.lbl_frame3.grid(sticky="ew", columnspan=5, row=2, padx=10, pady=2)

    self.lbl_frame2 = ttk.LabelFrame(rframe, text="Groups")
    self.lbl_frame2.grid(sticky="ew", columnspan=5, row=7, padx=10, pady=5)

    self.lbl_domains = ttk.Label(rframe, text="Domains:")
    self.lbl_domains.grid(sticky="wn", column=0, row=0, padx=10, pady=5)

    self.primary_domain = ttk.StringVar(rframe, "Select Domain")
    self.combo_domain = ttk.Combobox(rframe, textvariable=self.primary_domain, width=29)
    self.combo_domain["state"] = "readonly"
    self.combo_domain.grid(sticky="ws", column=0, row=0, padx=10, pady=5)

    lbl_dpass = ttk.Label(rframe, text="Password:")
    lbl_dpass.grid(sticky="ne", column=3, row=0, padx=10, pady=5)

    self.dpass = ttk.Entry(rframe, width=42)
    self.dpass.grid(sticky="se", column=3, row=0, padx=10, pady=5)
    self.dpass.configure(show="*")
    # lbl_homeDrive = ttk.Label(self.lbl_frame3, text="Home Drive:")
    # lbl_homeDrive.grid(sticky="nw", column=0, row=0, padx=10, pady=10)

    # self.hdrive = ttk.StringVar(self.lbl_frame3, "Select Drive")
    # self.combo_hdrive = ttk.Combobox(
    #     self.lbl_frame3, textvariable=self.hdrive, width=15
    # )
    # self.combo_hdrive["values"] = [
    #     "A",
    #     "B",
    #     "C",
    #     "D",
    #     "E",
    #     "F",
    #     "G",
    #     "H",
    #     "I",
    #     "J",
    #     "K",
    #     "L",
    #     "M",
    #     "N",
    #     "O",
    #     "P",
    #     "Q",
    #     "R",
    #     "S",
    #     "T",
    #     "U",
    #     "V",
    #     "W",
    #     "X",
    #     "Y",
    #     "Z",
    # ]
    # self.combo_hdrive["state"] = "readonly"
    # self.combo_hdrive.bind("<<ComboboxSelected>>", self.driveSelect)
    # self.combo_hdrive.grid(sticky="ne", column=1, row=0, padx=10, pady=10)

    # lbl_homePath = ttk.Label(self.lbl_frame3, text="Home Path:")
    # lbl_homePath.grid(sticky="we", column=3, row=0, padx=10, pady=10)

    # self.paths = ttk.StringVar(self.lbl_frame3, "Select Homepath")
    # self.homePath = ttk.Combobox(self.lbl_frame3, textvariable=self.paths, width=20)
    # self.homePath["state"] = "readonly"
    # self.homePath.grid(sticky="ne", column=4, row=0, padx=10, pady=10)

    lbl_desc = ttk.Label(self.lbl_frame3, text="Description:")
    lbl_desc.grid(sticky="wsn", column=0, row=1, padx=10, pady=10)

    self.desc = ttk.Entry(self.lbl_frame3, width=20)
    self.desc.insert(0, self.date)
    self.desc.grid(sticky="es", column=1, row=1, padx=10, pady=10)

    lbl_dep = ttk.Label(self.lbl_frame3, text="Department:")
    lbl_dep.grid(sticky="wsn", column=0, row=2, padx=10, pady=10)

    self.depEnt = ttk.Entry(self.lbl_frame3, width=20)
    self.depEnt.grid(sticky="es", column=1, row=2, padx=10, pady=10)

    lbl_jobTitle = ttk.Label(self.lbl_frame3, text="Job Title:")
    lbl_jobTitle.grid(sticky="wsn", column=3, row=1, padx=10, pady=10)

    self.jobTitleEnt = ttk.Entry(self.lbl_frame3, width=22)
    self.jobTitleEnt.grid(sticky="en", column=4, row=1, padx=10, pady=10)

    lbl_orCampTitle = ttk.Label(self.lbl_frame3, text="Company:")
    lbl_orCampTitle.grid(sticky="wsn", column=3, row=2, padx=10, pady=10)

    self.orgCompEnt = ttk.Entry(self.lbl_frame3, width=22)
    self.orgCompEnt.grid(sticky="en", column=4, row=2, padx=10, pady=10)

    self.campH = ttk.StringVar(self.lbl_frameC, "balaklava")


# def Tab3(self, tab3):
#     lbl_title = ttk.Label(tab3, text="Disabled Users Group Cleanup")
#     lbl_title.grid(sticky="n", columnspan=4, padx=10, pady=5)

#     self.lbl_frame5 = ttk.Labelframe(tab3, text="Disabled User OU's")
#     self.lbl_frame5.grid(sticky="new", columnspan=4, row=1, padx=10, pady=5)

#     self.tree2 = ttk.Treeview(tab3, column=("c1", "c2", "c3"), show="headings")
#     scrollbar = ttk.Scrollbar(tab3, orient=ttk.VERTICAL, bootstyle="primary-round")
#     scrollbar.config(command=self.tree2.yview)
#     scrollbar.grid(sticky=ttk.NSEW, row=2, column=4, pady=5)
#     scrollbar2 = ttk.Scrollbar(tab3, orient=ttk.HORIZONTAL, bootstyle="primary-round")
#     scrollbar2.config(command=self.tree2.xview, orient=ttk.HORIZONTAL)
#     scrollbar2.grid(sticky=ttk.NSEW, row=3, columnspan=4, padx=10)

#     self.tree2.column("# 1", anchor=ttk.CENTER)
#     self.tree2.heading("# 1", text="USERNAME")
#     self.tree2.column("# 2", anchor=ttk.CENTER)
#     self.tree2.heading("# 2", text="DISPLAY NAME")
#     self.tree2.column("# 3", anchor=ttk.CENTER)
#     self.tree2.heading("# 3", text="USER DN")
#     self.tree2.grid(sticky=ttk.NS, row=2, column=2, rowspan=2, pady=5)
#     # self.tree2.grid(sticky="nsew", row=2, columnspan=4, padx=15, pady=5)


# def Tab4(self, tab4):
#     lbl_title4 = ttk.Label(tab4, text="Active Directory Move Users")
#     lbl_title4.grid(sticky="n", columnspan=4, padx=10)

#     tab4.columnconfigure(0, weight=1)
#     tab4.columnconfigure(2, weight=1)

#     lframe4 = ttk.Frame(tab4)
#     rframe4 = ttk.Frame(tab4)

#     lframe4.rowconfigure(6, weight=0, pad=26)

#     rframe4.rowconfigure(0, weight=0, pad=26)

#     lframe4.grid(sticky=ttk.NSEW, column=0, row=1, pady=10, padx=10)
#     rframe4.grid(sticky=ttk.NSEW, column=2, row=1, pady=10)

#     self.lbl_frameF = ttk.Labelframe(rframe4, text="Campus")
#     self.lbl_frameF.grid(sticky=ttk.NSEW, columnspan=2, row=1, padx=10, pady=5)
#     self.McampH = ttk.StringVar(self.lbl_frameF, "balaklava")

#     self.lbl_frame6 = ttk.Labelframe(rframe4, text="Staff User OU's")
#     self.lbl_frame6.grid(sticky="new", columnspan=2, row=2, padx=10, pady=5)

#     self.lbl_frame7 = ttk.Labelframe(rframe4, text="Student User OU's")
#     self.lbl_frame7.grid(sticky="new", columnspan=2, row=3, padx=10, pady=5)

#     self.tree3 = ttk.Treeview(lframe4, column=("c1", "c2", "c3"), show="headings")
#     self.tree3.column("# 1", anchor=ttk.CENTER)
#     self.tree3.heading("# 1", text="USERNAME")
#     self.tree3.column("# 2", anchor=ttk.CENTER)
#     self.tree3.heading("# 2", text="DISPLAY NAME")
#     self.tree3.column("# 3", anchor=ttk.CENTER)
#     self.tree3.heading("# 3", text="USER DN")
#     self.tree3.bind("<ButtonRelease-1>", self.selectItem2)
#     self.tree3.grid(row=0, columnspan=2, sticky=ttk.NSEW, padx=7, pady=5)

#     scrollbar = ttk.Scrollbar(lframe4, orient=ttk.VERTICAL, bootstyle="primary-round")
#     scrollbar.config(command=self.tree3.yview)
#     scrollbar.grid(row=0, column=2, sticky="nsw", pady=5)
#     scrollbar2 = ttk.Scrollbar(
#         lframe4, orient=ttk.HORIZONTAL, bootstyle="primary-round"
#     )
#     scrollbar2.config(command=self.tree3.xview)
#     scrollbar2.grid(column=0, columnspan=2, sticky="new", padx=10)

#     self.lbl_frameF2 = ttk.Labelframe(lframe4, text="Move To Campus")
#     self.lbl_frameF2.grid(sticky="esw", columnspan=2, row=2, padx=10, pady=10)
#     self.McampH2 = ttk.StringVar(self.lbl_frameF2, "balaklava")

#     self.lbl_frame8 = ttk.Labelframe(lframe4, text="Move To OU")
#     self.lbl_frame8.grid(column=0, columnspan=2, sticky="new", padx=10, pady=5)


def Tab5(self, tab5):
    lbl_title5 = ttk.Label(tab5, text="Active Directory Edit Users")
    lbl_title5.grid(sticky="n", columnspan=4, padx=10)

    tab5.columnconfigure(0, weight=1)
    tab5.columnconfigure(1, weight=1)

    lframe5 = ttk.Frame(tab5)
    rframe5 = ttk.Frame(tab5)

    rframe5.rowconfigure(0, weight=1)
    rframe5.rowconfigure(1, weight=1)
    rframe5.columnconfigure(0, weight=1)

    lframe5.columnconfigure(0, weight=1)

    lframe5.grid(sticky="nsew", column=0, row=1, pady=10)
    rframe5.grid(sticky="nsew", column=1, row=1, pady=10, padx=10)

    self.lbl_frameG = ttk.Labelframe(lframe5, text="Campus")
    self.lbl_frameG.grid(sticky=ttk.EW, columnspan=2, row=0, padx=10, pady=5)
    self.EcampH = ttk.StringVar(self.lbl_frameG, "balaklava")
    self.lbl_frame9 = ttk.Labelframe(lframe5, text="Staff User OU's")
    self.lbl_frame9.grid(sticky="new", columnspan=2, row=2, padx=10, pady=5)

    # self.lbl_frame10 = ttk.Labelframe(lframe5, text="Student User OU's")
    # self.lbl_frame10.grid(sticky="new", columnspan=2, row=3, padx=10, pady=5)

    self.tree4 = ttk.Treeview(rframe5, column=("c1", "c2"), show="headings", height=18)
    self.tree4.column("# 1", anchor=ttk.CENTER)
    self.tree4.heading("# 1", text="USERNAME")
    self.tree4.column("# 2", anchor=ttk.CENTER)
    self.tree4.heading("# 2", text="DISPLAY NAME")
    self.tree4.bind("<ButtonRelease-1>", self.selectItem3)
    scrollbar = ttk.Scrollbar(rframe5, orient=ttk.VERTICAL, bootstyle="primary-round")
    scrollbar.config(command=self.tree4.yview)
    scrollbar.grid(sticky=ttk.NS, row=0, column=2, rowspan=2, pady=5)
    scrollbar2 = ttk.Scrollbar(
        rframe5, orient=ttk.HORIZONTAL, bootstyle="primary-round"
    )
    scrollbar2.config(command=self.tree4.xview)
    scrollbar2.grid(sticky=ttk.EW, row=2, columnspan=3, padx=15)
    self.tree4.grid(sticky=ttk.EW, columnspan=3, row=0, rowspan=2, padx=15, pady=5)

    lbl_frame11 = ttk.Labelframe(rframe5, text="Attributes")
    lbl_frame11.grid(sticky="new", row=3, columnspan=3, padx=5, pady=5)

    lbl_frame11.rowconfigure(0, weight=0, pad=20)
    lbl_frame11.rowconfigure(1, weight=0, pad=20)
    lbl_frame11.rowconfigure(2, weight=0, pad=20)

    lblfname = ttk.Label(lbl_frame11, text="Firstname")
    lblfname.grid(sticky="nw", column=0, row=0, padx=10, pady=5)

    lbllname = ttk.Label(lbl_frame11, text="Lastname")
    lbllname.grid(sticky="nw", column=1, row=0, padx=10, pady=5)

    lbldomain = ttk.Label(lbl_frame11, text="Domain")
    lbldomain.grid(sticky="nw", column=2, row=0, padx=10, pady=5)

    self.fname_entry = ttk.Entry(lbl_frame11, width=20)
    self.fname_entry.grid(sticky="sew", column=0, row=0, padx=10, pady=5)

    self.lname_entry = ttk.Entry(lbl_frame11, width=30)
    self.lname_entry.grid(sticky="sew", column=1, row=0, padx=10, pady=5)

    self.entDomain = ttk.Entry(lbl_frame11, width=35)
    self.entDomain["state"] = "readonly"
    self.entDomain.grid(sticky="sew", column=2, row=0, padx=10, pady=5)

    lbllsname = ttk.Label(lbl_frame11, text="Login")
    lbllsname.grid(sticky="nw", column=0, row=1, padx=10, pady=5)

    self.entSamname = ttk.Entry(lbl_frame11, width=20)
    self.entSamname.grid(sticky="sew", column=0, row=1, padx=10, pady=5)

    lbllPass = ttk.Label(lbl_frame11, text="Password")
    lbllPass.grid(sticky="nw", column=1, row=1, padx=10, pady=5)

    self.entPass = ttk.Entry(lbl_frame11, width=30)
    self.entPass.grid(sticky="sew", column=1, row=1, padx=10, pady=5)

    lbllDesc = ttk.Label(lbl_frame11, text="Description")
    lbllDesc.grid(sticky="nw", column=2, row=1, padx=10, pady=5)

    self.entDesc = ttk.Entry(lbl_frame11, width=35)
    self.entDesc.grid(sticky="sew", column=2, row=1, padx=10, pady=5)

    lbltitle = ttk.Label(lbl_frame11, text="Title (Signature)")
    lbltitle.grid(sticky="nw", column=0, row=2, padx=10, pady=5)

    self.entJobTitle = ttk.Entry(lbl_frame11)
    self.entJobTitle.grid(sticky="sew", column=0, row=2, columnspan=2, padx=10, pady=5)

    lbldep = ttk.Label(lbl_frame11, text="Department (Signature sub title)")
    lbldep.grid(sticky="nw", column=2, row=2, padx=10, pady=5)

    self.entDep = ttk.Entry(lbl_frame11, width=35)
    self.entDep.grid(sticky="sew", column=2, row=2, padx=10, pady=5)


# def Tab6(self, tab6):
#     lbl_title6 = ttk.Label(tab6, text="Active Directory Disable Users")
#     lbl_title6.grid(sticky="n", columnspan=4, padx=10)

#     tab6.columnconfigure(0, weight=1)
#     tab6.columnconfigure(1, weight=1)

#     lframe4 = ttk.Frame(tab6)
#     rframe4 = ttk.Frame(tab6)

#     rframe4.rowconfigure(0, weight=0, pad=26)

#     lframe4.rowconfigure(1, weight=0, pad=26)
#     lframe4.rowconfigure(2, weight=1)

#     lframe4.grid(sticky=ttk.NSEW, column=0, row=1, pady=10, padx=5)
#     rframe4.grid(sticky=ttk.NSEW, column=1, row=1, pady=10, padx=5)

#     self.lbl_frameC6 = ttk.LabelFrame(lframe4, text="Campus")
#     self.lbl_frameC6.grid(sticky=ttk.EW, columnspan=2, row=1, padx=15, pady=5)

#     self.tree6 = ttk.Treeview(lframe4, column=("c1", "c2", "c3"), show="headings")
#     self.tree6.column("# 1", anchor=ttk.CENTER)
#     self.tree6.heading("# 1", text="USERNAME")
#     self.tree6.column("# 2", anchor=ttk.CENTER)
#     self.tree6.heading("# 2", text="DISPLAY NAME")
#     self.tree6.column("# 3", anchor=ttk.CENTER)
#     self.tree6.heading("# 3", text="USER DN")
#     self.tree6.bind("<ButtonRelease-1>", self.selectItem6)
#     self.tree6.grid(sticky=ttk.NS, row=2, column=0, rowspan=2, pady=5)
#     # self.tree6.grid(row=2, columnspan=2, sticky=ttk.NSEW, padx=7, pady=5)

#     scrollbar = ttk.Scrollbar(lframe4, orient=ttk.VERTICAL, bootstyle="primary-round")
#     scrollbar.config(command=self.tree6.yview)
#     scrollbar.grid(row=2, column=2, rowspan=2, sticky=ttk.NS, pady=5, padx=5)
#     scrollbar2 = ttk.Scrollbar(
#         lframe4, orient=ttk.HORIZONTAL, bootstyle="primary-round"
#     )
#     scrollbar2.config(command=self.tree6.xview)
#     scrollbar2.grid(column=0, columnspan=2, sticky="new", padx=10)

#     lbl_frameC7 = ttk.LabelFrame(rframe4, text="Disable OU's")
#     lbl_frameC7.grid(sticky="ew", column=0, columnspan=2, row=1, padx=10, pady=5)

#     lbl_frameC7.columnconfigure(0, weight=1)
#     self.disVals = ttk.StringVar(lbl_frameC7)
#     self.cmbDisable = ttk.Combobox(lbl_frameC7, textvariable=self.disVals, width=60)
#     self.cmbDisable.grid(columnspan=2, row=0, padx=10, pady=15)
#     self.cmbDisable.set("Select OU")
#     self.cmbDisable.bind("<<ComboboxSelected>>", self.disableSelect)
#     self.McampH6 = ttk.StringVar(self.lbl_frameC6, "balaklava")

#     self.lbl_frame9S = ttk.LabelFrame(lframe4, text="Staff Groups")
#     self.lbl_frame9S.grid(sticky="ew", column=0, columnspan=2, row=4, padx=10, pady=15)
#     self.lbl_frame9STU = ttk.LabelFrame(lframe4, text="Students Groups")
#     self.lbl_frame9STU.grid(sticky="ew", column=0, columnspan=2, row=5, padx=10)

#     self.tree7 = ttk.Treeview(rframe4, column=("c1", "c2", "c3"), show="headings")
#     self.tree7.column("# 1", anchor=ttk.CENTER)
#     self.tree7.heading("# 1", text="USERNAME")
#     self.tree7.column("# 2", anchor=ttk.CENTER)
#     self.tree7.heading("# 2", text="DISPLAY NAME")
#     self.tree7.column("# 3", anchor=ttk.CENTER)
#     self.tree7.heading("# 3", text="USER DN")
#     # self.tree7.grid(row=3, columnspan=2, sticky=ttk.NSEW, padx=7, pady=5)
#     self.tree7.grid(sticky=ttk.NS, row=3, column=0, rowspan=2, pady=5, padx=5)
#     scrollbar3 = ttk.Scrollbar(rframe4, orient=ttk.VERTICAL, bootstyle="primary-round")
#     scrollbar3.config(command=self.tree7.yview)
#     scrollbar3.grid(row=3, column=2, rowspan=2, sticky=ttk.NS, pady=5)
#     scrollbar4 = ttk.Scrollbar(
#         rframe4, orient=ttk.HORIZONTAL, bootstyle="primary-round"
#     )
#     scrollbar4.config(command=self.tree7.xview)
#     scrollbar4.grid(column=0, row=5, sticky=ttk.EW, padx=10)
