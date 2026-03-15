import wave
import struct
import math

# mu-law decoding table
def mu_law_decode(u_val):
    u_val = ~u_val & 0xFF
    sign = (u_val & 0x80)
    exponent = (u_val & 0x70) >> 4
    mantissa = (u_val & 0x0F)
    sample = (mantissa << 3) + 0x84
    sample <<= exponent
    sample -= 0x84
    return sample if not sign else -sample

def extract_mulaw(filename, output_name, rate=23437.5, max_seconds=40):
    with open(filename, 'rb') as f:
        data = f.read()[0::2] # Left channel

    # Skip patterns area
    start_offset = 6144
    num_samples = int(rate * max_seconds)
    chunk = data[start_offset : start_offset + num_samples]
    
    if not chunk:
        print("No data to extract.")
        return

    decoded = [mu_law_decode(b) for b in chunk]
    
    with wave.open(output_name, 'wb') as wf:
        wf.setnchannels(1)
        wf.setsampwidth(2) # Output as 16-bit PCM
        wf.setframerate(int(rate))
        wf.writeframes(struct.pack(f'<{len(decoded)}h', *decoded))
    print(f"Extracted {len(decoded)} samples (~{len(decoded)/rate:.2f}s) to {output_name}")

if __name__ == "__main__":
    extract_mulaw('big_file_unique_data.bin', 'big_mulaw.wav')
    extract_mulaw('small_file_repeating_data.bin', 'small_mulaw.wav')
