# import the necessary packages
import time
import cv2
import numpy as np
import math
import sys

# Function to calculate distance between four points


def calDis(x1, y1, x2, y2):
    dist = math.sqrt((x2 - x1)**2 + (y2 - y1)**2)
    return dist


class Sticker:
    def __init__(self, *args, **kwargs):
        # define range of green color in HSV
        self.lower_green = np.array([45, 50, 50])
        self.upper_green = np.array([75, 255, 255])
        # define range of red color in HSV
        self.lower_red = np.array([0, 50, 50])
        self.upper_red = np.array([15, 255, 255])
        # define range of blue color in HSV
        self.lower_blue = np.array([105, 50, 50])
        self.upper_blue = np.array([125, 255, 255])
        # define range of yellow color in HSV
        self.lower_yellow = np.array([22, 50, 50])
        self.upper_yellow = np.array([32, 255, 255])

    def find_sticker(self, frame, show_image=False):
        #if show_image:
            #cv2.imshow("abc", frame)
        # Create empty points array
        yellow = []
        green = []
        red = []
        blue = []

        # Get default camera window size
        # Here we pass the frame
        Height, Width = frame.shape[:2]

        # Capture webcame frame
        hsv_img = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
        blank_image = np.zeros((frame.shape[0], frame.shape[1], 3))
        print(blank_image.shape)

        # detection of each color begins
        # Threshold the HSV image to get only green color
        maskg = cv2.inRange(hsv_img, self.lower_green, self.upper_green)
        kernelg = np.ones((5, 5), np.uint8)
        maskg = cv2.morphologyEx(maskg, cv2.MORPH_OPEN, kernelg)
        _, contoursg, _ = cv2.findContours(
            maskg.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

        # Threshold the HSV image to get only yellow color
        masky = cv2.inRange(hsv_img, self.lower_yellow, self.upper_yellow)
        kernely = np.ones((5, 5), np.uint8)
        masky = cv2.morphologyEx(masky, cv2.MORPH_OPEN, kernely)
        _, contoursy, _ = cv2.findContours(
            masky.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

        # Threshold the HSV image to get only blue color
        maskb = cv2.inRange(hsv_img, self.lower_blue, self.upper_blue)
        kernelb = np.ones((5, 5), np.uint8)
        maskb = cv2.morphologyEx(maskb, cv2.MORPH_OPEN, kernelb)
        _, contoursb, _ = cv2.findContours(
            maskb.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

        # Threshold the HSV image to get only red color
        maskr = cv2.inRange(hsv_img, self.lower_red, self.upper_red)
        kernelr = np.ones((5, 5), np.uint8)
        maskr = cv2.morphologyEx(maskr, cv2.MORPH_OPEN, kernelr)
        _, contoursr, _ = cv2.findContours(
            maskr.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

        flag = 1
        if len(contoursg) > 0:
            for c in contoursg:
                (x, y), radius = cv2.minEnclosingCircle(c)
                if radius > 2:
                    green.append((x, y))
                    cv2.circle(blank_image, (int(x), int(y)),
                               int(radius), (255, 255, 255), 2)
        else:
            flag = 0
        if len(contoursy) > 0:
            for c in contoursy:
                (x, y), radius = cv2.minEnclosingCircle(c)
                if radius > 2:
                    yellow.append((x, y))
                    cv2.circle(blank_image, (int(x), int(y)),
                               int(radius), (255, 255, 0), 2)
        else:
            flag = 0
        if len(contoursr) > 0:
            for c in contoursr:
                (x, y), radius = cv2.minEnclosingCircle(c)
                if radius > 2:
                    red.append((x, y))
                    cv2.circle(blank_image, (int(x), int(y)),
                               int(radius), (255, 0, 0), 2)
        else:
            flag = 0
        if len(contoursb) > 0:
            for c in contoursb:
                (x, y), radius = cv2.minEnclosingCircle(c)
                if radius > 2:
                    blue.append((x, y))
                    cv2.circle(blank_image, (int(x), int(y)),
                               int(radius), (0, 0, 255), 2)
        else:
            flag = 0
        if flag == 1:
            for xg, yg in green:
                for xy, yy in yellow:
                    for xr, yr in red:
                        for xb, yb in blue:
                            dis_gy = calDis(xy, xg, yy, yg)
                            dis_gr = calDis(xr, xg, yr, yg)
                            dis_gb = calDis(xb, xg, yb, yg)
                            dis_yr = calDis(xy, xr, yy, yr)
                            dis_yb = calDis(xy, xb, yy, yb)
                            dis_rb = calDis(xr, xb, yr, yb)
                            # print(dis_gy, dis_gr, dis_gb, dis_yr, dis_yb, dis_rb)
                            # cv2.imshow("kuch bhi", blank_image)
                            # cv2.waitKey(1000)
                            dist = 275
                            if dis_gy < dist and dis_gr < dist and dis_gb < dist and dis_yr < dist and dis_yb < dist and dis_rb < dist:
                                print("YES")
                                cv2.circle(blank_image, (int(xg), int(yg)), int(
                                    radius), (255, 255, 255), -1)
                                if show_image:
                                    cv2.destroyAllWindows()
                                    # sys.exit()
                                centroid_x = (xg + xy + xr + xb) / 4
                                centroid_y = (yg + yy + yr + yb) / 4
                                return True, centroid_x, centroid_y

        blank_image = cv2.flip(blank_image, 1)
        if show_image:
            cv2.imshow("Object Tracker", blank_image)
        return False, None, None
