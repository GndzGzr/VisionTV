import tkinter as tk

class GuidePage(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller

        label = tk.Label(self, text="Guide Page")
        label.pack(side="top", fill="x", pady=10)

        button = tk.Button(self, text="Go to Main Page",
                           command=lambda: controller.show_frame("Home"))
        button.pack()
