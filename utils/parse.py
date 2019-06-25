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

def compile_video(frames, rgb=True, target='./output.mp4'):
	assert len(frames) > 0, 'Frames list is empty.'

	height, width, layers = frames[0].shape
	codec = cv2.VideoWriter_fourcc(*'mp4v')
	video = cv2.VideoWriter(target, codec, 60, (width,height))
	
	print("Writing to video " + target)
	for frame in tqdm(frames):
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

def extract_imgs_from_sframe(sframe, draw=False):
	sf = tc.load_sframe(sframe)

	if draw:
		print("Drawing bounding boxes...")
		imgs = [img.pixel_data for img in tqdm(tc.object_detector.util.draw_bounding_boxes(sf['image'], sf['annotations']))]
		print("Drawing masks...")
		return [draw_mask(imgs[i], sf['stateMasks'][i]) for i in tqdm(range(len(sf)))]

	else:
		imgs = [img.pixel_data for img in tqdm(sf['image'])]

	return imgs

