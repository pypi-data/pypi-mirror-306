import base64

class EncryptionService:
    @staticmethod
    def encrypt(data: str) -> str:
        return base64.b64encode(data.encode()).decode()

    @staticmethod
    def decrypt(data: str) -> str:
        return base64.b64decode(data.encode()).decode()