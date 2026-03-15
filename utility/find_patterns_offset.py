import sys

def scan(file_path):
    with open(file_path, 'rb') as f:
        data = f.read()[0::2] # L channel

    print(f"Total L channel bytes: {len(data)}")
    
    # scan moving 256-byte window (or just chunked by 256)
    for i in range(0, min(len(data), 65536), 256):
        block = data[i:i+256]
        if len(block) < 256: break
        
        unique_4b = set()
        aa_count = 0
        for j in range(0, 256, 4):
            b = block[j:j+4]
            unique_4b.add(b)
            if b == b'\xaa\xaa\xaa\xaa':
                aa_count += 1
                
        if len(unique_4b) > 4: # Not just the repetitive header
            print(f"Offset {i} (0x{i:x}): {len(unique_4b)} unique 4-byte sequences, {aa_count} empty steps (0xAA)")

if __name__ == "__main__":
    scan('my_data_v3.bin')
