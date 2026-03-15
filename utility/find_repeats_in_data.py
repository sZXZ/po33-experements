import sys

def find_exact_repeats_in_data(filename):
    with open(filename, 'rb') as f:
        data = f.read()[0::2] # Left channel

    # Only look in the diverse area (after index 2000)
    data = data[2000:]
    
    print(f"--- {filename} ---")
    counts = {}
    for i in range(len(data) - 256):
        block = data[i : i + 256]
        counts[block] = counts.get(block, []) + [i + 2000]

    repeats = {b: offsets for b, offsets in counts.items() if len(offsets) > 1}
    
    if not repeats:
        print("No exact repeating 256-byte blocks in data area.")
        return

    # Filter out blocks that are just constant bytes
    interesting_repeats = []
    for block, offsets in repeats.items():
        if len(set(block)) > 10:
            interesting_repeats.append((block, offsets))
            
    if not interesting_repeats:
        print("No interesting repeating blocks found.")
        return

    sorted_repeats = sorted(interesting_repeats, key=lambda x: len(x[1]), reverse=True)
    for block, offsets in sorted_repeats[:10]:
        print(f"Block repeats {len(offsets)} times. Offsets: {[hex(o) for o in offsets]}")

if __name__ == "__main__":
    find_exact_repeats_in_data('small_file_repeating_data.bin')
