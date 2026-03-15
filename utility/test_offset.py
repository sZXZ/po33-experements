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

def extract_from_offset(filename, offset):
    with open(filename, 'rb') as f:
        data = f.read()[0::2] # Left channel

    print(f"// Patterns from offset {offset}")
    for pat in range(16):
        base = offset + pat * 256
        block = data[base : base+256]
        phases = unpack_phases(block)
        
        voices = []
        for voice in range(4):
            v_notes = []
            for step in range(16):
                start = (step * 64) + (voice * 16)
                b = phases_to_bytes(phases[start : start + 16])
                if b[0] != 0xAA or b[2] != 0xAA:
                    pitch = b[1] >> 4
                    v_notes.append(str(pitch))
                else:
                    v_notes.append("~")
            voices.append(v_notes)
            
        print(f"// Pattern {pat+1}")
        for v_idx, v_notes in enumerate(voices):
            seq = " ".join(v_notes)
            print(f"n(\"{seq}\"),")
        print()

if __name__ == "__main__":
    extract_from_offset(sys.argv[1], int(sys.argv[2]))
