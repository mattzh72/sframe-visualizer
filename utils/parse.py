import cv2
import turicreate as tc

def read_video(video_path):
	video = cv2.VideoCapture(video_path)
	ret, frame = video.read()

	count = 0
	frames = []

	while ret:
		frames.append(frame)
		ret, frame = vidcap.read()
		count += 1

	return frames

def compile_video(frames, target='./output.avi'):
	assert len(frames) > 0, 'Frames list is empty.'

	height, width, layers = frames[0].shape
	video = cv2.VideoWriter(target, 0, 1, (width,height))
	for frame in frames:
		video.write(frame)

	cv2.destroyAllWindows()
	video.release()

def convert_img(img):
	assert (isinstance(img, numpy.ndarray)), 'Image is not of type numpy.ndarray.'

	RAW_FORMAT = 2
	return tc.Image(_image_data=img.tobytes(), 
		_width=img.shape[1], 
		_height=img.shape[0], 
		_channels=img.shape[2], 
		_format_enum=RAW_FORMAT, 
		_image_data_size=img.size)

"""
[{'label': 'barbell', 'type': 'rectangle', 'coordinates': {'x': 134.6328066601753, 'y': 192.2079239648583, 'width': 231.50588915898248, 'height': 110.18064159613388}, 'confidence': 0.7823181846848669}, {'label': 'barbell', 'type': 'rectangle', 'coordinates': {'x': 212.3092042818808, 'y': 186.7778821093862, 'width': 362.41656083327075, 'height': 179.77102903219372}, 'confidence': 0.5556210402434759}]
"""
def extract_bb(annotations):
	bbs = {}

	for a in annotations:
		label = a['label']
		coords = a['coordinates']
		if label not in bbs:
			bbs[label] = []			

		bbs[label].append({'x': int(coords['x']), 'y': int(coords['y']), 'w': int(coords['width']), 'h': int(coords['height'])})

	return bbs

def read_sframe(sframe, draw=False):
	sf = tc.load_sframe(sframe)

	if draw:
		return [img.pixel_data for img in tc.object_detector.util.draw_bounding_boxes(sf['image'], sf['annotations'])]
	else:
		return [img.pixel_data for img in sf['image']]














