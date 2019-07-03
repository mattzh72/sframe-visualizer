import turicreate as tc
import os
from tqdm import tqdm

from tools.utils.parse import extract_imgs_from_sframe, compile_video, predict_on_video 

def predict(configs):
	vid_exts = (".3g2", ".3gp", ".asf", ".asx", ".avi", ".flv", ".m2ts", ".mkv", ".mov", ".mp4", ".mpg", ".mpeg", ".rm", ".swf", ".vob", ".wmv")
	model_exts = (".model")

	videos = [file for file in os.listdir(configs['input_dir']) if file.endswith(vid_exts)] 
	print("{0} videos found.".format(len(videos)))
	models = [file for file in os.listdir(configs['input_dir']) if file.endswith(model_exts)]
	print("{0} models found.".format(len(models)))

	file_name_template = "{0}_{1}.mp4"
	for i, video in enumerate(videos):
		video_name = video.split('.')[-2]
		for j, model in enumerate(models):
			print("{0}/{1} video; {2}/{3} model".format(i, len(videos), j, len(models)))
			model_name = model.split('.')[-2]

			frames = predict_on_video(
				os.path.join(configs['input_dir'], video), 
				os.path.join(configs['input_dir'], model), 
				target_label=configs['target_label'], 
				confidence_threshold=configs['confidence_threshold'],
				iou_threshold=configs['iou_threshold'],
				num_objs=configs['max_num_objects'],
				draw_masks=configs['draw_masks'],
				draw_frame_num=configs['draw_frame_num'])

			# Write to disk
			compile_video(frames, target=os.path.join(configs['output_dir'], file_name_template.format(video_name, model_name)), fps=configs['fps'])
