import wave
import struct

def extract_experiment(filename, prefix):
    with open(filename, 'rb') as f:
        data = f.read()[0::2] # Left channel

    chunk = data[2048:] # Skip pilot
    
    # 1. Linear 8-bit signed
    decoded_linear = [b - 128 for b in chunk]
    
    # 2. Inverted bits
    decoded_inverted = [~b & 0xFF for b in chunk]
    decoded_inverted = [b - 128 for b in decoded_inverted]

    rates = [8000, 11025, 23437]
    
    for rate in rates:
        # Linear
        with wave.open(f"{prefix}_linear_{rate}.wav", 'wb') as wf:
            wf.setnchannels(1)
            wf.setsampwidth(1)
            wf.setframerate(rate)
            wf.writeframes(bytes([min(max(x + 128, 0), 255) for x in decoded_linear]))
            
        # Inverted
        with wave.open(f"{prefix}_inverted_{rate}.wav", 'wb') as wf:
            wf.setnchannels(1)
            wf.setsampwidth(1)
            wf.setframerate(rate)
            wf.writeframes(bytes([min(max(x + 128, 0), 255) for x in decoded_inverted]))

if __name__ == "__main__":
    extract_experiment('big_file_unique_data.bin', 'big')
