# Pose Identification for Sport Activities (Work in Progress)

The main goal of this project is to identify different poses a body makes while exercising with the use of camera or pre-recorded videos.
The equipment you need is just a camera(live feed or video) and laptop.


## Index
1. [Introduction](#Introduction)
2. [Setup](#Setup)
    * [Install pip packages](#1.-Installing-pip-packages)
3. [Usage](#Usage)
4. [Repository structure](#Repository-structure)


## Introduction
This project relies on the Body Keypoints detection model YOLOv8-pose.

It is a GPU compatible, fast and better keypoint detection model compared to Mediapipe.

![image](https://raw.githubusercontent.com/ultralytics/assets/main/yolov8/banner-yolov8.png)



![image](https://user-images.githubusercontent.com/26833433/239691398-d62692dc-713e-4207-9908-2f6710050e5c.jpg)

## Setup
I would recommend to use a virtual python environment for this project. 

### 1. Installing pip packages
First, we need to install python dependencies(list below). Make sure you that you are using `python3.6` or above.

List of packages
```sh
argparse>=1.1
ConfigArgParse>=1.2.3
ultralytics>=8.0.136
numpy>=1.21.5
opencv-python>=4.6.0.66
Pillow>=9.0.1
```

You can individually install the libraries or use the procedure below to install them.

To clone the repository and install dependent libraries:
```sh
git clone https://github.com/shubhendu-ranadive/fit-form.git
cd fit-form
pip install -r requirements.txt
```


## Usage
Run the following command to start the keypoint detection tester:

```sh
python pose_detect.py
```

Run the following command to start the exercise identification (currently Pushup, Squat and Arm-curl):

```sh
python spose_main.py
```

## Repository structure
<pre>
│  pose_detect.py
│  poses.txt
│  spose_main.py
│  requirements.txt
├─ data
│  └─ fonts
│     ├─ arial.ttf
│     └─ TangoSans.ttf
├─ utils
│   ├─ pose_utils
│   │   ├─ pose.py
│   │   └─ const.py
│   ├─ drawing_utils.py
│   ├─ exercise_utils.py
│   ├─ operation_utils.py
│   └─ video_reader_utils.py
</pre>

# TODO
- [ ] Pose identification functionality
- [ ] Web UI for mobile on-device 

# Reference
* [YOLOv8-Pose](https://github.com/ultralytics/ultralytics/issues/1915)
