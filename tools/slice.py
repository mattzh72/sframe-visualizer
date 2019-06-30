import yaml
import os
import turicreate as tc
from tqdm import tqdm

def slice_vids(configs):
	input_dir = configs[-1]['input']
	output_dir = configs[-1]['output']

	slices = configs[0]
	file_name_template = '{0}_{1}_{2}.sframe'

	sliced_sframes = {}
	for sframe, indices in tqdm(slices.items(), desc='Slicing'):
		name = sframe.split('.')[0]
		master_sframe = tc.load_sframe(os.path.join(input_dir, sframe))

		for idx in indices:
			start = idx[0]
			end = idx[1]

			path = os.path.join(output_dir, file_name_template.format(name, start, end))
			sframes[path] = master_sframe[start:end]

	for path, sf in sliced_sframes.items():
		sf.save(path, sf)






