import sys

def inspect_bits(filename):
    with open(filename, 'rb') as f:
        data = f.read()[0::2] # Left channel

    print(f"--- {filename} ---")
    # Convert first 1000 bytes to a bit string
    bit_str = ""
    for b in data[2048:3048]:
        bit_str += bin(b)[2:].zfill(8)

    # Search for recurring bit patterns of various lengths
    for length in range(8, 20):
        # check if it repeats every 'length' bits
        matches = 0
        for i in range(len(bit_str) - length*2):
            if bit_str[i : i+length] == bit_str[i+length : i+2*length]:
                matches += 1
        print(f"Bit length {length}: {matches} matches")

if __name__ == "__main__":
    inspect_bits('big_file_unique_data.bin')
