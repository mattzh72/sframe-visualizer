class Configs:
	# Model Testing 
	TEST_MODEL = True
	VIDEO_PATH = './test.mov'
	MODEL_PATH = './sample.model'
	MAX_NUM_OBJECTS = 2

	# Input/Output Configurations
	TARGET_DIR = './'
	OUTPUT_NAME = 'result.mp4'
	SFRAME = './sample.sframe'


	# SFrame Column Configurations
	ANNOTATIONS_COL = 'annotations'
	IMAGE_COL = 'image'
	MASKS_COL = 'stateMasks'

	# Video Options Configurations
	TARGET_LABEL = 'mainPlate'
	DRAW_BOUNDINGS = False
	DRAW_MASKS = False
	DRAW_CENTERS = False
	DRAW_CENTER_LINES = False
	DRAW_FRAME_NUM = True
	FPS = 30
	BUFFER = 64
