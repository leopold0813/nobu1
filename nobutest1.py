#nobutest1.py
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.touch_actions import TouchActions
from time import sleep
import threading
password=''
def check_middle(driver):
    Action = TouchActions(driver)
    bhave=False
    try:
        a=driver.find_element_by_xpath("//td[contains(text(),'進む')]")
        bhave=True
    except:
        pass
    if not bhave:
        try:
            a=driver.find_element_by_xpath("//td[contains(text(),'次へ')]")
            bhave=True
        except:
            pass
    if bhave:
        btn=driver.find_element_by_id("sp-header-middle-btn")
        Action.tap(btn).perform()
        return True
    else:
        return False
def check_movie(driver):
    Action = TouchActions(driver)
    try:
        a=driver.find_element_by_id("canvas")
    except:
        return False
    x=a.location['x']+a.size['width']/2
    y=a.location['y']+a.size['height']/2
    Action.tap_and_hold(x,y).release(x,y).perform()
    return True
def check_scene(driver, scene):
    try:
        a=driver.find_element_by_xpath("//div[@class='pagetitle_flare']/span")
    except:
        return False
    if (a.text).find(scene)!=-1:
        return True
    else:
        return False
def login(driver,username):
