import sys
import csv
import selenium
from selenium import webdriver
import time
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
import pandas as pd

from selenium.common.exceptions import WebDriverException


# default path to file to store data
listings_file = "aibnb_corfu_gouvia.csv"
df = pd.read_csv(listings_file, header=None)
df.columns = ['id', 'title', 'text', 'beds', 'date', 'rate', 'price', 'total']
urls = df.id.tolist()

print("found ", len(urls))

path_to_file = "aibnb_corfu_gouvia_reviews.csv"

#df  = pd.read_csv(path_to_file, header=None)
#print ("Starting with ", len(df), " properties" )

# default number of scraped pages
num_page = 3

# default tripadvisor website of hotel or things to do (attraction/monument)

#urls = ["31283658",  "10691883", "652820565764195736", "51516782",]
urls = [url.split("_")[1] for url in urls]


# if you pass the inputs in the command line
if (len(sys.argv) == 4):
    path_to_file = sys.argv[1]
    num_page = int(sys.argv[2])
    url = sys.argv[3]

# import the webdriver
#chrome_options.add_argument("--headless")


# open the file to save the review
csvFile = open(path_to_file, 'w', encoding="utf-8")
csvWriter = csv.writer(csvFile)


inew = 1

for url in urls:
    print (url)
    try:
        chrome_options = Options()
        driver = webdriver.Chrome(options=chrome_options)
        driver.implicitly_wait(5)
        driver.get("https://www.airbnb.com/rooms/" + url)
        time.sleep(5)

        close_translation_buttons = driver.find_elements(By.CLASS_NAME, "czcfm7x")
        print ("translation: ", len(close_translation_buttons))
        if len(close_translation_buttons) == 1:
            print("closing...")
            close = close_translation_buttons[0]
            close.click()
            time.sleep(1)

        if len(close_translation_buttons) > 2:
            close = close_translation_buttons[2]
            close.click()
            time.sleep(1)


        els =  driver.find_elements(By.CLASS_NAME, "_11eqlma4")
        if len(els) > 0:
            el =els[0]

            el.click()

            time.sleep(3)
            sups = driver.find_elements(By.CLASS_NAME, "_17itzz4")
            if len(sups) > 0:
                sup = sups[0]

                prev_levs = -1
                for i in range(40):
                    driver.execute_script("arguments[0].scrollTop = arguments[0].scrollHeight;", sup);
                    time.sleep(3)
                    revs = driver.find_elements(By.CLASS_NAME,"r1are2x1")
                    print ('found  -> ', len(revs))
                    if len(revs) == prev_levs:
                        break
                    prev_levs = len(revs)


                for i in range(len(revs)):
                    comment = revs[i].text
                    comment = comment.replace('\n', ' ')
                    comment = comment.replace(',', ' ')
                    csvWriter.writerow([url, comment])

                    print (comment)

                csvFile.flush()


        driver.quit()
    except WebDriverException:
        print ("continue")
