import sys

def find_repeating_consecutive_raw(filename):
    with open(filename, 'rb') as f:
        raw = f.read()

    print(f"--- {filename} ---")
    
    # scan for anything diverse that repeats
    for i in range(15000, len(raw) - 512):
        if raw[i : i+256] == raw[i+256 : i+512]:
            if len(set(raw[i:i+256])) > 100: # Very diverse data
                print(f"RAW: Found consecutive matching 256-byte blocks at offset {i} (0x{i:x})")
                return i

    L = raw[0::2]
    for i in range(10000, len(L) - 512):
        if L[i : i+256] == L[i+256 : i+512]:
            if len(set(L[i:i+256])) > 100:
                print(f"LEFT: Found consecutive matching 256-byte blocks at offset {i} (0x{i:x})")
                return i
                
    print("No matches found skipping 15000 bytes.")

if __name__ == "__main__":
    find_repeating_consecutive_raw('small_file_repeating_data.bin')
