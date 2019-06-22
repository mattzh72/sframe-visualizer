from utils.parse import read_sframe, compile_video
from config import Configs

frames = read_sframe(Configs.SFRAME, draw=True)
compile_video(frames)