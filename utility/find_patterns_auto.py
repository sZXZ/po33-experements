import sys

def find_patterns_automatically(filename):
    with open(filename, 'rb') as f:
        data = f.read()[0::2] # Left channel

    # Scan for a 4096-byte region that has the most 4-byte 0xAA AA fillers
    # aligned to 4-byte boundaries.
    
    max_aa_count = -1
    best_offset = -1
    
    # The patterns are usually after the header. 
    # Let's scan in 4-byte increments.
    for offset in range(0, len(data) - 4096, 4):
        aa_count = 0
        for j in range(0, 4096, 4):
            if data[offset + j : offset + j + 4] == b'\xaa\xaa\xaa\xaa':
                aa_count += 1
        
        if aa_count > max_aa_count:
            max_aa_count = aa_count
            best_offset = offset
            
    # However, if there are NO 0xAA fillers, we might be looking for something else.
    # But usually, it should have some.
    
    print(f"--- {filename} ---")
    print(f"Most pattern-like region found at offset {best_offset} (0x{best_offset:x})")
    print(f"AA Filler count: {max_aa_count} out of 1024 slots")
    
    return best_offset

if __name__ == "__main__":
    find_patterns_automatically('big_file_unique_data.bin')
    find_patterns_automatically('small_file_repeating_data.bin')
