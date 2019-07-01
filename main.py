import argparse
import yaml

import tools

parser = argparse.ArgumentParser()
parser.add_argument('-v', action='store_true')
parser.add_argument('-t', action='store_true')
parser.add_argument('-s', action='store_true')
parser.add_argument('-e', action='store_true')
args = parser.parse_args()

with open('./configs.yaml', 'r') as stream:
	try:
		configs = yaml.safe_load(stream)
	except yaml.YAMLError as exc:
		print(exc)

if args.v:
	tools.visualize(configs)
elif args.t:
	tools.predict(configs)
elif args.s:
	tools.slice_vids(configs)
elif args.e:
	tools.evaluate(configs)
else:
	raise ValueError('Did not set flag: -v, -p, -s')




