import sys

def find_best_alignment(filename):
    with open(filename, 'rb') as f:
        data = f.read()[0::2] # Left channel

    best_count = 0
    best_offset = 0
    
    # slide a 256-byte window, but count how many 4-byte sequences are exactly \xaa\xaa\xaa\xaa
    # doing sliding window byte by byte is slow, we can optimize:
    
    aa = b'\xaa\xaa\xaa\xaa'
    
    # First find all indices of `aa`
    aa_indices = []
    for i in range(len(data) - 4):
        if data[i:i+4] == aa:
            aa_indices.append(i)
            
    print(f"[{filename}] Found {len(aa_indices)} instances of 0xaa 0xaa 0xaa 0xaa")
    
    # We want to find an alignment `offset` where `aa` occurrences fall on 4-byte boundaries relative to `offset`
    # and we want the maximum concentration in the first 4096 bytes (16 patterns).
    
    # Let's just create a quick scoring function
    scores = {}
    for idx in aa_indices:
        # A valid pattern offset would be `idx - k * 4` where k is the 4-byte step index
        # To simplify, the offset modulo 4 must be the same as idx modulo 4
        # Also, the offset should be somewhere between 0 and len(data) - 4096
        
        # Let's just group them by offset modulo 4
        pass

    # Actually, we know the true pattern data starts somewhere, maybe around byte 15000-16000?
    max_score = 0
    best_off = 0
    
    for offset in range(0, min(20000, len(data) - 4096)):
        score = 0
        for pat in range(16):
            base = offset + pat * 256
            for step in range(0, 256, 4):
                if data[base+step:base+step+4] == aa:
                    score += 1
        if score > max_score:
            max_score = score
            best_off = offset

    print(f"[{filename}] Best offset: {best_off} with {max_score}/1024 empty blocks")

if __name__ == "__main__":
    find_best_alignment('big_file_unique_data.bin')
    find_best_alignment('small_file_repeating_data.bin')
