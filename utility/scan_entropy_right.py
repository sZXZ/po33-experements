import sys

def entropy_profile_right(filename):
    with open(filename, 'rb') as f:
        data = f.read()[1::2] # Right channel

    print(f"--- {filename} (RIGHT) ---")
    for i in range(0, 10000, 256):
        chunk = data[i : i + 256]
        if not chunk: break
        unique = len(set(chunk))
        print(f"{i:6} (0x{i:05x}): {unique:3}")

if __name__ == "__main__":
    entropy_profile_right('small_file_repeating_data.bin')
