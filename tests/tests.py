import time
import unittest
import multiprocessing

from SukiScan import create_app, db
from SukiScan.config import TestConfig
from SukiScan.models import User
from werkzeug.security import generate_password_hash, check_password_hash

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions

localHost = "http://127.0.0.1:5000"

class SeleniumTests(unittest.TestCase):
    def setUp(self):
        self.app = create_app(TestConfig)  # Pass in 'testing' config
        self.app_context = self.app.app_context()
        self.app_context.push()
        db.create_all()
        
        self.server_thread = multiprocessing.Process(target=self.app.run)
    
    def test_home_status_code(self):
        response = self.client.get('/')
        self.assertEqual(response.status_code, 200)

    def seed(self):
        user = User(user_id=1, 
                    email="ilovematthewdaggit@gmail.com", 
                    username="Matthew_Daggit", 
                    password=generate_password_hash("ILoveMatthewDaggit"))
        db.session.add(user)
        db.session.commit()
        
        self.client = self.app.test_client()
    

    def tearDown(self):
        db.session.remove()
        db.drop_all()
        self.app_context.pop()
        
if __name__ == "__main__":
    unittest.main()