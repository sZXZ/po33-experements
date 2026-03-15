import os

def find_fixed_block_repetition(bin_path, stride=256):
    with open(bin_path, 'rb') as f:
        data = f.read()
        
    print(f"Analyzing {bin_path} with stride {stride}...")
    
    n_blocks = len(data) // stride
    unique_blocks = []
    block_map = []
    
    for i in range(n_blocks):
        block = data[i*stride : (i+1)*stride]
        if block not in unique_blocks:
            unique_blocks.append(block)
        block_map.append(unique_blocks.index(block))
        
    print(f"Found {len(unique_blocks)} unique blocks out of {n_blocks} total.")
    
    # Print the sequence of block IDs
    for i in range(0, len(block_map), 16):
        line = block_map[i : i+16]
        print(f"0x{i*stride:05x}: " + " ".join(f"{b:3}" for b in line))

if __name__ == "__main__":
    import sys
    path = sys.argv[1] if len(sys.argv) > 1 else 'my_data_v3_small.bin'
    find_fixed_block_repetition(path, 256)
