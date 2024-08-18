import tkinter as tk
import home
import tkinter as tk
from pages.start import StartPage
from pages.guide import GuidePage
from pages.settings import SettingsPage
from intrusiondetection.JSONReader.settings import Settings

class App(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Vision TV")


        container = tk.Frame(self)
        container.pack(side="top", fill="both", expand=True)
        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)

        self.frames = {}
        for F in (home.Home, StartPage, GuidePage, SettingsPage):
            page_name = F.__name__
            frame = F(parent=container, controller=self)
            self.frames[page_name] = frame
            frame.grid(row=0, column=0, sticky="nsew")

        self.show_frame("Home")

    def show_frame(self, page_name):
        frame = self.frames[page_name]
        frame.configure(bg="white")
        frame.tkraise()


if __name__ == "__main__":

    app = App()

    app.attributes('-fullscreen', True)
    app.configure(bg="white")
    app.mainloop()
