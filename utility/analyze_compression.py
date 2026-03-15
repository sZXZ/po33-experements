import sys
from collections import Counter
import math

def analyze_compression(filename):
    with open(filename, 'rb') as f:
        data = f.read()[0::2] # Left channel

    print(f"--- {filename} ---")
    # Patterns end approx at 2048 + 4096 = 6144
    sample_data = data[6144:6144 + 65536] # Take a 64KB chunk
    if not sample_data:
        print("No sample data found.")
        return

    counts = Counter(sample_data)
    
    # Calculate Shannon Entropy
    entropy = 0
    for count in counts.values():
        p = count / len(sample_data)
        entropy -= p * math.log2(p)
    
    print(f"Entropy: {entropy:.4f} bits/byte (Max 8.0)")
    
    # If entropy is very high (> 7.5), it's likely compressed or high-quality audio
    # If entropy is low (< 6.0), it might be sparse or low bit depth
    
    # Check for mu-law signs: values concentrated near the ends or middle?
    # Actually, mu-law is biased.
    
    # Print 5 most common bytes
    print("Most common bytes:")
    for b, count in counts.most_common(5):
        print(f"  0x{b:02x}: {count}")

if __name__ == "__main__":
    analyze_compression('big_file_unique_data.bin')
    analyze_compression('small_file_repeating_data.bin')
