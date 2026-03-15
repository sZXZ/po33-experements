import sys

def find_complex_repeats(filename):
    with open(filename, 'rb') as f:
        data = f.read()[0::2] # Left channel

    print(f"--- {filename} ---")
    counts = {}
    for i in range(0, len(data) - 256, 16):
        block = data[i : i + 256]
        if len(set(block)) > 40: # High entropy block
            counts[block] = counts.get(block, []) + [i]

    repeats = {b: offsets for b, offsets in counts.items() if len(offsets) > 1}
    
    if not repeats:
        print("No complex repeating blocks found.")
        return

    sorted_repeats = sorted(repeats.items(), key=lambda x: len(x[1]), reverse=True)
    for block, offsets in sorted_repeats[:5]:
        print(f"Block repeats {len(offsets)} times. Offsets: {[hex(o) for o in offsets]}")

if __name__ == "__main__":
    find_complex_repeats('small_file_repeating_data.bin')
