import unittest
from SukiScan import create_app, db
from SukiScan.models import User
from SukiScan.config import TestConfig 

class BasicTests(unittest.TestCase):
    def setUp(self):
        self.app = create_app(TestConfig) 
        self.app_context = self.app.app_context()
        self.app_context.push()
        db.create_all()
        self.client = self.app.test_client()

    def tearDown(self):
        db.session.remove()
        db.drop_all()
        self.app_context.pop()

    def test_index_page(self):
        response = self.client.get('/')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b"SukiScan", response.data)  
    
    def test_home_page(self):
        response = self.client.get('/home')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b"Welcome to SukiScans!", response.data) 

    def test_login_page(self):
        response = self.client.get('/login')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b"Login", response.data)  
    
    def test_signup_page(self):
        response = self.client.get('/signup')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b"Sign Up", response.data)

    def test_create_user(self):
        user = User(email="test@example.com", username="testuser", password="testpass")
        db.session.add(user)
        db.session.commit()
        found = User.query.filter_by(username="testuser").first()
        self.assertIsNotNone(found)
        self.assertEqual(found.email, "test@example.com")

    import unittest
from SukiScan import create_app, db
from SukiScan.models import User
from SukiScan.config import TestConfig 

class BasicTests(unittest.TestCase):
    def setUp(self):
        self.app = create_app(TestConfig) 
        self.app_context = self.app.app_context()
        self.app_context.push()
        db.create_all()
        self.client = self.app.test_client()

    def tearDown(self):
        db.session.remove()
        db.drop_all()
        self.app_context.pop()

    def test_index_page(self):
        response = self.client.get('/')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b"SukiScan", response.data)  
    
    def test_home_page(self):
        response = self.client.get('/home')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b"Welcome to SukiScans!", response.data) 

    def test_login_page(self):
        response = self.client.get('/login')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b"Login", response.data)  
    
    def test_signup_page(self):
        response = self.client.get('/signup')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b"Sign Up", response.data)

    def test_create_user(self):
        user = User(email="test@example.com", username="testuser", password="testpass")
        db.session.add(user)
        db.session.commit()
        found = User.query.filter_by(username="testuser").first()
        self.assertIsNotNone(found)
        self.assertEqual(found.email, "test@example.com")

    def test_password_hashing(self):
        plain_password = "password"
        hashed_password = generate_password_hash(plain_password)
        user = User(email="test@example.com", username="testuser", password=hashed_password)
        db.session.add(user)
        db.session.commit()
        found = User.query.filter_by(username="testuser").first()
        self.assertIsNotNone(found)
        self.assertNotEqual(found.password, plain_password)
        self.assertTrue(check_password_hash(found.password, plain_password))
        self.assertFalse(check_password_hash(found.password, "wrongpassword"))

if __name__ == '__main__':
    unittest.main()
