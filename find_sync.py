import sys

def find_sync(filename):
    try:
        with open(filename, 'rb') as f:
            data = f.read()[0::2] # Left channel

        # Pilot tone appears to be sequence of:
        # 0xaa 0xaa 0x42 0xbd 0x96 0x96 0x7e 0x81
        # Let's search for when this sequence stops.
        
        pilot = bytes([0xaa, 0xaa, 0x42, 0xbd, 0x96, 0x96, 0x7e, 0x81])
        
        # Or let's just look for the first 256-byte window that has diverse data
        for offset in range(0, len(data) - 256):
            window = data[offset:offset+256]
            unique_bytes = len(set(window))
            if unique_bytes > 20: 
                print(f"--- {filename} ---")
                print(f"Found diverse data starting at offset {offset}")
                print(f"Bytes: {[hex(x) for x in data[offset:offset+32]]}")
                
                # Check 16 patterns from here
                for pat in range(16):
                    block = data[offset + pat * 256 : offset + (pat+1) * 256]
                    phases = []
                    for b in block:
                        phases.extend([b & 0x03, (b >> 2) & 0x03, (b >> 4) & 0x03, (b >> 6) & 0x03])
                    
                    # Just count non-empty
                    non_empty = 0
                    for b in block:
                        if b != 0xaa:
                            non_empty += 1
                    print(f"Pattern {pat+1} non-empty bytes: {non_empty}")
                return
                
    except Exception as e:
        print(f"Error on {filename}: {e}")

if __name__ == "__main__":
    find_sync('big_file_unique_data.bin')
    find_sync('small_file_repeating_data.bin')
