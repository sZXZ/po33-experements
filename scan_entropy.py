import sys

def scan_entropy(filename):
    with open(filename, 'rb') as f:
        data = f.read()[0::2] # Left channel

    print(f"--- {filename} ---")
    for i in range(0, 10000, 256):
        chunk = data[i : i + 256]
        if not chunk: break
        unique = len(set(chunk))
        print(f"Offset {i:5} (0x{i:04x}): {unique:3} unique bytes")

if __name__ == "__main__":
    scan_entropy('big_file_unique_data.bin')
    scan_entropy('small_file_repeating_data.bin')
