## Header & Scrambling

The PO-33 backup begins with a sync preamble followed by a metadata region.
- **Pattern Start Offset:** The actual pattern data traditionally starts after a **2048-byte (2KB)** header area (which includes sync tones).
- **Patterns:** 16
- **Pattern Size:** 256 bytes per pattern.
- **Auto-Sync:** The `po33_strudel.py` script automatically detects the end of the sync tone by scanning for a sudden increase in byte entropy and starts extraction from that point.

### Scrambling Warning
As of recent analysis, it has been discovered that even if patterns are musically identical (cloned), their binary representation in the `.bin` file differs. This suggests the pattern memory is **scrambled** or **obfuscated** at the bit level. The note values extracted by current scripts are a direct interpretation of the bits, but may require a descrambling pass for perfect accuracy across all devices.

## Pattern Internal Structure

Each 256-byte pattern block is divided into a grid representing **16 Steps** across **4 Voices**.

### Hierarchy
- **1 Pattern (256 bytes)** = 16 Steps
- **1 Step (16 bytes)** = 4 Voices
- **1 Voice/Step (4 bytes / 16 phases)** = Note Event Data

### Offset Calculation
`Internal_Offset = (PatternID * 256) + (StepID * 16) + (VoiceID * 4)`

## Data Grid (Observed)

| Step | Offset | Voice 1 | Voice 2 | Voice 3 | Voice 4 |
| :--- | :--- | :--- | :--- | :--- | :--- |
| **1** | `0x00` | 4 bytes | 4 bytes | 4 bytes | 4 bytes |
| **2** | `0x10` | ... | ... | ... | ... |
| ... | ... | ... | ... | ... | ... |
| **16** | `0xF0` | 4 bytes | 4 bytes | 4 bytes | 4 bytes |

### Phase Values & Filler
Data is stored as 2-bit phases (0-3).
- **Filler/Empty Byte (AA):** Encoded as repeating phase `2` (`10` in binary). Note that some backups may not use `0xAA` if they are scrambled or use a different filler.
- **Event Data:** Non-repeating phase sequences indicate triggers, pitches, and sound assignments.

## Decompilation Rules
1. **LSB-First Unpacking:** Each byte must be unpacked using `(b & 0x03)`, `((b >> 2) & 0x03)`, etc.
2. **Step Repetition:** In many motifs, the PO-33 repeats the same 16-byte step block across multiple grid positions (e.g., Steps 1-4 are identical if no sub-step offsets are used).
