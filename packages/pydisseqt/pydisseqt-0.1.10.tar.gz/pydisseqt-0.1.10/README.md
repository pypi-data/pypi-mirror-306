Python wrapper around [disseqt](https://github.com/pulseq-frame/disseqt) built using https://github.com/PyO3/maturin

# Changelog:

### 0.1.10
- Updated pulseq-rs: can now load .seq files using the rfshim pTx extension

### 0.1.9
- Updated disseqt: Now respects ref_voltage for correct units on .dsv import

### 0.1.8
- Updated disseqt: Make pulse phase (RFP) file optional as it is not always provided

### 0.1.5
- Switched to WIP disseqt that includes a .dsv backend

### 0.1.4
- Updated disseqt: allow backwards integration in integrate and integrate_one (t_start >= t_end)

### 0.1.3
- Updated disseqt, fixed trap integration bug

### 0.1.2
- Updated pulseq-rs: allow empty .seq file sections

### 0.1.1
- Updated disseqt, use double precision floats

### 0.1.0
Baseline
