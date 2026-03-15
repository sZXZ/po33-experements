import wave
import struct

def mu_law_decode(u_val):
    u_val = ~u_val & 0xFF
    sign = (u_val & 0x80)
    exponent = (u_val & 0x70) >> 4
    mantissa = (u_val & 0x0F)
    sample = (mantissa << 3) + 0x84
    sample <<= exponent
    sample -= 0x84
    return sample if not sign else -sample

def extract_mulaw_variations(filename, prefix):
    with open(filename, 'rb') as f:
        data = f.read()[0::2] # Left channel

    chunk = data[6144:6144+460000] # approx 20s
    
    # Variation 1: Normal
    decoded1 = [mu_law_decode(b) for b in chunk]
    
    # Variation 2: Bit-inverted before decode
    decoded2 = [mu_law_decode(b ^ 0xFF) for b in chunk]
    
    # Variation 3: Reverse bits of byte
    def rev(b):
        return int(bin(b)[2:].zfill(8)[::-1], 2)
    decoded3 = [mu_law_decode(rev(b)) for b in chunk]

    for i, dec in enumerate([decoded1, decoded2, decoded3], 1):
        with wave.open(f"{prefix}_var{i}.wav", 'wb') as wf:
            wf.setnchannels(1)
            wf.setsampwidth(2)
            wf.setframerate(23437)
            wf.writeframes(struct.pack(f'<{len(dec)}h', *dec))
        print(f"Created {prefix}_var{i}.wav")

if __name__ == "__main__":
    extract_mulaw_variations('big_file_unique_data.bin', 'big')
