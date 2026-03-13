import os
import struct

def unpack_phases(data_bytes):
    """Unpacks bytes into a list of 2-bit phase values (0-3)."""
    phases = []
    for b in data_bytes:
        # LSB-first packing of 4 phases (2 bits each)
        phases.append(b & 0x03)
        phases.append((b >> 2) & 0x03)
        phases.append((b >> 4) & 0x03)
        phases.append((b >> 6) & 0x03)
    return phases

def analyze_pattern(pattern_data, pattern_id):
    """
    Analyzes one 256-byte pattern block.
    We assume 16 steps, with data for 4 voices.
    """
    phases = unpack_phases(pattern_data)
    # 256 bytes * 4 phases/byte = 1024 phases per pattern
    # 1024 phases / 16 steps = 64 phases per step
    # 64 phases / 4 voices = 16 phases per voice/step (4 bytes or 32 bits)
    
    print(f"\n--- Pattern {pattern_id} ---")
    print("Step | Voice 1 | Voice 2 | Voice 3 | Voice 4")
    print("-" * 45)
    
    for step in range(16):
        voice_results = []
        for voice in range(4):
            # Extract the 16 phases (32 bits) for this voice/step
            start_off = (step * 64) + (voice * 16)
            v_phases = phases[start_off : start_off + 16]
            
            # Simple heuristic: see if there's any non-zero (non-'C') data
            # C=0, D=1, B=2, A=3. AA (all B) is 2,2,2,2.
            # In your file, AA (all 2s) seems to be the 'empty' or 'null' filler.
            is_empty = all(p == 2 for p in v_phases)
            
            if is_empty:
                voice_results.append("  .  ")
            else:
                # Convert phases back to hex for visual inspection
                v_hex = "".join([f"{p}" for p in v_phases])
                voice_results.append(v_hex[:5] + "...")
                
        print(f"{step+1:4} | {' | '.join(voice_results)}")

def run_extraction(bin_path):
    with open(bin_path, 'rb') as f:
        # Patterns are in the first 4KB (16 * 256 bytes)
        for i in range(16):
            block = f.read(256)
            if not block: break
            analyze_pattern(block, i + 1)

if __name__ == "__main__":
    import sys
    run_extraction(sys.argv[1] if len(sys.argv) > 1 else 'my_data_v3_small.bin')
