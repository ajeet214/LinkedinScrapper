import time
import json
from selenium import webdriver
from selenium.webdriver import ChromeOptions, Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait


class Linkedin:

    options = ChromeOptions()
    # maximized and disable forbar
    options.add_argument("--start-maximized")
    options.add_experimental_option("useAutomationExtension", False)
    options.add_experimental_option("excludeSwitches", ["enable-automation"])
    options.add_experimental_option(
        "prefs",
        {
            "credentials_enable_service": False,
            "profile.password_manager_enabled": False,
            "profile.default_content_setting_values.notifications": 2
            # with 2 should disable/block notifications and 1 to allow
        },
    )

    def __init__(self):
        self.driver = webdriver.Chrome(options=Linkedin.options)

    def login(self, email, password):
        """
        This method takes two parameters email and password and logins to the LinkedIn.

        param email: LinkedIn email
        param password: LinkedIn password
        return:
        """

        url = "https://www.linkedin.com/uas/login"
        self.driver.get(url)
        WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.ID, "organic-div")))
        container = self.driver.find_element(By.ID, "organic-div")

        # login: fill the email account, password
        email_con = container.find_element(By.ID, 'username')
        password_con = container.find_element(By.ID, 'password')
        email_con.send_keys(email)
        password_con.send_keys(password)
        password_con.send_keys(Keys.ENTER)
        time.sleep(2)

        WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.CLASS_NAME, "authentication-outlet")))

    def save_cookie(self, email, password, path):
        """
        This method takes three parameters email, password and path as input. It calls the login method which
        logins to the LinkedIn and then saves the cookies at the given path.

        param email: LinkedIn email
        param password: LinkedIn password
        param path: path to save the cookie file
        return:
        """
        self.login(email, password)
        json_object = json.dumps(self.driver.get_cookies())
        # Writing to sample.json
        with open(path, "w") as outfile:
            outfile.write(json_object)

    def load_cookies(self, path):
        """
        This method takes one parameter, path. It then opens & reads the cookie file, and loads the cookies
        to the Web driver.

        param path: path to saved cookie file
        return:
        """

        f = open(path)
        cookies = json.load(f)

        self.driver.get("https://www.linkedin.com/")

        # load cookies to the driver
        for cookie in cookies:
            self.driver.add_cookie(cookie)

        time.sleep(2)
        # refresh the browser
        self.driver.refresh()
        time.sleep(2)


if __name__ == '__main__':
    obj = Linkedin()
    # obj.login(email="your email", password="your password")
    # obj.save_cookie(email="your email", password="your password", path="path to save cookie file")
    # obj.load_cookies(path="linkedin_cookies.json")

