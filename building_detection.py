import cv2
import numpy as np
import matplotlib.pyplot as plt
import os
import os.path

test_img=cv2.imread('./buildings/b7.jpeg',1)


building_cascade = cv2.CascadeClassifier('/home/hackingbot/Desktop/hack/haartrain/haar/cascade.xml')
gray = cv2.cvtColor(test_img, cv2.COLOR_BGR2GRAY)

buildings = building_cascade.detectMultiScale(gray, 1.20, 50)

print buildings

if len(buildings) is not 0:
	print 'Result: Building'
	print len(buildings)
	
	for values in buildings:
		temp = test_img.copy()
		cv2.rectangle(temp, (values[2], values[3]), (values[0], values[1]), (255,255,0), 1)
		cv2.imshow('Final', temp)
		cv2.waitKey(0)
		cv2.destroyAllWindows()
	#cv2.imshow('Final', test_img)
	#cv2.waitKey(0)
	#cv2.destroyAllWindows()
else:
	print 'No'
