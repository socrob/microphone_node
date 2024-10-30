#!/usr/bin/env python3
#check https://pypi.org/project/SpeechRecognition/

import rospy

#Import service messages and data types
from std_msgs.msg import String
from audio_common_msgs.msg import AudioData, AudioInfo
from threading import Lock

# ros independent imports
from .utils import open_audio_stream

DEBUG = False

class Mbot_ASR(object):
    def __init__(self):
        if not DEBUG:
            rospy.init_node('microphone_node')
        else:
            rospy.init_node('microphone_node', log_level=rospy.DEBUG)

        if rospy.has_param("~microphone_device"):
            self.microphone_in_use = rospy.get_param("~microphone_device")
        else:
            self.microphone_in_use = "respeaker"
            rospy.logwarn(f"Microphone device not set. Using default value of {self.microphone_in_use}")

        rospy.loginfo("Using {} microphone.".format(self.microphone_in_use))
            
        #Publishers
        self.audio_pub = rospy.Publisher("~audio", AudioData, queue_size = 5)
        self.audio_info_pub = rospy.Publisher("~audio_info", AudioInfo, queue_size = 1)

        #Subscriptions
        self.event_sub = rospy.Subscriber('~event_in', String, self.event_in_callback)

        self.rate = rospy.Rate(2)

        self.listening = False

        # Audio recording properties
        self.sample_rate = rospy.get_param("~sample_rate", 16000)
        self.frame_length = rospy.get_param("~frame_length", 512)
        self.audio_stream = None

        self.listening_lock = Lock()

        rospy.set_param("~recording", False)

        rospy.loginfo(f"Microphone interface initialized (sample_rate={self.sample_rate}, frame_length={self.frame_length})")

        self.event_in_callback(String("e_start"))

    def main(self):
        while not rospy.is_shutdown():
            self.listening_lock.acquire()
            if self.listening:
                self.audio_pub.publish(
                    self.audio_stream.read(self.frame_length, exception_on_overflow = False)
                    )
                self.listening_lock.release()

            else:
                self.listening_lock.release()
                self.rate.sleep()
            
    def event_in_callback(self, msg):
        command = msg.data.split("_")
        if command[0] != "e":
            return

        if msg.data == "e_stop" and self.listening:
            rospy.set_param("~microphone_recording", False)

            self.listening = False

            self.listening_lock.acquire()
            self.audio_stream.close()
            self.listening_lock.release()

            rospy.loginfo("Stopped recording")

        elif msg.data == "e_start" and not self.listening:
            # Open audio stream
            self.audio_stream = open_audio_stream(self.microphone_in_use, self.sample_rate, self.frame_length)
                
            self.listening = True

            # Put audio settings in parameter server
            rospy.set_param("~sample_rate", self.sample_rate)
            rospy.set_param("~frame_length", self.frame_length)
            rospy.set_param("~recording", True)

            rospy.loginfo("Started recording")

def main():
    my_obj = Mbot_ASR()
    my_obj.main()
