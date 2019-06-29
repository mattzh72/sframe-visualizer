from utils.parse import extract_imgs_from_sframe, compile_video, predict_on_video
from config import Configs

import os
import turicreate as tc

if Configs.TEST_MODEL:
	frames = predict_on_video(
		Configs.VIDEO_PATH, 
		Configs.MODEL_PATH, 
		target_label=Configs.TARGET_LABEL, 
		draw_masks=Configs.DRAW_MASKS,
		num_objs=Configs.MAX_NUM_OBJECTS, 
		draw_frame_num=Configs.DRAW_FRAME_NUM)
else:
	frames = extract_imgs_from_sframe(
		Configs.SFRAME, 
		target_label=Configs.TARGET_LABEL,
		buffer=Configs.BUFFER,
		draw_center=Configs.DRAW_CENTERS,
		draw_center_line=Configs.DRAW_CENTER_LINES,
		draw_boundings=Configs.DRAW_BOUNDINGS, 
		draw_masks=Configs.DRAW_MASKS,
		draw_frame_num=Configs.DRAW_FRAME_NUM, 
		annotations_col=Configs.ANNOTATIONS_COL, 
		image_col=Configs.IMAGE_COL, 
		masks_col=Configs.MASKS_COL)

compile_video(frames, target=os.path.join(Configs.TARGET_DIR, Configs.OUTPUT_NAME), fps=Configs.FPS)
