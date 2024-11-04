# DecentryK QR

A Python package for combining and verifying QR codes using cryptographic hashes.

## Installation

```bash
pip install decentryk_qr
```

## Usage

### Command Line Interface

Combine two QR codes:
```bash
decentryk_qr combine --files qr_1.png qr_2.png
```

Verify two QR codes against stored hash:
```bash
decentryk_qr verify --files qr_1.png qr_2.png
```

Additional options:
```bash
# Specify output file for combined QR
decentryk_qr combine --files qr_1.png qr_2.png --output custom_output.png

# Disable hash storage
decentryk_qr combine --files qr_1.png qr_2.png --no-store-hash

# Specify custom hash file location for verification
decentryk_qr verify --files qr_1.png qr_2.png --hash-file custom_hash.json
```

### Python API

```python
from decentryk_qr import QRHashCombiner

# Create processor instance
processor = QRHashCombiner()

# Combine QR codes
combined_hash, hash1, hash2 = processor.process_qr_codes('qr_1.png', 'qr_2.png', 'output.png')

# Verify QR codes
is_valid, current_hash, expected_hash = processor.verify_qr_codes(
    'qr_1.png', 
    'qr_2.png', 
    stored_combined_hash
)
```

## Features

- Combine two QR codes using cryptographic hashing
- Generate a new QR code containing the combined hash
- Verify QR codes against previously stored hashes
- Command-line interface for easy use
- Comprehensive Python API for integration into other projects

## Requirements

- Python 3.6+
- OpenCV
- qrcode
- Pillow
- numpy
- click

## License

MIT License

## Author

Zac Weigold