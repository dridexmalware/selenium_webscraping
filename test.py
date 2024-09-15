from selenium import webdriver
from selenium.webdriver.chrome.service import Service

chromePath = r'C:\Users\yuljh\OneDrive\Documents\PythonScripts\Drivers\chromedriver.exe'
service = Service(executable_path=chromePath)
driver = webdriver.Chrome(service=service)
driver.get('https://www.google.com')
