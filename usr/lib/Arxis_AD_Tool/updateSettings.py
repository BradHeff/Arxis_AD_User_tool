# import sys
import base64
from pathlib import Path
import os
import json
from configparser_crypt import ConfigParserCrypt

exe_dir = str(Path(__file__).parents[2])

settings_file = "Settings.dat"
settings_dir = "".join([exe_dir, "/share/Arxis_AD_Tool/"])


class MakeConf:
    def __init__(self):
        super(MakeConf, self).__init__()
        self.old = ""
        self.key = ""
        self.lines = []
        self.diabled = {}
        self.groups = {}
        self.positions = {}
        self.pOU = {}
        self.titles = {}

        self.getJSON()

        # print((str(self.diabled).strip()))
        self.readLines()
        self.writeConfig()
        self.writeLines()

        print(self.key)

    def _getPosition(self, file, text):
        nlist = [x for x in file if text in x]
        # print(exe_dir + "\\Functions.py")
        position = file.index(nlist[0])
        return position

    def getJSON(self):
        with open(settings_dir + "disabled.json", "r") as f:
            self.diabled = json.load(f)
        with open(settings_dir + "groups.json", "r") as f:
            self.groups = json.load(f)
        with open(settings_dir + "positions.json", "r") as f:
            self.positions = json.load(f)
        with open(settings_dir + "pOU.json", "r") as f:
            self.pOU = json.load(f)
        with open(settings_dir + "titles.json", "r") as f:
            self.titles = json.load(f)

    def readLines(self):
        with open(exe_dir + "/lib/Arxis_AD_Tool/Functions.py", "r") as f:
            self.lines = f.readlines()
            pos = self._getPosition(self.lines, "key = ")
            line = self.lines[pos]
            self.old = line.split(" = ")[1].strip()
            f.close()

    def writeLines(self):
        with open(exe_dir + "/lib/Arxis_AD_Tool/Functions.py", "w") as w:
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
                    str(self.groups).strip(),
                    "UTF-8",
                )
            ).decode("UTF-8")
        )
        conf_file["Horizon"]["positions"] = str(
            base64.b64encode(
                bytes(
                    str(self.positions).strip(),
                    "UTF-8",
                )
            ).decode("UTF-8")
        )
        conf_file["Horizon"]["positionsou"] = str(
            base64.b64encode(
                bytes(
                    str(self.pOU).strip(),
                    "UTF-8",
                )
            ).decode("UTF-8")
        )
        conf_file["Horizon"]["title"] = str(
            base64.b64encode(
                bytes(
                    str(self.titles).strip(),
                    "UTF-8",
                )
            ).decode("UTF-8")
        )
        conf_file["Horizon"]["expiredous"] = str(
            base64.b64encode(
                bytes(
                    str(self.diabled).strip(),
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
