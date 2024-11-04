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

### Python API

```python
from decentryk_qr import QRHashCombiner

# Create processor instance
processor = QRHashCombiner()

# Combine QR codes
combined_hash, hash_data = processor.process_qr_codes(
    'qr_1.png', 
    'qr_2.png', 
    'output.png'
)
```

## Features

- Combine two QR codes using cryptographic hashing
- Generate a new QR code containing the combined hash
- Command-line interface for easy use
- Python API for integration into other projects

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