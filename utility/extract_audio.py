import wave
import sys
import os

def extract_audio(filename, output_prefix):
    with open(filename, 'rb') as f:
        data = f.read()[0::2] # Left channel

    # Start after patterns (2048 + 4096 = 6144)
    # Actually, let's just take a large chunk
    raw_audio = data[6144:]
    
    # Try different sample rates and encodings
    for rate in [8000, 11025, 16000, 23437]:
        out_name = f"{output_prefix}_{rate}.wav"
        with wave.open(out_name, 'wb') as wf:
            wf.setnchannels(1)
            wf.setsampwidth(1) # 8-bit
            wf.setframerate(rate)
            wf.writeframes(raw_audio)
        print(f"Created {out_name}")

if __name__ == "__main__":
    extract_audio('big_file_unique_data.bin', 'big')
    extract_audio('small_file_repeating_data.bin', 'small')
