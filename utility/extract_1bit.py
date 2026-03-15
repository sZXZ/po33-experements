import wave
import struct

def extract_as_bits(filename, output_name):
    with open(filename, 'rb') as f:
        data = f.read()[0::2] # Left channel

    print(f"--- {filename} as 1-bit ---")
    
    # Simple 1-bit to PCM: mapping 0/1 to -32k/+32k
    # This is basically a square wave representing the bitstream.
    # At 31200 Hz.
    
    samples = []
    for b in data[2048:]:
        # unpack 8 bits (MSB first? LSB first?)
        # Let's try LSB first
        for i in range(8):
            bit = (b >> i) & 1
            samples.append(32000 if bit else -32000)
            
    with wave.open(output_name, 'wb') as wf:
        wf.setnchannels(1)
        wf.setsampwidth(2)
        wf.setframerate(31200) # bit rate
        wf.writeframes(struct.pack(f'<{len(samples)}h', *samples))
    print(f"Extracted {len(samples)} bits to {output_name}")

if __name__ == "__main__":
    extract_as_bits('big_file_unique_data.bin', 'big_1bit.wav')
