import sys

def scan(file_path):
    with open(file_path, 'rb') as f:
        raw = f.read()

    data_L = raw[0::2]
    data_R = raw[1::2]
    
    for name, data in [("L-channel", data_L), ("R-channel", data_R)]:
        pattern_starts = []
        for i in range(0, min(len(data), 200000), 256):
            block = data[i:i+256]
            if len(block) < 256: break
            
            aa_count = 0
            for j in range(0, 256, 4):
                if block[j:j+4] == b'\xaa\xaa\xaa\xaa':
                    aa_count += 1
                    
            if aa_count > 10:  
                pattern_starts.append((i, aa_count))

        if pattern_starts:
            print(f"Found {len(pattern_starts)} pattern blocks at {name} offsets (de-interleaved):")
            for off, count in pattern_starts:
                print(f"Offset {off} (0x{off:x}): {count} empty steps")
        else:
            print(f"No pattern blocks found with 0xAA fillers in {name} :(")

if __name__ == "__main__":
    scan('my_data_v3.bin')
