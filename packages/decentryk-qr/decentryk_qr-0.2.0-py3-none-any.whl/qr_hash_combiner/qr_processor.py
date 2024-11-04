import qrcode
from PIL import Image
import hashlib
import hmac
import json
import base64
import os
import time
from datetime import datetime, timedelta
import cv2
import numpy as np
from typing import Tuple, Dict, Union

class QRHashCombiner:
    VERSION = "1.0.0"
    HASH_ITERATIONS = 10000
    KEY_LENGTH = 32
    
    def __init__(self, secret_key: str = None):
        """
        Initialize QRHashCombiner with an optional secret key
        
        Args:
            secret_key (str, optional): Secret key for HMAC. If not provided, a random one will be generated.
        """
        self.secret_key = secret_key or self._generate_secret_key()

    @staticmethod
    def _generate_secret_key() -> str:
        """Generate a random secret key"""
        return base64.b64encode(os.urandom(32)).decode('utf-8')

    def _create_salt(self) -> str:
        """Generate a random salt"""
        return base64.b64encode(os.urandom(16)).decode('utf-8')

    def _create_metadata(self, hash_type: str = 'combine') -> Dict[str, str]:
        """Create metadata for the hash"""
        return {
            'version': self.VERSION,
            'timestamp': datetime.utcnow().isoformat(),
            'type': hash_type,
            'algorithm': f'pbkdf2_sha256_{self.HASH_ITERATIONS}'
        }

    def _advanced_hash(self, content: str, salt: str = None) -> Tuple[str, str]:
        """
        Create a sophisticated hash using PBKDF2 with HMAC-SHA256
        
        Args:
            content: Content to hash
            salt: Optional salt to use
            
        Returns:
            Tuple of (hash, salt)
        """
        if salt is None:
            salt = self._create_salt()
            
        # Create PBKDF2 HMAC hash
        key = hashlib.pbkdf2_hmac(
            'sha256',
            content.encode('utf-8'),
            salt.encode('utf-8'),
            self.HASH_ITERATIONS,
            dklen=self.KEY_LENGTH
        )
        
        # Create HMAC with secret key
        hmac_obj = hmac.new(
            self.secret_key.encode('utf-8'),
            key,
            hashlib.sha256
        )
        
        return base64.b64encode(hmac_obj.digest()).decode('utf-8'), salt

    @staticmethod
    def read_qr(image_path: str) -> str:
        """Read QR code from an image file"""
        image = cv2.imread(image_path)
        if image is None:
            raise ValueError("Could not read image file")
            
        qr_detector = cv2.QRCodeDetector()
        data, bbox, _ = qr_detector.detectAndDecode(image)
        
        if not data:
            raise ValueError("No QR code found in the image")
            
        return data

    def process_qr_codes(self, qr1_path: str, qr2_path: str, output_path: str) -> Tuple[str, Dict[str, Union[str, Dict]]]:
        """
        Process two QR codes and generate a combined QR code with enhanced security
        
        Args:
            qr1_path: Path to first QR code image
            qr2_path: Path to second QR code image
            output_path: Path to save the resulting QR code
            
        Returns:
            Tuple of (combined_hash, full_hash_data)
        """
        # Read QR codes
        content1 = self.read_qr(qr1_path)
        content2 = self.read_qr(qr2_path)

        # Generate salts and hashes
        hash1, salt1 = self._advanced_hash(content1)
        hash2, salt2 = self._advanced_hash(content2)

        # Combine hashes with metadata
        metadata = self._create_metadata()
        combined_content = json.dumps({
            'hash1': hash1,
            'hash2': hash2,
            'metadata': metadata
        }, sort_keys=True)
        
        # Create final combined hash
        combined_hash, combined_salt = self._advanced_hash(combined_content)
        
        # Store all hash information
        hash_data = {
            'combined_hash': combined_hash,
            'combined_salt': combined_salt,
            'metadata': metadata,
            'components': {
                'qr1': {
                    'path': qr1_path,
                    'hash': hash1,
                    'salt': salt1
                },
                'qr2': {
                    'path': qr2_path,
                    'hash': hash2,
                    'salt': salt2
                }
            }
        }

        # Create QR code with combined hash
        self.create_qr(combined_hash, output_path)

        return combined_hash, hash_data

    def verify_qr_codes(self, qr1_path: str, qr2_path: str, stored_hash_data: Dict) -> Tuple[bool, str, Dict]:
        """
        Verify two QR codes against stored hash data with enhanced security
        
        Args:
            qr1_path: Path to first QR code image
            qr2_path: Path to second QR code image
            stored_hash_data: Previously stored hash data
            
        Returns:
            Tuple of (is_valid, message, verification_details)
        """
        try:
            # Extract stored data
            stored_combined_hash = stored_hash_data['combined_hash']
            stored_metadata = stored_hash_data['metadata']
            
            # Verify timestamp if it exists
            if 'timestamp' in stored_metadata:
                stored_time = datetime.fromisoformat(stored_metadata['timestamp'])
                if datetime.utcnow() - stored_time > timedelta(days=30):  # Example expiration
                    return False, "Hash has expired", {'error': 'expired_hash'}

            # Read and hash current QR codes
            content1 = self.read_qr(qr1_path)
            content2 = self.read_qr(qr2_path)
            
            # Generate hashes using stored salts
            hash1, _ = self._advanced_hash(content1, stored_hash_data['components']['qr1']['salt'])
            hash2, _ = self._advanced_hash(content2, stored_hash_data['components']['qr2']['salt'])
            
            # Create combined content
            current_combined = json.dumps({
                'hash1': hash1,
                'hash2': hash2,
                'metadata': stored_metadata
            }, sort_keys=True)
            
            # Generate final hash
            current_hash, _ = self._advanced_hash(current_combined, stored_hash_data['combined_salt'])
            
            # Verify hash
            is_valid = hmac.compare_digest(current_hash.encode(), stored_combined_hash.encode())
            
            verification_details = {
                'timestamp_verified': True,
                'hash_matched': is_valid,
                'verification_time': datetime.utcnow().isoformat()
            }
            
            return is_valid, "Verification successful" if is_valid else "Verification failed", verification_details
            
        except Exception as e:
            return False, f"Verification error: {str(e)}", {'error': str(e)}

    @staticmethod
    def create_qr(content: str, output_path: str) -> None:
        """Create a QR code from content and save it"""
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