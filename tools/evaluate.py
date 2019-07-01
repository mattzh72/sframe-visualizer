import turicreate as tc
import os
from tqdm import tqdm
import pickle

def evaluate(configs):
	sframe_exts = (".sframe")
	model_exts = (".model")

	sframes = [file for file in os.listdir(configs['input_dir']) if file.endswith(vid_exts)] 
	models = [file for file in os.listdir(configs['input_dir']) if file.endswith(model_exts)]

	pbar = tqdm(sframes)
	scores = {}
	for sframe in pbar:
		sf_name = sframe.split('.')[-2]
		scores[sf_name] = []
		for model in models:
			model_name = model.split('.')[-2]
			scores = model.evaluate(sframe)
			scores[sf_name].append({'model':model_name, 'scores': scores})

		scores[sf_name] = sorted(scores[sf_name], key=lambda x: x['scores'])

	with open('scores.txt', 'w') as file:
		file.write(pickle.dumps(os.path.join(configs['output_dir'], scores)))



