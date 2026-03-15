import sys

def find_exact_payload_start(filename):
    with open(filename, 'rb') as f:
        data = f.read()[0::2] # Left channel

    # Detect the 128-byte period in the first 500 bytes
    base = 0
    period = 128
    
    # Verify the period actually exists at the start
    if data[0:128] != data[128:256]:
        print(f"[{filename}] Period of 128 bytes not found at start.")
        # Try finding ANY repeating period
        period = -1
        for p in [8, 16, 32, 64, 128, 256]:
            if data[0:p] == data[p:2*p]:
                period = p
                break
        if period == -1: return 0
    
    print(f"[{filename}] Found initial period: {period}")

    # Now scan forward until the period breaks
    for i in range(period, len(data)):
        if data[i] != data[i - period]:
            # At this byte, the sync frame pattern broke.
            # Usually, there is a "sync word" or header right here.
            return i
            
    return 0

if __name__ == "__main__":
    for f in ['big_file_unique_data.bin', 'small_file_repeating_data.bin']:
        start = find_exact_payload_start(f)
        print(f"[{f}] Payload starts at offset {start} (0x{start:x})")
