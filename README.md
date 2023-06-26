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
This project relies on the Body Keypoints detection feature of Mediapipe library.
Mediapipe is an amazing ML platform with many robust solutions like Body Keypoints detections, Hand Keypoints detection and Objectron.

![image](https://user-images.githubusercontent.com/121268647/214214926-4ef30ccd-c857-4496-8668-5192642abb5a.png)



![image](https://user-images.githubusercontent.com/121268647/214214853-064034d9-ec8c-456f-8982-b65451f7e51e.png)

## Setup
I would recommend to use a virtual python environment for this project. 

### 1. Installing pip packages
First, we need to install python dependencies(list below). Make sure you that you are using `python3.6` or above.

List of packages
```sh
argparse>=1.1
ConfigArgParse>=1.2.3
mediapipe>=0.8.10.1
numpy>=1.21.5
opencv-python>=4.6.0.66
Pillow>=9.0.1
```
You can individually install the libraries or use the procedure below to install them.

To clone the repository and install dependent libraries:
```sh
git clone https://github.com/serio-teranishi/image-analysis
cd image-analysis/shubhendu
pip install -r requirements.txt
```


## Usage
Run the following command to start the keypoint detection :

```sh
python pose_detect.py
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
* [MediaPipe](https://github.com/google/mediapipe)
