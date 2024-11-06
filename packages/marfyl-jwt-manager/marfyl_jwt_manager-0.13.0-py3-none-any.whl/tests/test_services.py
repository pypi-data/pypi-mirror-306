import unittest
from jwt import encode
from jwt_manager.domain.services import JWTManager
from jwt_manager.exceptions.custom_exceptions import TokenExpiredException, InvalidTokenException
from jwt_manager.application.config import SECRET_KEY
from datetime import datetime, timedelta

class TestJWTManager(unittest.TestCase):
    def setUp(self):
        self.jwt_manager = JWTManager(SECRET_KEY)
        self.valid_payload = {
            "UserId": "12345",
            "Email": "user@example.com"
        }
        self.valid_token = encode(self.valid_payload, SECRET_KEY, algorithm="HS256")

    def test_decode_valid_token(self):
        user_data = self.jwt_manager.decode_token(self.valid_token)
        self.assertEqual(user_data.UserId, "12345")
        self.assertEqual(user_data.Email, "user@example.com")

    def test_decode_invalid_token(self):
        with self.assertRaises(InvalidTokenException):
            self.jwt_manager.decode_token("invalid.token.here")

    def test_decode_expired_token(self):
        expired_payload = self.valid_payload.copy()
        expired_payload["exp"] = datetime.utcnow() - timedelta(seconds=1)
        expired_token = encode(expired_payload, SECRET_KEY, algorithm="HS256")

        with self.assertRaises(TokenExpiredException):
            self.jwt_manager.decode_token(expired_token)

if __name__ == "__main__":
    unittest.main()