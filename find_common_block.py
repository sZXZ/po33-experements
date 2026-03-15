import sys
from collections import Counter

def find_common_block(filename):
    with open(filename, 'rb') as f:
        data = f.read()[0::2] # Left channel

    diverse_start = 2048
    payload = data[diverse_start:]
    
    blocks = []
    for i in range(0, len(payload) - 256, 256):
        blocks.append(payload[i : i+256])
        
    counts = Counter(blocks)
    print(f"--- {filename} ---")
    for block, count in counts.most_common(5):
        print(f"Block occurs {count} times. Unique bytes in block: {len(set(block))}")

if __name__ == "__main__":
    find_common_block('small_file_repeating_data.bin')
    find_common_block('big_file_unique_data.bin')
