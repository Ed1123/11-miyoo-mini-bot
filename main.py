import logging
import time
from typing import Optional

from selenium import webdriver
from selenium.common.exceptions import (
    NoSuchElementException,
    StaleElementReferenceException,
)
from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.remote.webelement import WebElement

SECONDS_BETWEEN_REFRESH = 1.5
MIYOO_MINI_WEBSITE = 'https://s.click.aliexpress.com/e/_DDDi82J'
# MIYOO_MINI_WEBSITE = 'https://s.click.aliexpress.com/e/_DBjkjv9'  # test with ANBERNIC RG35XX

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
)


def find_buy_button_element(driver: WebDriver) -> Optional[WebElement]:
    '''Tries tries to find the buy button'''
    try:
        return driver.find_element(By.CLASS_NAME, 'buy-now-wrap')
    except NoSuchElementException:
        return


def main():
    logging.info('Starting bot. Press Ctrl + C at any moment to close.')

    # Use local profile that saves to local folder
    options = webdriver.ChromeOptions()
    options.add_argument('user-data-dir=profile')
    driver = webdriver.Chrome(options=options)

    # Navigate to the Miyoo Mini website
    driver.get(MIYOO_MINI_WEBSITE)
    # driver.get('https://s.click.aliexpress.com/e/_DBjkjv9')

    input(
        'Login or change the language if necessary '
        '(the browser will remember this for the next time you run it).'
        'Press enter to start refreshing.\n'
    )

    buy_button = find_buy_button_element(driver)

    while buy_button and buy_button.text != 'Buy Now':
        logging.info(
            f'No stock yet. Refreshing in {SECONDS_BETWEEN_REFRESH} second(s).'
        )
        time.sleep(SECONDS_BETWEEN_REFRESH)
        driver.refresh()
        buy_button = find_buy_button_element(driver)

        # just for when the element is not attached
        if buy_button:
            try:
                buy_button.text
            except StaleElementReferenceException:
                driver.refresh()
                buy_button = find_buy_button_element(driver)

    input('It seems there is stock! BUY QUICKLY! (double enter to quick)')
    input()
    driver.quit()


if __name__ == '__main__':
    main()
