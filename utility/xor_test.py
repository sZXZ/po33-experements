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

def xor_lag_test(filename):
    with open(filename, 'rb') as f:
        data = f.read()[0::2] # Left channel

    data = data[2048:2048+10000] # Use a representative chunk
    
    print(f"--- {filename} ---")
    base_entropy = calc_entropy(data)
    print(f"Base entropy: {base_entropy:.4f}")
    
    best_lag = -1
    min_ent = base_entropy
    
    for lag in range(1, 1024):
        xored = bytes(a ^ b for a, b in zip(data, data[lag:]))
        ent = calc_entropy(xored)
        if ent < min_ent:
            min_ent = ent
            best_lag = lag
            
    if best_lag != -1 and min_ent < base_entropy - 0.5:
        print(f"Significant periodic XOR detected! Lag: {best_lag}, Entropy dropped to {min_ent:.4f}")
    else:
        print("No simple periodic XOR structure found.")

if __name__ == "__main__":
    xor_lag_test('big_file_unique_data.bin')
    xor_lag_test('small_file_repeating_data.bin')
