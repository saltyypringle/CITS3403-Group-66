import time
import unittest
from multiprocessing import Process

from SukiScan import create_app, db
from SukiScan.config import TestConfig
from SukiScan.models import User
from werkzeug.security import generate_password_hash, check_password_hash

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

localHost = "http://127.0.0.1:5000"


def run_app():
    app = create_app(TestConfig)
    app.run(port=5000)

class SeleniumTests(unittest.TestCase):
    def setUp(self):
        self.app = create_app(TestConfig)  # Pass in 'testing' config
        self.app_context = self.app.app_context()
        self.app_context.push()
        db.drop_all()
        db.create_all()
        
        #Add a user credentials
        user = User(user_id=1, 
                    email="ilovematthewdaggit@gmail.com", 
                    username="Matthew_Daggit", 
                    password=generate_password_hash("ILoveMatthewDaggit"))
        db.session.add(user)
        db.session.commit()
        
        self.server_process = Process(target=run_app)
        self.server_process.start()
        time.sleep(1)
        
        options = webdriver.ChromeOptions()
        options.add_argument("--headless")
        self.driver = webdriver.Chrome(options=options)
    
    #Testing login with username
    def test_correct_username_login(self):
        self.driver.get(localHost + "/login")
        
        username = self.driver.find_element(By.ID, "login-email-or-username")
        password = self.driver.find_element(By.ID, "login-password")
        login_button = self.driver.find_element(By.ID, "login")
        
        username.send_keys("Matthew_Daggit")
        password.send_keys("ILoveMatthewDaggit")
        login_button.click()
        
        WebDriverWait(self.driver, 5).until(
            EC.url_to_be(localHost + "/mypage")
        )
    
        self.assertEqual(self.driver.current_url, localHost + "/mypage")
    
    #Testing login with email
    def test_correct_email_login(self):
        self.driver.get(localHost + "/login")
        
        email = self.driver.find_element(By.ID, "login-email-or-username")
        password = self.driver.find_element(By.ID, "login-password")
        login_button = self.driver.find_element(By.ID, "login")
        
        email.send_keys("ilovematthewdaggit@gmail.com")
        password.send_keys("ILoveMatthewDaggit")
        login_button.click()
        
        WebDriverWait(self.driver, 5).until(
            EC.url_to_be(localHost + "/mypage")
        )
    
        self.assertEqual(self.driver.current_url, localHost + "/mypage")
    
    #Testing Wrong password
    def test_wrong_password(self):
        self.driver.get(localHost + "/login")
        
        username = self.driver.find_element(By.ID, "login-email-or-username")
        password = self.driver.find_element(By.ID, "login-password")
        login_button = self.driver.find_element(By.ID, "login")
        
        username.send_keys("Matthew_Daggit")
        password.send_keys("MatthewDaggitHatesBubbleTea")
        login_button.click()
        
        WebDriverWait(self.driver, 5).until(
            EC.url_to_be(localHost + "/login")
        )
    
        self.assertEqual(self.driver.current_url, localHost + "/login")
        
        error_div = self.driver.find_element(By.CSS_SELECTOR, "div[style='color:red;']")
        error_text = error_div.text
        self.assertIn("Password Incorrect", error_text)
        
    #Testing User doesn't exist
    def test_no_user(self):
        self.driver.get(localHost + "/login")
        
        username = self.driver.find_element(By.ID, "login-email-or-username")
        password = self.driver.find_element(By.ID, "login-password")
        login_button = self.driver.find_element(By.ID, "login")
        
        username.send_keys("Matthew")
        password.send_keys("ILoveMatthewDaggit")
        login_button.click()
        
        WebDriverWait(self.driver, 5).until(
            EC.url_to_be(localHost + "/login")
        )
    
        self.assertEqual(self.driver.current_url, localHost + "/login")
        
        error_div = self.driver.find_element(By.CSS_SELECTOR, "div[style='color:red;']")
        error_text = error_div.text
        self.assertIn("Username or Email not found", error_text)
    
    #Check if email already being used
    def test_email_exists(self):
        self.driver.get(localHost + "/signup")
        
        email = self.driver.find_element(By.ID, "signup-email")
        username = self.driver.find_element(By.ID, "signup-username")
        password = self.driver.find_element(By.ID, "signup-password")
        login_button = self.driver.find_element(By.ID, "signup")
        
        email.send_keys("ilovematthewdaggit@gmail.com")
        username.send_keys("Matthew_Daggit")
        password.send_keys("ILoveMatthewDaggit")
        login_button.click()
        
        WebDriverWait(self.driver, 5).until(
            EC.url_to_be(localHost + "/signup")
        )
    
        self.assertEqual(self.driver.current_url, localHost + "/signup")
        
        error_div = self.driver.find_element(By.CSS_SELECTOR, "div[style='color:red;']")
        error_text = error_div.text
        self.assertIn("Email already in use. Choose another", error_text)
    
    #Check if username already being used
    def test_username_exists(self):
        self.driver.get(localHost + "/signup")
        
        email = self.driver.find_element(By.ID, "signup-email")
        username = self.driver.find_element(By.ID, "signup-username")
        password = self.driver.find_element(By.ID, "signup-password")
        login_button = self.driver.find_element(By.ID, "signup")
        
        email.send_keys("matthewt@gmail.com")
        username.send_keys("Matthew_Daggit")
        password.send_keys("ILoveMatthewDaggit")
        login_button.click()
        
        WebDriverWait(self.driver, 5).until(
            EC.url_to_be(localHost + "/signup")
        )
    
        self.assertEqual(self.driver.current_url, localHost + "/signup")
        
        error_div = self.driver.find_element(By.CSS_SELECTOR, "div[style='color:red;']")
        error_text = error_div.text
        self.assertIn("Username already in use. Choose another", error_text)


    def tearDown(self):
        self.driver.quit()
        
        self.server_process.terminate()
        self.server_process.join()
        
        db.session.remove()
        db.drop_all()
        self.app_context.pop()
        
if __name__ == "__main__":
    unittest.main()