import cv2
import turicreate as tc
from tqdm import tqdm

from utils.draw import *

def predict_on_video(video_path, model_path, draw_frame_num=True):
	video = cv2.VideoCapture(video_path)
	ret, frame = video.read()

	count = 0
	frames = []
	frame_num = 1

	while ret:
		# Predict and draw
		tc_frame = get_tc_img(frame)
		pred = model.predict(tc_frame)
		frame = tc.object_detector.util.draw_bounding_boxes(tc_frame, pred).pixel_data

		if draw_frame_num:
			frame = draw_text(frame, str(frame_num))

		frames.append(frame)
		count += 1
		frame_num += 1
		ret, frame = vidcap.read()

	return frames

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

def get_tc_img(img):
	assert (isinstance(img, np.ndarray)), 'Image is not of type numpy.ndarray.'

	RAW_FORMAT = 2
	return tc.Image(_image_data=img.tobytes(), 
		_width=img.shape[1], 
		_height=img.shape[0], 
		_channels=img.shape[2], 
		_format_enum=RAW_FORMAT, 
		_image_data_size=img.size)

def extract_imgs_from_sframe(sframe, target_label='mainPlate', buffer=64, draw_center=False, draw_center_line=False, draw_boundings=False, draw_masks=False, draw_frame_num=True, annotations_col='annotations', image_col='image', masks_col='stateMasks'):
	sf = list(tc.load_sframe(sframe))

	frames = []
	frame_num = 1
	centers = {}

	for x in tqdm(sf, desc='Parsing'):
		img = x[image_col].pixel_data
		append_centers(x[annotations_col], centers, buffer=buffer, target_label=target_label)

		if draw_boundings:
			img = tc.object_detector.util.draw_bounding_boxes(get_tc_img(img), x[annotations_col]).pixel_data

		if draw_masks:
			img = draw_mask_data(img, x[masks_col]) 

		if draw_center:
			img = draw_nearest_centers(img, centers)

		if draw_center_line:
			img = draw_center_lines(img, centers, buffer=buffer)

		if draw_frame_num:
			img = draw_text(img, str(frame_num))

		frames.append(img)
		frame_num += 1

	return frames



