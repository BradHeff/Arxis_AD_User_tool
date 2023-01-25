from pathlib import Path

paths = str(Path(__file__).parents[0])


class PreBuild():
    def __init__(self):
        super(PreBuild, self).__init__()
        self.old = ''
        self.old2 = ''
        self.lines = []
        self.lines2 = []
        self.new = "False"
        self.new2 = "Horizon"

        self.readLines()
        self.writeLines()


    def _getPosition(self, file, text):
        nlist = [x for x in file if text in x]
        # print(paths + "\\Functions.py")
        position = file.index(nlist[0])
        return position

    def readLines(self):
        with open(paths + "\\Functions.py", "r") as f:
            self.lines = f.readlines()
            pos = self._getPosition(self.lines, "DEBUG =")
            line = self.lines[pos]
            self.old = line.split("=")[1].strip()
            f.close()
        with open(paths + "\\main.pyw", "r") as e:
            self.lines2 = e.readlines()
            pos = self._getPosition(self.lines2, "DComputers")
            line = self.lines2[pos]
            self.old2 = "DComputers"
            e.close()

    def writeLines(self):
        with open(paths + "\\Functions.py", "w") as w:
            pos = self._getPosition(self.lines, "DEBUG =")

            self.lines[pos] = self.lines[pos].replace(self.old, self.new)

            w.writelines(self.lines)
            w.close()
        with open(paths + "\\main.pyw", "w") as e:
            pos = self._getPosition(self.lines2, "DComputers")

            self.lines2[pos] = self.lines2[pos].replace(self.old2, self.new2)

            e.writelines(self.lines2)
            e.close()

if __name__ == "__main__":
    PreBuild()