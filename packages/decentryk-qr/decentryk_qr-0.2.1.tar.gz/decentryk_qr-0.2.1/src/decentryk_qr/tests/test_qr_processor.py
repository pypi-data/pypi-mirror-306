# qr_hash_combiner/tests/test_qr_processor.py
import pytest
import os
from src.decentryk_qr.qr_processor import QRHashCombiner  # This is the correct import path
import qrcode

class TestQRHashCombiner:
    @pytest.fixture
    def processor(self):
        return QRHashCombiner()

    @pytest.fixture
    def sample_qr_files(self):
        # Create temporary QR codes for testing
        qr1_path = "test_qr1.png"
        qr2_path = "test_qr2.png"
        
        # Create first QR code
        qr = qrcode.QRCode()
        qr.add_data("Test content 1")
        qr.make(fit=True)
        img = qr.make_image()
        img.save(qr1_path)
        
        # Create second QR code
        qr = qrcode.QRCode()
        qr.add_data("Test content 2")
        qr.make(fit=True)
        img = qr.make_image()
        img.save(qr2_path)
        
        yield qr1_path, qr2_path
        
        # Cleanup
        os.remove(qr1_path)
        os.remove(qr2_path)

    def test_read_qr(self, processor, sample_qr_files):
        qr1_path, _ = sample_qr_files
        content = processor.read_qr(qr1_path)
        assert content == "Test content 1"

    def test_hash_content(self, processor):
        content = "test"
        hash_result = processor.hash_content(content)
        assert isinstance(hash_result, str)
        assert len(hash_result) == 64  # SHA-256 produces 64 character hex string

    def test_combine_hashes(self, processor):
        hash1 = "a" * 64
        hash2 = "b" * 64
        combined = processor.combine_hashes(hash1, hash2)
        assert isinstance(combined, str)
        assert len(combined) == 64

    def test_create_qr(self, processor):
        output_path = "test_output.png"
        processor.create_qr("test content", output_path)
        assert os.path.exists(output_path)
        os.remove(output_path)

    def test_process_qr_codes(self, processor, sample_qr_files):
        qr1_path, qr2_path = sample_qr_files
        output_path = "test_combined.png"
        
        combined_hash = processor.process_qr_codes(qr1_path, qr2_path, output_path)
        
        assert isinstance(combined_hash, str)
        assert len(combined_hash) == 64
        assert os.path.exists(output_path)
        
        os.remove(output_path)

    def test_invalid_qr_code(self, processor):
        with pytest.raises(ValueError):
            processor.read_qr("nonexistent_file.png")