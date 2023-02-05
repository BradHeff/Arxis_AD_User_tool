
from configparser_crypt import ConfigParserCrypt
from pathlib import Path
# import sys
import base64

exe_dir = str(Path(__file__).parents[0])

settings_file = "Settings.dat"
settings_dir = ''.join([exe_dir, '\\Settings\\'])

class MakeConf():
    def __init__(self):
        super(MakeConf, self).__init__()
        self.old = ""
        self.key = ""
        self.lines = []
        self.readLines()
        self.writeConfig()
        self.writeLines()
        print(self.key)
        # str(base64.b64encode(bytes('HCS-DC01.HORIZON.local','UTF-8')).decode("UTF-8"))

    def _getPosition(self, file, text):
        nlist = [x for x in file if text in x]
        print(exe_dir + "\\Functions.py")
        position = file.index(nlist[0])
        return position

    def readLines(self):
        with open(exe_dir + "\\Functions.py", "r") as f:
            self.lines = f.readlines()
            pos = self._getPosition(self.lines, "key = ")
            line = self.lines[pos]
            self.old = line.split(" = ")[1].strip()
            f.close()

    def writeLines(self):
        with open(exe_dir + "\\Functions.py", "w") as w:
            pos = self._getPosition(self.lines, "key = ")

            self.lines[pos] = self.lines[pos].replace(
                self.old, str(self.key))

            w.writelines(self.lines)
            w.close()

    def writeConfig(self):
        conf_file = ConfigParserCrypt()
        conf_file.generate_key()
        self.key = conf_file.aes_key

        conf_file.add_section('Horizon')
        # conf_file['Horizon']['server'] = str(base64.b64encode(bytes('DCM-DC01.DCOMPUTERS.local','UTF-8')).decode("UTF-8"))
        # conf_file['Horizon']['server_user'] = str(base64.b64encode(bytes('administrator','UTF-8')).decode("UTF-8"))
        # conf_file['Horizon']['server_pass'] = str(base64.b64encode(bytes('Heffserver2022!','UTF-8')).decode("UTF-8"))
        # conf_file['Horizon']['userou'] = str(base64.b64encode(bytes('OU=Users,OU=DCOMPUTERS,DC=DCOMPUTERS,DC=local','UTF-8')).decode("UTF-8"))
        # conf_file['Horizon']['domainname'] = str(base64.b64encode(bytes('DCOMPUTERS','UTF-8')).decode("UTF-8"))
        conf_file['Horizon']['server'] = str(base64.b64encode(bytes('HCS-DC01.HORIZON.local','UTF-8')).decode("UTF-8"))
        conf_file['Horizon']['server_user'] = str(base64.b64encode(bytes('pyservice','UTF-8')).decode("UTF-8"))
        conf_file['Horizon']['server_pass'] = str(base64.b64encode(bytes('Duffel1-Wound-Antelope','UTF-8')).decode("UTF-8"))
        conf_file['Horizon']['userou'] = str(base64.b64encode(bytes('OU=Users,OU=Horizon,DC=HORIZON,DC=local','UTF-8')).decode("UTF-8"))
        conf_file['Horizon']['domainname'] = str(base64.b64encode(bytes('HORIZON','UTF-8')).decode("UTF-8"))
        conf_file['Horizon']['groups'] = str(base64.b64encode(bytes('{"Executive":["SG_FS_Management", "SG_FS_HR", "SG_FS_ExecDrive", "Local PC Administrators", "Office365-A1Plus-Faculty", "Office365-AzureAD-P2", "SG_FS_Adminfiles", "SG_WF_Staff", "Horizon Staff", "Library Users", "SG_FS_Photos", "GEveryone", "GTeachers", "SG_Admin"],"Managment":["SG_FS_Management","Local PC Administrators", "Office365-A1Plus-Faculty", "Office365-AzureAD-P2", "SG_FS_Adminfiles", "SG_WF_Staff", "Horizon Staff", "Library Users", "SG_FS_Photos", "GEveryone", "GTeachers", "SG_Teachers"],"Primary Teacher":["Office365-A1Plus-Faculty", "Office365-AzureAD-P2", "SG_FS_Adminfiles", "SG_WF_Staff", "Horizon Staff", "Library Users", "SG_FS_Photos", "GEveryone", "GTeachers", "SG_Teachers"],"Secondary Teacher":["Office365-A1Plus-Faculty", "Office365-AzureAD-P2", "SG_FS_Adminfiles", "SG_WF_Staff", "Horizon Staff", "Library Users", "SG_FS_Photos", "GEveryone", "GTeachers", "SG_Teachers"],"Temporary Teacher":["Office365-A1Plus-Faculty", "Office365-AzureAD-P2", "SG_FS_Adminfiles", "SG_WF_Staff", "Horizon Staff", "Library Users", "SG_FS_Photos", "GEveryone", "GTeachers", "SG_Teachers"],"ESO":["Office365-A1Plus-Faculty", "Office365-AzureAD-P2", "SG_FS_Adminfiles", "SG_WF_Staff", "Horizon Staff", "Office Staff", "Library Users", "SG_FS_Photos", "GEveryone", "GTeachers"],"Admin":["Office365-A1Plus-Faculty", "Office365-AzureAD-P2", "SG_FS_Adminfiles", "SG_WF_Staff", "Horizon Staff", "SG_FS_PCSchools", "SG_FS_Photos", "SG_LA_Reception", "SG_LA_STAFF055", "SG_LA_StudentDesk", "SG_Admin"],"Admin Temp":["Office365-A1Plus-Faculty", "Office365-AzureAD-P2", "SG_FS_Adminfiles", "SG_WF_Staff", "Horizon Staff", "SG_FS_PCSchools", "SG_FS_Photos", "SG_LA_Reception", "SG_LA_STAFF055", "SG_LA_StudentDesk", "SG_Admin"],"Grounds":["Office365-A1Plus-Faculty", "Office365-AzureAD-P2", "SG_WF_Staff", "Horizon Staff"],"Counsellor":["Office365-A1Plus-Faculty", "Office365-AzureAD-P2", "SG_FS_Adminfiles", "SG_WF_Staff", "Horizon Staff", "SG_FS_Photos", "GEveryone", "GTeachers", "Library Users", "Primary", "SG_FS_Counsellors", "SG_MFA_Counsellors", "SG_Admin"],"Foundation":["SG_Reception", "Office365-A3-Student", "Office365-AzureAD-P2", "SG_Students", "SG_WF_Student"],"Year1":["SG_Year1", "Office365-A3-Student", "Office365-AzureAD-P2", "SG_Students", "SG_WF_Student"],"Year2":["SG_Year2", "Office365-A3-Student", "Office365-AzureAD-P2", "SG_Students", "SG_WF_Student"],"Year3":["SG_Year3", "Office365-A3-Student", "Office365-AzureAD-P2", "SG_Students", "SG_WF_Student"],"Year4":["SG_Year4", "Office365-A3-Student", "Office365-AzureAD-P2", "SG_Students", "SG_WF_Student"],"Year5":["SG_Year5", "Office365-A3-Student", "Office365-AzureAD-P2", "SG_Students", "SG_WF_Student"],"Year6":["SG_Year6", "Office365-A3-Student", "Office365-AzureAD-P2", "SG_Students", "SG_WF_Student"],"Year7":["SG_Year7", "Office365-A3-Student", "Office365-AzureAD-P2", "SG_Students", "SG_WF_Student"],"Year8":["SG_Year8", "Office365-A3-Student", "Office365-AzureAD-P2", "SG_Students", "SG_WF_Student"],"Year9":["SG_Year9", "Office365-A3-Student", "Office365-AzureAD-P2", "SG_Students", "SG_WF_Student"],"Year10":["SG_Year10", "Office365-A3-Student", "Office365-AzureAD-P2", "SG_Students", "SG_WF_Student"],"Year11":["SG_Year11", "Office365-A3-Student", "Office365-AzureAD-P2", "SG_Students", "SG_WF_Student"],"Year12":["SG_Year12", "Office365-A3-Student", "Office365-AzureAD-P2", "SG_Students", "SG_WF_Student"]}','UTF-8')).decode("UTF-8"))
        conf_file['Horizon']['positions'] = str(base64.b64encode(bytes('{"Staff":["Executive","Managment","Admin","Admin Temp","Primary Teacher","Secondary Teacher","Temporary Teacher","ESO","Grounds","Counsellor"],"Students":["Foundation","Year1","Year2","Year3","Year4","Year5","Year6","Year7","Year8","Year9","Year10","Year11","Year12"]}','UTF-8')).decode("UTF-8"))
        conf_file['Horizon']['positionsou'] = str(base64.b64encode(bytes('{"Executive":"OU=Executive,OU=Staff,OU=Users,OU=Horizon,DC=HORIZON,DC=local","Managment":"OU=Managment,OU=Staff,OU=Users,OU=Horizon,DC=HORIZON,DC=local","Primary Teacher":"OU=Primary Teachers,OU=Teachers,OU=Staff,OU=Users,OU=Horizon,DC=HORIZON,DC=local","Secondary Teacher":"OU=Secondary Teachers,OU=Teachers,OU=Staff,OU=Users,OU=Horizon,DC=HORIZON,DC=local","Temporary Teacher":"OU=Temporary Teachers,OU=Teachers,OU=Staff,OU=Users,OU=Horizon,DC=HORIZON,DC=local","ESO":"OU=Student Support,OU=Staff,OU=Users,OU=Horizon,DC=HORIZON,DC=local","Admin":"OU=Admin Staff,OU=Staff,OU=Users,OU=Horizon,DC=HORIZON,DC=local","Admin Temp":"OU=Admin Temp,OU=Staff,OU=Users,OU=Horizon,DC=HORIZON,DC=local","Grounds":"OU=Ancillary,OU=Staff,OU=Users,OU=Horizon,DC=HORIZON,DC=local","Counsellor":"OU=Student Support,OU=Staff,OU=Users,OU=Horizon,DC=HORIZON,DC=local","Foundation":"OU=Foundation,OU=Students,OU=Users,OU=Horizon,DC=HORIZON,DC=local","Year1":"OU=Year 1,OU=Students,OU=Users,OU=Horizon,DC=HORIZON,DC=local","Year2":"OU=Year 2,OU=Students,OU=Users,OU=Horizon,DC=HORIZON,DC=local","Year3":"OU=Year 3,OU=Students,OU=Users,OU=Horizon,DC=HORIZON,DC=local","Year4":"OU=Year 4,OU=Students,OU=Users,OU=Horizon,DC=HORIZON,DC=local","Year5":"OU=Year 5,OU=Students,OU=Users,OU=Horizon,DC=HORIZON,DC=local","Year6":"OU=Year 6,OU=Students,OU=Users,OU=Horizon,DC=HORIZON,DC=local","Year7":"OU=Year 7,OU=Students,OU=Users,OU=Horizon,DC=HORIZON,DC=local","Year8":"OU=Year 8,OU=Students,OU=Users,OU=Horizon,DC=HORIZON,DC=local","Year9":"OU=Year 9,OU=Students,OU=Users,OU=Horizon,DC=HORIZON,DC=local","Year10":"OU=Year 10,OU=Students,OU=Users,OU=Horizon,DC=HORIZON,DC=local","Year11":"OU=Year 11,OU=Students,OU=Users,OU=Horizon,DC=HORIZON,DC=local","Year12":"OU=Year 12,OU=Students,OU=Users,OU=Horizon,DC=HORIZON,DC=local","Foundation-Clare":"OU=Foundation,OU=Students-Clare,OU=Users,OU=Horizon,DC=HORIZON,DC=local","Year1-Clare":"OU=Year 1,OU=Students-Clare,OU=Users,OU=Horizon,DC=HORIZON,DC=local","Year2-Clare":"OU=Year 2,OU=Students-Clare,OU=Users,OU=Horizon,DC=HORIZON,DC=local","Year3-Clare":"OU=Year 3,OU=Students-Clare,OU=Users,OU=Horizon,DC=HORIZON,DC=local","Year4-Clare":"OU=Year 4,OU=Students-Clare,OU=Users,OU=Horizon,DC=HORIZON,DC=local","Year5-Clare":"OU=Year 5,OU=Students-Clare,OU=Users,OU=Horizon,DC=HORIZON,DC=local","Year6-Clare":"OU=Year 6,OU=Students-Clare,OU=Users,OU=Horizon,DC=HORIZON,DC=local","Year7-Clare":"OU=Year 7,OU=Students-Clare,OU=Users,OU=Horizon,DC=HORIZON,DC=local","Year8-Clare":"OU=Year 8,OU=Students-Clare,OU=Users,OU=Horizon,DC=HORIZON,DC=local","Year9-Clare":"OU=Year 9,OU=Students-Clare,OU=Users,OU=Horizon,DC=HORIZON,DC=local","Year10-Clare":"OU=Year 10,OU=Students-Clare,OU=Users,OU=Horizon,DC=HORIZON,DC=local","Year11-Clare":"OU=Year 11,OU=Students-Clare,OU=Users,OU=Horizon,DC=HORIZON,DC=local","Year12-Clare":"OU=Year 12,OU=Students-Clare,OU=Users,OU=Horizon,DC=HORIZON,DC=local"}','UTF-8')).decode("UTF-8"))
        conf_file['Horizon']['title'] = str(base64.b64encode(bytes('{"Executive":"Executive Team","Managment":"Management Team","Admin":"Administration","Admin Temp":"Temporary Administrator","Primary Teacher":"Primary Teacher","Secondary Teacher":"Secondary Teacher","Temporary Teacher":"Temporary Teacher","ESO":"Student Support","Grounds":"Grounds and Maintenance","Counsellor":"Counsellor","Foundation":"Foundation Student","Year1":"Year 1 Student","Year2":"Year 2 Student","Year3":"Year 3 Student","Year4":"Year 4 Student","Year5":"Year 5 Student","Year6":"Year 6 Student","Year7":"Year 7 Student","Year8":"Year 8 Student","Year9":"Year 9 Student","Year10":"Year 10 Student","Year11":"Year 11 Student","Year12":"Year 12 Student"}','UTF-8')).decode("UTF-8"))
        conf_file['Horizon']['expiredous'] = str(base64.b64encode(bytes('{"Disabled":"OU=Disabled,OU=Users,OU=Horizon,DC=HORIZON,DC=local","ExpiredStaff":"OU=ExpiredStaff,OU=Users,OU=Horizon,DC=HORIZON,DC=local","ExpiredStudents":"OU=ExpiredStudents,OU=Users,OU=Horizon,DC=HORIZON,DC=local"}','UTF-8')).decode("UTF-8"))
        # conf_file['Horizon']['groupsou'] = str(base64.b64encode(bytes('OU=Groups,OU=DCOMPUTERS,DC=DCOMPUTERS,DC=local','UTF-8')).decode("UTF-8"))
        conf_file['Horizon']['groupsou'] = str(base64.b64encode(bytes('OU=Groups,OU=Horizon,DC=HORIZON,DC=local','UTF-8')).decode("UTF-8"))
        conf_file['Horizon']['domains'] = str(base64.b64encode(bytes('{"Primary":["horizon.sa.edu.au"],"Secondary":"horizonsa.onmicrosoft.com"}','UTF-8')).decode("UTF-8"))
        conf_file['Horizon']['homepaths'] = str(base64.b64encode(bytes('\\\\HCS-FS01\\office_stuserver,\\\\HCS-FS01\\teachers_stuserver,\\\\HCS-FS01\\students_stuserver','UTF-8')).decode("UTF-8"))
        conf_file['Horizon']['campus'] = str(base64.b64encode(bytes('balaklava,clare','UTF-8')).decode("UTF-8"))
        
        conf_file.add_section('DComputers')
        conf_file['DComputers']['server'] = str(base64.b64encode(bytes('DCM-DC01.DCOMPUTERS.local','UTF-8')).decode("UTF-8"))
        conf_file['DComputers']['server_user'] = str(base64.b64encode(bytes('administrator','UTF-8')).decode("UTF-8"))
        conf_file['DComputers']['server_pass'] = str(base64.b64encode(bytes('Heffserver2022!','UTF-8')).decode("UTF-8"))
        conf_file['DComputers']['userou'] = str(base64.b64encode(bytes('OU=Users,OU=DCOMPUTERS,DC=DCOMPUTERS,DC=local','UTF-8')).decode("UTF-8"))
        conf_file['DComputers']['domainname'] = str(base64.b64encode(bytes('DCOMPUTERS','UTF-8')).decode("UTF-8"))
        conf_file['DComputers']['groups'] = str(base64.b64encode(bytes('{"Admin":["Office365_ES5", "DC-Admin", "Local-Administrator", "Remote Desktop Users", "SG_FS_Admin", "SG_FS_Course", "SG_FS_Backups", "SG_FS_Images", "Administrators"],"Member HF":["Office365_ES5", "DC-Member", "SG_FS_Backups", "SG_FS_Images"],"Member DCM":["Office365_ES5", "DC-Member", "SG_FS_Backups", "SG_FS_Images"],"Member AH":["Office365_ES5", "DC-Member", "SG_FS_Backups", "SG_Backups", "Backups", "SG_FS_Images", "SG_WF_Staff"]}','UTF-8')).decode("UTF-8"))
        conf_file['DComputers']['positions'] = str(base64.b64encode(bytes('{"Staff":["Member HF","Member DCM","Member AH","Admin"],"Students":[]}','UTF-8')).decode("UTF-8"))
        conf_file['DComputers']['positionsou'] = str(base64.b64encode(bytes('{"Member HF":"OU=Heffs Fabrications,OU=Members,OU=Users,OU=DCOMPUTERS,DC=DCOMPUTERS,DC=local","Member DCM":"OU=Doohan Computers,OU=Members,OU=Users,OU=DCOMPUTERS,DC=DCOMPUTERS,DC=local","Member AH":"OU=Ash_Heffernan,OU=Members,OU=Users,OU=DCOMPUTERS,DC=DCOMPUTERS,DC=local","Admin":"OU=Admins,OU=Users,OU=DCOMPUTERS,DC=DCOMPUTERS,DC=local"}','UTF-8')).decode("UTF-8"))
        conf_file['DComputers']['title'] = str(base64.b64encode(bytes('{"Member HF":"Welder","Member DCM":"Support Technicion","Member AH":"Consultant","Admin":"Systems Engineer"}','UTF-8')).decode("UTF-8"))
        conf_file['DComputers']['expiredous'] = str(base64.b64encode(bytes('{"Expired_Users":"OU=Expired_Users,OU=DCOMPUTERS,DC=DCOMPUTERS,DC=local"}','UTF-8')).decode("UTF-8"))
        conf_file['DComputers']['groupsou'] = str(base64.b64encode(bytes('OU=Groups,OU=DCOMPUTERS,DC=DCOMPUTERS,DC=local','UTF-8')).decode("UTF-8"))
        conf_file['DComputers']['domains'] = str(base64.b64encode(bytes('{"Primary":["doohancomputers.com.au","heffsfabrications.com.au","ashheffernan.org"],"Secondary":"heffserver.onmicrosoft.com"}','UTF-8')).decode("UTF-8"))
        conf_file['DComputers']['homepaths'] = str(base64.b64encode(bytes('\\\\DCM-DC01\\Profiles','UTF-8')).decode("UTF-8"))
        conf_file['DComputers']['campus'] = str(base64.b64encode(bytes('balaklava','UTF-8')).decode("UTF-8"))
        conf_file.add_section('Settings')
        conf_file['Settings']['company'] = str(base64.b64encode(bytes('Horizon,DComputers','UTF-8')).decode("UTF-8"))
        
        with open(settings_dir+settings_file, 'wb') as file_handle:
            conf_file.write_encrypted(file_handle)
    

if __name__ == "__main__":
    MakeConf()