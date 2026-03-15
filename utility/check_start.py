import sys

def analyze_zones(filename):
    with open(filename, 'rb') as f:
        data = f.read()[0::2] # Left channel

    zones = []
    current_pattern = None
    pattern_start = 0
    
    window_size = 32
    
    for i in range(0, min(len(data) - window_size, 40000), 32):
        b = data[i:i+window_size]
        if b != current_pattern:
            if current_pattern is not None:
                zones.append((pattern_start, i, current_pattern))
            current_pattern = b
            pattern_start = i

    for start, end, pat in zones:
        print(f"[{start} - {end}] (len {end-start})")

if __name__ == "__main__":
    analyze_zones('small_file_repeating_data.bin')
