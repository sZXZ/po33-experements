import sys
import argparse

def unpack_phases(data_bytes):
    phases = []
    for b in data_bytes:
        phases.append(b & 0x03)
        phases.append((b >> 2) & 0x03)
        phases.append((b >> 4) & 0x03)
        phases.append((b >> 6) & 0x03)
    return phases

def phases_to_bytes(phases):
    bytes_out = []
    for i in range(0, len(phases) - 3, 4):
        p = phases[i:i+4]
        b = (p[3] << 6) | (p[2] << 4) | (p[1] << 2) | p[0]
        bytes_out.append(b)
    return bytes_out

def parse_po33_to_strudel(file_path, offset=0, interleaved=False, num_patterns=16):
    with open(file_path, 'rb') as f:
        f.seek(offset)
        raw = f.read(num_patterns * 256 * (2 if interleaved else 1))

    if interleaved:
        # Replicate old notebook behavior (using interleaved L/R directly)
        data = raw
    else:
        # Proper behavior: use Left channel
        data = raw[0::2]

    # Pattern extraction
    strudel_code = ""

    for pat in range(num_patterns):
        block = data[pat*256 : (pat+1)*256]
        if len(block) < 256:
            break
            
        phases = unpack_phases(block)
        
        voices_notes = {1: [], 2: [], 3: [], 4: []}
        
        for step in range(16):
            for voice in range(4):
                start = (step * 64) + (voice * 16)
                b = phases_to_bytes(phases[start : start + 16])
                
                # Check for emptiness
                if b[0] != 0xAA or b[2] != 0xAA:
                    pitch = b[1] >> 4
                    voices_notes[voice+1].append(str(pitch))
                else:
                    voices_notes[voice+1].append("~")
                    
        # Check if pattern is totally empty
        has_notes = False
        for v in range(1, 5):
            if any(n != "~" for n in voices_notes[v]):
                has_notes = True
                
        if has_notes:
            strudel_code += f"// Pattern {pat + 1}\n"
            for v in range(1, 5):
                sequence = " ".join(voices_notes[v])
                strudel_code += f"note(\"{sequence}\").scale(\"C major\"), // Voice {v}\n"
            strudel_code += "\n"
            
    return strudel_code

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Convert PO-33 bin patterns to Strudel.cc code")
    parser.add_argument("file", help="Input .bin file")
    parser.add_argument("--offset", type=int, default=0, help="Offset in bytes (default 0). Note: pilot tone is usually ~15600 bytes.")
    parser.add_argument("--interleaved", action="store_true", help="Use old interleaved logic (from notebook)")
    parser.add_argument("--out", type=str, default="strudel_patterns.js", help="Output file")
    
    args = parser.parse_argument()
    
    print(f"Reading {args.file} at offset {args.offset}...")
    code = parse_po33_to_strudel(args.file, args.offset, args.interleaved)
    
    if not code:
        print("No patterns found!")
    else:
        with open(args.out, 'w') as f:
            f.write(code)
        print(f"Successfully wrote strudel code to {args.out}")

