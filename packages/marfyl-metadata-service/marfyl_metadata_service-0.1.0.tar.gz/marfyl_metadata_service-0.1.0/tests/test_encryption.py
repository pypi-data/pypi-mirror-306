import unittest
from metadata_service.infrastructure.encryption import EncryptionService

class TestEncryptionService(unittest.TestCase):
    def test_encryption_decryption(self):
        original_data = "Sensitive Data"
        encrypted_data = EncryptionService.encrypt(original_data)
        decrypted_data = EncryptionService.decrypt(encrypted_data)
        self.assertEqual(original_data, decrypted_data)

if __name__ == '__main__':
    unittest.main()