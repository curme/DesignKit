import os
import time

from selenium import webdriver
from selenium.webdriver.common.by import By

if __name__ == '__main__':

    url_temp = 'https://uigradients.com/#'
    xpath = '/html/body/main/section/div[3]/ul/li[4]/a'

    with open('./Colors/colors.txt', 'r+') as f:
        colors = f.read().split('\n')
        colors = [color for color in colors if color is not '']
    
    b = webdriver.Firefox()
    for color in colors[201:]:
        color = ''.join(color.split(' '))
        url = url_temp + color
        b.get(url)
        b.refresh()
        time.sleep(20)
        b.find_element(By.XPATH, xpath).click()
        time.sleep(10)
    b.close()