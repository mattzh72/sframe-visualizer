from utils.parse import extract_imgs_from_sframe, compile_video
from config import Configs
import matplotlib.pyplot as plt

import os


frames = extract_imgs_from_sframe(Configs.SFRAME, draw=True)
compile_video(frames, target=os.path.join(Configs.TARGET_DIR, Configs.OUTPUT_NAME))
