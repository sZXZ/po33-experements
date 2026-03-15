import os
from collections import Counter

def find_repeating_patterns(bin_path, pattern_len=16):
    with open(bin_path, 'rb') as f:
        data = f.read()

    # Find common N-byte sequences
    sequences = []
    for i in range(len(data) - pattern_len):
        sequences.append(data[i:i+pattern_len])
    
    counts = Counter(sequences)
    
    print(f"Top {pattern_len}-byte repeating sequences:")
    for seq, count in counts.most_common(10):
        if count > 1:
            # Find first occurrence
            first_idx = data.find(seq)
            print(f"Count: {count} | Hex: {seq.hex()} | First at: 0x{first_idx:05x}")

def find_aligned_blocks(bin_path, block_size=1024):
    """Check for similarity between fixed-size blocks."""
    with open(bin_path, 'rb') as f:
        data = f.read()
    
    n_blocks = len(data) // block_size
    print(f"\nComparing {n_blocks} blocks of size {block_size}:")
    
    for b in range(n_blocks - 1):
        block1 = data[b*block_size : (b+1)*block_size]
        block2 = data[(b+1)*block_size : (b+2)*block_size]
        
        # Calculate similarity (byte matches)
        matches = sum(1 for x, y in zip(block1, block2) if x == y)
        if matches > block_size * 0.1: # 10% similarity
            print(f"Block {b} & {b+1} similarity: {matches/block_size:.1%}")

if __name__ == "__main__":
    import sys
    path = sys.argv[1] if len(sys.argv) > 1 else 'my_data_v3_small.bin'
    find_repeating_patterns(path, 8)
    find_repeating_patterns(path, 16)
    find_aligned_blocks(path, 512)
