import sys

def full_raw_entropy(filename):
    with open(filename, 'rb') as f:
        raw = f.read()

    print(f"--- {filename} (RAW) ---")
    for i in range(0, min(10000, len(raw)), 256):
        chunk = raw[i : i + 256]
        if not chunk: break
        unique = len(set(chunk))
        marker = "!!!" if unique > 100 else "   "
        print(f"{i:6} (0x{i:05x}): {unique:3} {marker}")

if __name__ == "__main__":
    full_raw_entropy(sys.argv[1])
