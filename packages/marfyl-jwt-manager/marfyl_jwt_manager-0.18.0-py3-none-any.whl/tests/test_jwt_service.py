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
        user_data1.UserId == user_data2.UserId and
        user_data1.Email == user_data2.Email and
        user_data1.FirstName == user_data2.FirstName and
        user_data1.LastName == user_data2.LastName and
        user_data1.SubscriptionId == user_data2.SubscriptionId and
        user_data1.Language == user_data2.Language and
        user_data1.ActionIds == user_data2.ActionIds and
        user_data1.PermissionIds == user_data2.PermissionIds
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