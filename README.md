# ROS2 Bag to Video Converter

This script converts video data from ROS2 bag files containing image messages into a video file. It supports both uncompressed (`sensor_msgs/Image`) and compressed (`sensor_msgs/CompressedImage`) image messages using `rosbags` and `rosbags_image`.

## Overview

This Python script extracts video frames from ROS2 bag files, specifically from messages of type `sensor_msgs/Image` or `sensor_msgs/CompressedImage`, and compiles them into an MP4 video file. The script is designed for developers and roboticists working with ROS 2 who need to extract video data from bag files.

## Features

- Extracts video frames from specified ROS2 bag file and topic.
- Compiles the video frames into an MP4 video file.
- Saves the first image as an optional thumbnail separate file for debugging or reference purposes.
- Automatically estimates the frame rate from the timestamps in the ROS bag file.
- Adjustable video frame dimensions.
- Supports both uncompressed and compressed image messages.

## Requirements

- Python 3
- ROS2 (Robot Operating System) - actually, not mandatory at all
- The excellent `rosbags` and `rosbags_image` Python packages
- `opencv-python` Python package

### Install dependencies:

```bash
pip install rosbags rosbags-image opencv-python
```

## Usage

To run the script:

```bash
python rosbag_to_video.py -source <bag_file_path> -topic <video_topic_name> -output <output_video_file_path> [-thumbnail <thumbnail_file_path>]
```

### Example:

```bash
python rosbag_to_video.py -source /path/to/rosbag/ -topic /camera/image_raw -output /path/to/output_video.mp4
```

### Optional Parameters:

- `-thumbnail <thumbnail_file_path>`: Saves the first frame of the video as a separate image (for debugging or reference).
- `-width <video_frame_width>`: Specify the width of the video frames (defaults to the width of the first frame).
- `-height <video_frame_height>`: Specify the height of the video frames (defaults to the height of the first frame).

### Notes:

- The script automatically determines the correct frame rate based on the timestamps in the bag file.
- Both uncompressed (`sensor_msgs/Image`) and compressed (`sensor_msgs/CompressedImage`) image messages are supported.
- Ensure that the topic specified contains image data; otherwise, the script will not extract any frames.