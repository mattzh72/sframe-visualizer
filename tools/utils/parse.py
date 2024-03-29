import cv2
import turicreate as tc
from tqdm import tqdm
import numpy as np

from tools.utils.draw import *
from tools.utils.segment import *

def predict_on_video(video_path, model_path, confidence_threshold=0.75, iou_threshold=0.25, target_label=None, num_objs=-1, draw_masks=False, draw_frame_num=True):
	model = tc.load_model(model_path)
	frames = read_video(video_path)

	pred_frames = []

	for i in tqdm(range(len(frames)), desc='Predicting'):
		frame = frames[i]

		# Predict and draw
		pred = model.predict(get_tc_img(frame), 
			confidence_threshold=confidence_threshold, 
			iou_threshold=iou_threshold,
			verbose=False)
		pred = clean_predictions(pred, target_label=target_label, num_objs=num_objs)

		if draw_masks:
			crops = get_crops(frame, pred)
			segs = segment(crops)
			frame = draw(frame, pred, segs)

		if draw_frame_num:
			frame = draw_text(frame, str(i))

		frame = tc.object_detector.util.draw_bounding_boxes(get_tc_img(frame), pred).pixel_data
		pred_frames.append(frame)

	return pred_frames

def get_prediction_sframe(video_path, model_path, target_label=None, num_objs=-1):
	frames, model = read_video(video_path), tc.load_model(model_path)

	sf_dict = {'image': [], 'annotations': []}

	for i in tqdm(range(len(frames)), desc='Predicting'):
		frame = frames[i]

		# Predict and draw
		pred = model.predict(get_tc_img(frame), verbose=False)
		pred = clean_predictions(pred, target_label=target_label, num_objs=num_objs)

		sf_dict['image'].append(frame)
		sf_dict['annotations'].append(pred)

	return tc.SFrame(sf_dict)

def clean_predictions(pred, target_label=None, num_objs=-1):
	if target_label:
		pred = [p for p in pred if p['label'] == target_label]

	if num_objs > 0:
		pred = sorted(pred, reverse=True, key=lambda x: x['confidence'])[:num_objs]

	return pred

def read_video(video_path, downsize=0.3):
	video = cv2.VideoCapture(video_path)
	frame_count = int(video.get(cv2.CAP_PROP_FRAME_COUNT))

	ret, frame = video.read()
	frames = []

	pbar = tqdm(total=frame_count)
	while ret:
		if downsize != 1:
			frame = cv2.resize(frame, None, fx=downsize, fy=downsize)

		frames.append(frame)
		ret, frame = video.read()
		pbar.update(1)

	pbar.close()
	return frames

def compile_video(frames, fps=30, target='./output.mp4'):
	assert len(frames) > 0, 'Frames list is empty.'

	height, width, layers = frames[0].shape
	codec = cv2.VideoWriter_fourcc(*'mp4v')
	video = cv2.VideoWriter(target, codec, fps, (width,height))
	
	for frame in tqdm(frames, desc='Writing'):
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
	frame_num = 0
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



