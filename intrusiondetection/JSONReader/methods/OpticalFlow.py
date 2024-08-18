from .Method import Method
import os
from glob import glob
import re
import matplotlib
import numpy as np
import cv2
import matplotlib.pyplot as plt



class OpticalFlow(Method):
    def __init__(self, settings):
        Method.__init__(self, settings.data["method"])
        self.settings = settings
        self.method = settings.data["opticalflow"]
        self.min_thresh = self.method["min_thresh"]
        self.max_thresh = self.method["max_thresh"]
        x = self.method["kernel"]
        self.kernel_size = (x, x)
        self.bbox_thresh = self.method["bbox_thresh"]
        self.nms_thresh = self.method["nms_thresh"]
        g = self.method["gaussian_blur_kernel"]
        self.gaussian_blur_kernel = (g, g)
        self.sigma = self.method["sigma"]
        self.pyr_scale = self.method["pyr_scale"]
        self.levels = self.method["levels"]
        self.winsize = self.method["winsize"]
        self.iterations = self.method["iterations"]
        self.poly_n = self.method["poly_n"]
        self.poly_sigma = self.method["poly_sigma"]
        self.height = int(self.settings.Camera.cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
        self.width = int(self.settings.Camera.cap.get(cv2.CAP_PROP_FRAME_WIDTH))
        self.motion_thresh = np.c_[np.linspace(self.min_thresh, self.max_thresh, self.height)].repeat(self.width,
                                                                                                      axis=-1)

    def compute_flow(self, frame1, frame2):
        # convert to grayscale
        gray1 = cv2.cvtColor(frame1, cv2.COLOR_BGR2GRAY)
        gray2 = cv2.cvtColor(frame2, cv2.COLOR_BGR2GRAY)

        # blurr image
        gray1 = cv2.GaussianBlur(gray1, dst=None, ksize=self.gaussian_blur_kernel, sigmaX=self.sigma)
        gray2 = cv2.GaussianBlur(gray2, dst=None, ksize=self.gaussian_blur_kernel, sigmaX=self.sigma)

        flow = cv2.calcOpticalFlowFarneback(gray1, gray2, None,
                                            pyr_scale=self.pyr_scale,
                                            levels=self.levels,
                                            winsize=self.winsize,
                                            iterations=self.iterations,
                                            poly_n=self.poly_n,
                                            poly_sigma=self.poly_sigma,
                                            flags=0)
        return flow

    def get_flow_viz(self, flow):
        """ Obtains BGR image to Visualize the Optical Flow
            """
        hsv = np.zeros((flow.shape[0], flow.shape[1], 3), dtype=np.uint8)
        hsv[..., 1] = 255

        mag, ang = cv2.cartToPolar(flow[..., 0], flow[..., 1])
        hsv[..., 0] = ang * 180 / np.pi / 2
        hsv[..., 2] = cv2.normalize(mag, None, 0, 255, cv2.NORM_MINMAX)
        rgb = cv2.cvtColor(hsv, cv2.COLOR_HSV2RGB)

        return rgb

    def get_motion_mask(self, flow_mag, motion_thresh=1, kernel=np.ones((7, 7))):
        """ Obtains Detection Mask from Optical Flow Magnitude
            Inputs:
                flow_mag (array) Optical Flow magnitude
                motion_thresh - thresold to determine motion
                kernel - kernal for Morphological Operations
            Outputs:
                motion_mask - Binray Motion Mask
            """
        motion_mask = np.uint8(flow_mag > motion_thresh) * 255

        motion_mask = cv2.erode(motion_mask, kernel, iterations=1)
        motion_mask = cv2.morphologyEx(motion_mask, cv2.MORPH_OPEN, kernel, iterations=1)
        motion_mask = cv2.morphologyEx(motion_mask, cv2.MORPH_CLOSE, kernel, iterations=3)

        return motion_mask

    def run(self):

        frames = []
        frame_number = 0
        # get variable motion thresh based on prior knowledge of camera position
        self.motion_thresh = np.c_[np.linspace(self.min_thresh, self.max_thresh, self.height)].repeat(self.width, axis=-1)
        kernel = np.ones(self.kernel_size, dtype=np.uint8)

        ret, frame_first = self.settings.Camera.cap.read()
        if not ret:
            self.settings.Camera.cap = cv2.VideoCapture(self.settings.Camera.capture)
            ret, frame_first = self.settings.Camera.cap.read()
            if not ret:
                print("not")

        while ret:
            ret, frame_second = self.settings.Camera.cap.read()
            if not ret:
                self.settings.Camera.cap = cv2.VideoCapture(self.settings.Camera.capture)
                ret, frame_second = self.settings.Camera.cap.read()
                if not ret:
                    print("not")
                    break

            frame_number += 1
            # compute dense optical flow

            detections = self.get_detections(frame_first,
                                             frame_second,
                                             motion_thresh=self.motion_thresh,
                                             bbox_thresh=self.bbox_thresh,
                                             nms_thresh=self.nms_thresh,
                                             mask_kernel=kernel)
            frame_first = frame_second
            # draw bounding boxes on frame
            self.draw_bboxes(frame_second, detections)
            # Display the frame

            cv2.imshow("Intruder Detection", frame_second)
            if self.settings.Camera.createOutput:
                frames.append(frame_second)

            if cv2.waitKey(1) & 0xFF == ord("q"):
                break

        if self.settings.Camera.createOutput:
            self.settings.Camera.createOutputVid(frames)
        #self.settings.Camera.cap.release()
        cv2.destroyAllWindows()

    def get_contour_detections(self, mask, ang, angle_thresh=2, thresh=400):
        """ Obtains initial proposed detections from contours discoverd on the
            mask. Scores are taken as the bbox area, larger is higher.
            Inputs:
                mask - thresholded image mask
                angle_thresh - threshold for flow angle standard deviation
                thresh - threshold for contour size
            Outputs:
                detectons - array of proposed detection bounding boxes and scores
                            [[x1,y1,x2,y2,s]]
            """
        # get mask contours
        contours, _ = cv2.findContours(mask,
                                       cv2.RETR_EXTERNAL,  # cv2.RETR_TREE,
                                       cv2.CHAIN_APPROX_TC89_L1)
        temp_mask = np.zeros_like(mask)  # used to get flow angle of contours
        angle_thresh = angle_thresh * ang.std()
        detections = []
        for cnt in contours:
            # get area of contour
            x, y, w, h = cv2.boundingRect(cnt)
            area = w * h

            # get flow angle inside of contour
            cv2.drawContours(temp_mask, [cnt], 0, (255,), -1)
            flow_angle = ang[np.nonzero(temp_mask)]

            x1 = x + w/2
            y1 = y + h/2

            if (area > thresh) and (flow_angle.std() < angle_thresh) and self.settings.Zone.is_in_main_zone(x1, y1):  # hyperparameter
                detections.append([x, y, x + w, y + h, area])

        if len(detections) == 0:
            return np.array([])  # Return an empty array if no detections
        return np.array(detections)

    def get_detections(self, frame1, frame2, motion_thresh=1, bbox_thresh=400, nms_thresh=0.1,
                       mask_kernel=np.ones((7, 7), dtype=np.uint8)):
        """ Main function to get detections via Frame Differencing
            Inputs:
                frame1 - Grayscale frame at time t
                frame2 - Grayscale frame at time t + 1
                motion_thresh - Minimum flow threshold for motion
                bbox_thresh - Minimum threshold area for declaring a bounding box
                nms_thresh - IOU threshold for computing Non-Maximal Supression
                mask_kernel - kernel for morphological operations on motion mask
            Outputs:
                detections - list with bounding box locations of all detections
                    bounding boxes are in the form of: (xmin, ymin, xmax, ymax)
            """
        # get optical flow
        flow = self.compute_flow(frame1, frame2)

        # separate into magntiude and angle
        mag, ang = cv2.cartToPolar(flow[..., 0], flow[..., 1])

        motion_mask = self.get_motion_mask(mag, motion_thresh=motion_thresh, kernel=mask_kernel)

        # get initially proposed detections from contours
        detections = self.get_contour_detections(motion_mask, ang=ang, thresh=bbox_thresh)

        # separate bboxes and scores
        bboxes = detections[:, :4]
        scores = detections[:, -1]

        # perform Non-Maximal Supression on initial detections
        return self.non_max_suppression(bboxes, scores, threshold=nms_thresh)

    def non_max_suppression(self, boxes, scores, threshold=1e-1):
        """
        Perform non-max suppression on a set of bounding boxes
        and corresponding scores.
        Inputs:
            boxes: a list of bounding boxes in the format [xmin, ymin, xmax, ymax]
            scores: a list of corresponding scores
            threshold: the IoU (intersection-over-union) threshold for merging bboxes
        Outputs:
            boxes - non-max suppressed boxes
        """
        # Sort the boxes by score in descending order
        boxes = boxes[np.argsort(scores)[::-1]]

        # remove all contained bounding boxes and get ordered index
        order = self.remove_contained_bboxes(boxes)

        keep = []
        while order:
            i = order.pop(0)
            keep.append(i)
            for j in order:
                # Calculate the IoU between the two boxes
                intersection = max(0, min(boxes[i][2], boxes[j][2]) - max(boxes[i][0], boxes[j][0])) * \
                               max(0, min(boxes[i][3], boxes[j][3]) - max(boxes[i][1], boxes[j][1]))
                union = (boxes[i][2] - boxes[i][0]) * (boxes[i][3] - boxes[i][1]) + \
                        (boxes[j][2] - boxes[j][0]) * (boxes[j][3] - boxes[j][1]) - intersection
                iou = intersection / union

                # Remove boxes with IoU greater than the threshold
                if iou > threshold:
                    order.remove(j)

        return boxes[keep]

    def remove_contained_bboxes(self, boxes):
        """ Removes all smaller boxes that are contained within larger boxes.
            Requires bboxes to be soirted by area (score)
            Inputs:
                boxes - array bounding boxes sorted (descending) by area
                        [[x1,y1,x2,y2]]
            Outputs:
                keep - indexes of bounding boxes that are not entirely contained
                       in another box
            """
        check_array = np.array([True, True, False, False])
        keep = list(range(0, len(boxes)))
        for i in keep:  # range(0, len(bboxes)):
            for j in range(0, len(boxes)):
                # check if box j is completely contained in box i
                if np.all((np.array(boxes[j]) >= np.array(boxes[i])) == check_array):
                    try:
                        keep.remove(j)
                    except ValueError:
                        continue
        return keep

    def draw_bboxes(self, frame, detections):
        # Draw Zone
        self.settings.Zone.edgesList = self.settings.Zone.setEdgeList(self.settings.data["zone"]["edges"])
        self.settings.Camera.draw_zones(frame, self.settings.Zone.edges)
        for det in detections:
            x1, y1, x2, y2 = det
            cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 255, 0), 3)
            cv2.putText(frame, "Intruder in main zone", (x1, y1 - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0),
                        2)
