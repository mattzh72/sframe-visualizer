import turicreate as tc
import os
import yaml

from utils.parse import extract_imgs_from_sframe, compile_video, predict_on_video

# LOAD IN CONFIGURATIONS
configs = None
with open("configs.yaml", 'r') as stream:
    try:
		configs = yaml.safe_load(stream)
    except yaml.YAMLError as exc:
        print(exc)

output_name = configs['videos_dir'].split('.')[-1] + '.mp4'
frames = predict_on_video(
	configs['videos_dir'], 
	configs['model_path'], 
	target_label=configs['target_label'], 
	draw_masks=configs['draw_masks'],
	num_objs=configs['max_num_objects'], 
	draw_frame_num=configs['draw_frame_num'])

# Write to disk
compile_video(frames, target=os.path.join(configs['target_dir'], output_name), fps=configs['fps'])