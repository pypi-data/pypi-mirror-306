import unittest
from jwt_manager.domain.models import UserData

class TestUserDataModel(unittest.TestCase):
    def test_userdata_initialization(self):
        payload = {
            "UserId": "12345",
            "Email": "user@example.com",
            "FirstName": "John",
            "LastName": "Doe",
            "SubscriptionId": "sub_67890",
            "Accept-Language": "en",
            "ActionIds": "1,2,3",
            "PermissionIds": "4,5,6"
        }
        user_data = UserData(payload)

        self.assertEqual(user_data.UserId, "12345")
        self.assertEqual(user_data.Email, "user@example.com")
        self.assertEqual(user_data.FirstName, "John")
        self.assertEqual(user_data.SubscriptionId, "sub_67890")

if __name__ == "__main__":
    unittest.main()