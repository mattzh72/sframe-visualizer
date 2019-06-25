# SFrame-Visualizer

![Build Status](https://travis-ci.org/joemccann/dillinger.svg?branch=master)

SFrame-Visualizer is a video analysis tool written in 100%  Python to visualize SFrames for data analytics.

This package has the following dependencies: **OpenCV 4.1.0**, **Numpy 1.16.2**, **tqdm 4.28.1** and **Turicreate 5.6**.


## Preparing an SFrame 

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
A sample visualization with bounding boxes and masks drawn.
> ![Demo GIF](https://github.com/vitae-gravitas/sframe-visualizer/blob/master/README/demo.gif)

