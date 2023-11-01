import base64
import json
import sys
from os import mkdir, path, removedirs, system
from pathlib import Path

import configparser_crypt as cCrypt
import pythoncom
import win32security
from pyad_Trinity import adgroup, adsearch, aduser, pyad_Trinity
from ttkbootstrap import DISABLED, NORMAL

DEBUG = False
Version = "v1.0.4.9"
key = b'\x8f\xf2}\xcfEMVK2\x9a1\xfe\xea\x96\xf9\x9a 4\xbb\x8f\xdblj\xde(\xc1\xa6\xe6\xee6\xdd\xa9'
settings_file = "Settings.dat"

if not DEBUG:
    exe_dir = str(path.dirname(sys.executable))
else:
    exe_dir = str(Path(__file__).parents[0])

settings_dir = "".join([exe_dir, "\\Settings\\"])
# data_dir = ''.join([exe_dir, '\\Data\\'])


def clear_console():
    system("cls")


def Switch(string, lists):
    if string.lower() in lists:
        return True
    else:
        return False


def checkSettings(self):
    if base64.b64decode(self.company).decode("UTF-8").__len__() <= 0:
        return True
    else:
        return False


def saveConfig(self):
    parser = cCrypt.ConfigParserCrypt()
    parser["config"] = {}
    if "Select" not in self.options.get():
        parser["config"]["autoload"] = str(self.load.get())
        parser["config"]["company"] = self.options.get()
        parser["config"]["tab"] = str(self.tabControl.index(self.tabControl.select()))

        if not self.var.get() == "1":
            parser["newuser"] = {}
            data = getnewuser(self)
            parser["newuser"]["domain"] = data["domain"]
            parser["newuser"]["campus"] = data["campus"]
            parser["newuser"]["password"] = data["password"]
            parser["newuser"]["format"] = data["format"]
            parser["newuser"]["pos"] = data["pos"]
            parser["newuser"]["hdrive"] = data["hdrive"]
            parser["newuser"]["hpath"] = data["hpath"]
            parser["newuser"]["desc"] = data["desc"]
            parser["newuser"]["title"] = data["title"]

    with open(settings_dir + "Config.ini", "w") as w:
        parser.write(w)


def loadConfig(self, check=False):
    parser = cCrypt.ConfigParserCrypt()
    parser.read(settings_dir + "Config.ini")
    if parser.has_section("config"):
        if parser.has_option("config", "autoload"):
            self.load.set(eval(parser.get("config", "autoload")))
    if eval(parser.get("config", "autoload")) or check is True:
        if parser.has_option("config", "tab"):
            self.tabControl.select(int(parser.get("config", "tab")))
        if parser.has_section("newuser"):
            self.campH.set(parser.get("newuser", "campus"))
            self.var.set(parser.get("newuser", "pos"))
            self.posSelect()
            self.samFormat.set(parser.get("newuser", "format"))
            self.primary_domain.set(parser.get("newuser", "domain"))
            self.hdrive.set(parser.get("newuser", "hdrive"))
            self.paths.set(parser.get("newuser", "hpath"))
            self.desc.delete(0, "end")
            self.dpass.delete(0, "end")
            self.jobTitleEnt.delete(0, "end")
            self.dpass.insert(0, parser.get("newuser", "password"))
            self.desc.insert(0, parser.get("newuser", "desc"))
            self.jobTitleEnt.insert(0, parser.get("newuser", "title"))
            self.loaded = True
            # self.comboLoad()


def getSettings(self):
    parser = cCrypt.ConfigParserCrypt()
    parser.aes_key = key
    parser.read_encrypted(settings_dir + settings_file)
    if parser.has_section("Settings"):
        self.company = parser.get("Settings", "company")


def getConfig(self, section):  # noqa
    parser = cCrypt.ConfigParserCrypt()
    parser.aes_key = key
    parser.read_encrypted(settings_dir + settings_file)

    if parser.has_section(section):
        # ===================SERVER================================
        if parser.has_option(section, "server"):
            self.server = parser.get(section, "server")
            if not base64.b64decode(self.server).decode("UTF-8").__len__() <= 3:
                self.compFail = False
                self.servs = True
            else:
                self.compFail = True
                self.servs = False
                return
        # ===================SERVER USERNAME================================
        if parser.has_option(section, "server_user"):
            self.username = parser.get(section, "server_user")
            if not base64.b64decode(self.username).decode("UTF-8").__len__() <= 3:
                self.compFail = False
                self.servs = True
            else:
                self.compFail = True
                self.servs = False
                return
        # ===================SERVER PASSWORD================================
        if parser.has_option(section, "server_pass"):
            self.password = parser.get(section, "server_pass")
            if not base64.b64decode(self.password).decode("UTF-8").__len__() <= 3:
                self.compFail = False
                self.servs = True
            else:
                self.compFail = True
                self.servs = False
                return
        # ===================USEROU================================
        if parser.has_option(section, "userou"):
            self.ou = parser.get(section, "userou")
            if not base64.b64decode(self.ou).decode("UTF-8").__len__() <= 3:
                self.compFail = False
                self.servs = True
            else:
                self.compFail = True
                self.servs = False
                return
        # ===================DOMAIN NAME================================
        if parser.has_option(section, "domainname"):
            self.domainName = parser.get(section, "domainname")
            if base64.b64decode(self.domainName).decode("UTF-8").__len__() <= 3:
                self.state = True

        # ===================POSITIONS================================
        if parser.has_option(section, "positions"):
            self.positions = json.loads(
                base64.b64decode(parser.get(section, "positions")).decode("UTF-8")
            )
            if self.positions.__len__() <= 3:
                self.state = True

        # ===================GROUPS================================
        if parser.has_option(section, "groups"):
            self.groupPos = json.loads(
                base64.b64decode(parser.get(section, "groups")).decode("UTF-8")
            )
            if self.groupPos.__len__() <= 3:
                self.state = True

        # ===================POSITIONS OU================================
        if parser.has_option(section, "positionsou"):
            self.positionsOU = json.loads(
                base64.b64decode(parser.get(section, "positionsou")).decode("UTF-8")
            )
            if self.positionsOU.__len__() <= 3:
                self.state = True

        # ===================EXPIRED OU================================
        if parser.has_option(section, "expiredous"):
            self.expiredOUs = json.loads(
                base64.b64decode(parser.get(section, "expiredous")).decode("UTF-8")
            )
            if self.expiredOUs.__len__() <= 3:
                self.state = True

        # ===================GROUP OU================================
        if parser.has_option(section, "groupsou"):
            self.groupOU = parser.get(section, "groupsou")
            # print(base64.b64decode(self.groupOU).decode("UTF-8"))
            if base64.b64decode(self.groupOU).decode("UTF-8").__len__() <= 3:
                self.state = True

        # ===================DOMAINS================================
        if parser.has_option(section, "domains"):
            self.domains = json.loads(
                base64.b64decode(parser.get(section, "domains")).decode("UTF-8")
            )
            if self.domains.__len__() <= 3:
                self.state = True

        # ===================HOME DIRECTORIES================================
        if parser.has_option(section, "homepaths"):
            self.homePaths = parser.get(section, "homepaths")
            if (
                base64.b64decode(self.homePaths).decode("UTF-8").split(",").__len__()
                <= 3
            ):
                self.state = True

        # ===================TITLES================================
        if parser.has_option(section, "title"):
            self.jobTitle = json.loads(
                base64.b64decode(parser.get(section, "title")).decode("UTF-8")
            )
            if self.jobTitle.__len__() <= 3:
                self.state = True

        # ===================HOME DIRECTORIES================================
        if parser.has_option(section, "campus"):
            self.campus = parser.get(section, "campus")
            # print(base64.b64decode(self.campus).decode("UTF-8").split(","))
            if (
                not base64.b64decode(self.campus).decode("UTF-8").split(",").__len__()
                > 0
            ):
                self.state = True
        else:
            self.compFail = True
    else:
        self.compFail = True

    if not self.compFail:
        self.state = False
        widgetStatus(self, NORMAL)


def getnewuser(self):
    data = dict()
    data["format"] = self.samFormat.get()
    data["pos"] = self.var.get()
    data["campus"] = str(self.campH.get())
    data["domain"] = self.primary_domain.get()
    data["password"] = self.dpass.get()
    data["hdrive"] = self.hdrive.get()
    data["hpath"] = self.paths.get()
    data["desc"] = self.desc.get()
    data["title"] = self.jobTitleEnt.get()
    return data


def widgetStatus(self, status):
    if status == NORMAL:
        self.combobox["state"] = "readonly"
    else:
        self.combobox["state"] = DISABLED

    self.btn_unlockAll["state"] = status
    self.btn_search["state"] = status
    self.btn_userUnlock["state"] = status
    self.btn_reset["state"] = status
    # self.move_btn['state']=status
    self.addGroup["state"] = status


def widgetStatusFailed(self, state):
    if state:
        self.btn_unlockAll["state"] = DISABLED
        self.btn_search["state"] = DISABLED
        self.btn_userUnlock["state"] = DISABLED
        self.btn_reset["state"] = DISABLED
        # self.move_btn['state']=DISABLED
        self.addGroup["state"] = DISABLED
    else:
        self.btn_unlockAll["state"] = NORMAL
        self.btn_search["state"] = NORMAL
        self.btn_userUnlock["state"] = NORMAL
        self.btn_reset["state"] = NORMAL
        self.addGroup["state"] = NORMAL


def resetPassword(self, ou, newpass):
    pythoncom.CoInitialize()
    selected_item = self.tree.selection()[0]
    try:
        pyad_Trinity.set_defaults(
            ldap_server=base64.b64decode(self.server).decode("UTF-8").strip(),
            username=base64.b64decode(self.username).decode("UTF-8").strip(),
            password=base64.b64decode(self.password).decode("UTF-8").strip(),
            ssl=True,
        )
        lockeduser = aduser.ADUser.from_dn(ou)
        lockeduser.set_password(newpass)

        lockeduser.update_attribute("lockoutTime", "0")

        # lockeduser.update_attribute("PwdLastSet", "0")
        self.tree.delete(selected_item)
        self.selItem = []
        widgetStatus(self, NORMAL)
        self.messageBox("SUCCESS!!", "Password set and user unlocked!")
    except pyad_Trinity.aduser.win32Exception as e:
        self.selItem = []
        widgetStatus(self, NORMAL)
        self.messageBox(
            "ERROR!!",
            e.error_info["message"].strip() + "\nCheck password is in format abc123!!",
        )
    except:  # noqa
        self.selItem = []
        widgetStatus(self, NORMAL)
        self.messageBox("ERROR!!", "An error has occured!")


def unlockUser(self, ou, all=0):
    pythoncom.CoInitialize()
    pyad_Trinity.set_defaults(
        ldap_server=base64.b64decode(self.server).decode("UTF-8").strip(),
        username=base64.b64decode(self.username).decode("UTF-8").strip(),
        password=base64.b64decode(self.password).decode("UTF-8").strip(),
        ssl=True,
    )
    lockeduser = aduser.ADUser.from_dn(ou)
    lockeduser.update_attribute("lockoutTime", "0")
    if all == 0:
        widgetStatus(self, NORMAL)


def unlockAll(self, locked):
    pythoncom.CoInitialize()
    count = 0
    props = 1
    for x in locked:
        count += 1
        if count == self.all:
            props = 0
        self.status["text"] = "".join(["Unlocking ", locked[x]["name"]])
        self.progress["value"] = count
        unlockUser(self, locked[x]["ou"], all=props)
    self.tree.delete(*self.tree.get_children())
    widgetStatus(self, NORMAL)
    self.status["text"] = "Idle..."
    self.messageBox("SUCCESS!!", "Unlock Complete!")
    self.progress["value"] = 0


def listLocked(self):
    pythoncom.CoInitialize()
    pyad_Trinity.set_defaults(
        ldap_server=base64.b64decode(self.server).decode("UTF-8").strip(),
        username=base64.b64decode(self.username).decode("UTF-8").strip(),
        password=base64.b64decode(self.password).decode("UTF-8").strip(),
        ssl=True,
    )

    q = adsearch.ADQuery()
    q.execute_query(
        attributes=[
            "displayName",
            "lockoutTime",
            "distinguishedName",
            "sAMAccountName",
        ],
        where_clause="objectClass = 'user' and lockoutTime >= '1'",
        base_dn=base64.b64decode(self.ou).decode("UTF-8"),
    )
    users = {}
    for x in q.get_results():
        users[x["sAMAccountName"]] = {
            "name": x["displayName"],
            "ou": x["distinguishedName"],
        }

    return users


def update_user(self, data):
    pythoncom.CoInitialize()
    try:
        self.status["text"] = "".join(["Updating ", data["first"], " ", data["last"]])
        pyad_Trinity.set_defaults(
            ldap_server=base64.b64decode(self.server).decode("UTF-8").strip(),
            username=base64.b64decode(self.username).decode("UTF-8").strip(),
            password=base64.b64decode(self.password).decode("UTF-8").strip(),
            ssl=True,
        )

        Nou = pyad_Trinity.aduser.ADUser.from_dn(data["ou"])
        self.progress["value"] = 60

        if data["proxy"].__len__() > 3:
            proxy = "".join(["smtp:", data["login"], "@", data["proxy"]])
        else:
            proxy = ""

        Nou.update_attributes(
            {
                "givenName": data["first"],
                "sAMAccountName": data["login"],
                "sn": data["last"],
                "DisplayName": "".join([data["first"], " ", data["last"]]),
                "title": data["title"],
                "description": data["description"],
                "userPrincipalName": "".join([data["login"], "@", data["domain"]]),
                "mail": "".join([data["login"], "@", data["domain"]]),
                "proxyAddresses": [
                    "".join(["SMTP:", data["login"], "@", data["domain"]]),
                    proxy,
                ],
            }
        )

        if data["password"].__len__() >= 8:
            Nou.set_password(data["password"])
        self.progress["value"] = 100
        widgetStatus(self, NORMAL)
        self.status["text"] = "Idle..."
        self.messageBox("SUCCESS!!", "User Updated!")
        self.progress["value"] = 0
        self.updateSelect()
    except pyad_Trinity.aduser.win32Exception as e:
        self.status["text"] = "Idle..."
        widgetStatus(self, NORMAL)
        self.messageBox(
            "ERROR!!",
            e.error_info["message"].strip() + "\nCheck password is in format abc123!!",
        )
        self.progress["value"] = 0
    except:  # noqa
        self.status["text"] = "Idle..."
        widgetStatus(self, NORMAL)
        self.messageBox("ERROR!!", "An error has occured!")
        self.progress["value"] = 0


def createUser(self, data):
    pythoncom.CoInitialize()
    # try:
    self.status["text"] = "".join(["Creating ", data["first"], " ", data["last"]])
    pyad_Trinity.set_defaults(
        ldap_server=base64.b64decode(self.server).decode("UTF-8").strip(),
        username=base64.b64decode(self.username).decode("UTF-8").strip(),
        password=base64.b64decode(self.password).decode("UTF-8").strip(),
        ssl=True,
    )

    Nou = pyad_Trinity.adcontainer.ADContainer.from_dn(self.posOU)
    self.progress["value"] = 30
    pyad_Trinity.aduser.ADUser.create(
        sAMAccountName=data["login"],
        cn="".join([data["first"], " ", data["last"]]),
        password=data["password"],
        container_object=Nou,
        enable=True,
        optional_attributes={
            "givenName": data["first"],
            "userPrincipalName": "".join([data["login"], "@", data["domain"]]),
            "DisplayName": "".join([data["first"], " ", data["last"]]),
            "sn": data["last"],
            "mail": "".join([data["login"], "@", data["domain"]]),
            "proxyAddresses": [
                "".join(["SMTP:", data["login"], "@", data["domain"]]),
                "".join(["smtp:", data["login"], "@", data["proxy"]]),
            ],
            "HomeDirectory": data["homeDirectory"],
            "HomeDrive": data["homeDrive"],
            "title": data["title"],
            "description": data["description"],
            "department": data["department"],
            "company": data["company"],
            "pwdLastSet": 0,
        },
    )
    newuser = pyad_Trinity.aduser.ADUser.from_cn(
        "".join([data["first"], " ", data["last"]])
    )
    # newuser.set_password(data["password"])
    newuser.set_user_account_control_setting("DONT_EXPIRE_PASSWD", True)
    newuser.set_user_account_control_setting("PASSWD_NOTREQD", False)

    self.progress["value"] = 50
    self.status["text"] = "".join(
        ["Adding ", data["first"], " ", data["last"], " to groups"]
    )
    for gp in data["groups"]:
        print(gp)
        newgroup = pyad_Trinity.adgroup.ADGroup.from_cn(gp)
        newuser.add_to_group(newgroup)
    self.progress["value"] = 80
    self.status["text"] = "".join(
        ["Creating ", data["first"], " ", data["last"], " home directory"]
    )
    createHomeDir(
        data["login"],
        data["homeDirectory"],
        base64.b64decode(self.domainName).decode("UTF-8").strip(),
    )
    self.progress["value"] = 100
    widgetStatus(self, NORMAL)
    self.status["text"] = "Idle..."
    self.messageBox("SUCCESS!!", "User Created!")
    self.progress["value"] = 0
    # except Exception as e:
    #     self.status["text"] = "Idle..."
    #     widgetStatus(self, NORMAL)
    #     self.progress["value"] = 0
    #     self.messageBox("ERROR!!", e)
    #     # self.messageBox("ERROR!!","An error has occured!")


def createHomeDir(username, homeDir, domainName):
    if path.exists(homeDir) is False:
        mkdir(homeDir)

        user, domain, type = win32security.LookupAccountName(
            "", domainName + "\\" + username
        )
        sd = win32security.GetFileSecurity(
            homeDir, win32security.DACL_SECURITY_INFORMATION
        )

        dacl = sd.GetSecurityDescriptorDacl()
        dacl.AddAccessAllowedAceEx(win32security.ACL_REVISION, 3, 2032127, user)

        sd.SetSecurityDescriptorDacl(1, dacl, 0)
        win32security.SetFileSecurity(
            homeDir, win32security.DACL_SECURITY_INFORMATION, sd
        )


# =========================================================================


def remove_groups(self):
    pythoncom.CoInitialize()
    try:
        userlist = listUsers(self, self.expiredOU)
        group = listGroups(self, base64.b64decode(self.groupOU).decode("UTF-8"))
        maxs = userlist.__len__()
        self.status["text"] = "Loading Users..."
        userCount = 1
        for x in userlist:
            self.tree2.insert(
                "", "end", values=(x, userlist[x]["name"], userlist[x]["homeDir"])
            )
            self.progress["value"] = userCount
        count = 1
        self.progress["value"] = count
        self.status["text"] = "Cleaning Users: " + str(count) + "/" + str(maxs)
        self.progress["maximum"] = float(maxs)
        for y in userlist:
            count += 1
            self.progress["value"] = count
            for x in group:
                removeGroups(self, userlist[y]["ou"], group[x]["ou"])
            self.status["text"] = "Cleaning Users: " + str(count) + "/" + str(maxs)
            removeHomedrive(userlist[y]["homeDir"])
            for child in self.tree2.get_children():
                if y in self.tree2.item(child)["values"]:
                    self.tree2.delete(child)
    except Exception as e:
        print(e)
        self.messageBox("ERROR!", "An error has occurred!")
    widgetStatus(self, NORMAL)
    self.status["text"] = "Idle..."
    self.after(1000, self.resetProgress)


def listGroups(self, ou):
    # try:
    pythoncom.CoInitialize()
    pyad_Trinity.set_defaults(
        ldap_server=base64.b64decode(self.server).decode("UTF-8").strip(),
        username=base64.b64decode(self.username).decode("UTF-8").strip(),
        password=base64.b64decode(self.password).decode("UTF-8").strip(),
        ssl=True,
        type="GC",
    )
    # print(base64.b64decode(self.server).decode("UTF-8"))
    # print(base64.b64decode(self.username).decode("UTF-8"))
    # print(base64.b64decode(self.password).decode("UTF-8"))
    q = adsearch.ADQuery()
    q.execute_query(
        attributes=["cn", "distinguishedName", "sAMAccountName"],
        where_clause="objectClass = 'Group'",
        base_dn=ou,
    )
    groups = {}
    for x in q.get_results():
        # print(x)
        groups[x["sAMAccountName"]] = {
            "name": x["cn"],
            "ou": x["distinguishedName"],
        }
    return groups
    # except Exception as e:
    #     print(e)


def listUsers(self, ou):
    pythoncom.CoInitialize()
    pyad_Trinity.set_defaults(
        ldap_server=base64.b64decode(self.server).decode("UTF-8").strip(),
        username=base64.b64decode(self.username).decode("UTF-8").strip(),
        password=base64.b64decode(self.password).decode("UTF-8").strip(),
        ssl=True,
        type="GC",
    )
    print(base64.b64decode(self.server).decode("UTF-8"))
    print(base64.b64decode(self.username).decode("UTF-8"))
    print(base64.b64decode(self.password).decode("UTF-8"))
    q = adsearch.ADQuery()
    q.execute_query(
        attributes=[
            "displayName",
            "distinguishedName",
            "sAMAccountName",
            "homeDirectory",
        ],
        where_clause="objectClass = 'user'",
        base_dn=ou,
    )
    users = {}
    for x in q.get_results():
        users[x["sAMAccountName"]] = {
            "name": x["displayName"],
            "ou": x["distinguishedName"],
            "homeDir": x["homeDirectory"],
        }
    return users


def listUsers2(self, ou):
    pythoncom.CoInitialize()
    pyad_Trinity.set_defaults(
        ldap_server=base64.b64decode(self.server).decode("UTF-8").strip(),
        username=base64.b64decode(self.username).decode("UTF-8").strip(),
        password=base64.b64decode(self.password).decode("UTF-8").strip(),
        ssl=True,
        type="GC",
    )
    print(base64.b64decode(self.server).decode("UTF-8"))
    print(base64.b64decode(self.username).decode("UTF-8"))
    print(base64.b64decode(self.password).decode("UTF-8"))
    q = adsearch.ADQuery()
    q.execute_query(
        attributes=[
            "displayName",
            "distinguishedName",
            "sAMAccountName",
            "description",
            "title",
            "mail",
            "userPrincipalName",
            "sn",
            "givenName",
            "proxyAddresses",
        ],
        where_clause="objectClass = 'user'",
        base_dn=ou,
    )
    users = {}
    for x in q.get_results():
        users[x["sAMAccountName"]] = {
            "name": x["displayName"],
            "ou": x["distinguishedName"],
            "fname": x["givenName"],
            "lname": x["sn"],
            "description": x["description"],
            "title": x["title"],
            "mail": x["mail"],
            "userPrincipalName": x["userPrincipalName"],
            "proxyAddresses": x["proxyAddresses"],
        }
    return users


def removeGroups(self, users, groupOU):
    pythoncom.CoInitialize()
    pyad_Trinity.set_defaults(
        ldap_server=base64.b64decode(self.server).decode("UTF-8").strip(),
        username=base64.b64decode(self.username).decode("UTF-8").strip(),
        password=base64.b64decode(self.password).decode("UTF-8").strip(),
        ssl=True,
        type="GC",
    )
    u = aduser.ADUser.from_dn(users)
    g = adgroup.ADGroup.from_dn(groupOU)
    u.remove_from_group(g)


def removeHomedrive(paths):
    try:
        if path.exists(paths):
            removedirs(paths)
    except Exception as e:
        print(e)


# =============================================


# def moveUser(self, bOU, aOU):
#     pythoncom.CoInitialize()
#     pyad_Trinity.set_defaults(ldap_server=base64.b64decode(self.server).decode("UTF-8"),
#                       username=base64.b64decode(self.username).decode("UTF-8"),
#                       password=base64.b64decode(self.password).decode("UTF-8"),
#                       ssl=True)
#     u = aduser.ADUser.from_dn(bOU)
#     newOrg = adcontainer.ADContainer.from_dn(aOU)
#     self.progress['value'] = 60
#     aduser.ADUser.move(u,newOrg)
#     selected_item = self.tree3.selection()[0]
#     self.tree3.delete(selected_item)
#     self.progress['value'] = 100
#     self.selItem2 = []
#     self.status['text'] = "Idle..."
#     self.messageBox("SUCCESS!!","Move Complete!")
#     widgetStatus(self, NORMAL)
#     self.progress['value'] = 0
