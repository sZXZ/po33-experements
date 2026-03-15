import sys
from collections import Counter

def find_common_step(filename):
    with open(filename, 'rb') as f:
        data = f.read()[0::2] # Left channel

    diverse_start = 2048
    payload = data[diverse_start : diverse_start + 16384] # Check first 16KB
    
    steps = []
    for i in range(0, len(payload) - 4, 4):
        steps.append(payload[i : i+4])
        
    counts = Counter(steps)
    print(f"--- {filename} ---")
    for step, count in counts.most_common(5):
        print(f"Step {step.hex()} occurs {count} times")

if __name__ == "__main__":
    find_common_step('big_file_unique_data.bin')
    find_common_step('small_file_repeating_data.bin')
