import time
import validators
import random
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.common.exceptions import *
from config import config

options = Options()
# options.add_argument('--headless')
options.add_argument('--disable-gpu')

driver = webdriver.Chrome(options=options)
driver.set_page_load_timeout(config.page_load_timeout)


def get_urls_list_for_subscribe():
    with open(config.input_file) as f:
        url_list_data = f.read()
    url_list = url_list_data.split("\n")
    url_list = list(filter(validators.url, url_list))
    url_list_to_subscribe = random.sample(url_list, config.random_count)
    return url_list_to_subscribe


def try_to_subscribe_url(url_item):
    query = "//*[text()='Subscribe']"
    close_all_tabs()
    driver.get(url_item)
    try:
        element = driver.find_element_by_xpath(query)
        element.click()
        wait_all_pages_has_loaded()
        if get_tab_count() == 2:
            driver.switch_to.window(driver.window_handles[1])
        email_fields = driver.find_elements_by_xpath("//input[@type='email']")
        for email_field_item in email_fields:
            try_to_fill_email(email_field_item)

        breakpoint()
        print(f"Element : {element} for URL : {url_item}")
    except NoSuchElementException as not_found:
        print(f"Element not found for URL : {url_item}")


def page_has_loaded(window_name):
    # self.log.info("Checking if {} page is loaded.".format(self.driver.current_url))
    print("Checking if {} page is loaded.".format(window_name))
    driver.switch_to.window(window_name)
    page_state = driver.execute_script('return document.readyState;')
    return page_state == 'complete'


def wait_all_pages_has_loaded():
    current_tab = driver.current_window_handle
    while not all([page_has_loaded(window_item) for window_item in driver.window_handles]):
        time.sleep(1)
    driver.switch_to.window(current_tab)


def try_to_fill_email(email_input_element):
    try:
        email_input_element.send_keys("test")
    except ElementNotVisibleException as not_visible:
        print(not_visible)
    except Exception as e:
        print(e)


def get_tab_count():
    return len(driver.window_handles)


def close_all_tabs():
    for x in range(1, get_tab_count()):
        driver.find_element_by_tag_name('body').send_keys(Keys.COMMAND + 'W')


def main():
    # url_list = get_urls_list_for_subscribe()
    # for url in url_list:
    #     try_to_subscribe_url(url)
    try_to_subscribe_url("https://frontendfront.com/")


if __name__ == "__main__":
    main()
