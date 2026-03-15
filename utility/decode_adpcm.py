import wave
import struct
import sys

# IMA ADPCM step table
STEP_TABLE = [
    7, 8, 9, 10, 11, 12, 13, 14, 16, 17, 19, 21, 23, 25, 28, 31, 34, 37, 41, 45,
    50, 55, 60, 66, 73, 80, 88, 97, 107, 118, 130, 143, 157, 173, 190, 209, 230,
    253, 279, 307, 337, 371, 408, 449, 494, 544, 598, 658, 724, 796, 876, 963,
    1060, 1166, 1282, 1411, 1552, 1707, 1878, 2066, 2272, 2499, 2749, 3024, 3327,
    3660, 4026, 4428, 4871, 5358, 5894, 6484, 7132, 7845, 8630, 9493, 10442,
    11487, 12635, 13899, 15289, 16818, 18500, 20350, 22385, 24623, 27086, 29794,
    32767
]

# IMA ADPCM index table
INDEX_TABLE = [-1, -1, -1, -1, 2, 4, 6, 8, -1, -1, -1, -1, 2, 4, 6, 8]

class ImaAdpcmDecoder:
    def __init__(self):
        self.predictor = 0
        self.index = 0

    def decode_sample(self, nibble):
        step = STEP_TABLE[self.index]
        
        # Calculate difference
        diff = step >> 3
        if nibble & 0x04: diff += step
        if nibble & 0x02: diff += step >> 1
        if nibble & 0x01: diff += step >> 2
        
        if nibble & 0x08:
            self.predictor -= diff
        else:
            self.predictor += diff
            
        # Clamp predictor
        if self.predictor > 32767: self.predictor = 32767
        elif self.predictor < -32768: self.predictor = -32768
        
        # Update index
        self.index += INDEX_TABLE[nibble & 0x0F]
        if self.index < 0: self.index = 0
        elif self.index > 88: self.index = 88
        
        return self.predictor

def decode_file(filename, output_name, offset=6144, rate=16000):
    with open(filename, 'rb') as f:
        data = f.read()[0::2] # Left channel

    packed = data[offset:]
    decoder = ImaAdpcmDecoder()
    samples = []
    
    for b in packed:
        # Lower nibble first or upper? Usually lower first in Intel IMA ADPCM
        samples.append(decoder.decode_sample(b & 0x0F))
        samples.append(decoder.decode_sample((b >> 4) & 0x0F))
        
    with wave.open(output_name, 'wb') as wf:
        wf.setnchannels(1)
        wf.setsampwidth(2)
        wf.setframerate(rate)
        wf.writeframes(struct.pack(f'<{len(samples)}h', *samples))
    print(f"Decoded {len(samples)} samples to {output_name}")

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python3 decode_adpcm.py <input.bin> <output.wav> [offset] [rate]")
        sys.exit(1)
    
    inf = sys.argv[1]
    outf = sys.argv[2]
    off = int(sys.argv[3]) if len(sys.argv) > 3 else 6144
    r = int(sys.argv[4]) if len(sys.argv) > 4 else 16000
    
    decode_file(inf, outf, off, r)
