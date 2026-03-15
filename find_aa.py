import sys

def find_aa_blocks(filename):
    with open(filename, 'rb') as f:
        data = f.read()[0::2] # Left channel

    print(f"--- {filename} ---")
    aa_block = b'\xaa\xaa\xaa\xaa'
    
    first_aa = data.find(aa_block)
    if first_aa != -1:
        print(f"First 0xAA AA AA AA found at offset {first_aa} (0x{first_aa:x})")
        # Check alignment relative to 4-byte boundaries
        print(f"Alignment modulo 4: {first_aa % 4}")
    else:
        print("No 0xAA AA AA AA found in file.")

if __name__ == "__main__":
    find_aa_blocks('big_file_unique_data.bin')
    find_aa_blocks('small_file_repeating_data.bin')
