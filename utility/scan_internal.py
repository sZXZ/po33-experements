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
    return notes # list

def scan_for_internal_repeats(filename):
    with open(filename, 'rb') as f:
        data = f.read()[0::2] # Left channel

    print(f"--- {filename} ---")
    
    for offset in range(2000, min(10000, len(data) - 256), 4):
        notes = get_notes(data[offset : offset + 256])
        
        # A pattern has 16 steps, each 4 voices.
        # Check if the first 8 steps are same as next 8.
        if notes[:32] == notes[32:64] and notes[0] != "~":
             if "10" in notes[0] and "9" in notes[1]: continue # Skip pilot
             print(f"FOUND INTERNAL REPEATING PATTERN at offset {offset} (0x{offset:x})")
             print(f"Notes: {' '.join(notes[:32])}...")
             return offset

if __name__ == "__main__":
    scan_for_internal_repeats('small_file_repeating_data.bin')
    scan_for_internal_repeats('big_file_unique_data.bin')
