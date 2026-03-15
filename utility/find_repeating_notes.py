import sys

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

def find_repeating_strudel(filename):
    with open(filename, 'rb') as f:
        data = f.read()[0::2] # Left channel

    print(f"--- {filename} ---")
    data = data[2000:] # Skip pilot
    
    seen_notes = {}
    for offset in range(0, 1000): # Check starting alignment
        p1 = data[offset : offset + 256]
        p2 = data[offset + 256 : offset + 512]
        
        n1 = get_notes(p1)
        n2 = get_notes(p2)
        
        if n1 == n2 and "~" not in n1[:10]: # Heuristic: skip empty-ish
             print(f"Found repeating notes at offset {offset + 2000}")
             print(f"Notes: {n1[:50]}...")
             return offset + 2000
             
    print("No repeating strudel notes found in first 1000 bytes after pilot.")

if __name__ == "__main__":
    find_repeating_strudel('small_file_repeating_data.bin')
