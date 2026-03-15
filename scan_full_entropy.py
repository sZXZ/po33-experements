import sys

def entropy_profile(filename):
    with open(filename, 'rb') as f:
        data = f.read()[0::2] # Left channel

    print(f"--- {filename} ---")
    for i in range(0, len(data), 256):
        chunk = data[i : i + 256]
        if not chunk: break
        unique = len(set(chunk))
        # marker for diverse blocks
        marker = "!!!" if unique > 100 else "   "
        print(f"{i:6} (0x{i:05x}): {unique:3} {marker}")

if __name__ == "__main__":
    entropy_profile('small_file_repeating_data.bin')
