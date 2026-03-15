import sys

# reuse the same unpack/phases logic...
def unpack_phases(data_bytes):
    phases = []
    for b in data_bytes:
        phases.extend([b & 0x03, (b >> 2) & 0x03, (b >> 4) & 0x03, (b >> 6) & 0x03])
    return phases

def phases_to_bytes(phases):
    bytes_out = []
    for i in range(0, len(phases) - 3, 4):
        p = phases[i:i+4]
        b = (p[3] << 6) | (p[2] << 4) | (p[1] << 2) | p[0]
        bytes_out.append(b)
    return bytes_out

def get_notes(block):
    phases = unpack_phases(block)
    notes = []
    for step in range(16):
        for voice in range(4):
            start = (step * 64) + (voice * 16)
            b = phases_to_bytes(phases[start : start + 16])
            if b[0] != 0xAA or b[2] != 0xAA:
                notes.append(str(b[1] >> 4))
            else:
                notes.append("~")
    return " ".join(notes)

def scan_for_redundancy_deeper(filename):
    with open(filename, 'rb') as f:
        data = f.read()[0::2] # Left channel

    print(f"--- {filename} ---")
    
    # scan for any alignment where pattern 1 == pattern 2
    for offset in range(2000, len(data) - 1024, 4):
        p1 = data[offset : offset + 256]
        p2 = data[offset + 256 : offset + 512]
        
        n1 = get_notes(p1)
        n2 = get_notes(p2)
        
        if n1 == n2:
            # Check if it's the pilot tone note pattern
            if "10 9 10 9" in n1:
                continue
                
            print(f"FOUND REPEATING PATTERNS at offset {offset} (0x{offset:x})")
            print(f"Notes: {n1[:70]}...")
            return offset
            
    return -1

if __name__ == "__main__":
    scan_for_redundancy_deeper('small_file_repeating_data.bin')
