import os
import math

def calculate_entropy(chunk):
    if not chunk: return 0
    counts = [0] * 256
    for b in chunk: counts[b] += 1
    entropy = 0
    for c in counts:
        if c > 0:
            p = c / len(chunk)
            entropy -= p * math.log2(p)
    return entropy

def analyze_structure(bin_path, chunk_size=256):
    with open(bin_path, 'rb') as f:
        data = f.read()

    print("Index,Address,Type,Size,Entropy,Repetitions,Description")
    
    i = 0
    prev_chunk = None
    rep_count = 0
    block_start = 0
    idx = 0
    
    while i < len(data):
        chunk = data[i:i+chunk_size]
        entropy = calculate_entropy(chunk)
        
        # Check if this chunk is identical to the previous one
        if chunk == prev_chunk:
            rep_count += 1
        else:
            if prev_chunk is not None:
                # Log the previous run of identical chunks
                size = (rep_count + 1) * chunk_size
                res_type = "REPEATING" if rep_count > 0 else ("SAMPLE" if calculate_entropy(prev_chunk) > 4.5 else "DATA")
                desc = f"Identical block repeated {rep_count+1} times" if rep_count > 0 else "Unique block"
                print(f"{idx},0x{block_start:05x},{res_type},{size},{calculate_entropy(prev_chunk):.2f},{rep_count+1},{desc}")
                idx += 1
            
            block_start = i
            rep_count = 0
            prev_chunk = chunk
            
        i += chunk_size

    # Final block
    if prev_chunk:
        size = (rep_count + 1) * chunk_size
        print(f"{idx},0x{block_start:05x},END,{size},{calculate_entropy(prev_chunk):.2f},{rep_count+1},End of file")

if __name__ == "__main__":
    import sys
    analyze_structure(sys.argv[1] if len(sys.argv) > 1 else 'my_data_v3_small.bin', 64)
