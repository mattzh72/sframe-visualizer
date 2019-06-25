import numpy as np
import cv2

def draw_mask(img, masks, threshhold=0.3):
	if masks:
		for mask in masks:
			mask = mask > threshhold
			img[:, :, 2] = (mask > 0) * 255 + (mask == 0) * img[:, :, 2]

	return img



