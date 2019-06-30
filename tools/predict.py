import turicreate as tc
import os
import yaml

from utils.parse import extract_imgs_from_sframe, compile_video, predict_on_video 

def predict(configs):
	vid_exts = (".3g2", ".3gp", ".asf", ".asx", ".avi", ".flv", ".m2ts", ".mkv", ".mov", ".mp4", ".mpg", ".mpeg", ".rm", ".swf", ".vob", ".wmv")

	videos = [file for file in os.listdir(configs['videos_dir']) if file.endswith(vid_exts)] 
	pbar = tqdm(videos)
	for video in pbar:
		frames = predict_on_video(
			configs['videos_dir'], 
			configs['model_path'], 
			target_label=configs['target_label'], 
			draw_masks=configs['draw_masks'],
			num_objs=configs['max_num_objects'], 
			draw_frame_num=configs['draw_frame_num'])

		# Write to disk
		compile_video(frames, target=os.path.join(configs['target_dir'], video.split('.')[-2] + '.sframe'), fps=configs['fps'])