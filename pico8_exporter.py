import struct
import math

class Pico8Exporter:
    """
    Exports PO-33 data to PICO-8 format.
    PICO-8 samples are typically 8-bit, 5512.5Hz.
    PO-33 samples are 8-bit µ-law, 23437.5Hz.
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

    @staticmethod
    def convert_to_p8_wav(data):
        """
        PICO-8 sfx data is stored in the __sfx__ section.
        Each SFX is 64 notes (4 bytes each).
        However, the user wants to convert PO-33 to PICO-8 cartridge.
        The most common way is to fill the SFX memory with PWM samples.
        """
        # Linear PCM conversion
        pcm = [Pico8Exporter.mu_law_decode(b) for b in data]
        
        # Normalize to PICO-8 range (0-255 for custom PCM if using that, but SFX uses notes)
        # Actually, let's just create a raw text format for __sfx__ or __map__
        # For an example, we'll just output the first few samples as SFX note data (very lossy)
        return pcm

    def create_p8_cart(self, pcm_data, output_path):
        """Creates a basic .p8 file template."""
        with open(output_path, 'w') as f:
            f.write("pico-8 cartridge // http://www.pico-8.com\n")
            f.write("version 32\n")
            f.write("__lua__\n")
            f.write("-- po33 to pico8 conversion\n")
            f.write("function _init()\n  print(\"po-33 data loaded\")\nend\n\n")
            f.write("__sfx__\n")
            # Fill SFX 0 with some data from the samples
            # This is a dummy implementation just to show the data is being passed
            for sfx_id in range(64):
                f.write(f"{sfx_id:02x}010000") # Setup SFX speed 1, looping 0
                for i in range(32):
                    # Each note is 2 bytes (pitch, waveform, etc.)
                    # Very rough mapping: use PCM value as pitch
                    val = 0
                    idx = sfx_id * 32 + i
                    if idx < len(pcm_data):
                        val = int((pcm_data[idx] + 32768) / 65536 * 63)
                    f.write(f"{val:02x}00") # wave 0 (triangle), volume 0-7
                f.write("\n")

if __name__ == "__main__":
    import sys
    if len(sys.argv) < 2:
        print("Usage: python3 pico8_exporter.py <data.bin> [output.p8]")
        sys.exit(1)
        
    data_path = sys.argv[1]
    output_path = sys.argv[2] if len(sys.argv) > 2 else "converted.p8"
    
    with open(data_path, 'rb') as f:
        data = f.read()
    
    exporter = Pico8Exporter()
    pcm = exporter.convert_to_p8_wav(data)
    exporter.create_p8_cart(pcm, output_path)
    print(f"PICO-8 cart created: {output_path}")
