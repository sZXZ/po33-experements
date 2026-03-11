import wave
import struct
import math

class PO33Reconstitutor:
    CARRIER_HZ = 7800
    PI = math.pi
    
    PHASE_MAP = {
        3: 'A',
        2: 'B',
        0: 'C',
        1: 'D'
    }

    def __init__(self, sample_rate=48000, amplitude=28000):
        self.sample_rate = sample_rate
        self.amplitude = amplitude

    def get_oscillator_value(self, phase, radians):
        if phase == 'A':
            return math.sin(radians)
        elif phase == 'B':
            return math.cos(radians)
        elif phase == 'C':
            return -math.sin(radians)
        elif phase == 'D':
            return -math.cos(radians)
        else:
            return 0

    def get_envelope_value(self, radians):
        # Logic from RE repo: mix from 1.2*PI to 1.8*PI
        start = 1.2 * self.PI
        end = 1.8 * self.PI
        if radians < start:
            return 0
        if radians > end:
            return 1
        return (radians - start) / (end - start)

    def mix(self, amount, val_a, val_b):
        return val_a * (1 - amount) + val_b * amount

    def bytes_to_phases(self, data):
        """Unpack interleaved bytes L, R, L, R..."""
        phases_l = []
        phases_r = []
        for i in range(0, len(data), 2):
            l_byte = data[i]
            r_byte = data[i+1] if i+1 < len(data) else 0
            
            # Left channel phases
            phases_l.extend(self._byte_to_phases(l_byte))
            # Right channel phases
            phases_r.extend(self._byte_to_phases(r_byte))
            
        return phases_l, phases_r

    def _byte_to_phases(self, byte):
        p1 = byte & 0x03
        p2 = (byte >> 2) & 0x03
        p3 = (byte >> 4) & 0x03
        p4 = (byte >> 6) & 0x03
        return [self.PHASE_MAP[p] for p in [p1, p2, p3, p4]]

    def phases_to_audio(self, phases_l, phases_r):
        samples_per_cycle = self.sample_rate / self.CARRIER_HZ
        sample_to_radians = 2 * self.PI / samples_per_cycle
        
        # Calibration preamble: The original repo doesn't explicitly define it,
        # but the PO-33 uses a long carrier 'A' sequence at the start.
        sync_len = int(self.CARRIER_HZ * 2.0) 
        phases_l = (['A'] * sync_len) + phases_l
        phases_r = (['A'] * sync_len) + phases_r
        
        audio_samples = []
        sample_index = 0
        radians_start = 0
        
        max_len = max(len(phases_l), len(phases_r))
        
        for i in range(max_len - 1):
            this_l = phases_l[i] if i < len(phases_l) else 'A'
            next_l = phases_l[i+1] if i+1 < len(phases_l) else 'A'
            this_r = phases_r[i] if i < len(phases_r) else 'A'
            next_r = phases_r[i+1] if i+1 < len(phases_r) else 'A'
            
            while True:
                radians = sample_index * sample_to_radians
                if radians > radians_start + 2 * self.PI:
                    break
                
                mix_val = self.get_envelope_value(radians - radians_start)
                
                # Left Channel
                sl = self.mix(mix_val, self.get_oscillator_value(this_l, radians), 
                                     self.get_oscillator_value(next_l, radians))
                # Right Channel
                sr = self.mix(mix_val, self.get_oscillator_value(this_r, radians), 
                                     self.get_oscillator_value(next_r, radians))
                
                audio_samples.append(int(sl * self.amplitude))
                audio_samples.append(int(sr * self.amplitude))
                
                sample_index += 1
            
            radians_start += 2 * self.PI
            
        return audio_samples

    def save_wav(self, samples, output_path):
        with wave.open(output_path, 'wb') as wf:
            wf.setnchannels(2) # STEREO
            wf.setsampwidth(2) # 16-bit
            wf.setframerate(self.sample_rate)
            
            fmt = '<' + ('h' * len(samples))
            data = struct.pack(fmt, *samples)
            wf.writeframes(data)

if __name__ == "__main__":
    import sys
    if len(sys.argv) < 2:
        print("Usage: python3 po33_reconstitute.py <data.bin> [output.wav]")
        sys.exit(1)
        
    input_file = sys.argv[1]
    output_file = sys.argv[2] if len(sys.argv) > 2 else "reconstituted.wav"
    
    with open(input_file, 'rb') as f:
        data = f.read()
        
    reconstitutor = PO33Reconstitutor()
    print(f"Reconstituting {input_file}...")
    phases_l, phases_r = reconstitutor.bytes_to_phases(data)
    samples = reconstitutor.phases_to_audio(phases_l, phases_r)
    reconstitutor.save_wav(samples, output_file)
    print(f"WAV written to {output_file} ({len(samples)} samples)")
