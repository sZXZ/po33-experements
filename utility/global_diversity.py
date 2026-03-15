import sys
from collections import Counter

def global_step_diversity(filename):
    with open(filename, 'rb') as f:
        data = f.read()[0::2] # Left channel

    # Skip pilot
    data = data[2182:]
    
    steps = []
    for i in range(0, len(data) - 16, 16):
        steps.append(data[i : i+16])
        
    counts = Counter(steps)
    print(f"--- {filename} ---")
    print(f"Total steps: {len(steps)}")
    print(f"Unique steps: {len(counts)}")
    
    for step, count in counts.most_common(5):
        if count > 10:
            print(f"Step {step.hex()} occurs {count} times")

if __name__ == "__main__":
    global_step_diversity('small_file_repeating_data.bin')
    global_step_diversity('big_file_unique_data.bin')
