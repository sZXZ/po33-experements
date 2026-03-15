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

def scan_for_redundancy(filename):
    with open(filename, 'rb') as f:
        data = f.read()[0::2] # Left channel

    print(f"--- {filename} ---")
    
    best_offset = -1
    min_unique = 17
    
    # scan for best alignment
    for offset in range(2000, min(10000, len(data) - 4096), 4):
        p_notes = []
        for i in range(16):
            block = data[offset + i*256 : offset + (i+1)*256]
            p_notes.append(get_notes(block))
            
        unique = len(set(p_notes))
        
        # Check if patterns have actual data (not just pilot)
        # Pilot tone notes look like "13 11 2 4 ..." 
        if "13" in p_notes[0] and "11" in p_notes[0]:
            continue
            
        if unique < min_unique:
            min_unique = unique
            best_offset = offset
            
    print(f"Best offset: {best_offset} (0x{best_offset:x}) with {min_unique} unique patterns out of 16")
    return best_offset

if __name__ == "__main__":
    scan_for_redundancy('small_file_repeating_data.bin')
    scan_for_redundancy('big_file_unique_data.bin')
