import unittest
from metadata_service.infrastructure.header_parser import HeaderParser

class TestHeaderParser(unittest.TestCase):
    def test_parse(self):
        headers = {
            "UserId": "123",
            "Email": "test@example.com",
            "FirstName": "John"
        }
        parsed = HeaderParser.parse(headers)
        self.assertEqual(parsed["userid"], "123")
        self.assertEqual(parsed["email"], "test@example.com")
        self.assertEqual(parsed["firstname"], "John")

if __name__ == '__main__':
    unittest.main()