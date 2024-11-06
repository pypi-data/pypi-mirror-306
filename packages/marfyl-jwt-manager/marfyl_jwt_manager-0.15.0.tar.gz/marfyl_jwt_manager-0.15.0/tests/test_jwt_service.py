import unittest
from unittest.mock import Mock, patch
from fastapi import Request, HTTPException
from jwt_manager.domain.services import JWTManager
from jwt_manager.infrastructure.header_parser import extract_token_from_header
from jwt_manager import generate_token_for_user, get_current_user


class TestJWTFunctions(unittest.TestCase):
    def setUp(self):
        self.jwt_manager = JWTManager(secret_key="your-default-secret-key", algorithm="HS256", expires_in=30)
        self.valid_payload = {
            "UserId": "12345",
            "Email": "user@example.com"
        }
        self.valid_token = self.jwt_manager.create_token(self.valid_payload)

    @patch('jwt_manager.domain.services.JWTManager.create_token')
    def test_generate_token_for_user_success(self, mock_create_token):
        mock_create_token.return_value = self.valid_token

        token = generate_token_for_user(self.valid_payload)

        self.assertEqual(token, self.valid_token)
        mock_create_token.assert_called_once_with(self.valid_payload)

    @patch('jwt_manager.domain.services.JWTManager.create_token')
    def test_generate_token_for_user_exception(self, mock_create_token):
        mock_create_token.side_effect = Exception("Error generating token")

        with self.assertRaises(HTTPException) as context:
            generate_token_for_user(self.valid_payload)

        self.assertEqual(context.exception.status_code, 401)
        self.assertEqual(context.exception.detail, "Error generating token")

if __name__ == "__main__":
    unittest.main()