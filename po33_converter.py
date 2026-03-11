import wave
import struct
import math

class PO33Converter:
    CARRIER_HZ = 7800
    ENCODING_RATE = CARRIER_HZ * 4
    PHASES = {
        (1, 1): 'A',
        (1, 0): 'B',
        (0, 0): 'C',
        (0, 1): 'D'
    }
    
    def __init__(self, sample_rate=44100):
        self.sample_rate = sample_rate
        self.samples_per_bit = sample_rate / self.ENCODING_RATE

    def get_zero_crossings(self, audio_data, threshold=10, min_amplitude=50000):
        """
        Extract zero crossings from audio data, skipping leading silence.
        """
        crossings = []
        last_crossing_time = 0
        
        # Skip until we see real signal
        start_idx = 0
        for i, val in enumerate(audio_data):
            if abs(val) > min_amplitude:
                start_idx = i
                print(f"  Signal detected at sample {i}")
                break
        
        # Track positive and negative peaks for interpolation
        pos_index, pos_val = 0, 0
        neg_index, neg_val = 0, 0
        is_above = True
        
        for i in range(start_idx, len(audio_data)):
            val = audio_data[i]
            if abs(val) < threshold:
                continue
                
            if val >= 0:
                pos_index, pos_val = i, val
                if not is_above:
                    # Transition to positive
                    is_above = True
                    # Interpolate crossing point
                    crossing_time = neg_index + abs(neg_val) / (abs(neg_val) + val + 1e-9) * (i - neg_index)
                    delta = crossing_time - last_crossing_time if last_crossing_time != 0 else 0
                    crossings.append({'side': 1, 'time': crossing_time, 'delta': delta})
                    last_crossing_time = crossing_time
            else:
                neg_index, neg_val = i, val
                if is_above:
                    # Transition to negative
                    is_above = False
                    # Interpolate crossing point
                    crossing_time = pos_index + pos_val / (pos_val + abs(val) + 1e-9) * (i - pos_index)
                    delta = crossing_time - last_crossing_time if last_crossing_time != 0 else 0
                    crossings.append({'side': -1, 'time': crossing_time, 'delta': delta})
                    last_crossing_time = crossing_time
        return crossings

    def crossings_to_bits(self, crossings):
        """
        Convert zero crossings to a bitstream.
        """
        bits = []
        for c in crossings:
            num_bits = round(c['delta'] / self.samples_per_bit)
            bit_val = 0 if c['side'] == 1 else 1
            for _ in range(num_bits):
                bits.append(bit_val)
        return bits

    def bits_to_phases(self, bits):
        """
        Convert bitstream to phases (A, B, C, D).
        Matches the 1-bit shift logic in PO-33-KO-backup-re:
        1. Find first 11
        2. Prepend a 1 to the rest of the stream
        """
        # Find first sync '11'
        start_idx = -1
        for i in range(len(bits) - 1):
            if bits[i] == 1 and bits[i+1] == 1:
                start_idx = i + 2 # Consume the '11'
                break
        
        if start_idx == -1:
            return []
            
        # Add the '1' back (start with the second bit of the sync)
        processed_bits = [1] + bits[start_idx:]
        
        phases = []
        i = 0
        while i + 4 <= len(processed_bits):
            b_pair = (processed_bits[i], processed_bits[i+1])
            phase = self.PHASES.get(b_pair, '-')
            phases.append(phase)
            i += 4
        return phases

    def phases_to_bytes(self, phases):
        """
        Each phase is 2 bits. 4 phases = 1 byte.
        Actually, the RE repo suggests A/B/C/D are just labels for 00, 01, 10, 11 (approx).
        Wait, bitsToPhases in parse.ts says:
        [1, 1] -> A
        [1, 0] -> B
        [0, 0] -> C
        [0, 1] -> D
        This means A=11 (3), B=10 (2), C=00 (0), D=01 (1).
        """
        phase_map = {'A': 3, 'B': 2, 'C': 0, 'D': 1}
        data_bytes = []
        current_byte = 0
        bit_count = 0
        
        for p in phases:
            if p == '-': continue
            val = phase_map[p]
            # Val is 2 bits, pack LSB-first
            current_byte |= (val << bit_count)
            bit_count += 2
            if bit_count == 8:
                data_bytes.append(current_byte)
                current_byte = 0
                bit_count = 0
        return bytes(data_bytes)

    def process_wav(self, file_path):
        with wave.open(file_path, 'rb') as wf:
            params = wf.getparams()
            self.sample_rate = params.framerate
            self.samples_per_bit = self.sample_rate / self.ENCODING_RATE
            
            n_frames = wf.getnframes()
            n_samples = n_frames * params.nchannels
            frames = wf.readframes(n_frames)
            
            print(f"  Sample Rate: {self.sample_rate}")
            print(f"  Channels: {params.nchannels}")
            print(f"  Sample Width: {params.sampwidth} bytes")
            
            audio_left = []
            audio_right = []
            
            # Extract samples based on width
            if params.sampwidth == 1:
                raw = [x - 128 for x in struct.unpack(f'<{n_samples}B', frames)]
            elif params.sampwidth == 2:
                raw = struct.unpack(f'<{n_samples}h', frames)
            elif params.sampwidth == 3:
                raw = []
                for i in range(0, len(frames), 3):
                    raw.append(int.from_bytes(frames[i:i+3], 'little', signed=True))
            else:
                raw = struct.unpack(f'<{n_samples}i', frames)

            if params.nchannels >= 2:
                audio_left = raw[0::params.nchannels]
                audio_right = raw[1::params.nchannels]
            else:
                audio_left = raw
                audio_right = raw # Fallback mono

            print("  Extracting Left channel...")
            data_l = self._decode_channel(audio_left)
            print("  Extracting Right channel...")
            data_r = self._decode_channel(audio_right)
            
            # Interleave bytes: L, R, L, R...
            combined = []
            min_len = min(len(data_l), len(data_r))
            for i in range(min_len):
                combined.append(data_l[i])
                combined.append(data_r[i])
                
            return bytes(combined)

    def _decode_channel(self, audio):
        crossings = self.get_zero_crossings(audio)
        bits = self.crossings_to_bits(crossings)
        phases = self.bits_to_phases(bits)
        return self.phases_to_bytes(phases)

if __name__ == "__main__":
    import sys
    if len(sys.argv) < 2:
        print("Usage: python3 po33_converter.py <input.wav> [output.bin]")
        sys.exit(1)
        
    input_file = sys.argv[1]
    output_file = sys.argv[2] if len(sys.argv) > 2 else "po33_data.bin"
    
    converter = PO33Converter()
    print(f"Processing {input_file}...")
    data = converter.process_wav(input_file)
    
    with open(output_file, 'wb') as f:
        f.write(data)
    print(f"Data written to {output_file} ({len(data)} bytes total)")
