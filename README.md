# SFrame-Visualizer

![Build Status](https://travis-ci.org/joemccann/dillinger.svg?branch=master)

SFrame-Visualizer is a video analysis tool written in 100%  Python to visualize SFrames for data analytics. It can be used to purely visualize a given SFrame, or can be used to visualize predictions made by `.model` on a target video. It is also capable of drawing **bounding boxes, segmentations, moment centers, and contrail paths**.

This package has the following dependencies: **OpenCV 4.1.0**, **Numpy 1.16.2**, **tqdm 4.28.1** and **Turicreate 5.6**.


## Option 1: Preparing an SFrame for Visualization

This tool expects an SFrame in a standard Turicreate format. At the minimum, the SFrame needs two columns: 

 - An **image** column. This contains `turicreate.Image` objects that represent an image. 
 - An **annotations** column. This will contain a list of annotations, which Turicreate expects as a dictionary (`confidence` is optional).
```python
{'confidence':..,
  'coordinates': {'height':...,
                  'width':...,
                  'x':...,
                  'y':...},
  'label':...,
  'type':...}
```

Optionally, you can also have a third column which represents **masks**. Currently, this only support masks outputted by SiamMask. Go [here](https://github.com/foolwood/SiamMask) for more details.

Here's an example set of configurations:
```python
TARGET_DIR = './'
OUTPUT_NAME = 'result.mp4'
SFRAME = './sample.sframe'
ANNOTATIONS_COL = 'annotations'
IMAGE_COL = 'image'
MASKS_COL = 'stateMasks'
DRAW_BOUNDINGS = False
DRAW_MASKS = False
DRAW_CENTERS = False
DRAW_CENTER_LINES = False
DRAW_FRAME_NUM = True
FPS = 30
BUFFER = 64
```
This will take in input `sample.sframe` in the current working directory, and write the output at 30 frames a second to the current working directory as `result.mp4`. The tool will specifically search for columns named `annotations`, `image`, and `stateMasks` for annotation, image, and mask data respectively. There are no bounding boxes, masks, centers, or length 64 contrails drawn. The frame number will be shown.

## Option 2: Preparing a Turicreate Model for Visualization

This tool expects a model in a standard Turicreate format and a video (in any FOURCC-accpeted format). Simply set the right configurations! Here's an example set of configurations for model testing, where the video is named `test.mov` in the working directory, the model is named `sample.model` in the working directory, and every object predicted with the label `mainPlate` should be drawn.

```python
TEST_MODEL = True
VIDEO_PATH = './test.mov'
MODEL_PATH = './sample.model'
MAX_NUM_OBJECTS = -1
TARGET_LABEL = 'mainPlate'
```

## Getting Started

Download the repo.

```bash 
git clone https://github.com/vitae-gravitas/sframe-visualizer.git
```

Configure the `config.py` file. There are lots of ways to customize this.

| Configuration  | Type    | Purpose    |       
| -------------  |------------- |-------------| 
| `TEST_MODEL`  | `bool` | If true, this will load in the test video and model to visualize the model's predictions. Otherwise, it takes in an existing SFrame.| 
| `VIDEO_PATH`  | `str` | The path of the test video. | 
| `MODEL_PATH`  | `str` | The path of the Turicreate model. **Make sure this has a `.model` extension!** | 
| `MAX_NUM_OBJECTS`   | `int` |The maximum number of objects to draw on the screen. This is done by taking the top two objects with the highest prediction confidence. Set this to a negative number to include all objects.| 
| `TARGET_DIR` | `str` | The output directory. | 
| `OUTPUT_NAME`  | `str` | The name of the output file. **Make sure this has a `.mp4` extension!**    |  
| `SFRAME` | `str` | The path of the input SFrame. |  
| `ANNOTATIONS_COL` | `str`|Name of the annotations column in the SFrame.|  
| `IMAGE_COL`| `str` |Name of the image column in the SFrame.|  
| `MASKS_COL` | `str`|Name of the masks column in the SFrame.|  
| `DRAW_BOUNDINGS`| `bool` |If true, draws bounding boxes.|  
| `DRAW_MASKS` | `bool`|If true, draws masks. **Make sure to enable this only if you have an SFrame with mask data.**|  
| `DRAW_CENTERS`| `bool` |If true, draws the centers of the bounding boxes.| 
| `DRAW_CENTER_LINES` | `bool`|If true, draws a contrail (based on the centers of the bounding boxes).| 
| `DRAW_FRAME_NUM`| `bool` |Draws the frame number on the top left corner of the video.| 
| `FPS`| `int` |Frames per second of the output video.|  
| `BUFFER` | `int`|The length of the contrail (based on the centers of the bounding boxes).|

After configuration, simply run `main.py`.
```bash
python main.py
```

## Demo
Sample visualizations with bounding boxes and/or masks drawn.

SFrame Visualization             |  Model Predictions
:-------------------------:|:-------------------------:
<img src="https://github.com/vitae-gravitas/sframe-visualizer/blob/master/README/visual.gif" width="425"/>  |  <img src="https://github.com/vitae-gravitas/sframe-visualizer/blob/master/README/pred.gif" width="425"/> 

