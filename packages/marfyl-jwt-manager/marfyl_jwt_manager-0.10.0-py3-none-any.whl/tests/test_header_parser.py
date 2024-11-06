import unittest
from fastapi import Request
from starlette.datastructures import Headers
from jwt_manager.infrastructure.header_parser import extract_token_from_header

class MockRequest:
    def __init__(self, headers):
        self.headers = Headers(headers)

class TestHeaderParser(unittest.TestCase):
    def test_extract_token_valid_header(self):
        request = MockRequest({"Authorization": "Bearer valid.token"})
        token = extract_token_from_header(request)
        self.assertEqual(token, "valid.token")

    def test_extract_token_missing_header(self):
        request = MockRequest({})
        with self.assertRaises(Exception):
            extract_token_from_header(request)

if __name__ == "__main__":
    unittest.main()