import logging
import time

from selenium import webdriver
from selenium.common.exceptions import (
    NoSuchElementException,
    StaleElementReferenceException,
)
from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webelement import WebElement

SECONDS_BETWEEN_REFRESH = 1.5
MIYOO_MINI_WEBSITE = 'https://s.click.aliexpress.com/e/_DDDi82J'
# MIYOO_MINI_WEBSITE = 'https://s.click.aliexpress.com/e/_DBjkjv9'  # test with ANBERNIC RG35XX

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
)
# disable logging for urllib3
logging.getLogger("urllib3").propagate = False


class Bot:
    def __init__(self):
        # Use local profile that saves to local folder
        options = webdriver.ChromeOptions()
        options.add_argument('user-data-dir=profile')
        self.driver = webdriver.Chrome(options=options)

    def __start_bot__(self):
        logging.info('Starting bot. Press Ctrl + C at any moment to close.')
        # Navigate to the Miyoo Mini website
        self.driver.get(MIYOO_MINI_WEBSITE)
        # driver.get('https://s.click.aliexpress.com/e/_DBjkjv9')

        input(
            'Login or change the language if necessary '
            '(the browser will remember this for the next time you run it).\n'
            'Press enter to start refreshing...\n'
        )

    def __check_stock__(self):
        buy_button = self.__find_buy_button_element__()

        while buy_button.text != 'Buy Now':
            logging.info(
                f'No stock yet. Refreshing in {SECONDS_BETWEEN_REFRESH} second(s).'
            )
            time.sleep(SECONDS_BETWEEN_REFRESH)
            self.driver.refresh()
            buy_button = self.__find_buy_button_element__()

    def __find_buy_button_element__(self) -> WebElement:
        '''Tries tries to find the buy button'''
        try:
            element = self.driver.find_element(By.CLASS_NAME, 'buy-now-wrap')
            element.text
        except (StaleElementReferenceException, NoSuchElementException):
            logging.info('Could not find buy button, refreshing.')
            self.driver.refresh()
            element = self.__find_buy_button_element__()
        return element

    def quit(self):
        logging.info('Closing bot.')
        self.driver.quit()

    def __buy__(self):
        raise NotImplementedError

    def start_without_buying(self):
        try:
            self.__start_bot__()
            self.__check_stock__()
            input('It seems there is stock! BUY QUICKLY! (double enter to quick)')
            input()
        except KeyboardInterrupt:
            self.quit()

    def start_with_buying(self):
        try:
            self.__start_bot__()
            self.__check_stock__()
            self.__buy__()
        except KeyboardInterrupt:
            self.quit()


def main():
    bot = Bot()
    bot.start_without_buying()


if __name__ == '__main__':
    main()
