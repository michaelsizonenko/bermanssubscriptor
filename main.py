import time
import os
import re
import validators
import random
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.common.exceptions import *
from config import config
from main_logger import logger


error_file_name = ""
driver = None


def init_driver():
    options = Options()
    options.add_argument('--headless')
    options.add_argument('--disable-gpu')

    global driver
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
        try_to_submit_form()
        time.sleep(1)
        logger.info(f"Form submitted for URL: {url_item}")
        if check_if_recaptcha_present():
            logger.info("Sorry, recaptcha found.")
            close_all_tabs()
    except NoSuchElementException as not_found:
        logger.info(f"Element not found for URL : {url_item}")
        logger.error(not_found, exc_info=True)


def check_if_recaptcha_present():
    return len(driver.find_elements_by_xpath("//*[@class='g-recaptcha']")) > 0


def page_has_loaded(window_name):
    # self.log.info("Checking if {} page is loaded.".format(self.driver.current_url))
    logger.info("Checking if {} page is loaded.".format(window_name))
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
        email_input_element.send_keys(config.email_for_subscription)
    except ElementNotVisibleException as not_visible:
        logger.error(not_visible, exc_info=True)
    except Exception as e:
        logger.error(e, exc_info=True)


def try_to_submit_form():
    submit_element_list = driver.find_elements_by_xpath("//*[@type='submit']")
    for submit_element in submit_element_list:
        try:
            submit_element.submit()
        except Exception as e:
            logger.error(e, exc_info=True)


def get_tab_count():
    return len(driver.window_handles)


def close_all_tabs():
    for x in range(1, get_tab_count()):
        driver.find_element_by_tag_name('body').send_keys(Keys.COMMAND + 'W')


def create_error_file():
    pattern = r"(\([0-9]+\))"
    email = config.email_for_subscription.replace("@", "_").replace(".", "_")
    custom_name = config.error_file
    file_name = email + "_" + custom_name
    file_counter = 0
    while os.path.exists(file_name):
        file_name = re.sub(pattern, "", file_name)
        file_name_without_ext, ext = os.path.splitext(file_name)
        file_counter += 1
        file_name = file_name_without_ext + "({})".format(file_counter) + ext
    with open(file_name, "w+") as f:
        f.close()
    global error_file_name
    error_file_name = file_name


def append_to_the_error_file(message, reason):
    global error_file_name
    with open(error_file_name, 'a') as f:
        f.write("{}\t\t{}\n".format(message, reason))


def main():
    url_list = get_urls_list_for_subscribe()
    create_error_file()
    for url in url_list:
        try:
            init_driver()
            try_to_subscribe_url(url)
            driver.quit()
        except TimeoutException as time_out:
            logger.info(f"Timeout expired for URL : {url}")
            logger.error(time_out, exc_info=True)
            append_to_the_error_file(url, "Failed to load")
        except Exception as e:
            logger.error(e, exc_info=True)
            append_to_the_error_file(url, "Unknown error")
        finally:
            time.sleep(1)
    # try_to_subscribe_url("https://frontendfront.com/")


if __name__ == "__main__":
    main()
