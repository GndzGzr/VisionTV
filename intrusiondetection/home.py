import tkinter as tk
from pages.start import StartPage
from pages.guide import GuidePage
from pages.settings import SettingsPage
import tkinter.font as font
from intrusiondetection.JSONReader.settings import Settings
class Home(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller


        btnFont = font.Font(family="Helvetica", size=24, weight="normal")
        headerFont = font.Font(family="Helvetica", size=32, weight="bold")
        welcomeMessage = tk.Label(
            self,
            text="Welcome to Vision TV",
            font=headerFont,
            bg="white",
            fg="black",
        )
        startButton = tk.Button(
            self,
            text="START",
            bg="#333333",
            fg="white",
            activebackground="white",
            activeforeground="#333333",
            font=btnFont,
            cursor="hand2",
            command=lambda: controller.show_frame("StartPage")
        )
        guideButton = tk.Button(
            self,
            text="GUIDE",
            bg="#333333",
            fg="white",
            activebackground="white",
            activeforeground="#333333",
            font=btnFont,
            cursor="hand2",
            command=lambda: controller.show_frame("GuidePage")
        )
        settingsButton = tk.Button(
            self,
            text="SETTINGS",
            bg="#333333",
            fg="white",
            activebackground="white",
            activeforeground="#333333",
            font=btnFont,
            cursor="hand2",
            command=lambda: controller.show_frame("SettingsPage")
        )
        welcomeMessage.place(x=455, y=44, width=689, height=77)
        startButton.place(x=128, y=320, width=400, height=400)
        guideButton.place(x=600, y=320, width=400, height=400)
        settingsButton.place(x=1072, y=320, width=400, height=400)
