import sys
from collections import Counter

def find_pattern_block(filename):
    with open(filename, 'rb') as f:
        data = f.read()[0::2] # Left channel

    print(f"--- {filename} ---")
    
    max_repeats = -1
    best_off = -1
    best_filler = None
    
    # 4-byte aligned scan
    for offset in range(0, len(data) - 4096, 256): # Step by one pattern to be faster
        steps = []
        for j in range(0, 4096, 4):
            steps.append(data[offset + j : offset + j + 4])
        
        counts = Counter(steps)
        if not counts: continue
        filler, count = counts.most_common(1)[0]
        
        if count > max_repeats:
            max_repeats = count
            best_off = offset
            best_filler = filler

    print(f"Best pattern block at offset {best_off} (0x{best_off:x})")
    print(f"Most common step occurred {max_repeats} / 1024 times. Step: {best_filler.hex()}")

if __name__ == "__main__":
    find_pattern_block('big_file_unique_data.bin')
    find_pattern_block('small_file_repeating_data.bin')
