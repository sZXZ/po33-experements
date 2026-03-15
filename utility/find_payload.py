import sys

def verify_patterns(filename):
    with open(filename, 'rb') as f:
        data = f.read()[0::2] # Left channel

    offset = 2046
    
    # Check 16 patterns
    for pat in range(16):
        base = offset + pat * 256
        block = data[base:base+256]
        
        # count 0xaa full empty steps (4 bytes of 0xaa)
        empty_steps = 0
        for i in range(0, 256, 4):
            if block[i:i+4] == b'\xaa\xaa\xaa\xaa':
                empty_steps += 1
                
        print(f"[{filename}] Pattern {pat+1}: {empty_steps}/64 empty steps")

if __name__ == "__main__":
    verify_patterns('big_file_unique_data.bin')
    verify_patterns('small_file_repeating_data.bin')
