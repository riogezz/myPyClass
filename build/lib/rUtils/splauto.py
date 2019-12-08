#!/usr/bin/env python3
# -*- coding=utf-8 -*-

"""
splauto.py
"""

from selenium.webdriver.chrome.options import Options
from splinter import Browser
import logging
import re

class splauto(object):
    
    def __init__(self, browser="chrome", path=None, fullscreen=True, kiosk=True, infobars=False):
        self.exc_info=True
        if browser.lower()=="chrome":
            options = Options()
            if fullscreen==True: options.add_argument("--start-maximized") 
            options.add_argument('--disable-gpu')
            if infobars==False: options.add_argument("--disable-infobars")
            options.add_argument("--disable-extensions")
            options.add_argument("--no-sandbox")
            if kiosk==True: options.add_argument("--kiosk")
            options.add_argument("--disable-dev-shm-usage")
        self.browserOptions = options
        pass
    
    def clean_browser(self):
        self.driver.cookies.delete()

    
    def start_browser(self):
        try:
            self.driver = Browser('chrome' , options=self.browserOptions)
            logging.debug(f"opened browser")
            self.clean_browser()
        except Exception as e:
            logging.critical(str(e), exc_info=self.exc_info)
            raise
        
    def quit_browser(self):
        try:
            self.driver.quit()
            logging.debug("quitted browser.")
        except Exception as e:
            logging.critical(str(e), exc_info=True)
            pass
        
    def goto(self, URL):
        if not re.match("^https?://.*", URL):
            URL="http://"+URL
        self.driver.visit(URL)
        logging.debug(f"visiting {URL}")

    def check_and_click(self, id=None, xpath=None, text=None, partial_text=None, n=1):
        
        # finds id and tries clicks it
        if id is not None:
            if self.driver.is_element_present_by_id(id):
                logging.debug(f"{id} found in current page")
                try:
                    self.driver.find_by_id(id)[n].click()
                    logging.debug(f"Clicked: {id}")
                except Exception as e:
                    logging.critical(str(e), exc_info=True)
                    raise
            else:
                logging.debug(f"{id} is not present in current page")    

        # finds xpath and tries clicks it
        elif xpath is not None:
            if self.driver.is_element_present_by_xpath(xpath):
                logging.debug(f"{xpath} found in current page")
                try:
                    self.driver.find_by_xpath(xpath)[n].click()
                    logging.debug(f"Clicked: {xpath}")
                except Exception as e:
                    logging.critical(str(e), exc_info=True)
                    raise
            else:
                logging.debug(f"{xpath} is not present in current page")    

        # finds text and tries clicks it
        elif text is not None:
            if self.driver.is_element_present_by_text(text):
                logging.debug(f"{text} found in current page")
                try:
                    self.driver.find_by_text(text)[n].click()
                    logging.debug(f"Clicked: {text}")
                except Exception as e:
                    logging.critical(str(e), exc_info=True)
                    raise
            else:
                logging.debug(f"{text} is not present in current page")  

        # finds partial_text and tries clicks it
        elif partial_text is not None:
            if self.driver.is_text_present(partial_text):
                logging.debug(f"{partial_text} found in current page")
                try:
                    self.driver.find_link_by_partial_text(partial_text)[n].click()
                    logging.debug(f"Clicked: {partial_text}")
                except Exception as e:
                    logging.critical(str(e), exc_info=True)
                    raise
            else:
                logging.debug(f"{partial_text} is not present in current page")
        else:
            logging.critical(f"you are looking something without specifying any of <id>, <xpath>, <text>, <partial_text>")


class spaluto_commands(object):

    def __init__(self, filename):
        self.auto = splauto()
        try:
            with open(filename) as f:
                for line in f:
                    print(f"{line}")
                    self.__command_execution(line)
        except Exception as e:
            logging.error(str(e))
            raise
        pass       

    @staticmethod            
    def __check_command(c, s):
        return bool(re.search(s, c))
            
    def __command_execution(self, command):
        c = command.rstrip()
        if __class__.__check_command(c, "^OPEN BROWSER$"): self.auto.start_browser()
        if __class__.__check_command(c, "^CLOSE BROWSER$"): self.auto.quit_browser()
        if __class__.__check_command(c, "^GOTO"): self.auto.goto(c.split()[-1])
        if __class__.__check_command(c, "^CHECK AND CLICK"): 
            l = c.split()
            element=l[3].lower()
            value=' '.join(l[4:])
            print(f"{element}={value}")
            d=eval("{"+str(element)+":"+str(value)+"}")
            print(f"{d}")
            self.auto.check_and_click(**d)
        