import pyaudio

def open_audio_stream(microphone_in_use, sample_rate, frame_length):
    paudio = pyaudio.PyAudio()
    info = paudio.get_host_api_info_by_index(0)
    numdevices = info.get('deviceCount')

    respeaker_mic_id = None
    azure_mic_id = None
    rode_mic_id = None
    for i in range(0, numdevices):
        # print("---")
        # print(i, paudio.get_device_info_by_host_api_device_index(0, i).get('name'))
        if (paudio.get_device_info_by_host_api_device_index(0, i).get('maxInputChannels')) > 0:
            if 'ReSpeaker' in paudio.get_device_info_by_host_api_device_index(0, i).get('name'):
                respeaker_mic_id = i

            elif 'Azure' in paudio.get_device_info_by_host_api_device_index(0, i).get('name'):
                azure_mic_id = i

            elif 'USB Audio Device' in paudio.get_device_info_by_host_api_device_index(0, i).get('name'):
                rode_mic_id = i

    # Open audio stream
    if microphone_in_use == "respeaker":
        if respeaker_mic_id == None:
            raise Exception('Cannot find ReSpeaker input channel.')
        
        audio_stream = paudio.open(
            rate=sample_rate,
            channels=1,
            format=pyaudio.paInt16,
            input=True,
            frames_per_buffer=frame_length,
            input_device_index=respeaker_mic_id,
            )
        
    elif microphone_in_use == "azure":
        if azure_mic_id == None:
            raise Exception('Cannot find Azure input channel.')
        
        audio_stream = paudio.open(
            rate=sample_rate,
            channels=1,
            format=pyaudio.paInt16,
            input=True,
            frames_per_buffer=frame_length,
            input_device_index=azure_mic_id,
            )
        
    elif microphone_in_use == "rode":
        if rode_mic_id == None:
            raise Exception('Cannot find Rode input channel.')

        audio_stream = paudio.open(
            rate=sample_rate,
            channels=1,
            format=pyaudio.paInt16,
            input=True,
            frames_per_buffer=frame_length,
            input_device_index=rode_mic_id,
            )
        
    elif microphone_in_use == "default":
        audio_stream = paudio.open(
            rate=sample_rate,
            channels=1,
            format=pyaudio.paInt16,
            input=True,
            frames_per_buffer=frame_length,
            )
        
    else:
        raise Exception(f'{microphone_in_use} is not a valid microphone.')
    
    return audio_stream