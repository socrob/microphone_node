# Microphone Node

## Overview

The Microphone Node package is responsible for capturing audio data from a microphone and publishing it to a ROS topic. This package is designed to work seamlessly with other speech processing nodes in the TIAGo robot's speech recognition pipeline.

## Features
- **Audio Capture**: Captures audio data from a specified microphone device.
- **ROS Integration**: Publishes audio data to a ROS topic for use by other nodes.

## Requirements

- ROS version: Noetic
- Dependencies:
    - [audio_common](https://wiki.ros.org/audio_common)

## Installation

### 0. Install the audio_common package

```bash
sudo apt-get install ros-noetic-audio-common
```

### 1. Clone the repository
```bash
cd ~/<your_workspace>/src
git clone https://github.com/certafonso/microphone_node.git
```

### 2. Install dependencies

Navigate to the cloned repository and install the required dependencies:

```bash
cd microphone_node
pip install -r requirements.txt
```

### 3. Build the workspace
Navigate to your catkin workspace and build the package:

```bash
cd ~/<your_workspace>
catkin build
```

### 4. Source the setup file
After building, source the workspace to update the environment:

```bash
source ~/<your_workspace>/devel/setup.bash
```

## Usage

### Launching the Node

To launch the microphone node, use the following command:

```bash
roslaunch microphone_node microphone_node.launch
```

#### Launch File Arguments

The launch file `microphone_node.launch` accepts several arguments to customize the behavior of the microphone node:

- `microphone_device`: Specifies the microphone device to be used. Default is `"default"` which will use the default microphone of the computer.
