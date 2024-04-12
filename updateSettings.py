# import sys
import base64
from pathlib import Path
import os
from configparser_crypt import ConfigParserCrypt

exe_dir = str(Path(__file__).parents[0])

settings_file = "Settings.dat"
if os.name == "nt":
    settings_dir = "".join([exe_dir, "\\Settings\\"])
else:
    settings_dir = "".join([exe_dir, "/Settings/"])


class MakeConf:
    def __init__(self):
        super(MakeConf, self).__init__()
        self.old = ""
        self.key = ""
        self.lines = []
        self.readLines()
        self.writeConfig()
        self.writeLines()
        print(self.key)

    def _getPosition(self, file, text):
        nlist = [x for x in file if text in x]
        print(exe_dir + "\\Functions.py")
        position = file.index(nlist[0])
        return position

    def readLines(self):
        if os.name == "nt":
            with open(exe_dir + "\\Functions.py", "r") as f:
                self.lines = f.readlines()
                pos = self._getPosition(self.lines, "key = ")
                line = self.lines[pos]
                self.old = line.split(" = ")[1].strip()
                f.close()
        else:
            with open(exe_dir + "/Functions.py", "r") as f:
                self.lines = f.readlines()
                pos = self._getPosition(self.lines, "key = ")
                line = self.lines[pos]
                self.old = line.split(" = ")[1].strip()
                f.close()

    def writeLines(self):
        if os.name == "nt":
            with open(exe_dir + "\\Functions.py", "w") as w:
                pos = self._getPosition(self.lines, "key = ")

                self.lines[pos] = self.lines[pos].replace(self.old, str(self.key))

                w.writelines(self.lines)
                w.close()
        else:
            with open(exe_dir + "/Functions.py", "w") as w:
                pos = self._getPosition(self.lines, "key = ")

                self.lines[pos] = self.lines[pos].replace(self.old, str(self.key))

                w.writelines(self.lines)
                w.close()

    def writeConfig(self):
        conf_file = ConfigParserCrypt()
        conf_file.generate_key()
        self.key = conf_file.aes_key

        conf_file.add_section("Horizon")
        conf_file["Horizon"]["server"] = str(
            base64.b64encode(bytes("HCS-DC01.HORIZON.local", "UTF-8")).decode("UTF-8")
        )
        conf_file["Horizon"]["server_user"] = str(
            base64.b64encode(
                bytes(
                    "CN=python service account,OU=Services,OU=Users,OU=Horizon,DC=HORIZON,DC=local",
                    "UTF-8",
                )
            ).decode("UTF-8")
        )
        conf_file["Horizon"]["server_pass"] = str(
            base64.b64encode(bytes("BoomDoggy123", "UTF-8")).decode("UTF-8")
        )
        conf_file["Horizon"]["userou"] = str(
            base64.b64encode(
                bytes("OU=Users,OU=Horizon,DC=HORIZON,DC=local", "UTF-8")
            ).decode("UTF-8")
        )
        conf_file["Horizon"]["domainname"] = str(
            base64.b64encode(bytes("HORIZON", "UTF-8")).decode("UTF-8")
        )
        conf_file["Horizon"]["groups"] = str(
            base64.b64encode(
                bytes(
                    '{"Executive":["CN=SG_FS_Management,OU=SG_FileShare,OU=Groups,OU=Horizon,DC=HORIZON,DC=local", "SG_FS_HR,OU=SG_FileShare,OU=Groups,OU=Horizon,DC=HORIZON,DC=local", \
"SG_FS_ExecDrive,OU=SG_FileShare,OU=Groups,OU=Horizon,DC=HORIZON,DC=local", "CN=Local PC Administrators,OU=Groups,OU=Horizon,DC=HORIZON,DC=local",\
"CN=Office365-A1Plus-Faculty,OU=Office 365,OU=Groups,OU=Horizon,DC=HORIZON,DC=local", "CN=Office365-AzureAD-P2,OU=Office 365,OU=Groups,OU=Horizon,DC=HORIZON,DC=local",\
"SG_FS_Adminfiles,OU=SG_FileShare,OU=Groups,OU=Horizon,DC=HORIZON,DC=local", "CN=SG_WF_Staff,OU=Firewall,OU=Groups,OU=Horizon,DC=HORIZON,DC=local", "CN=Horizon Staff,OU=Groups,OU=Horizon,DC=HORIZON,DC=local",\
"CN=Library Users,OU=Groups,OU=Horizon,DC=HORIZON,DC=local", "SG_FS_Photos,OU=SG_FileShare,OU=Groups,OU=Horizon,DC=HORIZON,DC=local", "CN=GEveryone,OU=Groups,OU=Horizon,DC=HORIZON,DC=local", "CN=GTeachers,OU=Groups,OU=Horizon,DC=HORIZON,DC=local",\
"CN=SG_Admin,OU=User Groups,OU=Groups,OU=Horizon,DC=HORIZON,DC=local"],"Managment":["SG_FS_Management,OU=SG_FileShare,OU=Groups,OU=Horizon,DC=HORIZON,DC=local",\
"CN=Local PC Administrators,OU=Groups,OU=Horizon,DC=HORIZON,DC=local", "CN=Office365-A1Plus-Faculty,OU=Office 365,OU=Groups,OU=Horizon,DC=HORIZON,DC=local",\
"CN=Office365-AzureAD-P2,OU=Office 365,OU=Groups,OU=Horizon,DC=HORIZON,DC=local", "SG_FS_Adminfiles,OU=SG_FileShare,OU=Groups,OU=Horizon,DC=HORIZON,DC=local", "CN=SG_WF_Staff,OU=Firewall,OU=Groups,OU=Horizon,DC=HORIZON,DC=local",\
"CN=Horizon Staff,OU=Groups,OU=Horizon,DC=HORIZON,DC=local", "CN=Library Users,OU=Groups,OU=Horizon,DC=HORIZON,DC=local", "SG_FS_Photos,OU=SG_FileShare,OU=Groups,OU=Horizon,DC=HORIZON,DC=local",\
"CN=GEveryone,OU=Groups,OU=Horizon,DC=HORIZON,DC=local", "CN=GTeachers,OU=Groups,OU=Horizon,DC=HORIZON,DC=local", "CN=SG_Teachers,OU=User Groups,OU=Groups,OU=Horizon,DC=HORIZON,DC=local"],"Primary Teacher":\
["CN=Office365-A1Plus-Faculty,OU=Office 365,OU=Groups,OU=Horizon,DC=HORIZON,DC=local", "CN=Office365-AzureAD-P2,OU=Office 365,OU=Groups,OU=Horizon,DC=HORIZON,DC=local",\
"CN=SG_FS_Adminfiles,OU=SG_FileShare,OU=Groups,OU=Horizon,DC=HORIZON,DC=local", "CN=SG_WF_Staff,OU=Firewall,OU=Groups,OU=Horizon,DC=HORIZON,DC=local", "CN=Horizon Staff,OU=Groups,OU=Horizon,DC=HORIZON,DC=local",\
"CN=Library Users,OU=Groups,OU=Horizon,DC=HORIZON,DC=local", "CN=SG_FS_Photos,OU=SG_FileShare,OU=Groups,OU=Horizon,DC=HORIZON,DC=local", "CN=GEveryone,OU=Groups,OU=Horizon,DC=HORIZON,DC=local", "CN=GTeachers,OU=Groups,OU=Horizon,DC=HORIZON,DC=local",\
"CN=SG_Teachers,OU=User Groups,OU=Groups,OU=Horizon,DC=HORIZON,DC=local"],"Secondary Teacher":\
["CN=Office365-A1Plus-Faculty,OU=Office 365,OU=Groups,OU=Horizon,DC=HORIZON,DC=local", "CN=Office365-AzureAD-P2,OU=Office 365,OU=Groups,OU=Horizon,DC=HORIZON,DC=local",\
"CN=SG_FS_Adminfiles,OU=SG_FileShare,OU=Groups,OU=Horizon,DC=HORIZON,DC=local", "CN=SG_WF_Staff,OU=Firewall,OU=Groups,OU=Horizon,DC=HORIZON,DC=local", "CN=Horizon Staff,OU=Groups,OU=Horizon,DC=HORIZON,DC=local",\
"CN=Library Users,OU=Groups,OU=Horizon,DC=HORIZON,DC=local", "CN=SG_FS_Photos,OU=SG_FileShare,OU=Groups,OU=Horizon,DC=HORIZON,DC=local", "CN=GEveryone,OU=Groups,OU=Horizon,DC=HORIZON,DC=local", "CN=GTeachers,OU=Groups,OU=Horizon,DC=HORIZON,DC=local",\
"CN=SG_Teachers,OU=User Groups,OU=Groups,OU=Horizon,DC=HORIZON,DC=local"],"Temporary Teacher":\
["CN=Office365-A1Plus-Faculty,OU=Office 365,OU=Groups,OU=Horizon,DC=HORIZON,DC=local", "CN=Office365-AzureAD-P2,OU=Office 365,OU=Groups,OU=Horizon,DC=HORIZON,DC=local",\
"CN=SG_FS_Adminfiles,OU=SG_FileShare,OU=Groups,OU=Horizon,DC=HORIZON,DC=local", "CN=SG_WF_Staff,OU=Firewall,OU=Groups,OU=Horizon,DC=HORIZON,DC=local", "CN=Horizon Staff,OU=Groups,OU=Horizon,DC=HORIZON,DC=local",\
"CN=Library Users,OU=Groups,OU=Horizon,DC=HORIZON,DC=local", "CN=SG_FS_Photos,OU=SG_FileShare,OU=Groups,OU=Horizon,DC=HORIZON,DC=local", "CN=GEveryone,OU=Groups,OU=Horizon,DC=HORIZON,DC=local",\
"CN=GTeachers,OU=Groups,OU=Horizon,DC=HORIZON,DC=local", "CN=SG_Teachers,OU=User Groups,OU=Groups,OU=Horizon,DC=HORIZON,DC=local"],"ESO":\
["CN=Office365-A1Plus-Faculty,OU=Office 365,OU=Groups,OU=Horizon,DC=HORIZON,DC=local", "CN=Office365-AzureAD-P2,OU=Office 365,OU=Groups,OU=Horizon,DC=HORIZON,DC=local",\
"CN=SG_FS_Adminfiles,OU=SG_FileShare,OU=Groups,OU=Horizon,DC=HORIZON,DC=local", "CN=SG_WF_Staff,OU=Firewall,OU=Groups,OU=Horizon,DC=HORIZON,DC=local", "CN=Horizon Staff,OU=Groups,OU=Horizon,DC=HORIZON,DC=local",\
"CN=Office Staff,OU=Groups,OU=Horizon,DC=HORIZON,DC=local", "CN=Library Users,OU=Groups,OU=Horizon,DC=HORIZON,DC=local", "CN=SG_FS_Photos,OU=SG_FileShare,OU=Groups,OU=Horizon,DC=HORIZON,DC=local",\
"CN=GEveryone,OU=Groups,OU=Horizon,DC=HORIZON,DC=local", "CN=GTeachers,OU=Groups,OU=Horizon,DC=HORIZON,DC=local"],"Admin":\
["CN=Office365-A1Plus-Faculty,OU=Office 365,OU=Groups,OU=Horizon,DC=HORIZON,DC=local", "CN=Office365-AzureAD-P2,OU=Office 365,OU=Groups,OU=Horizon,DC=HORIZON,DC=local",\
"CN=SG_FS_Adminfiles,OU=SG_FileShare,OU=Groups,OU=Horizon,DC=HORIZON,DC=local", "CN=SG_WF_Staff,OU=Firewall,OU=Groups,OU=Horizon,DC=HORIZON,DC=local", "CN=Horizon Staff,OU=Groups,OU=Horizon,DC=HORIZON,DC=local",\
"CN=SG_FS_PCSchools,OU=SG_FileShare,OU=Groups,OU=Horizon,DC=HORIZON,DC=local", "CN=SG_FS_Photos,OU=SG_FileShare,OU=Groups,OU=Horizon,DC=HORIZON,DC=local", "CN=SG_LA_Reception,OU=LocalAdmin,OU=Groups,OU=Horizon,DC=HORIZON,DC=local",\
"CN=SG_LA_STAFF055,OU=LocalAdmin,OU=Groups,OU=Horizon,DC=HORIZON,DC=local", "CN=SG_LA_StudentDesk,OU=LocalAdmin,OU=Groups,OU=Horizon,DC=HORIZON,DC=local", "CN=SG_Admin,OU=User Groups,OU=Groups,OU=Horizon,DC=HORIZON,DC=local"],\
"Admin Temp":["CN=Office365-A1Plus-Faculty,OU=Office 365,OU=Groups,OU=Horizon,DC=HORIZON,DC=local",\
"CN=Office365-AzureAD-P2,OU=Office 365,OU=Groups,OU=Horizon,DC=HORIZON,DC=local", "CN=SG_FS_Adminfiles,OU=SG_FileShare,OU=Groups,OU=Horizon,DC=HORIZON,DC=local",\
"CN=SG_WF_Staff,OU=Firewall,OU=Groups,OU=Horizon,DC=HORIZON,DC=local", "CN=Horizon Staff,OU=Groups,OU=Horizon,DC=HORIZON,DC=local", "CN=SG_FS_PCSchools,OU=SG_FileShare,OU=Groups,OU=Horizon,DC=HORIZON,DC=local",\
"CN=SG_FS_Photos,OU=SG_FileShare,OU=Groups,OU=Horizon,DC=HORIZON,DC=local", "CN=SG_LA_Reception,OU=LocalAdmin,OU=Groups,OU=Horizon,DC=HORIZON,DC=local", "CN=SG_LA_STAFF055,OU=LocalAdmin,OU=Groups,OU=Horizon,DC=HORIZON,DC=local",\
"CN=SG_LA_StudentDesk,OU=LocalAdmin,OU=Groups,OU=Horizon,DC=HORIZON,DC=local", "CN=SG_Admin,OU=User Groups,OU=Groups,OU=Horizon,DC=HORIZON,DC=local"],"Grounds":\
["CN=Office365-A1Plus-Faculty,OU=Office 365,OU=Groups,OU=Horizon,DC=HORIZON,DC=local", "CN=Office365-AzureAD-P2,OU=Office 365,OU=Groups,OU=Horizon,DC=HORIZON,DC=local",\
"CN=SG_WF_Staff,OU=Firewall,OU=Groups,OU=Horizon,DC=HORIZON,DC=local", "CN=Horizon Staff,OU=Groups,OU=Horizon,DC=HORIZON,DC=local"],"Counsellor":\
["CN=Office365-A1Plus-Faculty,OU=Office 365,OU=Groups,OU=Horizon,DC=HORIZON,DC=local", "CN=Office365-AzureAD-P2,OU=Office 365,OU=Groups,OU=Horizon,DC=HORIZON,DC=local",\
"CN=SG_FS_Adminfiles,OU=SG_FileShare,OU=Groups,OU=Horizon,DC=HORIZON,DC=local", "CN=SG_WF_Staff,OU=Firewall,OU=Groups,OU=Horizon,DC=HORIZON,DC=local", "CN=Horizon Staff,OU=Groups,OU=Horizon,DC=HORIZON,DC=local",\
"CN=SG_FS_Photos,OU=SG_FileShare,OU=Groups,OU=Horizon,DC=HORIZON,DC=local", "CN=GEveryone,OU=Groups,OU=Horizon,DC=HORIZON,DC=local", "CN=GTeachers,OU=Groups,OU=Horizon,DC=HORIZON,DC=local",\
"CN=Library Users,OU=Groups,OU=Horizon,DC=HORIZON,DC=local", "Primary", "CN=SG_FS_Counsellors,OU=SG_FileShare,OU=Groups,OU=Horizon,DC=HORIZON,DC=local",\
"SG_MFA_Counsellors", "CN=SG_Admin,OU=User Groups,OU=Groups,OU=Horizon,DC=HORIZON,DC=local"],"Foundation":\
["CN=SG_Reception,OU=Year Levels,OU=Groups,OU=Horizon,DC=HORIZON,DC=local", "CN=Office365-A3-Student,OU=Office 365,OU=Groups,OU=Horizon,DC=HORIZON,DC=local",\
"CN=Office365-AzureAD-P2,OU=Office 365,OU=Groups,OU=Horizon,DC=HORIZON,DC=local", "CN=SG_Students,OU=User Groups,OU=Groups,OU=Horizon,DC=HORIZON,DC=local",\
"CN=SG_WF_Student,OU=Firewall,OU=Groups,OU=Horizon,DC=HORIZON,DC=local"],"Year1":["CN=SG_Year1,OU=Year Levels,OU=Groups,OU=Horizon,DC=HORIZON,DC=local",\
"CN=Office365-A3-Student,OU=Office 365,OU=Groups,OU=Horizon,DC=HORIZON,DC=local", "CN=Office365-AzureAD-P2,OU=Office 365,OU=Groups,OU=Horizon,DC=HORIZON,DC=local",\
"CN=SG_Students,OU=User Groups,OU=Groups,OU=Horizon,DC=HORIZON,DC=local", "CN=SG_WF_Student,OU=Firewall,OU=Groups,OU=Horizon,DC=HORIZON,DC=local"],"Year2":["CN=SG_Year2,OU=Year Levels,OU=Groups,OU=Horizon,DC=HORIZON,DC=local",\
"CN=Office365-A3-Student,OU=Office 365,OU=Groups,OU=Horizon,DC=HORIZON,DC=local", "CN=Office365-AzureAD-P2,OU=Office 365,OU=Groups,OU=Horizon,DC=HORIZON,DC=local",\
"CN=SG_Students,OU=User Groups,OU=Groups,OU=Horizon,DC=HORIZON,DC=local", "CN=SG_WF_Student,OU=Firewall,OU=Groups,OU=Horizon,DC=HORIZON,DC=local"],"Year3":["CN=SG_Year3,OU=Year Levels,OU=Groups,OU=Horizon,DC=HORIZON,DC=local",\
"CN=Office365-A3-Student,OU=Office 365,OU=Groups,OU=Horizon,DC=HORIZON,DC=local", "CN=Office365-AzureAD-P2,OU=Office 365,OU=Groups,OU=Horizon,DC=HORIZON,DC=local",\
"CN=SG_Students,OU=User Groups,OU=Groups,OU=Horizon,DC=HORIZON,DC=local", "CN=SG_WF_Student,OU=Firewall,OU=Groups,OU=Horizon,DC=HORIZON,DC=local"],"Year4":\
["CN=SG_Year4,OU=Year Levels,OU=Groups,OU=Horizon,DC=HORIZON,DC=local", "CN=Office365-A3-Student,OU=Office 365,OU=Groups,OU=Horizon,DC=HORIZON,DC=local",\
"CN=Office365-AzureAD-P2,OU=Office 365,OU=Groups,OU=Horizon,DC=HORIZON,DC=local", "CN=SG_Students,OU=User Groups,OU=Groups,OU=Horizon,DC=HORIZON,DC=local",\
"CN=SG_WF_Student,OU=Firewall,OU=Groups,OU=Horizon,DC=HORIZON,DC=local"],"Year5":\
["CN=SG_Year5,OU=Year Levels,OU=Groups,OU=Horizon,DC=HORIZON,DC=local", "CN=Office365-A3-Student,OU=Office 365,OU=Groups,OU=Horizon,DC=HORIZON,DC=local",\
"CN=Office365-AzureAD-P2,OU=Office 365,OU=Groups,OU=Horizon,DC=HORIZON,DC=local", "CN=SG_Students,OU=User Groups,OU=Groups,OU=Horizon,DC=HORIZON,DC=local",\
"CN=SG_WF_Student,OU=Firewall,OU=Groups,OU=Horizon,DC=HORIZON,DC=local"],"Year6":["CN=SG_Year6,OU=Year Levels,OU=Groups,OU=Horizon,DC=HORIZON,DC=local",\
"CN=Office365-A3-Student,OU=Office 365,OU=Groups,OU=Horizon,DC=HORIZON,DC=local", "CN=Office365-AzureAD-P2,OU=Office 365,OU=Groups,OU=Horizon,DC=HORIZON,DC=local",\
"CN=SG_Students,OU=User Groups,OU=Groups,OU=Horizon,DC=HORIZON,DC=local", "CN=SG_WF_Student,OU=Firewall,OU=Groups,OU=Horizon,DC=HORIZON,DC=local"],"Year7":\
["CN=SG_Year7,OU=Year Levels,OU=Groups,OU=Horizon,DC=HORIZON,DC=local", "CN=Office365-A3-Student,OU=Office 365,OU=Groups,OU=Horizon,DC=HORIZON,DC=local",\
"CN=Office365-AzureAD-P2,OU=Office 365,OU=Groups,OU=Horizon,DC=HORIZON,DC=local", "CN=SG_Students,OU=User Groups,OU=Groups,OU=Horizon,DC=HORIZON,DC=local",\
"CN=SG_WF_Student,OU=Firewall,OU=Groups,OU=Horizon,DC=HORIZON,DC=local"],"Year8":["CN=SG_Year8,OU=Year Levels,OU=Groups,OU=Horizon,DC=HORIZON,DC=local",\
"CN=Office365-A3-Student,OU=Office 365,OU=Groups,OU=Horizon,DC=HORIZON,DC=local", "CN=Office365-AzureAD-P2,OU=Office 365,OU=Groups,OU=Horizon,DC=HORIZON,DC=local",\
"CN=SG_Students,OU=User Groups,OU=Groups,OU=Horizon,DC=HORIZON,DC=local", "CN=SG_WF_Student,OU=Firewall,OU=Groups,OU=Horizon,DC=HORIZON,DC=local"],"Year9":\
["CN=SG_Year9,OU=Year Levels,OU=Groups,OU=Horizon,DC=HORIZON,DC=local", "CN=Office365-A3-Student,OU=Office 365,OU=Groups,OU=Horizon,DC=HORIZON,DC=local",\
"CN=Office365-AzureAD-P2,OU=Office 365,OU=Groups,OU=Horizon,DC=HORIZON,DC=local", "CN=SG_Students,OU=User Groups,OU=Groups,OU=Horizon,DC=HORIZON,DC=local",\
"CN=SG_WF_Student,OU=Firewall,OU=Groups,OU=Horizon,DC=HORIZON,DC=local"],"Year10":["CN=SG_Year10,OU=User Groups,OU=Groups,OU=Horizon,DC=HORIZON,DC=local",\
"CN=Office365-A3-Student,OU=Office 365,OU=Groups,OU=Horizon,DC=HORIZON,DC=local", "CN=Office365-AzureAD-P2,OU=Office 365,OU=Groups,OU=Horizon,DC=HORIZON,DC=local",\
"CN=SG_Students,OU=User Groups,OU=Groups,OU=Horizon,DC=HORIZON,DC=local", "CN=SG_WF_Student,OU=Firewall,OU=Groups,OU=Horizon,DC=HORIZON,DC=local"],"Year11":\
["CN=SG_Year11,OU=Year Levels,OU=Groups,OU=Horizon,DC=HORIZON,DC=local", "CN=Office365-A3-Student,OU=Office 365,OU=Groups,OU=Horizon,DC=HORIZON,DC=local",\
"CN=Office365-AzureAD-P2,OU=Office 365,OU=Groups,OU=Horizon,DC=HORIZON,DC=local", "CN=SG_Students,OU=User Groups,OU=Groups,OU=Horizon,DC=HORIZON,DC=local",\
"CN=SG_WF_Student,OU=Firewall,OU=Groups,OU=Horizon,DC=HORIZON,DC=local"],"Year12":["CN=SG_Year12,OU=Year Levels,OU=Groups,OU=Horizon,DC=HORIZON,DC=local",\
"CN=Office365-A3-Student,OU=Office 365,OU=Groups,OU=Horizon,DC=HORIZON,DC=local", "CN=Office365-AzureAD-P2,OU=Office 365,OU=Groups,OU=Horizon,DC=HORIZON,DC=local",\
"CN=SG_Students,OU=User Groups,OU=Groups,OU=Horizon,DC=HORIZON,DC=local", "CN=SG_WF_Student,OU=Firewall,OU=Groups,OU=Horizon,DC=HORIZON,DC=local"]}',
                    "UTF-8",
                )
            ).decode("UTF-8")
        )
        conf_file["Horizon"]["positions"] = str(
            base64.b64encode(
                bytes(
                    '{"Staff":["Executive","Managment","Admin",\
"Admin Temp","Primary Teacher","Secondary Teacher",\
"Temporary Teacher","ESO","Grounds",\
"Counsellor"],\
"Students":["Foundation","Year1","Year2","Year3","Year4","Year5","Year6",\
"Year7","Year8","Year9","Year10","Year11","Year12"]}',
                    "UTF-8",
                )
            ).decode("UTF-8")
        )
        conf_file["Horizon"]["positionsou"] = str(
            base64.b64encode(
                bytes(
                    '{"Executive":"OU=Executive,OU=Staff,OU=Users,\
OU=Horizon,DC=HORIZON,DC=local",\
"Managment":"OU=Managment,OU=Staff,OU=Users,OU=Horizon,\
DC=HORIZON,DC=local","Primary Teacher":\
"OU=Primary Teachers,OU=Teachers,OU=Staff,OU=Users,\
OU=Horizon,DC=HORIZON,DC=local","Secondary Teacher":\
"OU=Secondary Teachers,OU=Teachers,OU=Staff,OU=Users,\
OU=Horizon,DC=HORIZON,DC=local","Temporary Teacher":\
"OU=Temporary Teachers,OU=Teachers,OU=Staff,OU=Users,\
OU=Horizon,DC=HORIZON,DC=local","ESO":"OU=Student Support,\
OU=Staff,OU=Users,OU=Horizon,DC=HORIZON,DC=local",\
"Student Support Clare":"OU=Student Support Clare,OU=Staff,OU=Users,\
OU=Horizon,DC=HORIZON,DC=local","Admin":\
"OU=Admin Staff,OU=Staff,OU=Users,OU=Horizon,DC=HORIZON,\
DC=local","Admin Clare": "OU=Admin Staff Clare,OU=Staff,\
OU=Users,OU=Horizon,DC=HORIZON,DC=local",\
"Admin Temp":"OU=Admin Temp,OU=Staff,OU=Users,\
OU=Horizon,DC=HORIZON,DC=local","Grounds":"OU=Ancillary,\
OU=Staff,OU=Users,OU=Horizon,DC=HORIZON,DC=local",\
"Counsellor":"OU=Student Support,OU=Staff,OU=Users,\
OU=Horizon,DC=HORIZON,DC=local","Foundation":\
"OU=Foundation,OU=Students,OU=Users,OU=Horizon,\
DC=HORIZON,DC=local","Year1":"OU=Year 1,OU=Students,\
OU=Users,OU=Horizon,DC=HORIZON,DC=local","Year2":\
"OU=Year 2,OU=Students,OU=Users,OU=Horizon,DC=HORIZON,\
DC=local","Year3":"OU=Year 3,OU=Students,OU=Users,\
OU=Horizon,DC=HORIZON,DC=local","Year4":"OU=Year 4,\
OU=Students,OU=Users,OU=Horizon,DC=HORIZON,DC=local",\
"Year5":"OU=Year 5,OU=Students,OU=Users,OU=Horizon,\
DC=HORIZON,DC=local","Year6":"OU=Year 6,OU=Students,\
OU=Users,OU=Horizon,DC=HORIZON,DC=local","Year7":\
"OU=Year 7,OU=Students,OU=Users,OU=Horizon,DC=HORIZON,\
DC=local","Year8":"OU=Year 8,OU=Students,OU=Users,\
OU=Horizon,DC=HORIZON,DC=local","Year9":"OU=Year 9,\
OU=Students,OU=Users,OU=Horizon,DC=HORIZON,DC=local",\
"Year10":"OU=Year 10,OU=Students,OU=Users,OU=Horizon,\
DC=HORIZON,DC=local","Year11":"OU=Year 11,OU=Students,\
OU=Users,OU=Horizon,DC=HORIZON,DC=local","Year12":\
"OU=Year 12,OU=Students,OU=Users,OU=Horizon,DC=HORIZON,\
DC=local","Foundation-Clare":"OU=Foundation,\
OU=Students-Clare,OU=Users,OU=Horizon,DC=HORIZON,\
DC=local","Year1-Clare":"OU=Year 1,OU=Students-Clare,\
OU=Users,OU=Horizon,DC=HORIZON,DC=local","Year2-Clare":\
"OU=Year 2,OU=Students-Clare,OU=Users,OU=Horizon,\
DC=HORIZON,DC=local","Year3-Clare":"OU=Year 3,\
OU=Students-Clare,OU=Users,OU=Horizon,DC=HORIZON,\
DC=local","Year4-Clare":"OU=Year 4,OU=Students-Clare,\
OU=Users,OU=Horizon,DC=HORIZON,DC=local","Year5-Clare":\
"OU=Year 5,OU=Students-Clare,OU=Users,OU=Horizon,\
DC=HORIZON,DC=local","Year6-Clare":"OU=Year 6,\
OU=Students-Clare,OU=Users,OU=Horizon,DC=HORIZON,DC=local",\
"Year7-Clare":"OU=Year 7,OU=Students-Clare,OU=Users,\
OU=Horizon,DC=HORIZON,DC=local","Year8-Clare":"OU=Year 8,\
OU=Students-Clare,OU=Users,OU=Horizon,DC=HORIZON,DC=local",\
"Year9-Clare":"OU=Year 9,OU=Students-Clare,OU=Users,\
OU=Horizon,DC=HORIZON,DC=local","Year10-Clare":\
"OU=Year 10,OU=Students-Clare,OU=Users,OU=Horizon,\
DC=HORIZON,DC=local",\
"Year11-Clare":"OU=Year 11,OU=Students-Clare,OU=Users,\
OU=Horizon,DC=HORIZON,DC=local",\
"Year12-Clare":"OU=Year 12,\
OU=Students-Clare,OU=Users,OU=Horizon,\
DC=HORIZON,DC=local"}',
                    "UTF-8",
                )
            ).decode("UTF-8")
        )
        conf_file["Horizon"]["title"] = str(
            base64.b64encode(
                bytes(
                    '{"Executive":"Executive Team","Managment":\
"Management Team","Admin":"Administration","Admin Temp":\
"Temporary Administrator","Primary Teacher":"Primary Teacher",\
"Secondary Teacher":"Secondary Teacher","Temporary Teacher":\
"Temporary Teacher","ESO":"Student Support","Grounds":\
"Grounds and Maintenance","Counsellor":"Counsellor",\
"Foundation":"Foundation Student","Year1":"Year 1 Student",\
"Year2":"Year 2 Student","Year3":"Year 3 Student","Year4":\
"Year 4 Student","Year5":"Year 5 Student","Year6":\
"Year 6 Student","Year7":"Year 7 Student","Year8":\
"Year 8 Student","Year9":"Year 9 Student","Year10":\
"Year 10 Student","Year11":"Year 11 Student","Year12":\
"Year 12 Student"}',
                    "UTF-8",
                )
            ).decode("UTF-8")
        )
        conf_file["Horizon"]["expiredous"] = str(
            base64.b64encode(
                bytes(
                    '{"Disabled":"OU=Disabled,OU=Users,OU=Horizon,DC=HORIZON,\
DC=local","ExpiredStaff":"OU=ExpiredStaff,OU=Users,\
OU=Horizon,DC=HORIZON,DC=local","ExpiredStudents":\
"OU=ExpiredStudents,OU=Users,OU=Horizon,DC=HORIZON,\
DC=local"}',
                    "UTF-8",
                )
            ).decode("UTF-8")
        )
        conf_file["Horizon"]["groupsou"] = str(
            base64.b64encode(
                bytes("OU=Groups,OU=Horizon,DC=HORIZON,DC=local", "UTF-8")
            ).decode("UTF-8")
        )
        conf_file["Horizon"]["domains"] = str(
            base64.b64encode(
                bytes(
                    '{"Primary":["horizon.sa.edu.au"],"Secondary":"horizonsa.onmicrosoft.com"}',
                    "UTF-8",
                )
            ).decode("UTF-8")
        )
        conf_file["Horizon"]["homepaths"] = str(
            base64.b64encode(
                bytes(
                    "\\\\HCS-FS01\\office_stuserver,\
\\\\HCS-FS01\\teachers_stuserver,\
\\\\HCS-FS01\\students_stuserver",
                    "UTF-8",
                )
            ).decode("UTF-8")
        )
        conf_file["Horizon"]["campus"] = str(
            base64.b64encode(bytes("balaklava,clare", "UTF-8")).decode("UTF-8")
        )

        with open(settings_dir + settings_file, "wb") as file_handle:
            conf_file.write_encrypted(file_handle)


if __name__ == "__main__":
    MakeConf()
