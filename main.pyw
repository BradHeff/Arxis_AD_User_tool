import datetime
# from Importer import convertCSV, updateSettings, getTitleWindow
import threading
import tkinter as tk
from tkinter import Radiobutton, Checkbutton
import splash
import Functions as f
import Gui

class ADUnlocker(tk.Tk):
    def __init__(self):
        super(ADUnlocker, self).__init__()
        # global root
        
        # root.destroy()
                
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
        
        self.server = ""
        self.username = ""
        self.password = ""
        self.ou = ""
        self.posOU = ""
        self.domainName = ""
        self.company = ""
        self.samFormat = ""
        self.groupPos = ""
        self.movePosOU = ""

        self.expiredOU = None
        self.compFail = False
        self.servs = False
        self.isRunning = False
        self.loadConfig = False
        self.isExit = False
        self.data_file = False

        self.checkCount = 0
        self.checkRow = 0

        self.load = tk.BooleanVar(self, False)
        self.comp = "Select Company"
        
        currentDateTime = datetime.datetime.now()
        date = currentDateTime.date()
        self.date = date.strftime("%Y")
        
        f.getSettings(self)        
        
        self.error = f.checkSettings(self)
        
        Gui.baseGUI(self)
        
        self.title(''.join(["Horizon AD User Tool v", f.Version[4:f.Version.__len__()]]))
        
        # self.mainloop()
        
        if self.error:
            self.messageBox("ERROR!!","company settings is incomplete")
        
        self.options.set("Horizon")
        self.comboSelect("")
        if f.path.isfile(f.settings_dir + "Config.ini"):
            print(f.settings_dir + "Config.ini")
            # self.file.entryconfigure(0, state=tk.NORMAL)
        
        if not f.DEBUG:
            self.combobox['state'] = tk.DISABLED
        
        


    def addToGroups(self):
        if "Select" in self.add_groups.get():
            return
        if self.var.get() == "1":
            return
        p = self.lbl_frame2.grid_slaves()
        cont = True
        for y in p:
            if self.add_groups.get() == y['text']:
                cont = False
        if cont:
            if self.checkCount > 3:
                self.checkCount = 0
                self.checkRow += 1
            self.chkBtns[self.add_groups.get()] = tk.IntVar(self.lbl_frame2, 1)
            print([x for x in self.chkBtns])
            rbtn = Checkbutton(self.lbl_frame2, text=self.add_groups.get(), variable=self.chkBtns[self.add_groups.get()], onvalue=1, offvalue=0)
            rbtn.grid(row=self.checkRow, column=self.checkCount, padx=10)
            self.checkCount+=1
        else:
            self.messageBox('ERROR!!!', 'That group already exists!')

    def alterButton(self, widget):
        if self.tabControl.index(self.tabControl.select()) == 0:
            self.btn_unlockAll.configure(text="Unlock All")
            if self.state and self.servs:
                f.widgetStatusFailed(self, False)
        elif self.tabControl.index(self.tabControl.select()) == 1:
            self.btn_unlockAll.configure(text="Create User")
            if "Select" not in self.options.get():
                if not self.compFail:
                    if self.domains['Primary'].__len__() <= 0:
                        f.widgetStatusFailed(self, True)
                        self.messageBox("ERROR!!","Domains Settings is not complete!")
                        return
                    if self.groupPos.__len__() <= 0:
                        f.widgetStatusFailed(self, True)
                        self.messageBox("ERROR!!","Group Settings is not complete!")
                        return
                    if self.positions.__len__() <= 0:
                        f.widgetStatusFailed(self, True)
                        self.messageBox("ERROR!!","Positions Settings is not complete!")
                        return
                else:
                    if self.state:
                        f.widgetStatusFailed(self, True)
        # elif self.tabControl.index(self.tabControl.select()) == 2:
        #     self.btn_unlockAll.configure(text="Remove Groups")
        #     if not self.compFail:
        #         pass
        #     else:
        #         if self.state:
        #             f.widgetStatusFailed(self, True)
        # elif self.tabControl.index(self.tabControl.select()) == 3:
        #     self.btn_unlockAll.configure(text="Bulk Move Users")
        #     if not self.compFail:
        #         pass
        #     else:
        #         if self.state:
        #             f.widgetStatusFailed(self, True)
        elif self.tabControl.index(self.tabControl.select()) == 2:
            self.btn_unlockAll.configure(text="Update User")
            if not self.compFail:
                pass
            else:
                if self.state:
                    f.widgetStatusFailed(self, True)
                            
    def driveSelect(self, l):
        pass        

    def selectItem(self, a):
        curItem = self.tree.focus()
        self.selItem = self.tree.item(curItem)['values']
    
    def selectItem2(self, a):
        curItem = self.tree3.focus()
        self.selItem2 = self.tree3.item(curItem)['values']

    def selectItem3(self, a):
        curItem = self.tree4.focus()
        self.selItem3 = self.tree4.item(curItem)['values']
        self.entDomain['state'] = 'normal'
        self.entDesc.delete(0, 'end')
        self.entJobTitle.delete(0, 'end')
        self.entSamname.delete(0, 'end')
        self.entDomain.delete(0, 'end')
        self.lname_entry.delete(0, 'end')
        self.fname_entry.delete(0, 'end')
        # print(self.updateList[self.selItem3[0]]['proxyAddresses'])
        try:
            domain = str(self.updateList[self.selItem3[0]]['userPrincipalName'])
            domain = domain.split('@')[1].strip()
            self.entDomain.insert(0, domain)
        except:
            pass
        try:
            self.entJobTitle.insert(0, self.updateList[self.selItem3[0]]['title'])
        except:
            pass
        try:
            self.lname_entry.insert(0, self.updateList[self.selItem3[0]]['fname'])
        except:
            pass
        try:
            self.fname_entry.insert(0, self.updateList[self.selItem3[0]]['lname'])
        except:
            pass
        try:
            self.entSamname.insert(0, self.selItem3[0])
        except:
            pass
        try:
            desc = self.updateList[self.selItem3[0]]['description'][0]
            self.entDesc.insert(0, str(desc))
        except:
            pass
        self.entDomain['state'] = 'readonly'

    def getCheck(self):
        grp = []
        for x in self.chkBtns:
            if self.chkBtns.get(x).get() == 1:
                grp.append(x)
        return grp

    def posSelect(self):
        self.clear_group()
        if ("Year" in self.var.get() or "Found" in self.var.get()) and self.campH.get() == 0:
            self.posOU = self.positionsOU[self.var.get()+"-Clare"]
        else:
            self.posOU = self.positionsOU[self.var.get()]
        self.groups = self.groupPos[self.var.get()]
        if self.campH.get() == 0:
            descDate = ''.join([self.date, " Clare"])
        else:
            descDate = self.date
        if "Year" in self.var.get() or "Found" in self.var.get():
            self.desc.delete(0, 'end')
            if "Found" in self.var.get():
                text = ''.join([self.var.get(), " - ", descDate])
            else:
                text = ''.join([self.var.get()[0:4]," ",self.var.get()[4:len(self.var.get())], " - ", descDate])
            self.desc.insert(0, text)
        else:
            self.desc.delete(0, 'end')
            self.desc.insert(0, descDate)
        self.checkCount = 0
        self.checkRow = 0
        for x in self.groups:
            self.chkBtns[x] = tk.IntVar(self.lbl_frame2, 1)
            rbtn = Checkbutton(self.lbl_frame2, text=x, variable=self.chkBtns[x], onvalue=1, offvalue=0)
            rbtn.grid(row=self.checkRow, column=self.checkCount, padx=10)
            self.checkCount+=1
            if self.checkCount > 3:
                self.checkCount = 0
                self.checkRow += 1        
        if not self.jobTitle.__len__() <= 3:
            try:
                self.jobTitleEnt.delete(0, 'end')                
                self.jobTitleEnt.insert(0, self.jobTitle[self.var.get()])
            except:
                pass

    def movePosSelect(self):
        self.movePosOU = self.positionsOU[self.chkValue.get()]

    def updateSelect(self):
        self.entDomain['state'] = 'normal'
        self.entDesc.delete(0, 'end')
        self.entJobTitle.delete(0, 'end')
        self.entSamname.delete(0, 'end')
        self.entDomain.delete(0, 'end')
        self.lname_entry.delete(0, 'end')
        self.fname_entry.delete(0, 'end')
        self.entDomain['state'] = 'readonly'
        t = threading.Thread(target=self.editOption)
        t.daemon = True
        t.start()

    def editOption(self):
        f.pythoncom.CoInitialize()
        self.tree3.delete(*self.tree3.get_children())
        self.var2.set(None)
        list = self.lbl_frame8.grid_slaves()
        for l in list:
            l.destroy()
        self.status['text'] = "Loading Users ...."
        self.updateList = f.listUsers2(self, self.positionsOU[self.var3.get()])
        self.tree4.delete(*self.tree4.get_children())
        self.progress['maximum'] = self.updateList.__len__()
        count = 0
        for i in self.updateList:
            count+=1
            self.progress['value'] = count
            self.tree4.insert('', 'end', values=(i, self.updateList[i]['name'], self.updateList[i]['ou']))
        self.progress['value'] = 0
        self.status['text'] = "Idle..."

    def moveSelect(self):
        t = threading.Thread(target=self.moveOption)
        t.daemon = True
        t.start()

    def moveOption(self):
        f.pythoncom.CoInitialize()
        self.tree4.delete(*self.tree4.get_children())
        self.var3.set(None)
        self.entDomain['state'] = 'normal'
        self.entDesc.delete(0, 'end')
        self.entJobTitle.delete(0, 'end')
        self.entSamname.delete(0, 'end')
        self.entDomain.delete(0, 'end')
        self.lname_entry.delete(0, 'end')
        self.fname_entry.delete(0, 'end')
        self.entDomain['state'] = 'readonly'
        self.status['text'] = "Loading Users ...."
        
        usersList = f.listUsers(self, self.positionsOU[self.var2.get()])
        self.progress['maximum'] = float(usersList.__len__())
        progCount = 1
        self.tree3.delete(*self.tree3.get_children())
        for i in usersList:
            self.progress['value'] = progCount
            self.tree3.insert('', 'end', values=(i, usersList[i]['name'], usersList[i]['ou']))
            progCount+=1
        count = 0
        row = 0
        count2 = 0
        row2 = 0
        
        list = self.lbl_frame8.grid_slaves()
        for l in list:
            l.destroy()
        self.chkValue = tk.StringVar(self.lbl_frame8, "1")
        for j in self.positions:
            for y in self.positions[j]:
                if not "Student" == y:                    
                    rbtn1 = Radiobutton(self.lbl_frame8, text=y, variable=self.chkValue, command=self.movePosSelect, value=y)
                    rbtn1.grid(row=row, column=count, padx=10)
                    rbtn1.selection_clear()
                    count += 1
                    if count > 4:
                        count = 0
                        row += 1
                else:
                    rbtn2 = Radiobutton(self.lbl_frame8, text=y, variable=self.chkValue, command=self.movePosSelect, value=y)
                    rbtn2.grid(row=row, column=count, padx=10)
                    rbtn2.selection_clear()
                    count2 += 1
                    if count2 > 4:
                        count2 = 0
                        row2 += 1
        self.status['text'] = "Idle..."
        self.progress['value'] = 0

    def clear_group(self):
        list = self.lbl_frame2.grid_slaves()
        for l in list:
            l.destroy()

    def clear_campus(self):
        list = self.lbl_frameC.pack_slaves()
        for l in list:
            l.destroy()

    def clear_pos(self):
        list = self.lbl_frame.grid_slaves()
        for l in list:
            l.destroy()
        list = self.lbl_frame4.grid_slaves()
        for l in list:
            l.destroy()

    def clear_exp(self):
        list = self.lbl_frame5.grid_slaves()
        for l in list:
            l.destroy()
    
    def clear_move(self):
        list = self.lbl_frame6.grid_slaves()
        for l in list:
            l.destroy()
        list = self.lbl_frame7.grid_slaves()
        for l in list:
            l.destroy()
        list = self.lbl_frame8.grid_slaves()
        for l in list:
            l.destroy()

    def clear_edit(self):
        list = self.lbl_frame9.grid_slaves()
        for l in list:
            l.destroy()
        list = self.lbl_frame10.grid_slaves()
        for l in list:
            l.destroy()

    def expSelect(self):
        self.expiredOU = self.expiredOUs[self.exOU.get()]
        self.tree2.delete(*self.tree2.get_children())

    def comboSelect(self, widget):
        if not "camp" in str(widget):        
            f.getConfig(self,self.options.get())        
            self.clear_campus()
            if not f.base64.b64decode(self.campus).decode("UTF-8").split(",")[0].__len__() <= 0:
                counter = 1
                for x in f.base64.b64decode(self.campus).decode("UTF-8").split(","):
                    balak = tk.Radiobutton(self.lbl_frameC, text=x, variable=self.campH, value=counter, command=lambda:self.comboSelect("camp"))
                    if counter == 1:
                        balak.pack(side="left",fill=tk.BOTH, expand=True)
                    else:
                        balak.pack(side="right",fill=tk.BOTH, expand=True)
                    counter-=1

        t = threading.Thread(target=self.comboLoad)
        t.daemon = True
        t.start()
        # t.join()

    def comboLoad(self):
        print(self.positions)
        f.pythoncom.CoInitialize()
        self.status['text'] = "Loading..."
        self.clear_pos()        
        self.clear_group()
        self.clear_exp()
        self.clear_move()
        self.clear_edit()
        self.tree4.delete(*self.tree4.get_children())
        self.tree3.delete(*self.tree3.get_children())
        self.tree2.delete(*self.tree2.get_children())
        self.tree.delete(*self.tree.get_children())
        self.desc.delete(0, 'end')
        self.dpass.delete(0, 'end')
        self.jobTitleEnt.delete(0, 'end')
        self.desc.insert(0,self.date)        
        if not self.compFail:
            if not self.positions.__len__() <= 0:
                try:
                    self.progress['value'] = 20
                    count = 0
                    row = 0
                    count2 = 0
                    row2 = 0
                    self.var = tk.StringVar(None,"1")
                    self.var2 = tk.StringVar(None,"1")
                    self.var3 = tk.StringVar(None,"1")
                    for x in self.positions:
                        for y in self.positions[x]:
                            prog = 1
                            self.progress['maximum'] = float(self.positions.__len__())
                            self.progress['value'] = prog                            
                            if not x == "Students":
                                rbtn = Radiobutton(self.lbl_frame, text=y, variable=self.var, command=self.posSelect, value=y)
                                rbtn.grid(row=row, column=count, padx=10)
                                rbtn.selection_clear()
                                rbtn3 = Radiobutton(self.lbl_frame6, text=y, variable=self.var2, command=self.moveSelect, value=y)
                                rbtn3.grid(row=row, column=count, padx=10)
                                rbtn3.selection_clear()
                                rbtn5 = Radiobutton(self.lbl_frame9, text=y, variable=self.var3, command=self.updateSelect, value=y)
                                rbtn5.grid(row=row, column=count, padx=10)
                                rbtn5.selection_clear()
                                count+=1
                                if count > 3:
                                    count = 0
                                    row += 1
                            else:
                                rbtn2 = Radiobutton(self.lbl_frame4, text=y, variable=self.var, command=self.posSelect, value=y)
                                rbtn2.grid(row=row2, column=count2, padx=10)
                                rbtn2.selection_clear()
                                rbtn4 = Radiobutton(self.lbl_frame7, text=y, variable=self.var2, command=self.moveSelect, value=y)
                                rbtn4.grid(row=row2, column=count2, padx=10)
                                rbtn4.selection_clear()
                                rbtn6 = Radiobutton(self.lbl_frame10, text=y, variable=self.var3, command=self.updateSelect, value=y)
                                rbtn6.grid(row=row2, column=count2, padx=10)
                                rbtn6.selection_clear()
                                count2+=1
                                if count2 > 6:
                                    count2 = 0
                                    row2 += 1
                            prog+=1
                except Exception as e:
                    print(e)
            
            if not self.expiredOUs.__len__() <= 0:
                try:
                    self.progress['maximum'] = float(self.expiredOUs.__len__())
                    prog = 1
                    count3 = 0
                    row3 = 0
                    self.exOU = tk.StringVar(None,"1")
                    for i in self.expiredOUs:
                        self.progress['value'] = prog
                        rbtn3 = Radiobutton(self.lbl_frame5, text=i, variable=self.exOU, command=self.expSelect, value=i)
                        rbtn3.grid(row=row3, column=count3, padx=10)
                        rbtn3.selection_clear()
                        count3+=1
                        if count3 > 3:
                            count3 = 0
                            row3 += 1
                        prog+=1
                except:
                    pass
            if not self.domains['Primary'].__len__() <= 0:
                try:
                    self.progress['value'] = 60
                    self.pdomains = self.domains['Primary']
                    self.combo_domain['values'] = self.pdomains
                    self.primary_domain.set("Select Domain")
                except:
                    pass
            if not f.base64.b64decode(self.homePaths).decode("UTF-8").split(",").__len__() <=0:
                try:
                    self.progress['value'] = 70
                    self.homePath['values'] = f.base64.b64decode(self.homePaths).decode("UTF-8").split(",")
                    self.paths.set("Select Homepath")
                    self.hdrive.set("Select Drive")
                except:
                    pass
            if not f.base64.b64decode(self.groupOU).decode("UTF-8").__len__() <=3:
                try:
                    # print(f.base64.b64decode(self.username).decode("UTF-8"))
                    self.progress['value'] = 80
                    # print("START GROUPS SEARCH")
                    self.fullGroups = f.listGroups(self, f.base64.b64decode(self.groupOU).decode("UTF-8"))
                    # print(self.fullGroups)
                    groups = []
                    self.progress['maximum'] = float(self.fullGroups.__len__())
                    prog = 1
                    for x in self.fullGroups:
                        groups.append(x)
                        self.progress['value'] = prog
                        prog+=1
                    self.ex_groups['values'] = groups
                except:
                    pass            
            self.progress['value'] = 0
            self.status['text'] = "Idle..."            
        else:
            if self.state and self.servs:
                f.widgetStatusFailed(self, False)
                self.messageBox("ERROR!!","Some settings are incomplete")
            else:
                f.widgetStatusFailed(self, True)
                self.messageBox("ERROR!!","Server settings are incomplete")


    def resetPass(self):
        if self.selItem.__len__() <= 0:
            self.messageBox("ERROR!!","Must select a user!")
            return
        if self.passBox.get().__len__() < 8:
            self.messageBox("ERROR!!","Password Too Short!")
            return
        f.widgetStatus(self, tk.DISABLED)
        newPass = self.passBox.get()
        t = threading.Thread(target=f.resetPassword, args=[self,self.selItem[2], newPass])
        t.daemon = True
        t.start()        

    def moveUser(self):
        if self.var2.get().__len__() <= 2 or self.movePosOU.__len__() <= 1:
            self.messageBox("ERROR!!","You must select a position!")
            return
        if self.selItem2.__len__() <= 0:
            self.messageBox("ERROR!!","You must select a user!")
            return
        self.status['text'] = "Moving " + str(self.selItem2[1]) + "..."
        f.widgetStatus(self, tk.DISABLED)
        self.progress['max'] = 100
        self.progress['value'] = 30
        t = threading.Thread(target=f.moveUser, args=[self, self.selItem2[2], self.movePosOU])
        t.daemon = True
        t.start()

    def loadUsers(self):
        if "Select" in self.options.get():
            self.messageBox("ERROR!!","You must select a company!")
            return
        f.widgetStatus(self, tk.DISABLED)
        self.tree.delete(*self.tree.get_children())
        t = threading.Thread(target=self.loads, args=[])
        t.daemon = True
        t.start()
        
    def loads(self):
        f.pythoncom.CoInitialize()
        try:
            self.status['text'] = "Searching locked users ..."
            locked = f.listLocked(self)
            if locked.__len__() <= 0:
                f.widgetStatus(self, tk.NORMAL)
                self.status['text'] = "Idle..."
                self.messageBox("SUCCESS!!","No Locked Users!")
                return
            self.status['text'] = "Populating list..."
            for x in locked:
                self.tree.insert('', 'end', values=(x, locked[x]['name'], locked[x]['ou']))
        except:
            self.messageBox("Error", "An error occurred, Check settings")

        f.widgetStatus(self, tk.NORMAL)
        self.status['text'] = "Idle..."

    def unlockUsers(self):
        if self.tree.get_children() == ():
            self.messageBox("ERROR!!","List cannot be empty!")
            return
        
        if self.selItem.__len__() <= 0:
            self.messageBox("ERROR!!","Must select a user!")
            return
        
        f.widgetStatus(self, tk.DISABLED)
                
        f.unlockUser(self,self.selItem[2])
        selected_item = self.tree.selection()[0]
        self.tree.delete(selected_item)
        self.selItem = []
        self.messageBox("SUCCESS!!","Unlock Complete!")

    def unlockAll(self):
        f.widgetStatus(self, tk.DISABLED)
        if self.tabControl.index(self.tabControl.select()) == 0:
            if self.tree.get_children() == ():
                f.widgetStatus(self, tk.NORMAL)
                self.messageBox("ERROR!!","List cannot be empty!")
                return
            for line in self.tree.get_children():
                self.data[self.tree.item(line)['values'][0]] = {"name":self.tree.item(line)['values'][1],
                                "ou":self.tree.item(line)['values'][2]}
            maxs = self.tree.get_children().__len__()
            self.progress["maximum"] = float(maxs)
            self.all = maxs
            t = threading.Thread(target=f.unlockAll, args=[self,self.data])
            t.daemon = True
            t.start()
        elif self.tabControl.index(self.tabControl.select()) == 1:
            f.widgetStatus(self, tk.DISABLED)
            if not self.compFail:
                data = dict()
                if self.fname.get().__len__() >= 2 and self.lname.get().__len__() >= 2:
                    if not self.dpass.get().__len__() < 8:
                        if "Select" not in self.primary_domain.get() and "Select" not in self.hdrive.get() and self.homePath.get().__len__() > 0:
                            self.progress['value'] = 10
                            self.status['text'] = "Rebuilding groups..."
                            groups = self.getCheck()
                            self.status['text'] = "Setting login name..."
                            if "flast" in self.samFormat.get():
                                samname = ''.join([self.fname.get().strip()[0:1],self.lname.get().strip()])
                            elif "firstlast" in self.samFormat.get():
                                samname = ''.join([self.fname.get().strip(),self.lname.get().strip()])
                            else:
                                samname = ''.join([self.fname.get().strip(),".",self.lname.get().strip()])
                            self.status['text'] = "Rebuilding data..."
                            data['login'] = samname.lower()
                            data['first'] = self.fname.get().strip().capitalize()
                            data['last'] = self.lname.get().strip().capitalize()
                            data['password'] = self.dpass.get()
                            data['domain'] = self.primary_domain.get()
                            data['proxy'] = self.domains['Secondary']
                            data['groups'] = groups
                            data['homeDirectory'] = self.homePath.get() + "\\" + samname.lower()
                            data['homeDrive'] = self.hdrive.get() + ":"
                            data['description'] = self.desc.get()
                            data['title'] = self.jobTitleEnt.get()
                            self.progress['value'] = 20
                            t = threading.Thread(target=f.createUser, args=(self,data))
                            t.daemon = True
                            t.start()
                        else:
                            f.widgetStatus(self, tk.NORMAL)
                            self.status['text'] = "Idle..."
                            self.messageBox("ERROR!!","You must select domain\nHomeDrive and HomePath")
                    else:
                        f.widgetStatus(self, tk.NORMAL)
                        self.messageBox("ERROR!!","Must enter Password\nor password 8 characters min")
                else:
                    f.widgetStatus(self, tk.NORMAL)
                    self.messageBox("ERROR!!","First and Lastname must\nbe filled!")
            else:
                f.widgetStatus(self, tk.NORMAL)
                self.messageBox("ERROR!!","Your Settings are incomplete\nfor this TAB!")
        # elif self.tabControl.index(self.tabControl.select()) == 2:
        #     if not self.compFail:
        #         if not self.expiredOU == None:
        #             f.widgetStatus(self, tk.DISABLED)
        #             t = threading.Thread(target=f.remove_groups, args=[self])
        #             t.start()
        #         else:
        #             f.widgetStatus(self, tk.NORMAL)
        #             self.messageBox("ERROR!!","You must select an OU!")
        #     else:
        #         f.widgetStatus(self, tk.NORMAL)
        #         self.messageBox("ERROR!!","Your Settings are incomplete\nfor this TAB!")
        # elif self.tabControl.index(self.tabControl.select()) == 3:
        #     f.widgetStatus(self, tk.NORMAL)
        #     self.messageBox("MAINTENANCE!!","This Option is still being\ndeveloped.")            
        elif self.tabControl.index(self.tabControl.select()) == 2:
            if not self.compFail:
                if self.entPass.get().__len__() >= 8 or self.entPass.get().__len__() == 0:
                    if self.tree4.get_children() == ():
                        self.messageBox("ERROR!!","Must select a position")
                        return
                
                    if self.selItem3.__len__() <= 0:
                        self.messageBox("ERROR!!","Must select a user!")
                        return
                    
                    if self.fname_entry.get().__len__() <= 1:
                        self.messageBox("ERROR!!","First Name cannot be empty!")
                        return

                    data = dict()
                    f.widgetStatus(self, tk.DISABLED)
                    self.progress['value'] = 10
                    self.status['text'] = "Gathering Information..."
                    
                    data['login'] = self.entSamname.get()
                    data['first'] = self.fname_entry.get().capitalize()
                    data['last'] = self.lname_entry.get().capitalize()
                    data['domain'] = self.entDomain.get()
                    data['description'] = self.entDesc.get()
                    data['title'] = self.entJobTitle.get()
                    data['ou'] = self.updateList[self.selItem3[0]]['ou']
                    data['password'] = self.entPass.get()

                    self.progress['value'] = 20
                    
                    if not self.updateList[self.selItem3[0]]['proxyAddresses'] == None:
                        for x in self.updateList[self.selItem3[0]]['proxyAddresses']:
                            if self.entDomain.get() not in x and x.__len__() > 5:
                                data['proxy'] = x.split("@")[1]
                            else:
                                if not self.domains['Secondary'].__len__() <= 3:
                                    data['proxy'] = self.domains['Secondary']
                                else:
                                    data['proxy'] = ""
                    else:
                        if not self.domains['Secondary'].__len__() <= 3:
                            data['proxy'] = self.domains['Secondary']
                        else:
                            data['proxy'] = ""
                            
                    t = threading.Thread(target=f.update_user, args=[self, data])
                    t.daemon = True
                    t.start()
                else:
                    f.widgetStatus(self, tk.NORMAL)
                    self.messageBox("ERROR!!","Password must be 8 characters long")    
            else:
                f.widgetStatus(self, tk.NORMAL)
                self.messageBox("ERROR!!","Your Settings are incomplete\nfor this TAB!")

    def resetProgress(self):
        self.progress["value"] = 0

    def messageBox(self, title, txt):
        ap = tk.Tk()
        geo = self.winfo_geometry()
        posX = geo.split("+")[1]
        posY = geo.split("+")[2]
        
        center_x = int(int(posX) + (self.W/2) - 100)
        center_y = int(int(posY) + (self.H/2) - 25)

        message = tk.Label(ap, text=txt, wraplength=250, justify=tk.CENTER)
        btn = tk.Button(ap, text="OK", width=10, command=ap.destroy)
        ap.title(title)
        ap.geometry(f'300x100+{center_x}+{center_y}')
        ap.attributes("-fullscreen", False)
        ap.attributes("-toolwindow", True)
        ap.attributes("-topmost", True)
        
        message.pack(fill='both',expand=True, pady=5)
        btn.pack(anchor=tk.CENTER, padx=10, pady=5)
        
        ap.mainloop()


if __name__ == '__main__':
    global root
    # root = splash.Splash()
    root = ADUnlocker()
    # root.after(6700, ADUnlocker)
    root.mainloop()
    
        