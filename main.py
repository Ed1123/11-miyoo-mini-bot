import time
from typing import Optional

from selenium import webdriver
from selenium.common.exceptions import (
    NoSuchElementException,
    StaleElementReferenceException,
)
from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webelement import WebElement

SECONDS_BETWEEN_REFRESH = 1.5


print('Press Ctrl + C at any moment to stop the bot.')

# Use local profile that saves to local folder
options = webdriver.ChromeOptions()
options.add_argument('user-data-dir=profile')
driver = webdriver.Chrome(options=options)

# Navigate to the Miyoo Mini website
driver.get('https://s.click.aliexpress.com/e/_DDDi82J')
# driver.get('https://s.click.aliexpress.com/e/_DBjkjv9') # test with ANBERNIC RG35XX


def find_buy_button_element() -> Optional[WebElement]:
    '''Tries tries to find the buy button'''
    try:
        return driver.find_element(By.CLASS_NAME, 'buy-now-wrap')
    except NoSuchElementException:
        return


input(
    'Press enter to start refreshing.\n'
    'Login or change the language if necessary\n'
    '(the browser will remember this for the next time you run it).'
)

buy_button = find_buy_button_element()

while buy_button and buy_button.text != 'Buy Now':
    print(f'No stock yet. Refreshing in {SECONDS_BETWEEN_REFRESH} second(s).')
    time.sleep(SECONDS_BETWEEN_REFRESH)
    driver.refresh()
    buy_button = find_buy_button_element()

    # just for when the element is not attached
    if buy_button:
        try:
            buy_button.text
        except StaleElementReferenceException:
            driver.refresh()
            buy_button = find_buy_button_element()


input('It seems there is stock! BUY QUICKLY! (double enter to quick)')
input()
driver.quit()
