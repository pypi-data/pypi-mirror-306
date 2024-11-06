import unittest
from unittest.mock import patch
from jwt_manager.domain.services import JWTManager
from jwt_manager import generate_token_for_user
from jwt_manager.domain.models import UserData
from fastapi import Request, HTTPException

def user_data_equal(user_data1: UserData, user_data2: UserData) -> bool:
    """
    To compare twi+o instance UserData
    :param user_data1:
    :param user_data2:
    :return:
    """
    return (
        user_data1.user_id == user_data2.user_id and
        user_data1.email == user_data2.email and
        user_data1.first_name == user_data2.first_name and
        user_data1.last_name == user_data2.last_name and
        user_data1.subscription_id == user_data2.subscription_id and
        user_data1.language == user_data2.language and
        user_data1.action_ids == user_data2.action_ids and
        user_data1.permission_ids == user_data2.permission_ids
    )

class TestJWTFunctions(unittest.TestCase):
    def setUp(self):
        self.jwt_manager = JWTManager(secret_key="your-default-secret-key", algorithm="HS256", expires_in=30)
        self.valid_payload = {
            "UserId": "12345",
            "Email": "user@example.com"
        }
        self.valid_user_data = UserData(self.valid_payload)
        self.valid_token = self.jwt_manager.create_token(self.valid_user_data)

    @patch('jwt_manager.domain.services.JWTManager.create_token')
    def test_generate_token_for_user_success(self, mock_create_token):
        mock_create_token.return_value = self.valid_token

        token = generate_token_for_user(self.valid_payload)

        self.assertEqual(token, self.valid_token)

        mock_create_token.assert_called_once()
        actual_user_data = mock_create_token.call_args[0][0]

        self.assertTrue(user_data_equal(actual_user_data, self.valid_user_data))


    @patch('jwt_manager.domain.services.JWTManager.create_token')
    def test_generate_token_for_user_exception(self, mock_create_token):
        mock_create_token.side_effect = Exception("Error generating token")

        with self.assertRaises(HTTPException) as context:
            generate_token_for_user(self.valid_payload)

        self.assertEqual(context.exception.status_code, 401)
        self.assertEqual(context.exception.detail, "Error generating token")

if __name__ == "__main__":
    unittest.main()