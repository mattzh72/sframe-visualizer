import cv2
import numpy as np

def get_crops(img, annotations, padding=0):
	crops = []
	new_img = img.copy() # Prevent drawing on original image
	for a in annotations:
		c = a['coordinates']

		y1, y2 = int(c['y'] - c['height'] / 2 - padding), int(c['y'] + c['height'] / 2 + padding)
		x1, x2 = int(c['x'] - c['width'] / 2 - padding), int(c['x'] + c['width'] / 2 + padding)

		crop = new_img[y1: y2, x1:x2]
		crops.append(crop)
	return crops

def segment(crops):
	segs = []
	for c in crops:
		gray = cv2.cvtColor(c, cv2.COLOR_BGR2GRAY)
		ret, thresh = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU)

		# noise removal
		kernel = np.ones((3,3),np.uint8)
		opening = cv2.morphologyEx(thresh, cv2.MORPH_OPEN,kernel, iterations = 4)
		# sure background area
		sure_bg = cv2.dilate(opening,kernel, iterations=3)
		# Finding sure foreground area
		dist_transform = cv2.distanceTransform(opening,cv2.DIST_L2,5)
		ret, sure_fg = cv2.threshold(dist_transform,0.7*dist_transform.max(),255,0)
		# Finding unknown region
		sure_fg = np.uint8(sure_fg)
		unknown = cv2.subtract(sure_bg,sure_fg)
		# Marker labelling
		ret, markers = cv2.connectedComponents(sure_fg)
		# Add one to all labels so that sure background is not 0, but 1
		markers = markers+1
		# Now, mark the region of unknown with zero
		markers[unknown==255] = 0

		markers = cv2.watershed(c, markers)
		markers[:,[0,-1]] = markers[[0,-1]] = 1
		c[markers != 1] = [255,191,0]

		segs.append(c)

	return segs

def draw(img, annotations, segs, padding=0):
	overlay = img.copy()

	for i in range(len(annotations)):
		a = annotations[i]
		c = a['coordinates']

		y1, y2 = int(c['y'] - c['height'] / 2 - padding), int(c['y'] + c['height'] / 2 + padding)
		x1, x2 = int(c['x'] - c['width'] / 2 - padding), int(c['x'] + c['width'] / 2 + padding)

		overlay[y1: y2, x1:x2] = segs[i]

	alpha = 0.5
	cv2.addWeighted(overlay, alpha, img, 1 - alpha,0, img)

	return img





