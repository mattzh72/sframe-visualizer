from config import Configs
from utils.parse import read_video, compile_video, extract_bb
from utils.draw import draw_annotations

import turicreate as tc
import cv2

# Load model
model = tc.load_model(Configs.MODEL)
test = tc.Image('example.jpg')
pixels = test.pixel_data
pred = model.predict(test)
print(pred)
bbs = extract_bb(pred)

for label, annotations in bbs.items():
	if label == Configs.OBJECT_LABEL:
		draw_annotations(pixels, annotations)


cv2.imshow('image', pixels)
c = cv2.waitKey(0)
if 'q' == chr(c & 255):
    cv2.destroyAllWindows()
