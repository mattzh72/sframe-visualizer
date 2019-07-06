import argparse
import yaml

import tools

parser = argparse.ArgumentParser()
parser.add_argument('-visualize', action='store_true')
parser.add_argument('-predict', action='store_true')
parser.add_argument('-slice', action='store_true')
parser.add_argument('-evaluate', action='store_true')
args = parser.parse_args()

with open('./configs.yaml', 'r') as stream:
	try:
		configs = yaml.safe_load(stream)
	except yaml.YAMLError as exc:
		print(exc)

if args.visualize:
	tools.visualize(configs)
elif args.predict:
	tools.predict(configs)
elif args.slice:
	tools.slice_vids(configs)
elif args.evaluate:
	tools.evaluate(configs)
else:
	raise ValueError('Did not set flag: -v, -p, -s')




