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
    handlers=[logging.FileHandler("debug.log"), logging.StreamHandler()],
)
# disable logging for urllib3
logging.getLogger("urllib3").propagate = False


class Bot:
    def __init__(self):
        # Use local profile that saves to local folder
        options = webdriver.ChromeOptions()
        options.add_argument('user-data-dir=profile')
        self.driver = webdriver.Chrome(options=options)

    def __start_bot(self):
        logging.info('Starting bot. Press Ctrl + C at any moment to close.')
        # Navigate to the Miyoo Mini website
        self.driver.get(MIYOO_MINI_WEBSITE)
        # driver.get('https://s.click.aliexpress.com/e/_DBjkjv9')

        input(
            'Login or change the language if necessary '
            '(the browser will remember this for the next time you run it).\n'
            'Press enter to start refreshing...\n'
        )

    def __check_stock(self):
        buy_button = self.__find_buy_button_element()

        while buy_button.text != 'Buy Now':
            logging.info(
                f'No stock yet. Refreshing in {SECONDS_BETWEEN_REFRESH} second(s).'
            )
            time.sleep(SECONDS_BETWEEN_REFRESH)
            self.driver.refresh()
            buy_button = self.__find_buy_button_element()

    def __find_element(
        self, by: str, value: str, refresh_wait_time_seconds: float = 0.5
    ) -> WebElement:
        '''Tries to find element button'''
        try:
            element = self.driver.find_element(by, value)
            element.text
        except (StaleElementReferenceException, NoSuchElementException):
            logging.info(
                f'Could not find element, refreshing and waiting {refresh_wait_time_seconds} seconds.'
            )
            self.driver.refresh()
            time.sleep(refresh_wait_time_seconds)
            element = self.__find_element(by, value, refresh_wait_time_seconds + 0.5)
        return element

    def __find_buy_button_element(self) -> WebElement:
        '''Tries to find the buy button'''
        return self.__find_element(By.CLASS_NAME, 'buy-now-wrap')

    def quit(self):
        logging.info('Closing bot.')
        self.driver.quit()

    def __buy(self):
        # Click buy button
        logging.info('Clicking buy button')
        buy_button = self.__find_buy_button_element()
        buy_button.click()

        # Click to confirm the buy
        logging.info('Clicking confirm button')
        confirm_button = self.__find_element(
            By.CSS_SELECTOR,
            '#placeorder_wrap__inner > div > div.pl-side-container > div.pl-wrap-container > div > div > div.pl-order-toal-container__btn-box > button',
        )
        confirm_button.click()

        logging.info('Success 😃?')
        input('Enter to quit...')

    def start_without_buying(self):
        try:
            self.__start_bot()
            self.__check_stock()
            input('It seems there is stock! BUY QUICKLY! (double enter to quick)')
            input()
        except KeyboardInterrupt:
            self.quit()

    def start_with_buying(self):
        try:
            self.__start_bot()
            self.__check_stock()
            self.__buy()
        except KeyboardInterrupt:
            self.quit()


def main():
    bot = Bot()
    bot.start_with_buying()


if __name__ == '__main__':
    main()
