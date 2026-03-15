import struct

def extract_metadata(bin_path):
    with open(bin_path, 'rb') as f:
        data = f.read()

    print("Pad,RawData(First32Bytes)")
    for i in range(16):
        header = data[i*256 : i*256 + 32]
        print(f"{i+1:2}: {header.hex()}")

if __name__ == "__main__":
    import sys
    extract_metadata(sys.argv[1] if len(sys.argv) > 1 else 'my_data_v3_small.bin')
