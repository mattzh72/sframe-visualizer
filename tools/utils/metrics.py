import turicreate as tc
import numpy as np

def evaluate_mAP(model, sf, target_label=None, confidence_threshold=0.75, iou_threshold=0.25):
	results = model.evaluate(sf, metric='all', confidence_threshold=confidence_threshold, iou_threshold=iou_threshold)
	if target_label: 
		return float(results['average_precision_50'][target_label])
	else:
		return results['mean_average_precision_50'].item()

def evaluate_center_RSME(model, sf, confidence_threshold=0.5, iou_threshold=0.25, image_col='image', annotations_col='annotations'):
	results = model.predict(sf, confidence_threshold=confidence_threshold, iou_threshold=iou_threshold)
	ground = sf[annotations_col]

	predictions = []
	targets = []
	for r, g in zip(results, ground):
		r = clean_predictions(r)
		g, r = g[:len(r)], r[:len(g)]

		predictions.extend([[x['coordinates']['x'], x['coordinates']['y']] for x in r])
		targets.extend([[x['coordinates']['x'], x['coordinates']['y']] for x in g])

	return float(np.sqrt(np.mean((np.array(predictions)-np.array(targets))**2)))

def evaluate_center_MAE(model, sf, confidence_threshold=0.5, iou_threshold=0.25, image_col='image', annotations_col='annotations'):
	results = model.predict(sf, confidence_threshold=confidence_threshold, iou_threshold=iou_threshold)
	ground = sf[annotations_col]

	predictions = []
	targets = []
	for r, g in zip(results, ground):
		r = clean_predictions(r)
		g, r = g[:len(r)], r[:len(g)]

		predictions.extend([[x['coordinates']['x'], x['coordinates']['y']] for x in r])
		targets.extend([[x['coordinates']['x'], x['coordinates']['y']] for x in g])

	return float(np.mean(np.absolute((np.array(predictions)-np.array(targets)))))

def clean_predictions(pred, target_label=None):
	if target_label:
		pred = [p for p in pred if p['label'] == target_label]

	return pred



