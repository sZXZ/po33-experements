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

def get_payload_start(data):
    """
    Finds the start of the PO-33 data payload by scanning for the first
    256-byte block with a high number of unique bytes, bypassing the repetitive
    sync/pilot tones that appear at the start of all backup files.
    """
    for i in range(0, min(100000, len(data) - 256), 256):
        chunk = data[i:i+256]
        if len(set(chunk)) > 30:
            return i
    return 0
    
def parse_po33_to_strudel(file_path, interleaved=False, num_patterns=16):
    with open(file_path, 'rb') as f:
        raw = f.read()

    if interleaved:
        data = raw
    else:
        data = raw[0::2]
        
    start_offset = get_payload_start(data)
    print(f"Detected internal payload start at byte offset: {start_offset}")

    strudel_code = ""

    for pat in range(num_patterns):
        # We start extracting precisely from the detected start offset
        base = start_offset + (pat * 256)
        block = data[base : base + 256]
        if len(block) < 256:
            break
            
        phases = unpack_phases(block)
        
        voices_notes = {1: [], 2: [], 3: [], 4: []}
        
        for step in range(16):
            for voice in range(4):
                start = (step * 64) + (voice * 16)
                b = phases_to_bytes(phases[start : start + 16])
                
                if b[0] != 0xAA or b[2] != 0xAA:
                    pitch = b[1] >> 4
                    voices_notes[voice+1].append(str(pitch))
                else:
                    voices_notes[voice+1].append("~")
                    
        has_notes = False
        for v in range(1, 5):
            if any(n != "~" for n in voices_notes[v]):
                has_notes = True
                
        if has_notes:
            strudel_code += f"// Pattern {pat + 1}\n"
            for v in range(1, 5):
                sequence = " ".join(voices_notes[v])
                strudel_code += f"n(\"{sequence}\"),\n"
            strudel_code += "\n"
            
    return strudel_code

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Convert PO-33 bin patterns to Strudel.cc code")
    parser.add_argument("file", help="Input .bin file")
    parser.add_argument("--interleaved", action="store_true", help="Use old interleaved logic")
    parser.add_argument("--out", type=str, default="strudel_patterns.js", help="Output file")
    
    args = parser.parse_args()
    
    print(f"Reading {args.file}...")
    code = parse_po33_to_strudel(args.file, args.interleaved)
    
    if not code:
        print("No patterns found!")
    else:
        with open(args.out, 'w') as f:
            f.write(code)
        print(f"Successfully wrote strudel code to {args.out}")
