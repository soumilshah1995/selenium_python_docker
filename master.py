__AUTHOR__ = "Soumil Nitin Shah "

try:
    import os
    import json

    from selenium import webdriver
    from selenium.webdriver.common.keys import Keys
    from selenium.webdriver.common.by import By
    from selenium.webdriver.chrome.options import Options
    from selenium.webdriver.support.ui import WebDriverWait

    from bs4 import BeautifulSoup
    import base64
    from abc import ABC, abstractmethod
    from enum import Enum
    import datetime
    import re
    from time import sleep
    import boto3

    print("All modules loaded ")
except Exception as e:
    print("Error Modules not found : {} ".format(e))


class ChromeDriver(ABC):

    @abstractmethod
    def get_driver(self):
        """This will provide the Webdriver object """
        pass


class WebDriver(ChromeDriver):

    def __init__(self, path=None):
        self.path = path
        self.options = Options()
        self.options.add_argument('--headless')
        self.options.add_argument('--no-sandbox')
        self.options.add_argument('--start-maximized')
        self.options.add_argument('--start-fullscreen')
        self.options.add_argument('--single-process')
        self.options.add_argument('--disable-dev-shm-usage')
        self.driver_instance = self.get_driver()

    def get_driver(self):
        driver = webdriver.Chrome(chrome_options=self.options)
        return driver


class Commands(WebDriver):

    """
    {
         "commands":[
             {
                 "selector":"xpath",
                 "path":"/html/body/div[1]/div/form/div[1]/div/input",
                 "command":"type",
                 "search":"software Engineer"
              },
              {
                 "command":"sleep",
                 "time":"1"
              },
              {
                 "selector":"xpath",
                 "path":"//html/body/div[1]/div/form/button",
                 "command":"click"
              }
       ]
   }
    """

    def __init__(self, commands):
        self.commands = commands
        WebDriver.__init__(self)

    def execute(self):
        if self.commands is None:
            message = {
                "status":200,
                "data":{"message":"No commands to excute"},
                "error":{}
            }
        else:
            for command in self.commands:

                if command.get("command").lower() == "sleep":
                    sleep(int(command.get("time", 0)))

                if command.get("command").lower() == "click":

                    if command.get("selector").lower() == "xpath":
                        try:self.driver_instance.find_element_by_xpath(command.get("path")).click()
                        except Exception as e:pass

                    if command.get("selector").lower() == "id":
                        try:self.driver_instance.find_element_by_id(command.get("path")).click()
                        except Exception as e:pass

                if command.get("command").lower() == "type":

                    if command.get("selector").lower() == "xpath":
                        try:self.driver_instance.find_element_by_xpath(command.get("path")).send_keys(command.get("search"))
                        except Exception as e:print("error: {}".format(e))

                    if command.get("selector") == "id":
                        try:self.driver_instance.find_element_by_xpath(command.get("path")).send_keys(command.get("search"))
                        except Exception as e:pass

        return True


class Crawler(ABC):

    @abstractmethod
    def run(self):
        """This will provide the Webdriver object """
        pass


class Scrapper(Commands, Crawler):

    """
    {
         url:"some url ",
         "commands":[
             {
                 "selector":"xpath",
                 "path":"/html/body/div[1]/div/form/div[1]/div/input",
                 "command":"type",
                 "search":"software Engineer"
              },
              {
                 "command":"sleep",
                 "time":"1"
              },
              {
                 "selector":"xpath",
                 "path":"//html/body/div[1]/div/form/button",
                 "command":"click"
              }
       ]
   }
    """

    def __init__(self, action):
        self.action = action
        Commands.__init__(self, commands=self.action.get("commands"))

    def run(self):

        driver = self.driver_instance
        driver.get(self.action.get("url"))

        commands = self.action.get("commands")
        self.execute()
        return driver.page_source


def main():

    scrapper_commands = {
        "url":"https://www.amazon.com/",
        "commands":[
            {
                "command":"sleep",
                "time":"3"
            },
            {
                "selector":"xpath",
                "path":"""//*[@id="twotabsearchtextbox"]""",
                "command":"type",
                "search":"Alexa"
            },
            {
                "command":"sleep",
                "time":"1"
            },
            {
                "selector":"xpath",
                "path":"""//*[@id="nav-search-submit-button"]""",
                "command":"click"
            }
        ]
    }
    instance  = Scrapper(action=scrapper_commands)
    html = instance = instance.run()
    print(html)

if __name__ == "__main__":
    main()


