import turicreate as tc
import os
import yaml
from tqdm import tqdm

from utils.parse import extract_imgs_from_sframe, compile_video

ext = (".3g2", ".3gp", ".asf", ".asx", ".avi", ".flv", ".m2ts", ".mkv", ".mov", ".mp4", ".mpg", ".mpeg", ".rm", ".swf", ".vob", ".wmv")

# LOAD IN CONFIGURATIONS
with open("configs.yaml", 'r') as stream:
	try:
		configs = yaml.safe_load(stream)
	except yaml.YAMLError as exc:
		print(exc)

videos = [file for file in os.listdir(configs['videos_dir']) if file.endswith(ext)] 
pbar = tqdm(videos)
for video in pbar:
	frames = extract_imgs_from_sframe(
		os.path.join(configs['videos_dir'], video), 
		target_label=configs['target_label'],
		buffer=configs['buffer'],
		draw_center=configs['draw_centers'],
		draw_center_line=configs['draw_contrail'],
		draw_boundings=configs['draw_boundings'], 
		draw_masks=configs['draw_masks'],
		draw_frame_num=configs['draw_frame_num'], 
		annotations_col=configs['annotations_col'], 
		image_col=configs['image_col'], 
		masks_col=configs['masks_col'])

	# Write to disk
	compile_video(frames, target=os.path.join(configs['target_dir'], video.split('.')[-2] + '.mp4'), fps=configs['fps'])
