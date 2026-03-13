import os

def scan_samples(bin_path, threshold=50, min_len=1000, silence_len=500):
    """
    Scans the .bin file for loud segments (samples).
    Produces a starter CSV content.
    """
    with open(bin_path, 'rb') as f:
        data = f.read()
        
    def mu_law_val(mu):
        mu = ~mu & 0xFF
        exponent = (mu & 0x70) >> 4
        mantissa = (mu & 0x0F)
        return (mantissa << 3) << exponent

    segments = []
    in_sample = False
    start_idx = 0
    silence_count = 0
    
    # Interleaved L/R means every 2 bytes is one sample point (roughly)
    # We scan L channel primarily
    for i in range(0, len(data), 2):
        val = mu_law_val(data[i])
        if val > threshold:
            if not in_sample:
                in_sample = True
                start_idx = i
            silence_count = 0
        else:
            if in_sample:
                silence_count += 1
                if silence_count > silence_len:
                    end_idx = i - (silence_len * 2)
                    if (end_idx - start_idx) > min_len:
                        segments.append((start_idx, end_idx))
                    in_sample = False
                    silence_count = 0
                    
    print("sfx_id,name,start_byte,end_byte,speed,description")
    for idx, (s, e) in enumerate(segments[:8]):
        print(f"{idx},Sample_{idx},{s},{e},8,Auto-detected segment")

if __name__ == "__main__":
    import sys
    if len(sys.argv) > 1:
        scan_samples(sys.argv[1])
    else:
        print("Usage: python3 scan_samples.py <data.bin>")
