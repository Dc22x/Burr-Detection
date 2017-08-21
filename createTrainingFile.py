"""******************************************************************
File Name:createTrainingFile.py
Authors: Justin Jordan, David Ikemba, Thuong Nguyen
Date:
Project: Machine Vision Burr Detection System
Sponsor: Hunt and Hunt Ltd.
Faculty Advisor: Dr. Fred Chen
Instructor: Dr. Compeau
University: Texas State University Ingram School of Engineering
Description: The purpose of this program is to create a .vec
   file to be used for the purposes of training a Haar cascade
   capable of detecting a burr-free threading keyway intersection.
******************************************************************"""

import cv2

opencv_createsamples -vec trainingSamples.vec -info info.dat -w 300 -h 300