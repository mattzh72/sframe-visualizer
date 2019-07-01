import turicreate as tc
import os
from tqdm import tqdm
import yaml

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
		sf = tc.load_sframe(os.path.join(configs['input_dir'], sframe_path))[:10]

		for model_path in models:
			# Update progress bar description
			pbar.set_description("{0}: {1}".format(sframe_path, model_path))
			
			# Load in model and evaulate
			model = tc.load_model(os.path.join(configs['input_dir'], model_path))
			results = model.evaluate(sf)

			scores[sframe_path].append({'model':model_path, 'scores': results['mean_average_precision_50'].item()})

		scores[sframe_path] = sorted(scores[sframe_path], key=lambda x: x['scores'])

	pbar.close()

	with open(os.path.join(configs['output_dir'], 'scores.yaml'), 'w') as file:
		file.write(yaml.dump(scores))


		



