import tkinter as tk
from tkinter import ttk
from Functions import Version, setTheme, base64, loadConfig, saveConfig
# import sv_ttk
from icon import image


def Window(self):
    self.W,self.H = 665,755
    screen_width = self.winfo_screenwidth()
    screen_height = self.winfo_screenheight()
    center_x = int(screen_width/2 - self.W / 2)
    center_y = int(screen_height/2 - self.H / 2)
    self.geometry(f'{self.W}x{self.H}+{center_x}+{center_y}')
    self.resizable(0, 0)
    self.attributes("-fullscreen", False)


def Icon(self):
    photo = tk.PhotoImage('::img::test', master=self, data=image)
    self.wm_iconphoto(False, photo)


def baseGUI(self):
    
    Window(self)
    Icon(self)
    
    menubar = tk.Menu(self, activebackground='white', activeforeground='black')
    self.file = tk.Menu(menubar, tearoff=0)
    self.file.add_checkbutton(label="Auto Load", variable=self.load, command=self.setLoad)
    self.file.add_command(label="Load", command=lambda: loadConfig(self, True), state=tk.DISABLED)
    self.file.add_command(label="Save", command=lambda: saveConfig(self))
    # self.file.add_separator()
    # # self.file.add_command(label="Import", command=self.importConfig, state=tk.DISABLED)
    # self.file.add_separator()
    self.file.add_command(label="Exit", command=self.quit)
    # # self.theme = tk.Menu(menubar, tearoff=0)
    # # self.theme.add_command(label="Light", command=lambda: setTheme(self, "light"))
    # # self.theme.add_command(label="Dark", command=lambda: setTheme(self, "dark"))
    
    
    menubar.add_cascade(label="File", menu=self.file)
    # # menubar.add_cascade(label="Theme", menu=self.theme)
    self.config(menu=menubar)

    self.tabControl = ttk.Notebook(self)
  
    tab1 = ttk.Frame(self.tabControl)    
    self.tab2 = ttk.Frame(self.tabControl)
    tab3 = ttk.Frame(self.tabControl)
    tab4 = ttk.Frame(self.tabControl)
    tab5 = ttk.Frame(self.tabControl)
    
    self.tab2.columnconfigure(0, weight=1)
    self.tab2.columnconfigure(1, weight=1)
    self.tab2.columnconfigure(2, weight=0)
    self.tab2.rowconfigure(1, weight=0, pad=30)    
    
    tab1.rowconfigure(1, weight=1)
    tab1.columnconfigure(0, weight=1)
    
    tab3.rowconfigure(2, weight=1)
    tab3.columnconfigure(0, weight=1)
    
    tab4.rowconfigure(3, weight=1)
    tab4.columnconfigure(0, weight=1)

    tab5.rowconfigure(3, weight=1)
    tab5.columnconfigure(0, weight=1)

    self.columnconfigure(1, weight=1)
    self.columnconfigure(0, weight=0, pad=70)
    self.rowconfigure(0, weight=1)

    self.tabControl.add(tab1, text ='Locked Users')
    self.tabControl.add(self.tab2, text ='New Users')
    # self.tabControl.add(tab3, text ='Disabled User')
    # self.tabControl.add(tab4, text ='Move User')
    self.tabControl.add(tab5, text ='Edit User')
    self.tabControl.bind('<<NotebookTabChanged>>',self.alterButton)
    self.tabControl.grid(column=0, row=0, columnspan=4, sticky='nsew')

    Tab1(self, tab1)
    Tab2(self, self.tab2)
    Tab3(self, tab3)
    Tab4(self, tab4)
    Tab5(self, tab5)
    
    self.btn_unlockAll = tk.Button(self, text="Unlock All", width=20, command=self.unlockAll)
    self.btn_unlockAll.grid(sticky='e', column=3, row=2, padx=10, pady=5)
    self.btn_unlockAll.configure(state=tk.DISABLED)

    lbl_company = tk.Label(self, text="Company:")
    lbl_company.grid(sticky='w', row=2, column=0, padx=10, pady=5)

    self.options = tk.StringVar(self)
    value = base64.b64decode(self.company).decode("UTF-8").split(",")
    self.combobox = ttk.Combobox(self, textvariable=self.options, width=32)    
    self.combobox['values'] = value
    self.combobox['state'] = 'readonly'
    self.combobox.set("Select Company")
    self.combobox.bind('<<ComboboxSelected>>', self.comboSelect)
    self.combobox.grid(sticky='ens', column=0, row=2, padx=10, pady=5)

    self.status = tk.Label(self, text="Idle...")
    self.status.grid(sticky='w',column=0, row=3, padx=10)
    version = tk.Label(self, text=Version)
    version.grid(sticky='e', column=3, row=3, padx=10)
    self.progress = ttk.Progressbar(self)
    self.progress.grid(sticky='sew', row=5, columnspan=4)
    
def Tab1(self, tab1):
    
    lbl_title = tk.Label(tab1,text="Active Directory Locked Users")
    lbl_title.grid(sticky='n', columnspan=4, padx=10, pady=5)
    
    self.tree = ttk.Treeview(tab1, column=("c1", "c2", "c3"), show='headings')
    scrollbar = tk.Scrollbar(tab1)
    scrollbar.config(command=self.tree.yview)
    scrollbar.grid(sticky=tk.NSEW,row=1, column=4)
    scrollbar2 = tk.Scrollbar(tab1)
    scrollbar2.config(command=self.tree.xview, orient=tk.HORIZONTAL)
    scrollbar2.grid(sticky=tk.NSEW, row=2, columnspan=4)

    self.tree.config(yscrollcommand=scrollbar.set, xscrollcommand=scrollbar2.set)
    self.tree.column("# 1", anchor=tk.CENTER)
    self.tree.heading("# 1", text="USERNAME")
    self.tree.column("# 2", anchor=tk.CENTER)
    self.tree.heading("# 2", text="DISPLAY NAME")
    self.tree.column("# 3", anchor=tk.CENTER)
    self.tree.heading("# 3", text="OU")
    self.tree.bind('<ButtonRelease-1>', self.selectItem)
    self.tree.grid(sticky=tk.NSEW, row=1, columnspan=4, padx=10)

    self.btn_search = tk.Button(tab1, text="Load", width=20, command=self.loadUsers)
    self.btn_search.grid(sticky='e', row=3, column=3, padx=10, pady=10)
    self.btn_search.configure(state=tk.DISABLED)

    self.btn_userUnlock = tk.Button(tab1, text="Unlock User", width=20, command=self.unlockUsers)
    self.btn_userUnlock.grid(sticky='w', row=3, column=0, padx=10, pady=10)
    self.btn_userUnlock.configure(state=tk.DISABLED)

    lbl_password = tk.Label(tab1, text="Password:")
    lbl_password.grid(sticky='wn', row=4, column=0, padx=10)

    self.passBox = tk.Entry(tab1, width=30)
    self.passBox.grid(sticky='ws', row=4, column=0, padx=10, pady=10)

    self.btn_reset = tk.Button(tab1, text="Reset Password", width=20, command=self.resetPass)
    self.btn_reset.grid(sticky='es', row=4, column=3, padx=10, pady=10)
    self.btn_reset.configure(state=tk.DISABLED)

def Tab2(self, tab2):
    lbl_title = tk.Label(tab2,text="Active Directory New Users")
    lbl_title.grid(sticky='n', columnspan=3, padx=10, pady=5)

    lbl_fname = tk.Label(tab2, text="Firstname:")
    lbl_fname.grid(sticky='wn', column=0, row=1, padx=10, pady=10)
    self.fname = tk.Entry(tab2, width=40)
    self.fname.grid(sticky='en', column=0, row=1, padx=10, pady=10)
    lbl_lname = tk.Label(tab2, text="Lastname:")
    lbl_lname.grid(sticky='wn', column=1, row=1, padx=10, pady=10)
    self.lname = tk.Entry(tab2, width=40)
    self.lname.grid(sticky='en', column=1, row=1, padx=10, pady=10)

    self.frame = ttk.Frame(tab2)
    self.frame.grid(sticky='sew', columnspan=3, row=1, padx=10)
    self.frame.columnconfigure(0, weight=1)

    self.samFormat = tk.StringVar(tab2, "flastname")    
    f_last = tk.Radiobutton(self.frame, text="flastname", variable=self.samFormat, value="flastname")
    f_last.grid(sticky='nse', row=0, padx=10)

    f_dot_last = tk.Radiobutton(self.frame, text="first.last", variable=self.samFormat, value="first.lastname")
    f_dot_last.grid(sticky='sn', row=0, padx=10)

    first_last = tk.Radiobutton(self.frame, text="firstlast", variable=self.samFormat, value="firstlastname")
    first_last.grid(sticky='nsw', row=0, padx=10)

    self.lbl_frameC = tk.LabelFrame(tab2, text="Campus")
    self.lbl_frameC.grid(sticky='ew',columnspan=3, row=2, padx=10, pady=5)
    
    self.lbl_frame = tk.LabelFrame(tab2, text="Staff Position")
    self.lbl_frame.grid(sticky='ew',columnspan=3, row=3, padx=10, pady=5)

    self.lbl_frame4 = tk.LabelFrame(tab2, text="Students Position")
    self.lbl_frame4.grid(sticky='ew',columnspan=3, row=4, padx=10, pady=5)

    lbl_groups = tk.Label(tab2, text="Add Groups")
    lbl_groups.grid(sticky='wn',column=0, row=5, padx=10, pady=5)

    self.add_groups = tk.StringVar(tab2, "Select Group")
    self.ex_groups = ttk.Combobox(tab2, textvariable=self.add_groups, width=35)
    self.ex_groups['state'] = 'readonly'
    self.ex_groups.grid(sticky='en', column=0, row=5, padx=10, pady=5)

    self.addGroup = tk.Button(tab2, text="Add Group", width=20, command=self.addToGroups)
    self.addGroup['state']=tk.DISABLED
    self.addGroup.grid(sticky='en', column=1, row=5, padx=10, pady=5)

    self.lbl_frame2 = tk.LabelFrame(tab2, text="Groups")
    self.lbl_frame2.grid(sticky='ew',columnspan=3, row=6, padx=10, pady=5)

    self.lbl_domains = tk.Label(tab2, text="Domains:")
    self.lbl_domains.grid(sticky='nw', column=0, row=7, padx=10, pady=5)

    self.primary_domain = tk.StringVar(tab2, "Select Domain")
    self.combo_domain = ttk.Combobox(tab2, textvariable=self.primary_domain, width=37)    
    self.combo_domain['state'] = 'readonly'
    self.combo_domain.grid(sticky='ne', column=0, row=7, padx=10, pady=5)
    
    lbl_dpass = tk.Label(tab2, text="Password:")
    lbl_dpass.grid(sticky='wn', column=1, row=7, padx=10, pady=5)

    self.dpass = tk.Entry(tab2, width=40)
    self.dpass.grid(sticky='en', column=1, row=7, padx=10, pady=5)

    self.lbl_frame3 = tk.LabelFrame(tab2, text="Profile")
    self.lbl_frame3.grid(sticky='ew',columnspan=3, row=8, padx=10, pady=2)

    lbl_homeDrive = tk.Label(self.lbl_frame3, text="Home Drive:")
    lbl_homeDrive.grid(sticky='wn', column=0, row=0, padx=10, pady=10)

    self.hdrive = tk.StringVar(self.lbl_frame3,"Select Drive")
    self.combo_hdrive = ttk.Combobox(self.lbl_frame3, textvariable=self.hdrive, width=15)
    self.combo_hdrive['values'] = str("A,B,C,D,E,F,G,H,I,J,K,L,M,N,O,P,Q,R,S,T,U,V,W,X,Y,Z").split(",")
    self.combo_hdrive['state'] = 'readonly'
    self.combo_hdrive.bind('<<ComboboxSelected>>', self.driveSelect)
    self.combo_hdrive.grid(sticky='en', column=1, row=0, padx=10, pady=10)

    lbl_homePath = tk.Label(self.lbl_frame3, text="Home Path:")
    lbl_homePath.grid(sticky='wn', column=2, row=0, padx=10, pady=10)

    self.paths = tk.StringVar(self.lbl_frame3, "Select Homepath")
    self.homePath = ttk.Combobox(self.lbl_frame3, textvariable=self.paths, width=40)
    self.homePath['state'] = 'readonly'
    self.homePath.grid(sticky='en', column=3, row=0, padx=10, pady=10)
    
    lbl_desc = tk.Label(self.lbl_frame3, text="Description:")
    lbl_desc.grid(sticky='ws', column=0, row=1, padx=10, pady=10)

    self.desc = tk.Entry(self.lbl_frame3, width=18)
    self.desc.insert(0,self.date)
    self.desc.grid(sticky='es', column=1, row=1, padx=10, pady=10)

    lbl_jobTitle = tk.Label(self.lbl_frame3, text="Job Title:")
    lbl_jobTitle.grid(sticky='ws', column=2, row=1, padx=10, pady=10)

    self.jobTitleEnt = tk.Entry(self.lbl_frame3, width=43)
    self.jobTitleEnt.grid(sticky='en', column=3, row=1, padx=10, pady=10)
    
    self.campH = tk.IntVar(self.lbl_frameC, 1)
    
    # clare = tk.Radiobutton(self.lbl_frameC, text="Clare", variable=self.campH, value=0, command=lambda:self.comboSelect(""))
    # balak.pack(side="left", fill=tk.BOTH, expand=True)
    # clare.pack(side="right", fill=tk.BOTH, expand=True)
    

def Tab3(self, tab3):
    lbl_title = tk.Label(tab3, text="Disabled User Group Cleanup")
    lbl_title.grid(sticky='n', columnspan=4, padx=10, pady=5)

    self.lbl_frame5 = ttk.Labelframe(tab3, text="Disabled User OU\'s")
    self.lbl_frame5.grid(sticky='new', columnspan=4, row=1, padx=10, pady=5)

    self.tree2 = ttk.Treeview(tab3, column=("c1", "c2", "c3"), show='headings')
    scrollbar = tk.Scrollbar(tab3)
    scrollbar.config(command=self.tree2.yview)
    scrollbar.grid(sticky=tk.NSEW,row=2, column=4)
    scrollbar2 = tk.Scrollbar(tab3)
    scrollbar2.config(command=self.tree2.xview, orient=tk.HORIZONTAL)
    scrollbar2.grid(sticky=tk.NSEW, row=3, columnspan=4)

    self.tree2.column("# 1", anchor=tk.CENTER)
    self.tree2.heading("# 1", text="USERNAME")
    self.tree2.column("# 2", anchor=tk.CENTER)
    self.tree2.heading("# 2", text="DISPLAY NAME")
    self.tree2.column("# 3", anchor=tk.CENTER)
    self.tree2.heading("# 3", text="OU")
    self.tree2.grid(sticky='nsew', row=2, columnspan=4, padx=5)

def Tab4(self, tab4):
    lbl_title4 = tk.Label(tab4, text="Active Directory Move Users")
    lbl_title4.grid(sticky='n', columnspan=4, padx=10)

    self.lbl_frame6 = ttk.Labelframe(tab4, text="Staff User OU\'s")
    self.lbl_frame6.grid(sticky='new', columnspan=4, row=1, padx=10, pady=5)

    self.lbl_frame7 = ttk.Labelframe(tab4, text="Student User OU\'s")
    self.lbl_frame7.grid(sticky='new', columnspan=4, row=2, padx=10, pady=5)
    
    self.tree3 = ttk.Treeview(tab4, column=("c1", "c2", "c3"), show='headings')
    scrollbar = tk.Scrollbar(tab4)
    scrollbar.config(command=self.tree3.yview)
    scrollbar.grid(sticky=tk.NSEW,row=3, column=4)
    scrollbar2 = tk.Scrollbar(tab4)
    scrollbar2.config(command=self.tree3.xview, orient=tk.HORIZONTAL)
    scrollbar2.grid(sticky=tk.NSEW, row=4, columnspan=4)
    
    self.tree3.column("# 1", anchor=tk.CENTER)
    self.tree3.heading("# 1", text="USERNAME")
    self.tree3.column("# 2", anchor=tk.CENTER)
    self.tree3.heading("# 2", text="DISPLAY NAME")
    self.tree3.column("# 3", anchor=tk.CENTER)
    self.tree3.heading("# 3", text="OU")
    self.tree3.bind('<ButtonRelease-1>', self.selectItem2)
    self.tree3.grid(sticky='nsew', row=3, columnspan=4, padx=10)

    self.lbl_frame8 = ttk.Labelframe(tab4, text="Move To OU")
    self.lbl_frame8.grid(sticky='new', columnspan=4, row=5, padx=10, pady=5)

    self.move_btn = tk.Button(tab4, text="Move User", width=20, command=self.moveUser)
    self.move_btn.configure(state=tk.DISABLED)
    self.move_btn.grid(sticky='w', column=0, row=6, padx=10, pady=10)

def Tab5(self, tab5):
    lbl_title5 = tk.Label(tab5, text="Active Directory Edit Users")
    lbl_title5.grid(sticky='n', columnspan=4, padx=10)

    self.lbl_frame9 = ttk.Labelframe(tab5, text="Staff User OU\'s")
    self.lbl_frame9.grid(sticky='new', columnspan=4, row=1, padx=10, pady=5)

    self.lbl_frame10 = ttk.Labelframe(tab5, text="Student User OU\'s")
    self.lbl_frame10.grid(sticky='new', columnspan=4, row=2, padx=10, pady=5)
    
    self.tree4 = ttk.Treeview(tab5, column=("c1", "c2", "c3"), show='headings')
    self.tree4.column("# 1", anchor=tk.CENTER)
    self.tree4.heading("# 1", text="USERNAME")
    self.tree4.column("# 2", anchor=tk.CENTER)
    self.tree4.heading("# 2", text="DISPLAY NAME")
    self.tree4.column("# 3", anchor=tk.CENTER)
    self.tree4.heading("# 3", text="OU")
    self.tree4.bind('<ButtonRelease-1>', self.selectItem3)
    scrollbar = tk.Scrollbar(tab5)
    scrollbar.config(command=self.tree4.yview)
    scrollbar.grid(sticky=tk.NSEW,row=3, column=4)
    scrollbar2 = tk.Scrollbar(tab5)
    scrollbar2.config(command=self.tree4.xview, orient=tk.HORIZONTAL)
    scrollbar2.grid(sticky=tk.NSEW, row=4, columnspan=4)
    self.tree4.grid(sticky=tk.NSEW, row=3, columnspan=4, padx=10)

    lbl_frame11 = ttk.Labelframe(tab5, text="Attributes")
    lbl_frame11.grid(sticky='new', columnspan=4, padx=10, pady=5)
    
    lbl_frame11.rowconfigure(0, weight=0, pad=20)
    lbl_frame11.rowconfigure(1, weight=0, pad=20)
    lbl_frame11.rowconfigure(2, weight=0, pad=20)

    lblfname = tk.Label(lbl_frame11, text="Firstname")
    lblfname.grid(sticky='nw', column=0, row=0, padx=10, pady=5)

    lbllname = tk.Label(lbl_frame11, text="Lastname")
    lbllname.grid(sticky='nw', column=1, row=0, padx=10, pady=5)

    lbldomain = tk.Label(lbl_frame11, text="Domain")
    lbldomain.grid(sticky='nw', column=2, row=0, padx=10, pady=5)

    self.fname_entry = tk.Entry(lbl_frame11, width=30)
    self.fname_entry.grid(sticky='sew', column=0, row=0, padx=10, pady=5)

    self.lname_entry = tk.Entry(lbl_frame11, width=30)
    self.lname_entry.grid(sticky='sew', column=1, row=0, padx=10, pady=5)

    self.entDomain = tk.Entry(lbl_frame11, width=30)
    self.entDomain['state'] = 'readonly'
    self.entDomain.grid(sticky='sew', column=2, row=0, padx=10, pady=5)

    lbllsname = tk.Label(lbl_frame11, text="Login")
    lbllsname.grid(sticky='nw', column=0, row=1, padx=10, pady=5)

    self.entSamname = tk.Entry(lbl_frame11, width=30)
    self.entSamname.grid(sticky='sew', column=0, row=1, padx=10, pady=5)

    lbltitle = tk.Label(lbl_frame11, text="Title")
    lbltitle.grid(sticky='nw', column=1, row=1, padx=10, pady=5)

    self.entJobTitle = tk.Entry(lbl_frame11, width=30)
    self.entJobTitle.grid(sticky='sew', column=1, row=1, padx=10, pady=5)

    lbllDesc = tk.Label(lbl_frame11, text="Description")
    lbllDesc.grid(sticky='nw', column=2, row=1, padx=10, pady=5)

    self.entDesc = tk.Entry(lbl_frame11, width=30)
    self.entDesc.grid(sticky='sew', column=2, row=1, padx=10, pady=5)

    lbllPass = tk.Label(lbl_frame11, text="Password")
    lbllPass.grid(sticky='nw', column=0, row=2, padx=10, pady=5)

    self.entPass = tk.Entry(lbl_frame11, width=30)
    self.entPass.grid(sticky='sew', column=0, row=2, padx=10, pady=5)
