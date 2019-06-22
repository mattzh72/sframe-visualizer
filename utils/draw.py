import numpy as np
import cv2

def draw_annotations(img, annotations):
	for a in annotations:
		draw_box_wh(img, a['x'], a['y'], a['w'], a['h'])

"""
x1, y1 ----------|
|				 |
|				 |
|				 |
|------------x2, y2

"""
def draw_box_corners(img, x1, y1, x2, y2, color=(0,255,0), width=3):
	assert (isinstance(img, np.ndarray)), 'Image is not of type numpy.ndarray.'

	cv2.rectangle(img, (x1,y1), (x2,y2), color, width)

"""
x, y ------------|
|				 |
|				 |
|				 |
|----------------|

"""
def draw_box_wh(img, x, y, w, h, color=(0,255,0), width=3):
	assert (isinstance(img, np.ndarray)), 'Image is not of type numpy.ndarray.'

	print(x, y, w, h)
	cv2.rectangle(img, (x,y), (x+w,y+h), color, width)




