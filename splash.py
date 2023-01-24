import tkinter as tk
from tkinter import ttk
from icon import splashbg
import time
import threading

class Splash(tk.Tk):
    """docstring for Splash."""
    def __init__(self):
        super(Splash, self).__init__()
        global photo
        self.W,self.H = 500,250
        screen_width = self.winfo_screenwidth()
        screen_height = self.winfo_screenheight()
        center_x = int(screen_width/2 - self.W / 2)
        center_y = int(screen_height/2 - self.H / 2)
        self.geometry(f'{self.W}x{self.H}+{center_x}+{center_y}')
        self.attributes("-fullscreen", False)
        self.attributes("-toolwindow", True)
        self.attributes("-topmost", True)
        self.overrideredirect(True)

        photo = tk.PhotoImage(data=splashbg)
        tk.Label(self, image=photo).place(x=0,y=0)
        
        self.count = 1
        
        self.prog = ttk.Progressbar(self, length=498, maximum=100)
        self.prog.place(x=2,y=240)
        
        t = threading.Thread(target=self.runProg)
        t.daemon = True
        t.start()

        
    def runProg(self):
        while self.count < 99:
            self.count+=10
            self.prog['value'] = self.count            
            time.sleep(0.7)

        
if __name__ == '__main__':
    root = Splash()
    root.mainloop()