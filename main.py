"""******************************************************************
File Name:main.py
Authors: Justin Jordan, David Ikemba, Thuong Nguyen
Date:
Project: Machine Vision Burr Detection System
Sponsor: Hunt and Hunt Ltd.
Faculty Advisor: Dr. Fred Chen
Instructor: Dr. Compeau
University: Texas State University Ingram School of Engineering
Description: The Machine Vision Burr Detection System (MVBDS) will
be designed by Texas State University Electrical Engineering
students, for Hunt and Hunt Ltd., to detect burrs at the
intersection of the keyway and inner-diameter threading of precision
machined pipes. The system will generate a pass/fail signal to let
the user know if burrs are detected. This is a proof of concept
design to demonstrate that machine vision can be used to automate
burr detection.
Minimum Requirements: The MVBDS must comply with the following:
Must detect defects within 1.5 minute time frame
Must generate pass/fail signal with 95% accuracy or greater
Must use Hunt & Hunt Ltd. Machined pipes
Must detect defects 1mm or larger
Project budget needs to be $500 or less
******************************************************************"""

import numpy as np
import cv2
from matplotlib import pyplot as plt
import matplotlib.gridspec as gridspec

gs = gridspec.GridSpec(2, 2) #set plot into 2x2

# create webcam object. set to 0 when running on ODROID.
cam = cv2.VideoCapture(0)

choice = input ("Enter 'b' to begin test, \n'd' to display current image, \n'm' to display additional menu, 'q' to quit: ")
print("\n")

while choice != "q" and choice != "Q":
    #TMN M option
    if choice == "m" or choice == "M":
        preview_choice = input ("Enter 'p' to begin preview. Hit Esc to exit preview: ")
        if preview_choice == "p" or preview_choice == "P":
            while (True):
                # Capture frame-by-frame
                ret, frame = cam.read()
                # Operations on the frame
                gray = cv2.cvtColor(frame, cv2.COLOR_RGB2GRAY)
                # Display the resulting frame
                cv2.imshow('frame', gray)
                #Esc to Exit
                if cv2.waitKey(1) == 27:
                    cv2.destroyAllWindows()
                    break
        else:
            print ("Please reselect one of the options")

     #TMN D option
    elif choice == "d" or choice == "D":
        returnVal, workingImg = cam.read()
        workingImg = cv2.cvtColor(workingImg, cv2.COLOR_RGB2BGR)
        plt.imshow(workingImg, cmap='brg', interpolation='bicubic')
        plt.xticks([]), plt.yticks([])  # to hide tick values on X and Y axis
        plt.show()

    elif choice != "b" and choice != "B":
        choice = input ("\nEnter 'b' to begin test, \n'd' to display curent image, \n'm' to display additional menu, 'q' to quit: ")
        continue

    else:
        # capture 1 frame from cam
        returnVal, workingImg = cam.read()
        if returnVal == False:
            print("No communication with camera. Program terminating.")
            exit(-1)

        # convert to proper color format
        workingImg = cv2.cvtColor(workingImg, cv2.COLOR_RGB2BGR)

        # plot working image. this code is for testing and can be removed later.
        '''plt.imshow(workingImg, cmap='brg', interpolation='bicubic')
        plt.xticks([]), plt.yticks([])  # to hide tick values on X and Y axis
        ax1 = plt.subplot(gs[0]) #display image in 1st position
        #TMN: Commented out save and show image
        #f1 = plt.figure(1)
        #f1.savefig('pic1.png')
        #plt.show()'''

        # convert to grayscale
        grayImg = cv2.cvtColor(workingImg, cv2.COLOR_BGR2GRAY)

        # plot grayscale image. this code is for testing and can be removed later.
        '''plt.imshow(grayImg, cmap='gray', interpolation='bicubic')
        plt.xticks([]), plt.yticks([])  # to hide tick values on X and Y axis
        ax2 = plt.subplot(gs[1]) #display image in 2nd position
        # TMN: Commented out save and show image
        #f2 = plt.figure(2)
        #f2.savefig('pic2.png')
        #plt.show()'''

        # open the classifier, best to date (cascade_24_24_400_single.xml)
        detectCascade = cv2.CascadeClassifier('cascade.xml')
        if (detectCascade.empty() == True):
            print("Cascade Classifier not loaded, program terminating")
            exit(-1)

        # load a test image for detection testing (can be removed later)
        testImg = cv2.imread('train_test.png')
        resultsImg = testImg # to later display results of detection

        # detect the objects, detectCascade.detectMultiScale(image, scaleFactor, minNeighbors, flags, minSize, MaxSize)
        objectsFound = detectCascade.detectMultiScale(testImg, 1.1, 60, 0, (60, 60), (140, 140))

        # highlight each object detected in image (x = xCoord, y = yCoord, w = width, h = height)
        for (x, y, w, h) in objectsFound:
            resultsImg = cv2.rectangle(resultsImg, (x, y), (x+w,y+h), (255, 0, 0), 2)
            print(x, " ", y, " ", w, " ", h)

        # display results of detection
        plt.imshow(resultsImg, cmap='brg', interpolation='bicubic')
        plt.xticks([]), plt.yticks([])  # to hide tick values on X and Y axis
        plt.show()

        # apply Gaussian bilateral filter to grayscale image
        '''filterImg = cv2.bilateralFilter(grayImg, 5, 100, 100)

        # plot filtered image. this code is for testing and can be removed later.
        plt.imshow(filterImg, cmap='gray', interpolation='bicubic')
        plt.xticks([]), plt.yticks([])  # to hide tick values on X and Y axis
        ax3 = plt.subplot(gs[2]) #display image in 3rd position
        #TMN: Commented out save and show image
        #f3 = plt.figure(3)
        #f3.savefig('pic3.png')
        #plt.show()'''

        # apply Sobel filter
        '''sobelImg = cv2.Sobel(grayImg, cv2.CV_64F, 1, 1, ksize = 5)

        # plot results of Sobel filter. this code is for testing and can be removed later.
        plt.imshow(sobelImg, cmap='gray', interpolation='bicubic')
        plt.xticks([]), plt.yticks([])  # to hide tick values on X and Y axis
        ax4 = plt.subplot(gs[3]) #display image in 4th position
        #TMN: Commented out save and show image
        #f4 = plt.figure(4)
        #f4.savefig('pic4.png')
        # plt.show()'''

        # apply thresholding for binary image
        '''binaryImg = cv2.Canny(filterImg, 100, 125)

        # plot results of thresholding. this code is for testing and can be removed later.
        plt.imshow(binaryImg, cmap='gray', interpolation='bicubic')
        plt.xticks([]), plt.yticks([])  # to hide tick values on X and Y axis
        #TMN: Commented out save image
        #f5 = plt.figure(5)
        #f4.savefig('pic4.png')

        plt.show()'''

    choice = input ("Enter 'b' to begin test, \n'd' to display current image, \n'm' to display additional menu, 'q' to quit: ")

cam.release()
cv2.destroyAllWindows()