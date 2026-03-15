import sys

def scan_full_entropy(filename):
    with open(filename, 'rb') as f:
        data = f.read()[0::2] # Left channel

    print(f"--- {filename} ---")
    for i in range(0, len(data), 4096):
        chunk = data[i : i + 4096]
        if not chunk: break
        unique = len(set(chunk))
        print(f"Offset {i:7} (0x{i:05x}): {unique:4}")

if __name__ == "__main__":
    scan_full_entropy('big_file_unique_data.bin')
