from .Method import Method
import cv2


class MotionDetection(Method):
    def __init__(self, settings):
        Method.__init__(self, settings.data["method"])
        self.settings = settings
        self.method = settings.data["motiondetection"]
        self.cnt_filter = self.method["cnt_filter"]
        x = self.method["gaussian_kernel"]
        self.gaussian_kernel = (x, x)
        y = self.method["closing_kernel"]
        self.closing_kernel = (y, y)

    def run(self):
        # Initialize background subtractor
        back_sub = cv2.createBackgroundSubtractorMOG2()
        frames = []

        frame_number = 0

        while True:
            ret, frame = self.settings.Camera.cap.read()
            if not ret:
                self.settings.Camera.cap = cv2.VideoCapture(self.settings.Camera.capture)
                ret, frame = self.settings.Camera.cap.read()
                if not ret:
                    print("not")
                    break

            frame_number += 1

            # Draw Zone
            self.settings.Zone.edgesList = self.settings.Zone.setEdgeList(self.settings.data["zone"]["edges"])
            self.settings.Camera.draw_zones(frame, self.settings.Zone.edges)
            # Convert the frame to grayscale
            gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

            # Grayscale and noise removal
            blurred = cv2.GaussianBlur(gray, self.gaussian_kernel, 0)

            # Background subtraction
            fg_mask = back_sub.apply(blurred)

            # Morphological operations
            kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, self.closing_kernel)
            closing = cv2.morphologyEx(fg_mask, cv2.MORPH_CLOSE, kernel)

            # Object detection and tracking
            contours, _ = cv2.findContours(closing, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

            for cnt in contours:
                # Filter small contours
                if cv2.contourArea(cnt) < self.cnt_filter:
                    continue

                # Get bounding box
                x, y, w, h = cv2.boundingRect(cnt)

                # Check if the object is in the main zone
                if self.settings.Zone.is_in_main_zone(x, y):
                    cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)
                    cv2.putText(frame, "Intruder in main zone", (x, y - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0),
                                2)
                    print(f"Intruder detected in {frame_number}")

                # Display the frame
                if frame_number % 1 == 0:
                    cv2.imshow("Intruder Detection", frame)

            if self.settings.Camera.createOutput:
                frames.append(frame)

            if cv2.waitKey(1) & 0xFF == ord("q"):
                break

        if self.settings.Camera.createOutput:
            self.settings.Camera.createOutputVid(frames)
        self.settings.Camera.cap.release()
        cv2.destroyAllWindows()
