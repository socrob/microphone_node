import pyaudio
from rospkg import RosPack
import yaml

def open_audio_stream(microphone_in_use, sample_rate, frame_length):
    # Get the list of possible microphones
    config_path = f"{RosPack().get_path('microphone_node')}/config/mic_config.yaml"
    
    with open(config_path, 'r') as f:
        config = yaml.safe_load(f)

    # Initialize PyAudio
    paudio = pyaudio.PyAudio()
    info = paudio.get_host_api_info_by_index(0)
    numdevices = info.get('deviceCount')

    # Find the specified microphone device
    mic_id = None
    mic_name = config.get(microphone_in_use)
    if mic_name is not None:

        # Iterate through all devices and find the one with the specified name
        for i in range(0, numdevices):
            # print("---")
            # print(i, paudio.get_device_info_by_host_api_device_index(0, i).get('name'))

            if (paudio.get_device_info_by_host_api_device_index(0, i).get('maxInputChannels')) > 0:
                if mic_name in paudio.get_device_info_by_host_api_device_index(0, i).get('name'):
                    mic_id= i
                    break

    # Open default microphone
    if microphone_in_use == "default":
        audio_stream = paudio.open(
            rate=sample_rate,
            channels=1,
            format=pyaudio.paInt16,
            input=True,
            frames_per_buffer=frame_length,
            )
        
    # Open audio stream of non default microphone
    else:
        if mic_id == None:
            raise Exception(f"Cannot find {microphone_in_use} input channel.")
        
        audio_stream = paudio.open(
            rate=sample_rate,
            channels=1,
            format=pyaudio.paInt16,
            input=True,
            frames_per_buffer=frame_length,
            input_device_index=mic_id,
            )
    
    return audio_stream