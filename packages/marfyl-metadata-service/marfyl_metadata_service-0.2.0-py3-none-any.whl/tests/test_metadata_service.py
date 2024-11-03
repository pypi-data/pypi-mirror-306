import unittest
from metadata_service.domain.models import MetaData
from metadata_service.domain.services import MetaDataService

class TestMetaDataService(unittest.TestCase):
    def setUp(self):
        self.service = MetaDataService()

    def test_set_meta_data(self):
        header_values = {
            "UserId": "123",
            "Email": "test@example.com",
            "FirstName": "John",
            "LastName": "Doe",
            "SubscriptionId": "sub_456",
            "Accept-Language": "en",
            "ActionIds": "1,2,3",
            "PermissionIds": "1,2"
        }
        self.service.set_meta_data(header_values)
        self.assertEqual(self.service.meta_data.user_id, "123")
        self.assertEqual(self.service.meta_data.email, "test@example.com")
        self.assertEqual(self.service.meta_data.first_name, "John")
        self.assertEqual(self.service.meta_data.full_name, "John Doe")
        self.assertEqual(self.service.meta_data.subscription_id, "sub_456")
        self.assertEqual(self.service.meta_data.language, "en")
        self.assertEqual(self.service.meta_data.action_ids, [1, 2, 3])
        self.assertEqual(self.service.meta_data.permission_ids, [1, 2])

    def test_has_permission(self):
        self.service.meta_data.permission_ids = [1, 2]
        self.assertTrue(self.service.has_permission(1))
        self.assertFalse(self.service.has_permission(3))

if __name__ == '__main__':
    unittest.main()