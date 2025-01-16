import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from django.contrib.staticfiles.testing import LiveServerTestCase


class Tests(LiveServerTestCase):
    fixtures = ['users.json']  # Preload data from the users.json fixture

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.driver = webdriver.Chrome()
        cls.driver.wait = WebDriverWait(cls.driver, 10)

    @classmethod
    def tearDownClass(cls):
        cls.driver.quit()
        super().tearDownClass()
    
    # def test_unsuccessful_login(self):
    #     # Navigate to login page
    #     self.driver.get(f'{self.live_server_url}/api/login')
        
    #     time.sleep(2)

    #     # Find the login form fields and fill them out with wrong credentials
    #     username_input = self.driver.find_element("name", 'username')
    #     password_input = self.driver.find_element("name", 'password')
    #     username_input.send_keys('wronguser')
    #     password_input.send_keys('wrongpassword')

    #     # Submit the form
    #     password_input.send_keys(Keys.RETURN)

    #     # Wait for the page to load and check if an error message is displayed
    #     time.sleep(2)
    #     self.assertIn("Invalid username or password", self.driver.page_source)
        
    # def test_protected_page_requires_login(self):
    #     # Navigate to a page that requires login
        
    #     time.sleep(2)
    #     self.driver.get(f'{self.live_server_url}/profile')

    #     # Check if redirected to login page
    #     self.assertIn("Login", self.driver.title)
        
    def test1_user_registration(self):
        # Navigate to registration page
        self.driver.get(f"{self.live_server_url}/api/signup/")
        time.sleep(2)

        # Find the registration form fields and fill them out
        username_input = self.driver.find_element("name", 'username')
        email_input = self.driver.find_element("name", 'email')
        password_input = self.driver.find_element("name", 'password1')
        name_input = self.driver.find_element("name", 'name')
        confirm_password_input = self.driver.find_element("name", 'password2')
        dob_input = self.driver.find_element("name", 'date_of_birth')

        username_input.send_keys('TestUser')
        email_input.send_keys('newuser@example.com')
        password_input.send_keys('Testpassword')
        name_input.send_keys("Test User")
        confirm_password_input.send_keys('Testpassword')
        dob_input.send_keys("1990-01-01")
        
        time.sleep(200)

        # Submit the form
        button = self.driver.find_element("tag name", "button")
        button.click()

        # Wait for the page to load after registration
        time.sleep(2)

        # Check if registration was successful (look for confirmation message)
        self.assertIn("Login", self.driver.page_source)

    def test2_login(self):
        # Navigate to login page
        # self.driver.get(f"{self.live_server_url}/api/login/")
        time.sleep(2)

        # Find the login form fields and fill them out
        username_input = self.driver.find_element("name", 'username')
        password_input = self.driver.find_element("name", 'password')
        username_input.send_keys('TestUser')
        password_input.send_keys('Testpassword')

        # Submit the form 
        button = self.driver.find_element("tag name", "button")
        button.click()

        # Wait for the page to load after login
        time.sleep(2)

        # Check if login was successful (by checking for presence of a logout button or user profile)
        self.assertIn("Welcome to the Hobbies App", self.driver.page_source)





