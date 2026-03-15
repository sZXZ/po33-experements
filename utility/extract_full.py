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

def extract_full_mu(filename, output_name):
    with open(filename, 'rb') as f:
        data = f.read()[0::2] # Left channel

    chunk = data[2048:] # Start after sync
    decoded = [mu_law_decode(b) for b in chunk]
    
    with wave.open(output_name, 'wb') as wf:
        wf.setnchannels(1)
        wf.setsampwidth(2)
        wf.setframerate(11025) # Lower rate to get longer duration
        wf.writeframes(struct.pack(f'<{len(decoded)}h', *decoded))
    print(f"Extracted {len(decoded)} samples to {output_name}")

if __name__ == "__main__":
    extract_full_mu('big_file_unique_data.bin', 'big_full_11k.wav')
