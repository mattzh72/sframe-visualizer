import argparse
import yaml

import tools

parser = argparse.ArgumentParser()
parser.add_argument('-f', action='store_true')
parser.add_argument('-m', action='store_true')
parser.add_argument('-s', action='store_true')
args = parser.parse_args()

if args.f:
	config_path = "./configs/visualize.yaml"
	func = tools.visualize
elif args.m:
	config_path = "./configs/predict.yaml"
	func = tools.predict
elif args.s:
	config_path = "./configs/slice.yaml"
	func = tools.slice_vids
else:
	raise ValueError('Did not set flag: -f, -m, -s')

with open(config_path, 'r') as stream:
	try:
		configs = yaml.safe_load(stream)
	except yaml.YAMLError as exc:
		print(exc)

func(configs)

