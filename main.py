from selenium import webdriver
from time import sleep
from selenium.webdriver.common.by import By
from random import random
from print_color import print
import json

urls = [
    'https://rapidstorapp.com.au/live-demo',
    'https://mammothselfstore.com.au/book-online-2/',
]

class Logger():
    def __init__(self, level, message):
        self.level = level
        self.message = message
        self.log()
        
    def log(self):
        # Level 1 is a pass
        if self.level == 1:
            print(self.message, tag='SUCCESS', tag_color='green', color='white')
        # Level 2 is a fail
        if self.level == 2:
            print(self.message, tag='FAILED', tag_color='red', color='white')

class UITest():

    def __init__(self, url, testName):
        self.url = url
        self.testName = testName
        self.journeyStep = 0
        self.formattedUrl = url.replace('https://', '').replace('http://', '').split('.')[0]
        # Get the required URL with a cache bust timestamp to ensure we get the latest deployment
        self.getTestSteps()
        self.driver = webdriver.Firefox()
        self.driver.get(url + "?cb=" + str(random()))
        # Wait 8 seconds for the RS embed to load - Should probably just ping an element from the system until it appears, this works for now.
        sleep(8)
        self.runTest()

    def runTest(self):
        print("Starting Test For:" + self.url)
        for step in self.testSteps:
            self.runStep(step)
            sleep(1)
            self.journeyStep += 1

    def getTestSteps(self):
        testFile = open('tests/' + self.testName + '.json')
        testFile = json.load(testFile)
        self.testSteps = testFile

    def runStep(self, step):
        # Die
        if step['event'] == 'die':
            self.driver.quit()
            logger = Logger(1, 'Die event found, test ended')
        # Setup Target Div
        if step['event'] == 'target_div':
            self.targetDiv = step['value']
            logger = Logger(1, step['event'] + ' #' + step['value'] + ' set')
        # Capture Screenshot
        if step['event'] == 'screenshot':
            self.captureScreenshot()
        # Find Element On Page
        if step['event'] == 'find':
            if step['target'] == 'button':
                button = self.findButton(step['target'], step['value'])
                while button == None:
                    if step['fail'] == 'iterate':
                        if step['iterator']['target'] == 'button' and step['iterator']['event'] == 'click':
                            iterateButton = self.findButton('button', step['iterator']['value'])
                            self.clickButton(iterateButton)
                            button = self.findButton(step['target'], step['value'])
                    if step['fail'] == 'die':
                        self.driver.quit()
                        logger = Logger(2, 'failed at: ' + str(step['event']))
                    if step['fail'] == 'skip':
                        return
                if button:
                    for then in step['then']:
                        if then['event'] == 'click':
                            self.clickButton(button)
                            logger = Logger(1, then['event'] + ' - ' + step['target'] + ' - ' + step['value'])
                            sleep(1)
                        if then['event'] == 'screenshot':
                            self.captureScreenshot()
                        if then['event'] == 'find':
                            if then['target'] == 'button':
                                thenButton = self.findButton(then['target'], then['value'])
                                for evThen in then['then']:
                                    if evThen['event'] == 'click':
                                        self.clickButton(thenButton)
                                        logger = Logger(1, evThen['event'] + ' - ' + then['target'] + ' - ' + then['value'])
                            

    def findButton(self, elementType, value):
        buttons = self.driver.find_elements(By.TAG_NAME, elementType)
        for button in buttons:
            if button.text == value and button.is_displayed():
                return button
            if value in button.text and button.is_displayed():
                return button
    
    def clickButton(self, button):
        self.driver.execute_script("arguments[0].scrollIntoView();", button)
        sleep(1)
        self.driver.execute_script("arguments[0].click();", button)

    def captureScreenshot(self):
        if self.targetDiv is None:
            logger = Logger(2, 'unable to capture screenshot of targetDiv None')
            self.driver.quit()
        targetElement = self.driver.find_element(By.ID, self.targetDiv)
        targetElement.screenshot(self.formattedUrl + str('_' + str(random())) + ".png")
        logger = Logger(1, 'screenshot saved of #' + self.targetDiv)

uitest = UITest(urls[0], 'rapidstorv2')