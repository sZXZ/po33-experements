import sys

def compare_files(f1, f2):
    with open(f1, 'rb') as h1:
        d1 = h1.read()[0::2]
    with open(f2, 'rb') as h2:
        d2 = h2.read()[0::2]

    min_l = min(len(d1), len(d2))
    for i in range(min_l):
        if d1[i] != d2[i]:
            print(f"Files differ at offset {i} (0x{i:x})")
            print(f"f1: {[hex(x) for x in d1[i:i+16]]}")
            print(f"f2: {[hex(x) for x in d2[i:i+16]]}")
            return i
            
if __name__ == "__main__":
    compare_files('big_file_unique_data.bin', 'small_file_repeating_data.bin')
