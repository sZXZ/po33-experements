
def mu_law_decode(mu):
    mu = ~mu & 0xFF
    sign = (mu & 0x80)
    exponent = (mu & 0x70) >> 4
    mantissa = (mu & 0x0F)
    data = (mantissa << 3) + 0x84
    data <<= exponent
    data = data - 0x84
    return -data if sign else data

def find_boundaries(bin_path, threshold=2000, window=1000):
    with open(bin_path, 'rb') as f:
        data = f.read()
    
    # Calculate volume envelope
    env = []
    for i in range(0, len(data), window):
        chunk = data[i:i+window]
        vals = [abs(mu_law_decode(b)) for b in chunk]
        peak = max(vals) if vals else 0
        env.append(peak)
    
    # Detect "is quiet"
    in_silent = True
    start_points = []
    for idx, peak in enumerate(env):
        if peak > threshold and in_silent:
            start_points.append(idx * window)
            in_silent = False
        elif peak <= threshold:
            in_silent = True
            
    print("Detected Sample Start Addresses (Potential Pads):")
    for i, addr in enumerate(start_points):
        print(f"Pad {i+1:2}: 0x{addr:05x}")
        
    # Generate CSV snippet for the user
    print("\nSuggested CSV mapping:")
    print("sfx_id,start_byte,end_byte,speed")
    for i in range(len(start_points)):
        s = start_points[i]
        e = start_points[i+1] if i+1 < len(start_points) else len(data)
        print(f"{i},{s},{e},8")

if __name__ == "__main__":
    import sys
    find_boundaries(sys.argv[1] if len(sys.argv) > 1 else 'my_data_v3_small.bin')
