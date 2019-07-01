import turicreate as tc
import os
import yaml
from tqdm import tqdm

from tools.utils.parse import extract_imgs_from_sframe, compile_video

def visualize(configs):
	sf_exts = (".sframe")

	sframes = [file for file in os.listdir(configs['input_dir']) if file.endswith(sf_exts)] 
	pbar = tqdm(sframes)
	for sframe in sframes:
		frames = extract_imgs_from_sframe(
			os.path.join(configs['input_dir'], sframe), 
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
		compile_video(frames, target=os.path.join(configs['output_dir'], sframe.split('.')[-2] + '.mp4'), fps=configs['fps'])
