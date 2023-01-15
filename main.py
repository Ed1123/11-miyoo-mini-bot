import time
from typing import Optional

from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webelement import WebElement

SECONDS_BETWEEN_REFRESH = 0.5

# Trying to use default profile to avoid having to log in, but doesn't work...
# options = webdriver.ChromeOptions()
# options.add_argument(
#     'user-data-dir=/Users/edward/Library/Application Support/Google/Chrome/Default'
# )
# driver = webdriver.Chrome(options=options)

print('Press Ctrl + C at any moment to stop the bot.')

driver = webdriver.Chrome()

# Navigate to the Miyoo Mini website
driver.get('https://s.click.aliexpress.com/e/_DDDi82J')
# driver.get('https://s.click.aliexpress.com/e/_DBjkjv9') # test with ANBERNIC RG35XX


def find_buy_button_element() -> Optional[WebElement]:
    '''Tries tries to find the buy button'''
    try:
        return driver.find_element(By.CLASS_NAME, 'buy-now-wrap')
    except NoSuchElementException:
        return


input('Log in in the Chrome window that has opened and press enter.')


buy_button = find_buy_button_element()

while buy_button and buy_button.text != 'Buy Now':
    print(f'No stock yet. Refreshing in {SECONDS_BETWEEN_REFRESH} second(s).')
    time.sleep(SECONDS_BETWEEN_REFRESH)
    driver.refresh()
    buy_button = find_buy_button_element()

input('It seems there is stock! BUY QUICKLY! (double enter to quick)')
input()
driver.quit()
