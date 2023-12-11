from selenium import webdriver
from time import sleep
from selenium.webdriver.common.by import By
from random import random
import json


journeyStep = 1

urls = [
    'https://rapidstorapp.com.au/live-demo',
    'https://mammothselfstore.com.au/book-online-2/',
]

currentUrl = ''



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
        # Setup Target Div
        if step['event'] == 'target_div':
            self.targetDiv = step['value']
        # Capture Screenshot
        if step['event'] == 'screenshot':
            self.captureScreenshot()
        # Find Element On Page
        if step['event'] == 'find':
            if step['target'] == 'button':
                button = self.findButton(step['target'], step['value'])
                if button:
                    for then in step['then']:
                        if then['event'] == 'click':
                            self.clickButton(button)
                            sleep(1)
                        if then['event'] == 'screenshot':
                            self.captureScreenshot()
                        if then['event'] == 'find':
                            if then['target'] == 'button':
                                thenButton = self.findButton(then['target'], then['value'])
                                for evThen in then['then']:
                                    if evThen['event'] == 'click':
                                        self.clickButton(thenButton)

                else:
                    if step['fail'] == 'die':
                        self.driver.quit()
                        raise Exception('Test Failed: ' + str(step['event']))
                    if step['fail'] == 'skip':
                        return
                    if step['fail'] == 'try'

    def findButton(self, elementType, value):
        buttons = self.driver.find_elements(By.TAG_NAME, elementType)
        for button in buttons:
            if button.text == value:
                return button
            if value in button.text:
                return button
    
    def clickButton(self, button):
        self.driver.execute_script("arguments[0].scrollIntoView();", button)
        sleep(1)
        self.driver.execute_script("arguments[0].click();", button)

    def captureScreenshot(self):
        if self.targetDiv is None:
            print("Unable to capture screenshot as targetDiv is None")
            return
        targetElement = self.driver.find_element(By.ID, self.targetDiv)
        targetElement.screenshot(self.formattedUrl + "_step_" + str(self.journeyStep) + ".png")
        print("Saved screenshot of " + self.targetDiv)

uitest = UITest(urls[0], 'rapidstorv2')

# def getButton(driver, text):
#     buttons = driver.find_elements(By.TAG_NAME, "button")
#     for button in buttons:
#         if button.text == text:
#             if button.is_displayed():
#                 return button
#         if text in button.text:
#             if button.is_displayed():
#                 return button

# def saveScreenshot(driver):
#     global currentUrl
#     rapidstorEmbed = driver.find_element(By.ID, 'rapidstor-v2-frontend')
#     rapidstorEmbed.screenshot(currentUrl + "_step_" + str(journeyStep) + ".png")
#     # driver.save_full_page_screenshot(currentUrl + "_step_" + str(journeyStep) + ".png")
    
# def nextStepInJourney(driver, button):
#     clickButton(driver, button)
#     sleep(1)
#     global journeyStep
#     journeyStep += 1

# def scrollButtonIntoView(driver, button):
#     driver.execute_script("arguments[0].scrollIntoView();", button)

# def clickButton(driver, button):
#     driver.execute_script("arguments[0].click();", button)
    
# def processStorageTypesPage(driver):
#     saveScreenshot(driver)
#     button = getButton(driver, "Skip - Show me all prices")
#     scrollButtonIntoView(driver, button)
#     sleep(1)
#     if button:
#         nextStepInJourney(driver, button)

# def carouselBigger(driver):
#     biggerButton = getButton(driver, "Larger")
#     scrollButtonIntoView(driver, biggerButton)
#     clickButton(driver, biggerButton)
    
# def processUnitListingPage(driver):
#     saveScreenshot(driver)
#     global journeyStep
#     journeyStep += 1
#     enquireButton = getButton(driver, "Enquire")
#     if enquireButton:
#         scrollButtonIntoView(driver, enquireButton)
#         sleep(1)
#         nextStepInJourney(driver, enquireButton)
#         saveScreenshot(driver)
#         cancelButton = getButton(driver, "Cancel")
#         scrollButtonIntoView(driver, cancelButton)
#         sleep(1)
#         clickButton(driver, cancelButton)
#         continueButton = getButton(driver, "Continue")
#         while continueButton == None:
#             carouselBigger(driver)
#             continueButton = getButton(driver, "Continue")
#         if continueButton:
#             scrollButtonIntoView(driver, continueButton)
#             sleep(1)
#             nextStepInJourney(driver, continueButton)
#             saveScreenshot(driver)
#     else:
#         continueButton = getButton(driver, "Continue")
#         if continueButton:
#             scrollButtonIntoView(driver, continueButton)
#             sleep(1)
#             nextStepInJourney(driver, continueButton)
#             saveScreenshot(driver)

# def processDealsPage(driver):
#     saveScreenshot(driver)
#     global journeyStep
#     journeyStep += 1
#     continueButton = getButton(driver, "Continue")
#     scrollButtonIntoView(driver, continueButton)
#     clickButton(driver, continueButton)
#     sleep(2)

# def processUpsellPage(driver):
#     saveScreenshot(driver)

# def startSession(driver, url):
#     global currentUrl
#     currentUrl = u.replace('https://', '').replace('http://', '').split('.')[0]
#     # Open page in driver
#     driver.get(url + "?cachebust=" + str(random()))
#     # Sleep for 10 seconds to let RapidStorV2 load fully
#     sleep(10)
#     # After letting RapidStorV2 load we want to screenshot the first step, then click the skip button
#     processStorageTypesPage(driver)
#     # Now that we are on the slider page, we want to take a screenshot of the current view and the enquire modal if there is an enquire button. 
#     # Then if there is a continue button we click that to progress
#     processUnitListingPage(driver)
#     # We are now on the deals page, this is essentially the same process
#     processDealsPage(driver)
#     # Now onto the upsell/variants page
#     processUpsellPage(driver)

# for u in urls:
#     journeyStep = 1
#     print("Starting UI Test for: " + u)
#     driver = webdriver.Firefox()
#     startSession(driver, u)
#     driver.quit()