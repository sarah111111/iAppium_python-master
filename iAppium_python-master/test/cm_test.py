from appium import webdriver
import unittest
import time
import os
from pytest_testconfig import config

timeout = 30
poll = 2


class IAppium(unittest.TestCase):

    def setUp(self):
        desired_caps = {}
        # appium_server_url = "http://127.0.0.1:4723/wd/hub"
        desired_caps['platformName'] = "Android"
        desired_caps['udid'] = "127.0.0.1:7555"
        desired_caps['deviceName'] = "127.0.0.1:7555"
        desired_caps['appPackage'] = "com.example.android.contactmanager"
        desired_caps['appActivity'] = ".ContactManager"
        desired_caps['automationName'] = "UiAutomator2"
        desired_caps['noReset'] = "false"
        desired_caps['chromedriverExecutable'] = 'E:/工具/chromedriver_win32/chromedriver.exe'
        # desired_caps['app'] = f'{os.path.abspath(os.curdir)}/app/ContactManager.apk'

        # self.driver = webdriver.Remote(appium_server_url, desired_caps)
        self.driver = webdriver.Remote("http://127.0.0.1:4723/wd/hub", desired_caps)
        self.driver.implicitly_wait(50)

    def tearDown(self):
        self.driver.quit()

    def test_contact(self):
        """  """

        # Workaround for version issue
        self._click_confirm_ok_btn()

        self._click_add_contact_btn()
        self._input_contact_name('A san')
        self._input_email('asan@example.com')
        self._click_save_btn()

        # Workarount for version issue
        self._click_confirm_ok_btn()
        time.sleep(2)

    def _click_add_contact_btn(self):
        elem = self._find_elem_by_xpath('//android.widget.Button[contains(@resource-id,"addContactButton")]')
        print(f'Click add contact button')
        elem.click()

    def _input_contact_name(self, txt_name):
        elem = self._find_elem_by_xpath('//android.widget.EditText[contains(@resource-id, "contactNameEditText")]')
        print(f'Input contact name {txt_name}')
        elem.send_keys(txt_name)

    def _input_email(self, txt_email):
        elem = self._find_elem_by_xpath('//android.widget.EditText[contains(@resource-id, "contactEmailEditText")]')
        print(f'Input email {txt_email}')
        elem.send_keys(txt_email)

    def _click_save_btn(self):
        elem = self._find_elem_by_xpath('//android.widget.Button[contains(@resource-id, "contactSaveButton")]')
        print('Click the save button')
        elem.click()

    def _click_confirm_ok_btn(self):
        elem = self._find_elem_by_xpath('//android.widget.Button[contains(@resource-id, "android:id/button1")]',
                                        time_out=3, raise_exception=False)
        if elem is not None:
            print('Click the ok button on confirm dialog')
            elem.click()
        else:
            print('No confirm dialog found')

    def _find_elem_by_xpath(self, elem_xpath, time_out=timeout, raise_exception=True):
        start = time.time()
        elem = None
        while time.time() - start < time_out and elem is None:
            time.sleep(poll)
            try:
                elem = self.driver.find_element_by_xpath(elem_xpath)
            except Exception:
                print('by pass the element not found')

        if elem is None and raise_exception:
            raise LookupError(f'The element which xpath is {elem_xpath} could not be found')

        return elem
