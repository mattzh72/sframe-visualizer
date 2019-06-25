# SFrame-Visualizer

![Build Status](https://travis-ci.org/joemccann/dillinger.svg?branch=master)

SFrame-Visualizer is a video analysis tool written in 100%  Python to visualize SFrames for data analytics.

This package has the following dependencies: **OpenCV 4.1.0**, **Numpy 1.16.2**, **tqdm 4.28.1** and **Turicreate 5.6**.


## Preparing an SFrame 

This tool expects an SFrame in a standard Turicreate format. At the minimum, the SFrame needs two columns: 

 - An **image** column. This contains `turicreate.Image` objects that represent an image. 
> Helpful tip: If you want to do your own hacking, you can extract the image in a numpy format by using the `.pixel_data` attribute on an turicreate Image object. This numpy format is how OpenCV and other libraries represent images.
 - An **annotations** column. This will contain a list of annotations, which Turicreate expects as a dictionary in this format (confidence is optional): `{'confidence':..,
  'coordinates': {'height':...,
                  'width':...,
                  'x':...,
                  'y':...},
  'label':...,
  'type':....}`.

Optionally, you can also have a third column which represents **masks**. Currently, this only support masks outputted by SiamMask. Go [here]([https://github.com/foolwood/SiamMask](https://github.com/foolwood/SiamMask)) for more details.

## Getting Started

Download the repo.

```bash 
git clone https://github.com/vitae-gravitas/sframe-visualizer.git
```

Configure the `config.py` file. There are lots of ways to customize this.

| Configuration     | Purpose           
| -------------    |:-------------:| 
| TARGET_DIR       | The directory to write the output to. | 
| OUTPUT_NAME      | The name of the output MP4 file.    |  
| SFRAME | The path of the SFrame to visualize. |  
| DRAW_BOUNDINGS |If true, draws bounding boxes.|  
| DRAW_MASKS |If true, draws masks. Make sure to enable this only if you have an SFrame with mask data.|  
| FPS |Frames per second of the output video.|  
| ANNOTATIONS_COL |Name of the annotations column in the SFrame.|  
| IMAGE_COL |Name of the image column in the SFrame.|  
| MASKS_COL |Name of the masks column in the SFrame.|  

After configuration, simply run `main.py`.
```bash
python main.py
```
