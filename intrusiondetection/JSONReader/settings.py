import json

import cv2

from intrusiondetection.JSONReader.globals.Camera import Camera
from intrusiondetection.JSONReader.globals.Zone import Zone
from intrusiondetection.JSONReader.globals.System import System
from intrusiondetection.JSONReader.methods.Method import Method

from intrusiondetection.JSONReader.jsonReader import JSONReader


class Settings:
    def __init__(self):
        self.jsonReader = JSONReader()
        self.data = None
        self.AppSettings = None
        self.System = None
        self.Camera = None
        self.Zone = None
        self.model_name = None
        self.setup()

    def setup(self):

        with open(self.jsonReader.path + self.jsonReader.filename, 'r') as f:
            self.data = json.load(f)

        self.AppSettings = self.data["appsettings"]
        self.Camera = Camera(self.data["camera"])
        self.Zone = Zone(self.data["zone"])
        self.System = System(self.data["system"])
        self.model_name = self.data["objectdetection"]["model"]

    def updateZonePoints(self, newPoints):
        self.Zone.edges = Zone.setZoneEdges(self.Zone, edges=newPoints)
        self.Zone.edgesList = Zone.setEdgeList(self.Zone, edges=newPoints)
        self.update("edges", newPoints, self.data["zone"])

    def appendZonePoint(self, point):
        self.Zone.edges = Zone.appendEdge(self.Zone, point)
        self.appendSingle("edges", point, self.data["zone"])

    def deleteZonePoint(self, point):
        self.Zone.edges = Zone.deleteEdge(self.Zone, point)
        if point <= self.Zone.edgeNumber:
            self.deleteSingle("edges", point, self.data["zone"])

    def deleteAllZonePoint(self):
        self.Zone.edges = Zone.deleteAll(self.Zone)
        self.deleteAll("edges", self.data["zone"])

    def updateObjectDetection(self, model_name):
        self.model_name = model_name
        self.update("model", model_name, self.data["objectdetection"])

    def updateOpticalFlow(self, varList):
        self.update("min_thresh", varList[0], self.data["opticalflow"])
        self.update("max_thresh", varList[1], self.data["opticalflow"])
        self.update("kernel", varList[2], self.data["opticalflow"])
        self.update("bbox_thresh", varList[3], self.data["opticalflow"])
        self.update("nms_thresh", varList[4], self.data["opticalflow"])
        self.update("sigma", varList[5], self.data["opticalflow"])

    def updateMotionDetection(self, cnt_filter):
        self.update("cnt_filter", cnt_filter[0], self.data["motiondetection"])
        self.update("gaussian_kernel", cnt_filter[1], self.data["motiondetection"])
        self.update("closing_kernel", cnt_filter[2], self.data["motiondetection"])
    def updateSystem(self, capture, method, selectedcaptureopt):
        self.Camera.capture = capture
        self.update("capture", capture, self.data["camera"])
        self.Camera.cap = cv2.VideoCapture(self.Camera.capture)
        self.System.method = method
        self.update("method", method, self.data["system"])
        #self.updateMethod(method)
        self.System.input_option = selectedcaptureopt
        self.update("input_option", selectedcaptureopt, self.data["system"])


    """
    def updateMethod(self, method):
        if method == "Motion Detection":
            self.Method = MotionDetection(self)
        elif method == "Object Detection":
            pass
        elif method == "Optical Flow":
            pass
        elif method == "Mask RCNN":
            pass
    """
    def update(self, parameter, newvalue, jsonObject):

        jsonObject[parameter] = newvalue

        with open(self.jsonReader.path + self.jsonReader.filename, 'w') as f:
            json.dump(self.data, f, indent=4)

    def appendSingle(self, parameter, point, jsonObject):

        jsonObject[parameter].append(point)

        with open(self.jsonReader.path + self.jsonReader.filename, 'w') as f:
            json.dump(self.data, f, indent=4)

    def deleteSingle(self, parameter, point, jsonObject):

        del jsonObject[parameter][point]
        with open(self.jsonReader.path + self.jsonReader.filename, 'w') as f:
            json.dump(self.data, f, indent=4)

    def deleteAll(self, parameter, jsonObject):
        jsonObject[parameter] = ""
        with open(self.jsonReader.path + self.jsonReader.filename, 'w') as f:
            json.dump(self.data, f, indent=4)

global settings
settings = Settings()