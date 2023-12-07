from selenium import webdriver
from time import sleep
from selenium.webdriver.common.by import By

driver = webdriver.Firefox()
journeyStep = 1

urls = [
    'https://rapidstorapp.com.au/live-demo'
]

def getButton(driver, text):
    buttons = driver.find_elements(By.TAG_NAME, "button")
    for button in buttons:
        if button.text == text:
            if button.is_displayed():
                return button
        if text in button.text:
            if button.is_displayed():
                return button

def saveScreenshot(driver):
    driver.save_full_page_screenshot("step_" + str(journeyStep) + ".png")
    
def nextStepInJourney(button):
    button.click()
    sleep(1)
    global journeyStep
    journeyStep += 1
    
def processStorageTypesPage(driver):
    saveScreenshot(driver)
    button = getButton(driver, "Skip - Show me all prices")
    driver.execute_script("arguments[0].scrollIntoView();", button)
    sleep(1)
    if button:
        nextStepInJourney(button)
    
def processUnitListingPage(driver):
    saveScreenshot(driver)
    global journeyStep
    journeyStep += 1
    enquireButton = getButton(driver, "Enquire")
    if enquireButton:
        print("Clicking enquire button")
        driver.execute_script("arguments[0].scrollIntoView();", enquireButton)
        sleep(1)
        nextStepInJourney(enquireButton)
        saveScreenshot(driver)
    else:
        continueButton = getButton(driver, "Continue")
        if continueButton:
            print('Clicking continue button')
            driver.execute_script("arguments[0].scrollIntoView();", continueButton)
            sleep(1)
            nextStepInJourney(continueButton)
            saveScreenshot(driver)

def startSession(driver, url):
    # Open page in driver
    driver.get(url)
    # Sleep for 10 seconds to let RapidStorV2 load fully
    sleep(10)
    # After letting RapidStorV2 load we want to screenshot the first step, then click the skip button
    processStorageTypesPage(driver)
    # Now that we are on the slider page, we want to take a screenshot of the current view and the enquire modal if there is an enquire button. 
    # Then if there is a continue button we click that to progress
    processStorageTypesPage(driver)
    # We are now on the deals page, this is essentially the same process

startSession(driver, urls[0])
driver.quit()