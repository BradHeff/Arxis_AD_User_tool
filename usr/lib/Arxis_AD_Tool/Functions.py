import configparser_crypt as cCrypt

import OpenSSL
from os import mkdir, path, removedirs, system, name  # noqa
import json
import requests


from pathlib import Path
from ttkbootstrap import DISABLED, NORMAL
from ttkbootstrap.toast import ToastNotification

from ldap3 import (
    Connection,
    Server,
    MODIFY_REPLACE,
    SAFE_SYNC,
    SUBTREE,
    Tls,
    core,
)
from ldap3.extend.microsoft.removeMembersFromGroups import (
    ad_remove_members_from_groups as removeUsersInGroups,
)

DEBUG_SVR = False
DEBUG = True
Version = "2.0.11.3"
key = b"\xb1]\xdbM\xed\xc9d\x86\xfe\xc9\x97\x15\x93&R\xba\x9a\xb9#\xadh\x83\xc9D\xa6\xba\xdbX$\xb3TJ"
# settings_file = "Settings.dat"
if DEBUG_SVR:
    api_url = "http://localhost:5000"
else:
    api_url = "http://api.trincloud.cc"
# creds = "URip96k9xsm8pUaJ6f8fJPjGbTxxSxzQ4udC2kmmZCCcw2d77d.dat"
UAC = 32 + 65536
home = str(Path.home())

tls_configuration = Tls(
    validate=OpenSSL.SSL.VERIFY_NONE, version=OpenSSL.SSL.TLSv1_1_METHOD
)
server = None
exe_dir = str(Path(__file__).parents[2])

settings_dir = "".join([home, "/.config/arxis-ad-tool/"])
temp_dir = "".join([exe_dir, "/lib/Arxis_AD_Tool/Tmp/"])


def Toast(title, message, types="happy"):
    happy = "😀"
    sad = "😟"
    angry = "🤬"
    icon = ""
    if "er" in types:
        icon = angry
    elif "war" in types:
        icon = sad
    else:
        icon = happy
    toast = ToastNotification(
        title=title,
        message=message,
        icon=icon,
        duration=10000,
    )
    toast.show_toast()


def parse_status(self, json_data):
    ndata = json_data
    parsed = json.loads(
        str(ndata).replace("'", '"').lower(),
    )
    return parsed


def get_status(self):
    # res = requests.get("http://api.trincloud.cc/api/syncer")
    res = requests.get("".join([api_url, "/v1/data/LDAP"]))
    res.raise_for_status()
    return res.json()


def get_update(self):
    # res = requests.get("http://api.trincloud.cc/api/syncer")
    res = requests.get("".join([api_url, "/v1/data/Programs"]))
    res.raise_for_status()
    return res.json()


def verify_configuration(self):
    if not path.isdir(settings_dir):
        mkdir(settings_dir)


def clear_console():
    system("cls")


def ldap_connection(self):

    try:
        server = Server(
            self.server.strip(),
            use_ssl=True,
            tls=tls_configuration,
        )
        if DEBUG:
            print("Connected to LDAP server...")
        return Connection(
            server,
            self.username.strip(),
            self.password.strip(),
            client_strategy=SAFE_SYNC,
            auto_bind=True,
        )
    except Exception as e:
        print(f"ERROR: {e}")
        return None


def ldap_login(self, username, password):
    server = Server(
        self.server.strip(),
        use_ssl=True,
        tls=tls_configuration,
    )
    return Connection(
        server,
        "".join([self.company, "\\", username.strip()]),
        password.strip(),
        client_strategy=SAFE_SYNC,
        auto_bind=True,
    )


def get_operation_result(connection, operation_result):
    if not connection.strategy.sync:
        _, result = connection.get_response(operation_result)
    else:
        result = connection.result

    return result


def saveConfig(self):
    parser = cCrypt.ConfigParserCrypt()
    parser["config"] = {}

    parser["config"]["autoload"] = str(self.load.get())
    parser["config"]["tab"] = str(self.tabControl.index(self.tabControl.select()))

    if not self.var.get() == "1":
        parser["newuser"] = {}
        data = getnewuser(self)
        parser["newuser"]["domain"] = data["domain"]
        parser["newuser"]["campus"] = data["campus"]
        parser["newuser"]["password"] = data["password"]
        parser["newuser"]["format"] = data["format"]
        parser["newuser"]["pos"] = data["pos"]
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
            self.posSelect("H")
            self.samFormat.set(parser.get("newuser", "format"))
            self.primary_domain.set(parser.get("newuser", "domain"))
            self.desc.delete(0, "end")
            self.dpass.delete(0, "end")
            self.jobTitleEnt.delete(0, "end")
            self.dpass.insert(0, parser.get("newuser", "password"))
            self.desc.insert(0, parser.get("newuser", "desc"))
            self.jobTitleEnt.insert(0, parser.get("newuser", "title"))
            self.loaded = True


# def getServer(self, section):  # noqa
#     parser = cCrypt.ConfigParserCrypt()
#     parser.aes_key = key
#     parser.read_encrypted(settings_dir + settings_file)
#     if parser.has_section(section):
#         if parser.has_option(section, "server"):
#             return parser.get(section, "server")


# def getSettings(self):
#     parser = cCrypt.ConfigParserCrypt()
#     parser.aes_key = key
#     parser.read_encrypted(settings_dir + settings_file)
#     if parser.has_section("Settings"):
#         return parser.get("Settings", "company")


# def getConfig(self, section):  # noqa
#     parser = cCrypt.ConfigParserCrypt()
#     parser.aes_key = key
#     parser.read_encrypted(settings_dir + settings_file)

#     if parser.has_section(section):
#         # ===================SERVER================================
#         if parser.has_option(section, "server"):
#             self.server = parser.get(section, "server")
#             if not self.server.__len__() <= 3:
#                 self.compFail = False
#                 self.servs = True
#             else:
#                 self.compFail = True
#                 self.servs = False
#                 return
#         # ===================SERVER USERNAME================================
#         if parser.has_option(section, "server_user"):
#             self.username = parser.get(section, "server_user")
#             if not self.username.__len__() <= 3:
#                 self.compFail = False
#                 self.servs = True
#             else:
#                 self.compFail = True
#                 self.servs = False
#                 return
#         # ===================SERVER PASSWORD================================
#         if parser.has_option(section, "server_pass"):
#             self.password = parser.get(section, "server_pass")
#             if not self.password.__len__() <= 3:
#                 self.compFail = False
#                 self.servs = True
#             else:
#                 self.compFail = True
#                 self.servs = False
#                 return
#         # ===================USEROU================================
#         if parser.has_option(section, "userou"):
#             self.ou = parser.get(section, "userou")
#             if not self.ou.__len__() <= 3:
#                 self.compFail = False
#                 self.servs = True
#             else:
#                 self.compFail = True
#                 self.servs = False
#                 return
#         # ===================DOMAIN NAME================================
#         if parser.has_option(section, "domainname"):
#             self.domainName = parser.get(section, "domainname")
#             if self.domainName.__len__() <= 3:
#                 self.state = True

#         # ===================POSITIONS================================
#         if parser.has_option(section, "positions"):
#             JSON1 = parser.get(section, "positions")
#             JSON1 = JSON1.replace("'", '"')
#             self.positions = json.loads(JSON1)
#             if self.positions.__len__() <= 3:
#                 self.state = True

#         # ===================GROUPS================================
#         if parser.has_option(section, "groups"):
#             JSON2 = parser.get(section, "groups")
#             JSON2 = JSON2.replace("'", '"')
#             self.groupPos = json.loads(JSON2)
#             if self.groupPos.__len__() <= 3:
#                 self.state = True

#         # ===================POSITIONS OU================================
#         if parser.has_option(section, "positionsou"):
#             JSON3 = parser.get(section, "positionsou")
#             JSON3 = JSON3.replace("'", '"')
#             self.positionsOU = json.loads(JSON3)
#             if self.positionsOU.__len__() <= 3:
#                 self.state = True

#         # ===================EXPIRED OU================================
#         if parser.has_option(section, "expiredous"):
#             JSON4 = parser.get(section, "expiredous")
#             JSON4 = JSON4.replace("'", '"')
#             self.expiredOUs = json.loads(JSON4)
#             if self.expiredOUs.__len__() <= 3:
#                 self.state = True

#         # ===================GROUP OU================================
#         if parser.has_option(section, "groupsou"):
#             self.groupOU = parser.get(section, "groupsou")
#             if self.groupOU.__len__() <= 3:
#                 self.state = True

#         # ===================DOMAINS================================
#         if parser.has_option(section, "domains"):
#             JSON5 = parser.get(section, "domains")
#             JSON5 = JSON5.replace("'", '"')
#             self.domains = json.loads(JSON5)
#             if self.domains.__len__() <= 3:
#                 self.state = True

#         # ===================HOME DIRECTORIES================================
#         if parser.has_option(section, "homepaths"):
#             self.homePaths = parser.get(section, "homepaths")
#             if self.homePaths.split(",").__len__() <= 3:
#                 self.state = True

#         # ===================TITLES================================
#         if parser.has_option(section, "title"):
#             JSON6 = parser.get(section, "title")
#             JSON6 = JSON6.replace("'", '"')
#             self.jobTitle = json.loads(JSON6)
#             if self.jobTitle.__len__() <= 3:
#                 self.state = True

#         # ===================HOME DIRECTORIES================================
#         if parser.has_option(section, "campus"):
#             self.campus = parser.get(section, "campus")
#             if not self.campus.split(",").__len__() > 0:
#                 self.state = True
#         else:
#             self.compFail = True

#     else:
#         self.compFail = True

#     if not self.compFail:
#         self.state = False
#         widgetStatus(self, NORMAL)


def getnewuser(self):
    data = dict()
    data["format"] = self.samFormat.get()
    data["pos"] = self.var.get()
    data["campus"] = str(self.campH.get())
    data["domain"] = self.primary_domain.get()
    data["password"] = self.dpass.get()
    data["desc"] = self.desc.get()
    data["title"] = self.jobTitleEnt.get()
    return data


def widgetStatus(self, status):
    self.btn_unlockAll["state"] = status
    self.btn_search["state"] = status
    self.btn_userUnlock["state"] = status
    self.btn_reset["state"] = status


def widgetStatusFailed(self, state):
    if not state:
        self.btn_unlockAll["state"] = DISABLED
        self.btn_search["state"] = DISABLED
        self.btn_userUnlock["state"] = DISABLED
        self.btn_reset["state"] = DISABLED
    else:
        self.btn_unlockAll["state"] = NORMAL
        self.btn_search["state"] = NORMAL
        self.btn_userUnlock["state"] = NORMAL
        self.btn_reset["state"] = NORMAL


def resetPassword(self, ou, newpass):
    selected_item = self.tree.selection()[0]
    try:
        with ldap_connection(self) as c:
            c.extend.microsoft.modify_password(
                user=ou, new_password=newpass, old_password=None
            )
            result = c.modify(
                dn=ou,
                changes={"lockoutTime": "0"},
            )
            if not result:
                msg = "ERROR: '{0}'".format(
                    c.result.get("description"),
                )
                raise Exception(msg)

        self.tree.delete(selected_item)
        self.selItem = []
        widgetStatus(self, NORMAL)
        Toast("SUCCESS!!", "Password set and user unlocked!", "happy")
        if DEBUG:
            print("Password reset and user unlocked successfully.")
    except Exception:
        self.selItem = []
        widgetStatus(self, NORMAL)
        Toast("ERROR!!", "An error has occured!", "angry")
        print("An error occurred while resetting password.")


def unlockUser(self, ou, all=0):
    self.status["text"] = "".join(["Unlocking ", ou.split(",")[0].replace("CN=", "")])
    with ldap_connection(self) as c:
        result = c.modify(
            dn=ou,
            changes={"lockoutTime": (MODIFY_REPLACE, ["0"])},
        )
        if not result:
            msg = "ERROR: '{0}'".format(
                c.result.get("description"),
            )
            raise Exception(msg)

    if all == 0:
        widgetStatus(self, NORMAL)


def unlockAll(self, locked):
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
    # Toast("SUCCESS!!", "Unlock Complete!", "happy")
    self.progress["value"] = 0


def listLocked(self):
    users = {}
    results = ""
    with ldap_connection(self) as c:
        try:
            c.search(
                search_base=str(self.ou),
                search_filter="(&(objectClass=user)(&(lockoutTime=*)(!(lockoutTime=0))))",
                attributes=[
                    "displayName",
                    "lockoutTime",
                    "distinguishedName",
                    "sAMAccountName",
                ],
            )
            results = c.entries
        except core.exceptions.LDAPException as e:
            print(f"LIST UNLOCKED: {e}")

        for x in results:
            res = x["attributes"]
            users[res["sAMAccountName"]] = {
                "name": res["displayName"],
                "ou": res["distinguishedName"],
            }
        lockedaccounts = [str(y) for y in results]
        if lockedaccounts.__len__() >= 1:
            lockedaccounts = [x for x in lockedaccounts["attributes"]]
            if DEBUG:
                print(f"LOCKED ACCOUNTS: {lockedaccounts}")
    return users


def update_user(self, data):
    try:
        self.status["text"] = "".join(["Updating ", data["first"], " ", data["last"]])
        with ldap_connection(self) as c:
            self.progress["value"] = 60

            if data["proxy"] is None:
                proxy = "".join(
                    ["smtp:", data["login"], "@", self.domains["secondary"]]
                )
            else:
                proxy = "".join(["smtp:", data["login"], "@", data["proxy"]])

            attributes = {
                "givenName": (MODIFY_REPLACE, [data["first"]]),
                "sAMAccountName": (MODIFY_REPLACE, [data["login"]]),
                "sn": (MODIFY_REPLACE, [data["last"]]),
                "DisplayName": (
                    MODIFY_REPLACE,
                    ["".join([data["first"], " ", data["last"]])],
                ),
                "title": (MODIFY_REPLACE, [data["title"]]),
                "description": (MODIFY_REPLACE, [data["description"]]),
                "userPrincipalName": (
                    MODIFY_REPLACE,
                    ["".join([data["login"], "@", data["domain"]])],
                ),
                "mail": (
                    MODIFY_REPLACE,
                    ["".join([data["login"], "@", data["domain"]])],
                ),
                "proxyAddresses": [
                    (
                        MODIFY_REPLACE,
                        ["".join(["SMTP:", data["login"], "@", data["domain"]])],
                    ),
                    (MODIFY_REPLACE, [proxy]),
                ],
            }
            result = c.modify(
                dn=data["ou"],
                changes=attributes,
            )
            if not result:
                msg = "ERROR: User '{0}' was not created: {1}".format(
                    "".join([data["first"], " ", data["last"]]),
                    c.result.get("description"),
                )
                raise Exception(msg)
        if data["password"].__len__() >= 8:
            c.extend.microsoft.modify_password(
                user=data["ou"], new_password=data["password"], old_password=None
            )
        self.progress["value"] = 100
        widgetStatus(self, NORMAL)
        self.status["text"] = "User Updated!"
        # Toast("SUCCESS!!", "User Updated!", "happy")
        self.progress["value"] = 0
        self.editSelect("E")
    except:  # noqa
        self.status["text"] = "Idle..."
        widgetStatus(self, NORMAL)
        # Toast("ERROR!!", "An error has occured!", "angry")
        self.progress["value"] = 0


def createUser(self, data):
    try:
        self.status["text"] = "".join(["Creating ", data["first"], " ", data["last"]])
        result = "NOTHING"
        with ldap_connection(self) as c:
            attributes = {
                "SAMAccountName": data["login"],
                "givenName": data["first"],
                "userPrincipalName": "".join([data["login"], "@", data["domain"]]),
                "DisplayName": "".join([data["first"], " ", data["last"]]),
                "sn": data["last"],
                "mail": "".join([data["login"], "@", data["domain"]]),
                "proxyAddresses": [
                    "".join(["SMTP:", data["login"], "@", data["domain"]]),
                    "".join(["smtp:", data["login"], "@", data["proxy"]]),
                ],
                "title": data["title"],
                "description": data["description"],
                "department": data["department"],
                "company": data["company"],
                "pwdLastSet": 0,
            }
            user_dn = "".join(
                ["CN=", data["first"], " ", data["last"], ",", self.posOU]
            )
            result = c.add(
                dn=user_dn,
                object_class=["top", "person", "organizationalPerson", "user"],
                attributes=attributes,
            )
            if result[0] is not True:
                msg = "ERROR: User '{0}' was not created: {1}".format(
                    "".join([data["first"], " ", data["last"]]),
                    c.result.get("description"),
                )
                self.progress["value"] = 100
                widgetStatus(self, NORMAL)
                self.status["text"] = msg
                self.progress["value"] = 0
                return
        self.progress["value"] = 30
        c.extend.microsoft.unlock_account(user=user_dn)
        c.extend.microsoft.modify_password(
            user=user_dn, new_password=data["password"], old_password=None
        )
        enable_account = {"userAccountControl": (MODIFY_REPLACE, [UAC])}
        c.modify(user_dn, changes=enable_account)

        self.progress["value"] = 50
        self.status["text"] = "".join(
            ["Adding ", data["first"], " ", data["last"], " to groups"]
        )
        c.extend.microsoft.add_members_to_groups([user_dn], data["groups"])
        self.progress["value"] = 80

        self.progress["value"] = 100
        widgetStatus(self, NORMAL)
        self.status["text"] = "User Created!"
        Toast("SUCCESS!!", "User Created!", "happy")
        self.progress["value"] = 0
    except Exception as e:
        print("ERRORS:", str(e))
        self.status["text"] = "Idle..."
        widgetStatus(self, NORMAL)
        self.progress["value"] = 0
        Toast("ERROR!!", "An error has occured!", "angry")


# def remove_groups(self):
#     pythoncom.CoInitialize()
#     try:
#         userlist = listUsers(self, self.expiredOU)
#         maxs = userlist.__len__()
#         self.status["text"] = "Loading Users..."
#         userCount = 1
#         for x in userlist:
#             self.tree2.insert(
#                 "", "end", values=(x, userlist[x]["name"], userlist[x]["homeDir"])
#             )
#             self.progress["value"] = userCount
#         count = 1
#         self.progress["value"] = count
#         self.status["text"] = "Cleaning Users: " + str(count) + "/" + str(maxs)
#         self.progress["maximum"] = float(maxs)
#         for y in userlist:
#             count += 1
#             self.progress["value"] = count
#             self.status["text"] = "Cleaning Users: " + str(count) + "/" + str(maxs)
#             removeHomedrive(userlist[y]["homeDir"])
#             for child in self.tree2.get_children():
#                 if y in self.tree2.item(child)["values"]:
#                     self.tree2.delete(child)
#     except Exception as e:
#         print(e)
#         self.messageBox("ERROR!", "An error has occurred!", "error")
#     widgetStatus(self, NORMAL)
#     self.status["text"] = "Idle..."
#     self.after(1000, self.resetProgress)


def listUsers(self, ou):
    users = {}
    with ldap_connection(self) as c:
        status, result, response, _ = c.search(
            search_base=str(ou),
            search_filter="(&(objectClass=user)(objectCategory=person))",
            attributes=[
                "displayName",
                "distinguishedName",
                "sAMAccountName",
            ],
            search_scope=SUBTREE,
            get_operational_attributes=True,
        )
        if not result:
            msg = "ERROR: '{0}'".format(c.result.get("description"))
            raise Exception(msg)

        for x in response:
            res = x["attributes"]
            users[res["sAMAccountName"]] = {
                "name": res["displayName"],
                "ou": res["distinguishedName"],
                # "homeDir": res["homeDirectory"],
            }
    return users


def listUsers2(self, ou):
    users = {}
    with ldap_connection(self) as c:
        status, result, response, _ = c.search(
            search_base=str(ou),
            search_filter="(&(objectClass=user)(objectCategory=person))",
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
            search_scope=SUBTREE,
            get_operational_attributes=True,
        )
        if not result:
            msg = "ERROR: '{0}'".format(c.result.get("description"))
            raise Exception(msg)

        for x in response:
            res = x["attributes"]
            users[res["sAMAccountName"]] = {
                "name": res["displayName"],
                "ou": res["distinguishedName"],
                "fname": res["givenName"],
                "lname": res["sn"],
                "description": res["description"],
                "title": res["title"],
                "mail": res["mail"],
                "userPrincipalName": res["userPrincipalName"],
                "proxyAddresses": res["proxyAddresses"],
            }
    return users


def removeGroups(self, users, groupOU):
    with ldap_connection(self) as c:
        removeUsersInGroups(c, users, groupOU, fix=True)


def removeHomedrive(paths):
    try:
        if path.exists(paths):
            removedirs(paths)
    except Exception as e:
        print(f"ERROR REMOVE HOMEPATH: {e}")
