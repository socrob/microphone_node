import pyaudio

def get_supported_sample_rates(device_index):
    paudio = pyaudio.PyAudio()
    device_info = paudio.get_device_info_by_index(device_index)
    supported_sample_rates = []

    print(device_info)

    for rate in [8000, 16000, 32000, 44100, 48000]:
        try:
            stream = paudio.open(rate=rate, channels=1, format=pyaudio.paFloat32,
                                 input=True, frames_per_buffer=1024,
                                 input_device_index=device_index)
            stream.close()
            supported_sample_rates.append(rate)
        except Exception as e:
            pass

    return supported_sample_rates

# Example usage
device_index = 17  # Replace with the desired device index
supported_sample_rates = get_supported_sample_rates(device_index)
print(f"Supported sample rates for device {device_index}: {supported_sample_rates}")

