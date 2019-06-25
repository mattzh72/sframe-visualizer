import cv2
import turicreate as tc
from tqdm import tqdm

from utils.draw import draw_mask

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

def compile_video(frames, rgb=True, fps=30, target='./output.mp4'):
	assert len(frames) > 0, 'Frames list is empty.'

	height, width, layers = frames[0].shape
	codec = cv2.VideoWriter_fourcc(*'mp4v')
	video = cv2.VideoWriter(target, codec, fps, (width,height))
	
	for frame in tqdm(frames, desc='Writing'):
		if rgb:
			frame = cv2.cvtColor(frame,cv2.COLOR_BGR2RGB)

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

def extract_imgs_from_sframe(sframe, draw_boundings=False, draw_masks=False):
	sf = list(tc.load_sframe(sframe))

	frames = []
	for el in tqdm(sf, desc='Parsing'):
		img = el['image']

		if draw_boundings:
			img = tc.object_detector.util.draw_bounding_boxes(img, el['annotations']) 

		if draw_masks:
			img = draw_mask(img.pixel_data, el['stateMasks']) 

		frames.append(img.pixel_data if isinstance(img, tc.Image) else img)

	return frames



