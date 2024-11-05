import unittest
from jwt_manager.exceptions.custom_exceptions import TokenExpiredException, InvalidTokenException

class TestCustomExceptions(unittest.TestCase):
    def test_token_expired_exception(self):
        with self.assertRaises(TokenExpiredException):
            raise TokenExpiredException("Token has expired")

    def test_invalid_token_exception(self):
        with self.assertRaises(InvalidTokenException):
            raise InvalidTokenException("Invalid token")

if __name__ == "__main__":
    unittest.main()