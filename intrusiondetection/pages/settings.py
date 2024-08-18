import tkinter as tk
from tkinter import *
from tkinter.ttk import Combobox
import tkinter.font as font
from tkinter.filedialog import askopenfilename
import cv2
from intrusiondetection.JSONReader.settings import settings
from intrusiondetection.JSONReader.jsonReader import JSONReader
from intrusiondetection.JSONReader.settings import Settings
import os


class SettingsPage(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller

        self.selectedCapture = ""
        self.selectedCaptureOPT = ""
        self.labelFont = font.Font(family="Inter", size=12, weight="normal")
        self.smallLabelFont = font.Font(family="Inter", size=8, weight="bold")
        self.system_frame = Frame(
            self,
            highlightthickness=1,
            highlightbackground="black",
            bg="white"
        )
        system_label = Label(
            self,
            text="System",
            font=self.labelFont,
            bg="white",
            fg="black",
            anchor="w",
        )
        self.od_frame = Frame(
            self,
            highlightthickness=1,
            highlightbackground="black",
            bg="white"
        )
        self.od_label = Label(
            self,
            text="Object Detection",
            font=self.labelFont,
            bg="white",
            fg="black",
            anchor="w",
        )
        self.of_frame = Frame(
            self,
            highlightthickness=1,
            highlightbackground="black",
            bg="white"
        )
        self.of_label = Label(
            self,
            text="Optical Flow",
            font=self.labelFont,
            bg="white",
            fg="black",
            anchor="w",
        )
        self.md_frame = Frame(
            self,
            highlightthickness=1,
            highlightbackground="black",
            bg="white"
        )
        md_label = Label(
            self,
            text="Motion Detection",
            font=self.labelFont,
            bg="white",
            fg="black",
            anchor="w",
        )
        rcnn_frame = Frame(
            self,
            highlightthickness=1,
            highlightbackground="black",
            bg="white"
        )
        rcnn_label = Label(
            self,
            text="Mask R-CNN",
            font=self.labelFont,
            bg="white",
            fg="black",
            anchor="w",
        )
        self.zone_frame = Frame(
            self,
            highlightthickness=1,
            highlightbackground="black",
            bg="white",

        )
        zone_label = Label(
            self,
            text="Zone",
            font=self.labelFont,
            bg="white",
            fg="black",
            anchor="w",
        )

        self.initZoneLabels(self.zone_frame)

        btn_frame = Frame(
            self,
            highlightthickness=1,
            highlightbackground="black",
            bg="white"
        )

        headerFont = font.Font(family="Helvetica", size=24, weight="bold")
        welcomeMessage = tk.Label(
            self,
            text="Settings",
            font=headerFont,
            bg="white",
            fg="black",
        )

        camera_options = [
            "Live", "Video", "Image"
        ]

        self.cameraOptLabel = Label(
            self.system_frame,
            text="Input Option:",
            font=self.smallLabelFont,
            bg="white",
            fg="black",
            anchor="w",

        )
        self.cameraOptions = Combobox(
            self.system_frame,
            state="readonly",
            values=camera_options,
            font=self.smallLabelFont,
            justify="right",
        )
        cameras = self.get_available_cameras()

        def onSelect(event):
            selected = event.widget.get()
            self.selectedCaptureOPT = selected
            self.getInputOptionSelected(selected, cameras)

        # Bind the "<<ComboboxSelected>>" event to the on_combobox_select function
        self.cameraOptions.bind("<<ComboboxSelected>>", onSelect)

        detection_method = [
            "Object Detection", "Optical Flow", "Motion Detection", "Mask R-CNN"
        ]

        detection_methodLabel = Label(
            self.system_frame,
            text="Detection Method:",
            font=self.smallLabelFont,
            bg="white",
            fg="black",
            anchor="w",

        )
        self.detection_methodOpt = Combobox(
            self.system_frame,
            state="readonly",
            values=detection_method,
            font=self.smallLabelFont,
            justify="right",
        )

        self.model_name_label = Label(
            self.od_frame,
            text="Model:",
            font=self.smallLabelFont,
            bg="white",
            fg="black",
            anchor="w",

        )

        directory = "../intrusiondetection/models"
        files = []

        if not os.path.exists(directory):
            print(f"Directory {directory} does not exist.")
        else:
            files = []
            for f in os.listdir(directory):
                full_path = os.path.join(directory, f)
                if os.path.isfile(full_path):
                    files.append(f)
                else:
                    print(f"{f} is not a file.")

            if files:
                print("Files found:", files)
            else:
                print("No files found.")
        self.model_name_opt = Combobox(
            self.od_frame,
            state="readonly",
            values=files,
            font=self.smallLabelFont,
            justify="right",
        )

        self.min_thresh_lb = Label(
            self.of_frame,
            text="Min Tresh (0, 1):",
            font=self.smallLabelFont,
            bg="white",
            fg="black",
            anchor="w",

        )
        self.min_thresh_t = Text(self.of_frame, height=1, width=4, highlightthickness=1,
                                 highlightbackground="black")

        self.max_thresh_lb = Label(
            self.of_frame,
            text="Max Tresh (0, 1):",
            font=self.smallLabelFont,
            bg="white",
            fg="black",
            anchor="w",

        )
        self.max_thresh_t = Text(self.of_frame, height=1, width=4, highlightthickness=1,
                                 highlightbackground="black")

        self.kernel_size_lb = Label(
            self.of_frame,
            text="Kernel Size (odd):",
            font=self.smallLabelFont,
            bg="white",
            fg="black",
            anchor="w",

        )
        self.kernel_size_t = Text(self.of_frame, height=1, width=4, highlightthickness=1,
                                  highlightbackground="black")

        self.bbox_thresh_lb = Label(
            self.of_frame,
            text="Bounding Box Thresh:",
            font=self.smallLabelFont,
            bg="white",
            fg="black",
            anchor="w",

        )
        self.bbox_thresh_t = Text(self.of_frame, height=1, width=4, highlightthickness=1,
                                  highlightbackground="black")

        self.sigma_lb = Label(
            self.of_frame,
            text="Sigma: ",
            font=self.smallLabelFont,
            bg="white",
            fg="black",
            anchor="w",

        )
        self.sigma_t = Text(self.of_frame, height=1, width=4, highlightthickness=1,
                            highlightbackground="black")

        self.nms_thresh_lb = Label(
            self.of_frame,
            text="Non-Maximal Supression (0, 1): ",
            font=self.smallLabelFont,
            bg="white",
            fg="black",
            anchor="w",

        )
        self.nms_thresh_t = Text(self.of_frame, height=1, width=4, highlightthickness=1,
                                 highlightbackground="black")

        self.nms_thresh_lb = Label(
            self.of_frame,
            text="Non-Maximal Supression (0, 1): ",
            font=self.smallLabelFont,
            bg="white",
            fg="black",
            anchor="w",

        )
        self.nms_thresh_t = Text(self.of_frame, height=1, width=4, highlightthickness=1,
                                 highlightbackground="black")

        self.cnt_filter_lb = Label(
            self.md_frame,
            text="Contour Filter: ",
            font=self.smallLabelFont,
            bg="white",
            fg="black",
            anchor="w",

        )
        self.cnt_filter_t = Text(self.md_frame, height=1, width=4, highlightthickness=1,
                                 highlightbackground="black")

        self.gaussian_kernel_lb = Label(
            self.md_frame,
            text="Gaussian Kernel: ",
            font=self.smallLabelFont,
            bg="white",
            fg="black",
            anchor="w",

        )
        self.gaussian_kernel_t = Text(self.md_frame, height=1, width=4, highlightthickness=1,
                                      highlightbackground="black")

        self.closing_kernel_lb = Label(
            self.md_frame,
            text="Closing Kernel: ",
            font=self.smallLabelFont,
            bg="white",
            fg="black",
            anchor="w",

        )
        self.closing_kernel_t = Text(self.md_frame, height=1, width=4, highlightthickness=1,
                                     highlightbackground="black")

        button = tk.Button(btn_frame, text="Go to Main Page",
                           command=lambda: controller.show_frame("Home"))

        welcomeMessage.place(x=228, y=38, width=345, height=39)

        """ System """
        self.system_frame.place(x=10, y=125, width=275, height=580)
        system_label.place(x=10, y=100, width=275, height=20)

        self.cameraOptLabel.place(x=5, y=5, width=100, height=20)
        self.cameraOptions.place(x=160, y=5, width=100, height=20)

        detection_methodLabel.place(x=5, y=65, width=120, height=20)
        self.detection_methodOpt.place(x=160, y=65, width=100, height=20)

        tk.Button(self.system_frame, text="Save",
                  command=lambda: self.saveSystemSettings()).place(x=10, y=540, width=255, height=30)

        """ Object Detection """

        self.od_frame.place(x=300, y=125, width=275, height=580)
        self.od_label.place(x=300, y=100, width=275, height=20)

        self.model_name_label.place(x=5, y=5, width=100, height=20)
        self.model_name_opt.place(x=160, y=5, width=100, height=20)

        tk.Button(self.od_frame, text="Save",
                  command=lambda: self.saveObjectDetectionSettings()).place(x=10, y=540, width=255, height=30)

        """ Optical Flow """

        self.of_frame.place(x=590, y=125, width=275, height=580)
        self.of_label.place(x=590, y=100, width=275, height=20)

        self.min_thresh_lb.place(x=5, y=5, width=120, height=20)
        self.min_thresh_t.place(x=160, y=5, width=100, height=20)

        self.max_thresh_lb.place(x=5, y=35, width=120, height=20)
        self.max_thresh_t.place(x=160, y=35, width=100, height=20)

        self.kernel_size_lb.place(x=5, y=65, width=120, height=20)
        self.kernel_size_t.place(x=160, y=65, width=100, height=20)

        self.bbox_thresh_lb.place(x=5, y=95, width=120, height=20)
        self.bbox_thresh_t.place(x=160, y=95, width=100, height=20)

        self.nms_thresh_lb.place(x=5, y=125, width=120, height=20)
        self.nms_thresh_t.place(x=160, y=125, width=100, height=20)

        self.sigma_lb.place(x=5, y=155, width=120, height=20)
        self.sigma_t.place(x=160, y=155, width=100, height=20)

        tk.Button(self.of_frame, text="Save",
                  command=lambda: self.saveOpticalFlowSettings()).place(x=10, y=540, width=255, height=30)

        """ Motion Detection """

        self.md_frame.place(x=880, y=125, width=275, height=580)
        md_label.place(x=880, y=100, width=275, height=20)

        self.cnt_filter_lb.place(x=5, y=5, width=120, height=20)
        self.cnt_filter_t.place(x=160, y=5, width=100, height=20)

        self.gaussian_kernel_lb.place(x=5, y=35, width=120, height=20)
        self.gaussian_kernel_t.place(x=160, y=35, width=100, height=20)

        self.closing_kernel_lb.place(x=5, y=65, width=120, height=20)
        self.closing_kernel_t.place(x=160, y=65, width=100, height=20)

        tk.Button(self.md_frame, text="Save",
                  command=lambda: self.saveMotionDetectionSettings()).place(x=10, y=540, width=255, height=30)

        """ Mask R-CNN """

        rcnn_frame.place(x=1170, y=125, width=275, height=580)
        rcnn_label.place(x=1170, y=100, width=275, height=20)

        """ Zone """

        self.zone_frame.place(x=10, y=730, width=1150, height=130)
        zone_label.place(x=10, y=710, width=275, height=20)

        """ BTN """

        btn_frame.place(x=1170, y=730, width=275, height=130)

        button.pack(side="bottom", padx=10, pady=10)

    def saveSystemSettings(self):
        settings.updateSystem(self.selectedCapture, self.detection_methodOpt.get(), self.selectedCaptureOPT)


    def saveOpticalFlowSettings(self):
        var = [float(self.min_thresh_t.get(1.0, "end-1c")),
               float(self.max_thresh_t.get(1.0, "end-1c")),
               int(self.kernel_size_t.get(1.0, "end-1c")),
               int(self.bbox_thresh_t.get(1.0, "end-1c")),
               float(self.nms_thresh_t.get(1.0, "end-1c")),
               int(self.sigma_t.get(1.0, "end-1c"))]
        settings.updateOpticalFlow(var)

    def saveMotionDetectionSettings(self):
        varList = [
            int(self.cnt_filter_t.get(1.0, "end-1c")),
            int(self.gaussian_kernel_t.get(1.0, "end-1c")),
            int(self.closing_kernel_t.get(1.0, "end-1c"))

        ]
        settings.updateMotionDetection(varList)

    def saveObjectDetectionSettings(self):
        settings.updateObjectDetection(self.model_name_opt.get())

    def getInputOptionSelected(self, selected, cameras):
        def onSelectCameraIndex(event):
            selected = event.widget.get()
            self.selectedCapture = int(selected)

        if selected == "Live":
            inputDeviceLabel = Label(
                self.system_frame,
                text="Input Device:",
                font=self.smallLabelFont,
                bg="white",
                fg="black",
                anchor="w",
            )
            inputDevice = Combobox(
                self.system_frame,
                state="readonly",
                values=cameras,
                font=self.smallLabelFont,
                justify="right",
            )
            inputDevice.bind("<<ComboboxSelected>>", onSelectCameraIndex)
            ### Live Options
            inputDeviceLabel.place(x=5, y=35, width=120, height=20)
            inputDevice.place(x=160, y=35, width=100, height=20)
        elif selected == "Video":
            videoPath = Label(
                self.system_frame,
                text="Video Path:",
                font=self.smallLabelFont,
                bg="white",
                fg="black",
                anchor="w",
            )
            ### Video Options
            videoPath.place(x=5, y=35, width=120, height=20)
            tk.Button(self.system_frame, text="Select", command=lambda: self.selectFile()).place(
                x=160, y=35, width=100, height=20)
        elif selected == "Image":
            imagePath = Label(
                self.system_frame,
                text="Input Path:",
                font=self.smallLabelFont,
                bg="white",
                fg="black",
                anchor="w",

            )
            ### Image Options
            imagePath.place(x=5, y=35, width=120, height=20)
            tk.Button(self.system_frame, text="Select", command=lambda: self.selectFile()).place(
                x=160, y=35, width=100, height=20)

    def selectFile(self):
        Tk().withdraw()  # we don't want a full GUI, so keep the root window from appearing
        filename = askopenfilename()  # show an "Open" dialog box and return the path to the selected file
        self.selectedCapture = filename
        tk.Button(self.system_frame, text=f'{filename.split("/")[-1]}', command=lambda: self.selectFile()).place(
            x=160, y=35, width=100, height=20)
        return filename

    def initZoneLabels(self, frame):
        index_edges = 0
        for e in settings.Zone.edges:
            print(settings.Zone.edges)
            edgeLabel = Label(
                frame,
                text=f'{index_edges}: x={e["x"]} y={e["y"]}',
                font=self.smallLabelFont,
                bg="white",
                fg="black",
                anchor="w",
            )
            if index_edges <= 4:
                edgeLabel.place(x=5, y=5 + 25 * index_edges, width=125, height=20)
            else:
                edgeLabel.place(x=125, y=5 + 25 * (index_edges - 5), width=125, height=20)
            index_edges += 1
        if index_edges < 9:
            for i in range(index_edges, 9):
                edgeLabel = Label(
                    frame,
                    text=f'',
                    font=self.smallLabelFont,
                    bg="white",
                    fg="black",
                    anchor="w",
                )
                if i <= 4:
                    edgeLabel.place(x=5, y=5 + 25 * i, width=125, height=20)
                else:
                    edgeLabel.place(x=125, y=5 + 25 * (i - 5), width=125, height=20)
        tk.Button(frame, text="Edit Points", command=lambda: self.editZonePoints()).place(
            x=1060, y=5, width=75, height=30)
        tk.Button(frame, text="Select Zone", command=lambda: self.selectSource()).place(
            x=1060, y=50, width=75, height=30)

    def selectSource(self):
        # Toplevel object which will
        # be treated as a new window
        newWindow = Toplevel(self)
        # sets the title of the
        # Toplevel widget
        newWindow.title("Select Zone")
        # sets the geometry of toplevel
        newWindow.geometry("400x400")
        newWindow.configure(bg="white")

        tk.Button(newWindow, text="Select Image", command=lambda: self.selectSourceMedia(newWindow, "image")).place(
            x=5, y=5, width=150, height=30)
        tk.Button(newWindow, text="Select Video", command=lambda: self.selectSourceMedia(newWindow, "video")).place(
            x=5, y=40, width=150, height=30)
        tk.Button(newWindow, text="Select Live", command=lambda: self.selectSourceMedia(newWindow, "live")).place(
            x=5, y=75, width=150, height=30)

    def addSelectedEdge(self, frame, point_list):
        index = 0
        for i in point_list:
            edgeLabel = Label(
                frame,
                text=f'{index}: x={i[0]} y={i[1]}',
                font=self.smallLabelFont,
                bg="white",
                fg="black",
                anchor="w",
            )
            edgeLabel.place(x=5, y=125 + 25 * index, width=125, height=20)
            index += 1
        tk.Button(frame, text="Save", command=lambda: self.saveSelectedZonePoints(point_list, frame)).place(
            x=5, y=160 + 25 * index, width=60, height=30)

    def saveSelectedZonePoints(self, points, frame):
        self.clearZonePoints(None)
        new_points_array = []
        for point in points:
            x = int(point[0])
            y = int(point[1])
            new_points_array.append({"x": x, "y": y})
        settings.updateZonePoints(new_points_array)
        self.initZoneLabels(self.zone_frame)
        frame.destroy()

    def selectSourceMedia(self, prevWindow, type):
        selectedPoints = []

        def select_point(event, x, y, flags, param):
            if event == cv2.EVENT_LBUTTONDBLCLK:  # captures left button double-click
                # selectedPoints.append([x, y])

                selectedPoints.append([x, y])
                cv2.putText(img, f'({x},{y})', (x, y),
                            cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)

                # draw point on the image
                cv2.circle(img, (x, y), 3, (0, 255, 255), -1)

        img = None
        if type == 'video':
            Tk().withdraw()  # we don't want a full GUI, so keep the root window from appearing
            filename = askopenfilename()  # show an "Open" dialog box and return the path to the selected file
            print(filename)
            vid = cv2.VideoCapture(filename)
            success, image = vid.read()
            img = image
        elif type == 'image':
            Tk().withdraw()  # we don't want a full GUI, so keep the root window from appearing
            filename = askopenfilename()  # show an "Open" dialog box and return the path to the selected file
            print(filename)
            img = cv2.imread(filename)
        elif type == 'live':
            cap = cv2.VideoCapture(0)
            # Check if the webcam is opened correctly
            if not cap.isOpened():
                print("Error: Could not open webcam")
                exit()
            # Read the first frame from the webcam
            ret, frame = cap.read()
            # Check if the frame was captured successfully
            if ret:
                img = frame
            else:
                print("Error: Could not read frame")

            # Release the webcam
            cap.release()

        else:
            pass

        cv2.namedWindow('image')
        # bind select_point function to a window that will capture the mouse click
        cv2.setMouseCallback('image', select_point)
        while True:
            cv2.imshow('image', img)
            k = cv2.waitKey(1) & 0xFF
            if k == 27:
                break
        cv2.destroyAllWindows()
        self.addSelectedEdge(prevWindow, selectedPoints)

    def editZonePoints(self):
        # Toplevel object which will
        # be treated as a new window
        newWindow = Toplevel(self)
        # sets the title of the
        # Toplevel widget
        newWindow.title("Edit Zone")
        # sets the geometry of toplevel
        newWindow.geometry("400x400")
        newWindow.configure(bg="white")
        index_edges = 0
        inputs_zone = []
        for e in settings.Zone.edges:
            Label(
                newWindow,
                text=f'{index_edges}: x={str(e["x"])}',
                font=self.smallLabelFont,
                bg="white",
                fg="black",
                anchor="w",
            ).place(x=5, y=(5 + 30 * index_edges), width=40, height=20)

            x_point = Text(newWindow, height=1, width=4, highlightthickness=1,
                           highlightbackground="black")
            x_point.insert(INSERT, str(e["x"]))
            x_point.place(x=50, y=(5 + 30 * index_edges))

            Label(
                newWindow,
                text=f'y={str(e["y"])}',
                font=self.smallLabelFont,
                bg="white",
                fg="black",
                anchor="w",
            ).place(x=95, y=(5 + 30 * index_edges), width=40, height=20)

            y_point = tk.Text(newWindow, height=1, width=4, highlightthickness=1,
                              highlightbackground="black")
            y_point.insert(INSERT, str(e["y"]))
            y_point.place(
                x=140, y=(5 + 30 * index_edges))

            inputs_zone.append([x_point, y_point])
            index_edges += 1
        tk.Button(newWindow, text="Add", command=lambda: self.addZonePoint(newWindow)).place(
            x=200, y=5, width=60, height=30)
        tk.Button(newWindow, text="Save", command=lambda: self.saveZonePoints(inputs_zone, newWindow)).place(
            x=200, y=40, width=60, height=30)
        deleted_point = tk.Text(newWindow, height=1, width=4, highlightthickness=1,
                                highlightbackground="black")
        deleted_point.place(x=280, y=75)
        tk.Button(newWindow, text="Delete", command=lambda: self.deleteZonePoint(deleted_point, newWindow)).place(
            x=200, y=75, width=60, height=30)
        tk.Button(newWindow, text="Clear", command=lambda: self.clearZonePoints(newWindow)).place(
            x=200, y=110, width=60, height=30)

    def deleteZonePoint(self, index, prevWindow):
        x = int(index.get(1.0, "end-1c"))
        settings.deleteZonePoint(x)
        prevWindow.destroy()
        self.editZonePoints()
        self.initZoneLabels(self.zone_frame)

    def clearZonePoints(self, prevWindow):
        settings.deleteAllZonePoint()
        if prevWindow is not None:
            prevWindow.destroy()
            self.editZonePoints()
            self.initZoneLabels(self.zone_frame)

    def addZonePoint(self, prevWindow):
        # Toplevel object which will
        # be treated as a new window
        newWindow = Toplevel(self)
        # sets the title of the
        # Toplevel widget
        newWindow.title("Edit Zone")
        # sets the geometry of toplevel
        newWindow.geometry("300x100")
        newWindow.configure(bg="white")
        Label(
            newWindow,
            text=f'New Point: x=',
            font=self.smallLabelFont,
            bg="white",
            fg="black",
            anchor="w",
        ).place(x=5, y=5, width=80, height=20)

        x_point = Text(newWindow, height=1, width=4, highlightthickness=1,
                       highlightbackground="black")
        x_point.place(x=90, y=5)

        Label(
            newWindow,
            text=f'y=',
            font=self.smallLabelFont,
            bg="white",
            fg="black",
            anchor="w",
        ).place(x=130, y=5, width=40, height=20)

        y_point = Text(newWindow, height=1, width=4, highlightthickness=1,
                       highlightbackground="black")
        y_point.place(
            x=140, y=5)
        newPoint = [x_point, y_point]

        tk.Button(newWindow, text="Add", command=lambda: self.addPoint(newPoint, newWindow, prevWindow)).place(
            x=200, y=30, width=60, height=20)

    def addPoint(self, newPoint, newWindow, prevWindow):
        x = int(newPoint[0].get(1.0, "end-1c"))
        y = int(newPoint[1].get(1.0, "end-1c"))
        point = {"x": x, "y": y}
        settings.appendZonePoint(point)
        newWindow.destroy()
        prevWindow.destroy()
        self.initZoneLabels(self.zone_frame)
        self.editZonePoints()

    def saveZonePoints(self, newZonePoints, newWindow):
        new_points_array = []
        for inputtxt in newZonePoints:
            x = int(inputtxt[0].get(1.0, "end-1c"))
            y = int(inputtxt[1].get(1.0, "end-1c"))
            new_points_array.append({"x": x, "y": y})
        settings.updateZonePoints(new_points_array)
        self.initZoneLabels(self.zone_frame)
        newWindow.destroy()

    def get_available_cameras(self):
        available_cameras = []
        # Check for 5 cameras
        for i in range(5):
            cap = cv2.VideoCapture(i)
            if cap.isOpened():
                available_cameras.append(i)
                cap.release()
        return available_cameras
