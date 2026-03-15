import sys

def find_aa_honey_pot(filename):
    with open(filename, 'rb') as f:
        data = f.read()[0::2] # Left channel

    print(f"--- {filename} ---")
    
    max_aa = -1
    best_off = -1
    
    # 4-byte aligned scan
    for offset in range(0, len(data) - 4096, 4):
        aa_count = 0
        for j in range(offset, offset + 4096):
            if data[j] == 0xaa:
                aa_count += 1
        
        if aa_count > max_aa:
            max_aa = aa_count
            best_off = offset

    print(f"Best AA region at offset {best_off} (0x{best_off:x})")
    print(f"AA count: {max_aa} / 4096")
    
    # Let's see if 16384 is the magic number (standard metadata size for some POs)
    if len(data) > 16384 + 4096:
        aa_count_standard = sum(1 for b in data[16384:16384+4096] if b == 0xaa)
        print(f"AA count at standard offset 16384: {aa_count_standard} / 4096")

if __name__ == "__main__":
    find_aa_honey_pot('big_file_unique_data.bin')
    find_aa_honey_pot('small_file_repeating_data.bin')
