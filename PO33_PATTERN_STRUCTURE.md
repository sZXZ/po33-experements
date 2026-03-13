# PO-33 Pattern Memory Map (Reverse Engineered)

This document describes the structure and encoding of the 16 sequencer patterns found in the first 4096 bytes of a PO-33 backup binary file.

## Header Overview

The PO-33 backup begins with a **4096-byte (4KB)** metadata header.
- **Total Patterns:** 16
- **Pattern Size:** 256 bytes (1024 phases)
- **Offset Range:** `0x0000` to `0x0FFF`

## Pattern Internal Structure

Each 256-byte pattern block is divided into a grid representing **16 Steps** across **4 Voices**.

### Hierarchy
- **1 Pattern (256 bytes)** = 16 Steps
- **1 Step (16 bytes)** = 4 Voices
- **1 Voice/Step (4 bytes / 16 phases)** = Note Event Data

### Offset Calculation
To find the start of a specific note event:
`Offset = (PatternID * 256) + (StepID * 16) + (VoiceID * 4)`

## Data Grid (Observed)

| Step | Offset | Voice 1 | Voice 2 | Voice 3 | Voice 4 |
| :--- | :--- | :--- | :--- | :--- | :--- |
| **1** | `0x00` | 4 bytes | 4 bytes | 4 bytes | 4 bytes |
| **2** | `0x10` | ... | ... | ... | ... |
| ... | ... | ... | ... | ... | ... |
| **16** | `0xF0` | 4 bytes | 4 bytes | 4 bytes | 4 bytes |

### Phase Values & Filler
Data is stored as 2-bit phases (0-3).
- **Filler/Empty Byte (AA):** Encoded as repeating phase `2` (`10` in binary).
- **Event Data:** Non-repeating phase sequences indicate triggers, pitches, and sound assignments.

## Decompilation Rules
1. **LSB-First Unpacking:** Each byte must be unpacked using `(b & 0x03)`, `((b >> 2) & 0x03)`, etc.
2. **Step Repetition:** In many motifs, the PO-33 repeats the same 16-byte step block across multiple grid positions (e.g., Steps 1-4 are often identical if no sub-step offsets are used).
