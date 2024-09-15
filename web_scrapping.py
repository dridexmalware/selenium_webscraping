import bs4
import requests
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import os
import time

def download_image(url, folder_name, num):
    response = requests.get(url)
    if response.status_code == 200:
        with open(os.path.join(folder_name, str(num) + ".jpg"), 'wb') as file:
            file.write(response.content)

folder_name = 'car_accidents'
if not os.path.isdir(folder_name):
    os.makedirs(folder_name)

chromePath = r'C:\Users\yuljh\Downloads\PythonScripts\Drivers\chromedriver.exe'
service = Service(chromePath)
driver = webdriver.Chrome(service=service)

search_URL = "https://www.google.com/search?q=philippine+car+accidents&source=lnms&tbm=isch"
driver.get(search_URL)

input("Waiting for user input to start...")

driver.execute_script("window.scrollTo(0, 0);")

page_html = driver.page_source
pageSoup = bs4.BeautifulSoup(page_html, 'html.parser')
containers = pageSoup.findAll('div', {'class': "eA0Zlc WghbWd FnEtTd mkpRId m3LIae RLdvSe qyKxnc ivg-i PZPZlf GMCzAd"})

len_containers = len(containers)
print("Found %s image containers" % len_containers)

for i in range(1, len_containers + 1):
    if i % 25 == 0:
        continue

    xPath = f"(//div[@class='eA0Zlc WghbWd FnEtTd mkpRId m3LIae RLdvSe qyKxnc ivg-i PZPZlf GMCzAd'])[{i}]"
    
    try:
        previewImageElement = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.XPATH, xPath))
        )
        previewImageURL = previewImageElement.find_element(By.TAG_NAME, 'img').get_attribute("src")
        previewImageElement.click()

        timeStarted = time.time()

        while True:
            imageElement = WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.XPATH, """//*[@id="Sva75c"]/div[2]/div[2]/div/div[2]/c-wiz/div/div[3]/div[1]/a/img"""))
            )
            imageURL = imageElement.get_attribute('src')

            if imageURL != previewImageURL:
                break
            else:
                currentTime = time.time()
                if currentTime - timeStarted > 10:
                    print("Timeout! Will download a lower resolution image and move onto the next one")
                    break

        try:
            download_image(imageURL, folder_name, i)
            print("Downloaded element %s out of %s total. URL: %s" % (i, len_containers + 1, imageURL))
        except Exception as e:
            print(f"Couldn't download image {i}, continuing. Error: {e}")

    except Exception as e:
        print(f"Couldn't find the preview image element {i}. Error: {e}")
        continue
