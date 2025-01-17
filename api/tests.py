import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from django.contrib.staticfiles.testing import StaticLiveServerTestCase
from django.contrib.auth import get_user_model
from selenium.webdriver.common.keys import Keys
import time


class Tests(StaticLiveServerTestCase):
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
    
    def test1_unsuccessful_login(self):
        # Navigate to login page
        self.driver.get(f'{self.live_server_url}/api/login')
        
        time.sleep(2)

        # Find the login form fields and fill them out with wrong credentials
        username_input = self.driver.find_element("name", 'username')
        password_input = self.driver.find_element("name", 'password')
        username_input.send_keys('wronguser')
        password_input.send_keys('wrongpassword')
        
        time.sleep(2)

        # Submit the form
        password_input.send_keys(Keys.RETURN)

        # Wait for the page to load and check if an error message is displayed
        time.sleep(2)
        self.assertIn("Login", self.driver.page_source)
        
    def test2_user_registration(self):
        # Navigate to registration page
        self.driver.get(f"{self.live_server_url}/api/login/")
        time.sleep(2)
        
        # Navigate to next page
        link = self.driver.find_element("tag name", "a")
        link.click()

        time.sleep(2)

        # Find the registration form fields and fill them out
        username_input = self.driver.find_element("name", 'username')
        email_input = self.driver.find_element("name", 'email')
        password_input = self.driver.find_element("name", 'password1')
        name_input = self.driver.find_element("name", 'name')
        confirm_password_input = self.driver.find_element("name", 'password2')
        dob_input = self.driver.find_element("name", 'date_of_birth')

        username_input.send_keys('NewUser')
        email_input.send_keys('newuser@example.com')
        password_input.send_keys('newTestpassword')
        name_input.send_keys("New User")
        confirm_password_input.send_keys('newTestpassword')
        dob_input.send_keys("1990-01-01")
        
        time.sleep(2)

        # Submit the form
        button = self.driver.find_element("tag name", "button")
        button.click()

        # Wait for the page to load after registration
        time.sleep(2)

        # Check if registration was successful (look for confirmation message)
        self.assertIn("Login", self.driver.page_source)

    def test3_login(self):
        # Navigate to login page
        self.driver.get(f"{self.live_server_url}/api/login/")
        time.sleep(2)

        # Find the login form fields and fill them out
        username_input = self.driver.find_element("name", 'username')
        password_input = self.driver.find_element("name", 'password')
        username_input.send_keys('NewUser')
        password_input.send_keys('newTestpassword')

        # Submit the form 
        button = self.driver.find_element("tag name", "button")
        button.click()

        # Wait for the page to load after login
        time.sleep(2)

        # Check if login was successful (by checking for presence of a logout button or user profile)
        self.assertIn("Welcome to the Hobbies App", self.driver.page_source)
        
    def test4_sendreq(self):
        # Navigate to registration page
        self.driver.get(f"{self.live_server_url}/api/login/")
        time.sleep(2)
        link = self.driver.find_element("tag name", "a")
        link.click()

        time.sleep(2)

        # Find the registration form fields and fill them out
        username_input = self.driver.find_element("name", 'username')
        email_input = self.driver.find_element("name", 'email')
        password_input = self.driver.find_element("name", 'password1')
        name_input = self.driver.find_element("name", 'name')
        confirm_password_input = self.driver.find_element("name", 'password2')
        dob_input = self.driver.find_element("name", 'date_of_birth')

        username_input.send_keys('Friend')
        email_input.send_keys('friend@example.com')
        password_input.send_keys('Testpassword1')
        name_input.send_keys("Friend")
        confirm_password_input.send_keys('Testpassword1')
        dob_input.send_keys("1990-01-01")
        
        time.sleep(2)

        # Submit the form
        button = self.driver.find_element("tag name", "button")
        button.click()

        # Wait for the page to load after registration
        time.sleep(2)
        
        # Navigate to login page
        self.driver.get(f"{self.live_server_url}/api/login/")
        time.sleep(2)

        # Find the login form fields and fill them out
        username_input = self.driver.find_element("name", 'username')
        password_input = self.driver.find_element("name", 'password')
        username_input.send_keys('Friend')
        password_input.send_keys('Testpassword1')

        # Submit the form 
        button = self.driver.find_element("tag name", "button")
        button.click()

        # Wait for the page to load after login
        time.sleep(2)
        
        # Go to hobbies page
        self.driver.get(f"{self.live_server_url}/hobbies/")
        time.sleep(2)
        
        # Locate the button element by its text
        apply_filters_button = self.driver.find_element("xpath", "//button[normalize-space()='Send Friend Request']")        
        
    def test5_filter(self):
        # Navigate to login page
        self.driver.get(f"{self.live_server_url}/hobbies/")
        time.sleep(2)
        
        minage_input = self.driver.find_element("id", "min-age")
        maxage_input = self.driver.find_element("id", "max-age")
        
        minage_input.send_keys("0")
        maxage_input.send_keys("10")
        
        # Locate the button element by its text
        apply_filters_button = self.driver.find_element("xpath", "//button[normalize-space()='Apply Filters']")

    def test6_filter(self):
        #Login to another user
        # Navigate to login page
        self.driver.get(f"{self.live_server_url}/api/login/")
        time.sleep(2)

        # Find the login form fields and fill them out
        username_input = self.driver.find_element("name", 'username')
        password_input = self.driver.find_element("name", 'password')
        username_input.send_keys('NewUser')
        password_input.send_keys('newTestpassword')

        # Submit the form 
        button = self.driver.find_element("tag name", "button")
        button.click()

        # Wait for the page to load after login
        time.sleep(2)
        
        # Accept
        self.driver.get(f"{self.live_server_url}/friend-requests")
        apply_filters_button = self.driver.find_element("xpath", "//button[normalize-space()='Accept']")
