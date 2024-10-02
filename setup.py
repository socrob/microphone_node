#!/usr/bin/env python

from distutils.core import setup
from catkin_pkg.python_setup import generate_distutils_setup

# for your packages to be recognized by python
d = generate_distutils_setup(
 packages=['microphone_node', 'microphone_node_ros'],
 package_dir={'microphone_node_ros': 'src/microphone_node_ros'}
)

setup(**d)
