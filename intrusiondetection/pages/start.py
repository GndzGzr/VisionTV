import tkinter as tk
import tkinter.font as font
from intrusiondetection.JSONReader.methods.ObjectDetection import ObjectDetection
from intrusiondetection.JSONReader.methods.MotionDetection import MotionDetection
from intrusiondetection.JSONReader.methods.OpticalFlow import OpticalFlow
from intrusiondetection.JSONReader.settings import settings
class StartPage(tk.Frame):

    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller



        headerFont = font.Font(family="Helvetica", size=24, weight="bold")
        self.welcomeMessage = tk.Label(
            self,
            text=f'{settings.System.input_option}',
            font=headerFont,
            bg="white",
            fg="black",
        )
        self.welcomeMessage.pack(side="top", fill="x", pady=10)

        left_side = tk.Frame(
            self,
            width=800,
            height=600,
            bg="red"
        )
        left_side.pack()

        btnFont = font.Font(family="Helvetica", size=16, weight="normal")
        modelBtn = tk.Button(
            self,
            text="Run",
            bg="#333333",
            fg="white",
            activebackground="white",
            activeforeground="#333333",
            font=btnFont,
            cursor="hand2",
            command=lambda: self.runModel()
        )
        modelBtn.pack()

        prevBtn = tk.Button(
            self,
            text="BACK",
            bg="#333333",
            fg="white",
            activebackground="white",
            activeforeground="#333333",
            font=btnFont,
            cursor="hand2",
            command=lambda: controller.show_frame("Home")
        )
        prevBtn.pack()


    def updateWelcome(self,option):
        headerFont = font.Font(family="Helvetica", size=24, weight="bold")
        self.welcomeMessage = tk.Label(
            self,
            text=f'{option}',
            font=headerFont,
            bg="white",
            fg="black",
        )

    def runModel(self):
        print("entered run")
        method = settings.System.method
        if method == "Motion Detection":
            print(settings.Camera.capture)
            motionDetection = MotionDetection(settings)
            motionDetection.run()
        elif method == "Object Detection":
            print(settings.Camera.capture)
            objectDetection = ObjectDetection(settings)
            objectDetection()
        elif method == "Optical Flow":
            opticalFlow = OpticalFlow(settings)
            opticalFlow.run()
        elif method == "Mask R-CNN":
            pass
            #maskRCNN = MaskRCNN(settings)
            #maskRCNN.run()
