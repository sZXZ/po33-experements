# PO-33 to Strudel & PICO-8 Workflow

A suite of tools and scripts to convert, analyze, and extract pattern data from Teenage Engineering PO-33 KO backup files. This allows you to audit the sequences of your patterns visually, play them in the browser via [Strudel](https://strudel.cc/), and eventually build custom Pico-8 cartridges out of the notes and samples.

## Step 1: Creating `.bin` Files from Audio Backups

To start extracting patterns from your PO-33, you first need to convert the recorded `.wav` backup file into a standardized `.bin` data payload. This step parses the audio differential phase-shift keying (DPSK) modem signal and converts it to raw binary phases.

Use the `po33_converter.py` script to generate the `.bin` file:

```bash
python3 po33_converter.py <input_backup.wav> [optional_output_name.bin]
```

**Example:**
```bash
python3 po33_converter.py backup_260311-210744.WAV my_data_v3.bin
```

This extracts both Left and Right channels, parses the zero crossings, and creates the `.bin` file. *Note: this `.bin` file contains both stereo channels interleaved as well as the initial continuous transmission sync tone (pilot tone).*

## Step 2: Extracting Notes to Strudel (`.js`)

You can use the `po33_strudel.py` script to read the raw phases from the `.bin` file, decompile the 4-phase blocks into sequences, and output readable JavaScript notes formatted as `note("...").scale("C major")` for Strudel.

```bash
python3 po33_strudel.py [input_file.bin] [options]
```

### Examples

**Basic Conversion:**
Parse the data starting from the beginning and save the output to the default `strudel_patterns.js` file:
```bash
python3 po33_strudel.py my_data_v3.bin
```

**Skipping the "Pilot Tone" (Recommended Troubleshooting):**
PO-33 backups generally start with 2-3 seconds of a continuous transmission sync tone (which decodes as repeating `[0xaa, 0xaa, 0x42, 0xbd...]` bytes). If you scan from `offset 0`, the first few patterns decoded might just be this sync tone representing "notes". You can bypass the tone by specifying a starting byte offset.

For example, to skip the first 16,000 bytes:
```bash
python3 po33_strudel.py my_data_v3.bin --offset 16000
```

**Custom Output File:**
To save the generated JavaScript strudel notes into a different file:
```bash
python3 po33_strudel.py my_data_v3.bin --out my_custom_jam.js
```

**Interleaved Bug Simulation:**
The original Jupyter notebook didn't correctly separate the Left and Right stereo channels, reading interleaved data directly. If you want to replicate that behavior to see how it affected note generation (such as consistently yielding `13` or `2`), use the `--interleaved` flag:
```bash
python3 po33_strudel.py my_data_v3.bin --interleaved
```

## Step 3: Testing Your Strudel Patterns

1. Run the script to generate your `.js` file.
2. Open the resulting `strudel_patterns.js` file and copy one or more voices from an interesting pattern.
3. Go to [strudel.cc](https://strudel.cc/).
4. Paste the copied JS line directly into the web editor.
   ```js
   // You can paste the block like this:
   stack(
   n("~ ~ ~ ~ 2 4 13 11 2 4 13 11 2 4 13 11"), // Voice 1
   n("13 11 2 4 13 11 2 4 13 11 2 4 13 11 2 4")  // Voice 2
   )
   // Make sure to remove the comma from the very last line you evaluate!
   ```
5. Press **Ctrl + Enter** (or click "Play" in the top right) to instantly hear the exact sequences!

## Step 4: Reconstructing WAV Backups

If you have modified a `.bin` file or want to restore your data back to the PO-33, you can reconstruct an audio backup from the binary data using the `po33_reconstitute.py` script. This script converts the binary phases back into a differential phase-shift keying (DPSK) modem audio signal that the PO-33 can receive via its audio input.

Run the script to generate the `.wav` file:

```bash
python3 po33_reconstitute.py <input_data.bin> [optional_output.wav]
```

**Example:**
```bash
python3 po33_reconstitute.py my_data_v3.bin restored_backup.wav
```

To load the reconstructed backup back into your PO-33:
1. Connect your computer's audio output to the PO-33's line-in (left side).
2. Put the PO-33 into receive mode (press `write` + `sound` so it shows `rcv` on the screen).
3. Turn your computer's stereo output volume up to maximum (or a high, distortion-free level).
4. Play the generated `.wav` file.
