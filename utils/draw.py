import numpy as np
from collections import deque
import cv2

def draw_mask_data(img, masks, threshhold=0.3):
	if masks:
		for mask in masks:
			mask = mask > threshhold
			img[:, :, 2] = (mask > 0) * 255 + (mask == 0) * img[:, :, 2]

	return img

def draw_center_lines(img, centers, buffer=64, thickness=5, color=(255, 0, 0)):
	for object_ID, pts in centers.items():
		for i in range(1, len(pts)):
			thickness = int(np.sqrt(buffer / float(i + 1)) * 2.5)
			cv2.line(img, pts[i - 1], pts[i], color, thickness)

	return img

def draw_nearest_centers(img, centers, thickness=5, color=(255, 0, 0)):
	for object_ID, pts in centers.items():
		if pts:
			cv2.circle(img, pts[0], thickness, color, -1)

	return img

def draw_text(img, txt, font=cv2.FONT_HERSHEY_SIMPLEX, loc=(25,40), scale=1, color=(255,0,0), thickness=2):
	cv2.putText(img, txt, loc, font, scale, color, thickness)

	return img

def append_centers(annotations, centers, draw=True, buffer=64, target_label=None, round=True):
	for annotation in annotations:
		if target_label and annotation['label'] != target_label:
			continue

		x = annotation['coordinates']['x']
		y = annotation['coordinates']['y']

		if round:
			x, y = int(x), int(y)

		if not annotation['objectID'] in centers:
			centers[annotation['objectID']] = deque(maxlen=buffer)

		centers[annotation['objectID']].appendleft((x, y))

	return centers
