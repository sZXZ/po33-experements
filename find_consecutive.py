import sys

def find_periodic_repeats(filename):
    with open(filename, 'rb') as f:
        data = f.read()[0::2] # Left channel

    print(f"--- {filename} ---")
    data = data[2000:] # Skip pilot
    
    # Check every starting offset for 256-byte periodicity
    best_offset = -1
    max_matches = 0
    
    for offset in range(0, min(5000, len(data) - 512)):
        matches = 0
        for i in range(1, 16): # Check next 15 patterns
            if offset + (i+1)*256 > len(data): break
            if data[offset : offset+256] == data[offset + i*256 : offset + (i+1)*256]:
                matches += 1
        
        if matches > max_matches:
            max_matches = matches
            best_offset = offset + 2000

    if max_matches > 0:
        print(f"Found {max_matches} consecutive identical 256-byte patterns starting at {best_offset} (0x{best_offset:x})")
    else:
        print("No identical consecutive patterns found.")

if __name__ == "__main__":
    find_periodic_repeats('small_file_repeating_data.bin')
    find_periodic_repeats('big_file_unique_data.bin')
