import cv2
import random
import string
import os

class Camera:
    def __init__(self, settings):
        self.settings = settings
        self.capture = self.settings["capture"]
        self.cap = cv2.VideoCapture(self.capture)
        self.createOutput = self.settings["create_output"]
        self.createZone = self.settings["set_zone"]
        if self.createZone:
            pass

    def draw_zones(self, frame, edges):
        prevEdge = None
        for edge in edges:
            if prevEdge is not None:
                cv2.line(frame, (prevEdge["x"], prevEdge["y"]), (edge["x"], edge["y"]), (0, 0, 256), 2)
                prevEdge = edge
            else:
                prevEdge = edge
        edge = edges[0]
        cv2.line(frame, (prevEdge["x"], prevEdge["y"]), (edge["x"], edge["y"]), (0, 0, 256), 2)

    def createOutputVid(self, framelist):
        if self.createOutput:
            # Output
            height = int(self.cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
            width = int(self.cap.get(cv2.CAP_PROP_FRAME_WIDTH))
            size = (width, height)
            fps = self.cap.get(cv2.CAP_PROP_FPS)
            format_type = "mp4"
            fourcc = cv2.VideoWriter_fourcc(*'mp4v')
            S = 10  # number of characters in the string.
            outputPath = os.path.join(os.getcwd(), "media", "outputs")
            if not os.path.exists(outputPath):
                os.makedirs(outputPath)
                print(f"Directory created: {outputPath}")
            else:
                print(f"Directory already exists: {outputPath}")

            ran = ''.join(random.choices(string.ascii_uppercase + string.digits, k=S))
            outputFilePath = os.path.join(outputPath, f'{ran}.{format_type}')
            try:
                out = cv2.VideoWriter(outputFilePath, fourcc, fps, size)
                for frame in framelist:
                    out.write(frame)
                out.release()
                print(f"Files in {outputPath}: {os.listdir(outputPath)}")
                print(f"Video saved successfully at: {os.path.abspath(outputFilePath)}")

            except Exception as e:
                print(f"Failed to save video: {e}")


