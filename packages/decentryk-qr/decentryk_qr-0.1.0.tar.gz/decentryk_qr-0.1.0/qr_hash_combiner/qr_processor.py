import qrcode
from PIL import Image
import hashlib
import io
import cv2
import numpy as np

class QRHashCombiner:
    @staticmethod
    def read_qr(image_path):
        """
        Read QR code from an image file using OpenCV
        
        Args:
            image_path (str): Path to the QR code image
            
        Returns:
            str: Decoded QR code content
        """
        # Read image using OpenCV
        image = cv2.imread(image_path)
        if image is None:
            raise ValueError("Could not read image file")
            
        # Initialize QR Code detector
        qr_detector = cv2.QRCodeDetector()
        
        # Detect and decode QR code
        data, bbox, _ = qr_detector.detectAndDecode(image)
        
        if not data:
            raise ValueError("No QR code found in the image")
            
        return data

    @staticmethod
    def hash_content(content, algorithm='sha256'):
        """
        Hash the content using the specified algorithm
        
        Args:
            content (str): Content to hash
            algorithm (str): Hashing algorithm to use (default: sha256)
            
        Returns:
            str: Hexadecimal hash
        """
        hasher = hashlib.new(algorithm)
        hasher.update(content.encode('utf-8'))
        return hasher.hexdigest()

    @staticmethod
    def combine_hashes(hash1, hash2):
        """
        Combine two hashes to create a new hash
        
        Args:
            hash1 (str): First hash
            hash2 (str): Second hash
            
        Returns:
            str: Combined hash
        """
        combined = hash1 + hash2
        return hashlib.sha256(combined.encode('utf-8')).hexdigest()

    @staticmethod
    def create_qr(content, output_path):
        """
        Create a QR code from content and save it
        
        Args:
            content (str): Content to encode in QR
            output_path (str): Path to save the QR code image
        """
        qr = qrcode.QRCode(
            version=1,
            error_correction=qrcode.constants.ERROR_CORRECT_L,
            box_size=10,
            border=4,
        )
        qr.add_data(content)
        qr.make(fit=True)

        img = qr.make_image(fill_color="black", back_color="white")
        img.save(output_path)

    def process_qr_codes(self, qr1_path, qr2_path, output_path):
        """
        Process two QR codes and generate a combined QR code
        
        Args:
            qr1_path (str): Path to first QR code image
            qr2_path (str): Path to second QR code image
            output_path (str): Path to save the resulting QR code
            
        Returns:
            str: The combined hash value
        """
        # Read QR codes
        content1 = self.read_qr(qr1_path)
        content2 = self.read_qr(qr2_path)

        # Hash contents
        hash1 = self.hash_content(content1)
        hash2 = self.hash_content(content2)

        # Combine hashes
        combined_hash = self.combine_hashes(hash1, hash2)

        # Create new QR code
        self.create_qr(combined_hash, output_path)

        return combined_hash