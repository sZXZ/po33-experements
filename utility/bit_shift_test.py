import sys
import math
from collections import Counter

def calc_entropy(data):
    if not data: return 0
    counts = Counter(data)
    ent = 0
    for c in counts.values():
        p = c / len(data)
        ent -= p * math.log2(p)
    return ent

def bit_shift_test(filename):
    with open(filename, 'rb') as f:
        data = f.read()[0::2] # Left channel

    # Convert to bit string
    bit_str = "".join(bin(b)[2:].zfill(8) for b in data[2048:4048])
    
    print(f"--- {filename} Bit Shift Test ---")
    
    for shift in range(8):
        shifted_bits = bit_str[shift:]
        # Convert back to bytes
        new_bytes = []
        for i in range(0, len(shifted_bits) - 7, 8):
            new_bytes.append(int(shifted_bits[i:i+8], 2))
        
        ent = calc_entropy(new_bytes)
        print(f"Shift {shift}: Entropy {ent:.4f}")

if __name__ == "__main__":
    bit_shift_test('big_file_unique_data.bin')
