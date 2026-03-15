import os

def find_patterns(bin_path, section_end=4096):
    with open(bin_path, 'rb') as f:
        data = f.read(section_end)

    print(f"Analyzing first {section_end} bytes for structure...")
    
    # Try different pattern lengths
    for length in [64, 128, 256]:
        print(f"\nStride {length}:")
        n = len(data) // length
        seen = []
        mapping = []
        for i in range(n):
            block = data[i*length : (i+1)*length]
            if block not in seen:
                seen.append(block)
            mapping.append(seen.index(block))
        print(" ".join(f"{m:2}" for m in mapping))

if __name__ == "__main__":
    import sys
    find_patterns(sys.argv[1] if len(sys.argv) > 1 else 'my_data_v3_small.bin')
