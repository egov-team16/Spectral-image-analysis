# Spectral-image-analysis

Use objectmake.py to get the co-ordinates of Regions of Interest within your image. These ROI represent the positive class (positive.txt) that is to be detected.
Once the co-ordinate file is generated, this file is converted into a vector of samples which, along with the information about images within the negative class (negative.txt - primarily the background), is then used in training the haar cascade and generating a cascade xml file.
This cascade xml file is then used to detect any object of interest in building_detection.py
