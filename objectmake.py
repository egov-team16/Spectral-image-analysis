import cv2
import sys
import os
import numpy as np

#IMG_SIZE = (300,300)
#IMG_CHAN = 3
#IMG_DEPTH = cv2.uint8
#image = cv2.CreateImage(IMG_SIZE, IMG_DEPTH, IMG_CHAN)
#image2 = cv2.CreateImage(IMG_SIZE, IMG_DEPTH, IMG_CHAN) 
image = np.zeros((500,500,3), np.uint8)
image2 = np.zeros((500,500,3), np.uint8)
roi_x0 = 0
roi_y0 = 0
roi_x1 = 0
roi_y1 = 0
num_of_rec = 0
start_draw = False
window_name = "<Space> to save and continue, <B> to load next, <X> to skip, <ESC> to exit."

def on_mouse(event, x, y, flag, params):
	global start_draw
	global roi_x0
	global roi_y0
	global roi_x1
	global roi_y1
	if (event == cv2.EVENT_LBUTTONDOWN):
		if (not start_draw):
			roi_x0 = x
			roi_y0 = y
			start_draw = True
			print (str(roi_x0) + " " + str(roi_y0))
		else:
			roi_x1 = x
			roi_y1 = y
			start_draw = False
			print (str(roi_x1) + " " + str(roi_y1) + " " + str(roi_x0) + " " + str(roi_y0))
	elif (event == cv2.EVENT_MOUSEMOVE and start_draw):
		#Redraw ROI selection
		image2 = np.copy(image)
		cv2.rectangle(image2, (roi_x0, roi_y0), (x,y), (255,0,255), 1)
		#print (str(x) + " " + str(y) + " " + str(roi_x0) + " " + str(roi_y0))
		cv2.imshow(window_name, image2)

def main():
# Might want to divide this a bit more.
	global image
	iKey = 0
	
	#if (len(sys.argv) != 3):
	#	sys.stderr.write("%s output_info.txt raw/data/directory\n" 
	#		% sys.argv[0])
	#	return -1

	input_directory = "./buildings/";
	output_file = "../coordinates.txt";

	#Get a file listing of all files within the input directory
	try:
		files = os.listdir(input_directory)
		print files
	except OSError:
		sys.stderr.write("Failed to open dirctory %s\n" 
			% input_directory)
		return -1

	files.sort()

	sys.stderr.write("ObjectMarker: Input Directory: %s Output File %s\n" 
			% (input_directory, output_file))

	# init GUI
	cv2.namedWindow(window_name, 1)
	cv2.setMouseCallback(window_name, on_mouse, None)

	sys.stderr.write("Opening directory...")
	# init output of rectangles to the info file
	os.chdir(input_directory)
	sys.stderr.write("done.\n")

	str_prefix = input_directory

	try:
		output = open(output_file, 'a')
	except IOError:
		sys.stderr.write("Failed to open file %s.\n" % output_file)
		return -1

	for file in files:
                print file
		str_postfix = ""
		num_of_rec = 0
		img = file
		sys.stderr.write("Loading image %s...\n" % img)

		try: 
			image = cv2.imread(img, 1)
			#print image.shape
		except IOError: 
			sys.stderr.write("Failed to load image %s.\n" % img)
			return -1

		#  Work on current image
		cv2.imshow(window_name, image)
		# Need to figure out waitkey returns.
		# <ESC> = 27		exit program
		# <Space> = 32		add rectangle to current image
		# <x> = 136			skip image
		# <b> = 98			load next
		while(True):
			iKey = cv2.waitKey(0) % 255
			# This is ugly, but is actually a simplification of the C++.
			if iKey == 27 and num_of_rec==0:
				cv2.destroyWindow(window_name)
				#print num_of_rec
				return
			elif iKey == 32:
				num_of_rec += 1
				# Currently two draw directions possible:
				# from top left to bottom right or vice versa
				if (roi_x0 < roi_x1 and roi_y0 < roi_y1):
					str_postfix += " %d %d %d %d" % (roi_x0,
					roi_y0, (roi_x1-roi_x0), (roi_y1-roi_y0))
				elif (roi_x0 > roi_x1 and roi_y0 > roi_y1):
					str_postfix += " %d %d %d %d" % (roi_x1, 
					roi_y1, (roi_x0-roi_x1), (roi_y0-roi_y1))
				print (img + " " + str(num_of_rec) + str_postfix)
			elif iKey==98:
				if num_of_rec==0:
					sys.stderr.write("Nothing to save in %s.\n" % img)
					break
				else:
					output.write(img + " " + str(num_of_rec) + str_postfix)
					str_postfix += "\n"
					break
			elif iKey == 120 and num_of_rec==0:
				sys.stderr.write("Skipped %s.\n" % img)
				break
		
if __name__ == '__main__':
	main()
