import struct
import math

class Pico8Exporter:
    """
    Exports PO-33 data to PICO-8 format.
    Focuses on mapping samples to SFX 0-7 (custom instruments).
    """
    
    @staticmethod
    def mu_law_decode(mu):
        """Decode µ-law sample to linear PCM."""
        mu = ~mu & 0xFF
        sign = (mu & 0x80)
        exponent = (mu & 0x70) >> 4
        mantissa = (mu & 0x0F)
        
        data = (mantissa << 3) + 0x84
        data <<= (exponent)
        data = data - 0x84
        
        if sign:
            return -data
        else:
            return data

    def extract_pcm(self, data):
        """Extract raw linear PCM from PO-33 binary data."""
        # Un-interleave if it's dual channel (we'll just use Left for simplicity)
        # or treat the whole stream as a single source for now.
        return [self.mu_law_decode(b) for b in data]

    def create_p8_cart(self, pcm_data, config_list=None, pattern_map=None, melodies=None, output_path="output.p8"):
        sfx_data = {}
        
        # 1. Instruments (0-7)
        if config_list:
            for conf in config_list:
                s_id = int(conf.get('sfx_id', 0))
                start = int(conf.get('start_byte', 0))
                end = int(conf.get('end_byte', len(pcm_data)))
                speed = int(conf.get('speed', 1))
                sfx_data[s_id] = self._generate_sample_sfx(s_id, pcm_data[start:end], speed)

        # 2. Sequential SFX (Patterns 8-63)
        if melodies:
            for mel in melodies:
                m_id = mel.get('sfx_id')
                speed = mel.get('speed', 16)
                notes = mel.get('notes', []) # [(step, pitch, inst, vol)]
                sfx_data[m_id] = self._generate_melody_sfx(m_id, speed, notes)

        # Build final .p8 file
        header = (
            "pico-8 cartridge // http://www.pico-8.com\n"
            "version 32\n"
            "__lua__\n"
            "function _init()\n"
            "  cls()\n"
            "  print(\"po-33 pattern 1 loaded\")\n"
            "end\n"
        )
        
        with open(output_path, 'w') as f:
            f.write(header)
            f.write("__sfx__\n")
            for i in range(64):
                if i in sfx_data:
                    f.write(sfx_data[i] + "\n")
                else:
                    f.write(f"{i:02x}100000" + "0000" * 32 + "\n")
            
            f.write("__music__\n")
            if pattern_map:
                for p_id, p_conf in enumerate(pattern_map):
                    channels = p_conf.get('channels', [64, 64, 64, 64]) 
                    ch_hex = " ".join([f"{c:02x}" for c in channels])
                    f.write(f"{p_id:02x} 00 {ch_hex}\n")

    def _pack_note(self, pitch, instrument, volume, effect=0):
        """Correctly packs PICO-8 note data into 4 hex digits (2 bytes)."""
        pitch = max(0, min(63, int(pitch)))
        instrument = max(0, min(15, int(instrument)))
        volume = max(0, min(7, int(volume)))
        effect = max(0, min(7, int(effect)))
        
        # Byte 0: Pitch (bits 0-5) + Instrument low (bits 6-7)
        b0 = (pitch & 0x3F) | ((instrument & 0x03) << 6)
        # Byte 1: Instrument high (bits 0-1) + Volume (bits 2-4) + Effect (bits 5-7)
        b1 = ((instrument & 0x0C) >> 2) | ((volume & 0x07) << 2) | ((effect & 0x07) << 5)
        
        return f"{b0:02x}{b1:02x}"

    def _generate_sample_sfx(self, sfx_id, pcm_chunk, speed):
        """Generates a PICO-8 SFX for a raw sample slice."""
        header = f"{sfx_id:02x}{speed:02x}0000"
        notes = []
        step = max(1, len(pcm_chunk) // 32)
        for i in range(32):
            pitch = 0
            if i * step < len(pcm_chunk):
                sample = pcm_chunk[i * step]
                pitch = int((sample + 32768) / 65536 * 63)
            # Use correct packing: instrument 0 (triangle), volume 7, no effect
            notes.append(self._pack_note(pitch, 0, 7, 0))
        return header + "".join(notes)

    def _generate_melody_sfx(self, sfx_id, speed, note_list):
        """Generates a PICO-8 SFX for a melody using sounds 0-7 as instruments."""
        header = f"{sfx_id:02x}{speed:02x}0000"
        notes = [self._pack_note(0, 0, 0, 0)] * 32  # Default to silent
        for step_idx, pitch, inst, vol in note_list:
            if step_idx < 32:
                notes[step_idx] = self._pack_note(pitch, inst, vol, 0)
        return header + "".join(notes)

if __name__ == "__main__":
    import sys
    print("This script is now modular and should be imported into your notebooks.")
    print("Example usage:")
    print("  from pico8_exporter import Pico8Exporter")
    print("  exporter = Pico8Exporter()")
    print("  pcm = exporter.extract_pcm(data_bytes)")
    print("  exporter.create_p8_cart(pcm, config_list, 'my_cart.p8')")
