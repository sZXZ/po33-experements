import sys

def find_repeats_anywhere(filename, block_size=256):
    with open(filename, 'rb') as f:
        data = f.read()[0::2] # Left channel

    print(f"--- {filename} ---")
    data = data[2000:] # Skip pilot
    
    seen = {}
    for i in range(len(data) - block_size):
        block = data[i : i + block_size]
        if block in seen:
            print(f"Found repeat! Offset {i+2000} (0x{i+2000:x}) matches offset {seen[block]+2000} (0x{seen[block]+2000:x})")
            # Is it diverse?
            if len(set(block)) > 20:
                print("  (Block is diverse!)")
                # print(f"  First 16 bytes: {block[:16].hex()}")
            # return
        seen[block] = i

if __name__ == "__main__":
    find_repeats_anywhere('small_file_repeating_data.bin')
