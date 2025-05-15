import unittest
from SukiScan import create_app, db
from SukiScan.config import TestConfig



class BasicTests(unittest.TestCase):
    def setUp(self):
        self.app = create_app(TestConfig)  # Pass in 'testing' config
        self.app_context = self.app.app_context()
        self.app_context.push()
        self.client = self.app.test_client()
        db.create_all()

    def tearDown(self):
        db.session.remove()
        db.drop_all()
        self.app_context.pop()

    def test_home_status_code(self):
        response = self.client.get('/')
        self.assertEqual(response.status_code, 200)

if __name__ == "__main__":
    unittest.main()