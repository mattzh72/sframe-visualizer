import turicreate as tc
import os
from tqdm import tqdm
import yaml

from tools.utils.metrics import *

def evaluate(configs):
	sframe_exts = (".sframe")
	model_exts = (".model")

	sframes = [file for file in os.listdir(configs['input_dir']) if file.endswith(sframe_exts)] 
	models = [file for file in os.listdir(configs['input_dir']) if file.endswith(model_exts)]

	pbar = tqdm(sframes)
	scores = {}
	for sframe_path in pbar:
		# Initialize scores dictionary
		scores[sframe_path] = []

		# Load in Sframe
		sf = tc.load_sframe(os.path.join(configs['input_dir'], sframe_path))

		for model_path in models:
			# Update progress bar description
			pbar.set_description("{0}: {1}".format(sframe_path, model_path))
			
			# Load in model and evaulate
			model = tc.load_model(os.path.join(configs['input_dir'], model_path))

			if configs['metric'].upper() == 'MAP':
				results = evaluate_mAP(model, sf, 
					target_label=configs['target_label'],
					confidence_threshold=configs['confidence_threshold'], 
					iou_threshold=configs['iou_threshold'])
			elif configs['metric'].upper() == 'RSME':
				results = evaluate_center_RSME(model, sf,
					confidence_threshold=configs['confidence_threshold'], 
					iou_threshold=configs['iou_threshold'], 
					image_col=configs['image_col'], 
					annotations_col=configs['annotations_col'])
			else:
				results = evaluate_center_MAE(model, sf,
					confidence_threshold=configs['confidence_threshold'], 
					iou_threshold=configs['iou_threshold'], 
					image_col=configs['image_col'], 
					annotations_col=configs['annotations_col'])

			scores[sframe_path].append({'model':model_path, 'scores': results})

		scores[sframe_path] = sorted(scores[sframe_path], key=lambda x: x['scores'])

	pbar.close()

	with open(os.path.join(configs['output_dir'], 'scores_{0}.yaml'.format(configs['metric'])), 'w') as file:
		file.write(yaml.dump(scores))


		



