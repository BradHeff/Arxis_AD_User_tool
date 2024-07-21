from tkinter import Label
from PIL import Image, ImageTk
from itertools import count


class GifLabel(Label):
    """a label that displays images, and plays them if they are gifs"""

    def load(self, im):
        print("Loading %s..." % im)
        if isinstance(im, str):
            im = Image.open(im)
        self.loc = 0
        self.frames = []

        try:
            for i in count(1):
                self.frames.append(ImageTk.PhotoImage(im.copy()))
                im.seek(i)
        except EOFError as e:
            print("Warning: %s, continuing..." % e)
            pass

        try:
            self.delay = im.info["duration"]
        except KeyError as key:
            print("No duration info in %s, assuming 100ms delay" % key)
            self.delay = 100

        if len(self.frames) == 1:
            self.config(image=self.frames[0])
        else:
            self.next_frame()

    def unload(self):
        self.config(image="")
        self.frames = None

    def next_frame(self):
        self.update()
        if self.frames:
            self.loc += 1
            self.loc %= len(self.frames)
            self.config(image=self.frames[self.loc])
            self.after(self.delay, self.next_frame)
