import sys

def inspect(filename):
    try:
        with open(filename, 'rb') as f:
            data = f.read()[0::2] # Left channel

        print(f"--- {filename} ---")
        for i, b in enumerate(data):
            if b != 0xaa:
                print(f"First non-0xAA byte at offset {i} (0x{i:x}): {hex(b)}")
                print(f"Subsequent bytes: {[hex(x) for x in data[i:i+32]]}")
                print(f"Data length: {len(data)}")
                return
        print("File is all 0xAA or empty.")
    except Exception as e:
        print(f"Error on {filename}: {e}")

if __name__ == "__main__":
    inspect('big_file_unique_data.bin')
    inspect('small_file_repeating_data.bin')
