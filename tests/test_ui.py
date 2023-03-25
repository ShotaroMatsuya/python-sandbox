import time
import unittest

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait


class PythonOrgTest(unittest.TestCase):
    def setUp(self):
        self.driver = webdriver.Firefox()

    def tearDown(self):
        self.driver.close()

    def test_python_org(self):
        self.driver.get("http://www.python.org")
        self.assertIn("Python", self.driver.title)
        #
        self.driver.find_element_by_link_text("Downloads").click()

        element = WebDriverWait(self.driver, 10).until(
            EC.presence_of_element_located((By.CLASS_NAME, "widget-title"))
        )
        self.assertEqual("Looking for a specific release?", element.text)
        #
        self.driver.find_element_by_link_text("Documentation").click()

        element = WebDriverWait(self.driver, 10).until(
            EC.presence_of_element_located((By.CLASS_NAME, "call-to-action"))
        )
        self.assertIn("Browse the docs", element.text)

        element = self.driver.find_element_by_name("q")
        element.clear()
        element.send_keys("pycon")
        element.send_keys(Keys.RETURN)
        assert "No results found" not in self.driver.page_source
