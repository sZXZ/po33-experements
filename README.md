# PO-33 to Strudel & PICO-8 Workflow

A suite of tools and scripts to convert, analyze, and extract pattern data from Teenage Engineering PO-33 KO backup files. This allows you to audit the sequences of your patterns visually, play them in the browser via [Strudel](https://strudel.cc/), and eventually build custom Pico-8 cartridges.

## Project Structure

- **`data/`**: Storage for `.bin` payloads, raw `.wav` recordings, and test results.
- **`utility/`**: Advanced forensic scripts for entropy analysis, ADPCM decoding, bit-shifting, and sync detection.
- **Root Scripts**: Core tools for conversion and extraction (`po33_converter.py`, `po33_strudel.py`, `po33_reconstitute.py`).

---

## Step 1: Creating `.bin` Files from Audio Backups

To start extracting patterns from your PO-33, you first need to convert the recorded `.wav` backup file into a standardized `.bin` data payload. This step parses the audio differential phase-shift keying (DPSK) modem signal and converts it to raw binary phases.

```bash
python3 po33_converter.py data/backup_2024.wav data/backup_2024.bin
```

*Note: The de-interleaved Left channel typically contains the sync tone followed by actual data at bit offset 2046.*

---

## Step 2: Extracting Notes to Strudel (`.js`)

The `po33_strudel.py` script automatically detects the end of the modem sync tone and extracts the 16 sequencer patterns into Strudel-compatible JavaScript.

```bash
python3 po33_strudel.py data/backup_2024.bin --out data/strudel_patterns.js
```

### Key Features:
- **Auto-Sync**: Automatically bypasses the initial sync tone by detecting the density of unique bytes.
- **Simplified Output**: Uses the concise `n(...)` syntax for easy copy-pasting into Strudel.
- **Pattern Awareness**: Skips empty patterns (patterns consisting entirely of pilot tone or filler).

#### Optional Flags:
- `--interleaved`: Replicates legacy notebook behavior using raw interleaved data.
- `--out`: Specify a custom output path for the JS file.

---

## Step 3: Testing in Strudel

1. Run the extraction script.
2. Open the resulting `.js` file and copy a block.
3. Go to [strudel.cc](https://strudel.cc/).
4. Paste and wrap in a `stack()` for multi-voice playback:
   ```js
   stack(
     n("0 8 3 4 0 8 ~ ~ 0 2 13 11 0 8 ~ ~"),
     n("~ ~ 11 13 ~ ~ 10 9 ~ ~ ~ ~ 11 13 ~ ~")
   )
   ```
5. Press **Ctrl + Enter** to play.

---

## Step 4: Reconstructing WAV Backups

To restore binary data back to the PO-33, use `po33_reconstitute.py` to regenerate the modem signal.

```bash
python3 po33_reconstitute.py data/backup_2024.bin data/restored_backup.wav
```

### Loading into PO-33:
1. Connect line-out to PO-33 line-in.
2. PO-33: Hold `write` + `sound` → `rcv`.
3. Play the generated `.wav` at high volume.

---

## Technical Analysis (Deep Dive)
For those investigating the binary format, the `utility/` folder contains scripts to:
- **`utility/scan_full_entropy.py`**: Visualize where synchronization ends and patterns begin.
- **`utility/decode_adpcm.py`**: Attempt to recover compressed samples.
- **`utility/xor_test.py`**: Check for bit-level scrambling or padding.

Refer to [PO33_DATA_FORMAT.md](PO33_DATA_FORMAT.md) and [PO33_PATTERN_STRUCTURE.md](PO33_PATTERN_STRUCTURE.md) for detailed memory mapping.
