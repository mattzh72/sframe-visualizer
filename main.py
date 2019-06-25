from utils.parse import extract_imgs_from_sframe, compile_video
from config import Configs

import os


frames = extract_imgs_from_sframe(
	Configs.SFRAME, 
	draw_boundings=Configs.DRAW_BOUNDINGS, 
	draw_masks=Configs.DRAW_MASKS,
	annotations_col=Configs.ANNOTATIONS_COL, 
	image_col=Configs.IMAGE_COL, 
	masks_col=Configs.MASKS_COL)

compile_video(frames, target=os.path.join(Configs.TARGET_DIR, Configs.OUTPUT_NAME), fps=Configs.FPS)
