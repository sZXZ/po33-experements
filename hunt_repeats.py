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

def hunt_repeats_all(filename):
    with open(filename, 'rb') as f:
        data = f.read()[0::2] # Left channel

    diverse_start = 2000
    diverse_end = 15000
    
    seen_at = {} 
    
    for offset in range(diverse_start, diverse_end):
        block = data[offset : offset + 256]
        notes = get_notes(block)
        
        if "~" not in notes[:10]: # Valid data
            if notes in seen_at:
                # Check distance
                for prev_o in seen_at[notes]:
                    dist = offset - prev_o
                    if dist % 256 == 0:
                        print(f"[{filename}] MATCH found at {hex(prev_o)} and {hex(offset)} (distance {dist}, {dist//256} patterns)")
                        # return
            seen_at[notes] = seen_at.get(notes, []) + [offset]

if __name__ == "__main__":
    hunt_repeats_all('small_file_repeating_data.bin')
