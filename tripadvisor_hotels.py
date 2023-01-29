# Write your code here :-)
import sys
import csv
from selenium import webdriver
import time
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
import pandas as pd
from os.path import exists
import numpy as np

import os

# default path to file to store data
path_to_file = "tripadvisor_corfu_hotels.csv"
#os.remove(path_to_file)

if exists(path_to_file):
    df = pd.read_csv(path_to_file, header=None)
    list_ids = df[0].values.astype('str').tolist()
    print("Starting with ", len(df), " properties", len(list_ids))
else:
    list_ids = []
    print("Starting on empty file")

# default number of scraped pages
num_page = 17

# default tripadvisor website of hotel or things to do (attraction/monument)

urls = ["https://www.tripadvisor.com/Hotels-g189458-zft21371-Corfu_Ionian_Islands-Hotels.html"]

tagakia = ["Excellent", "Very good", "Average", "Poor", "Terrible"]

# if you pass the inputs in the command line
if len(sys.argv) == 4:
    path_to_file = sys.argv[1]
    num_page = int(sys.argv[2])
    url = sys.argv[3]

# import the webdriver
# chrome_options.add_argument("--headless")

# open the file to save the review
csvFile = open(path_to_file, "w", encoding="utf-8")
csvWriter = csv.writer(csvFile)


inew = 1

for url in urls:
    print(url)
    # try:
    chrome_options = Options()
    driver = webdriver.Chrome(options=chrome_options)
    driver.implicitly_wait(1)

    driver.get(url)
    time.sleep(4)

    overlay = driver.find_element(By.ID, "onetrust-accept-btn-handler")
    overlay.click()
    time.sleep(2)

    num_results_span = driver.find_elements(By.CLASS_NAME, "qrwtg")
    print(num_results_span)
    if len(num_results_span) > 0:
        num_results_text = num_results_span[0].text
        if "of" in num_results_text:
            ss = num_results_text.split("of")[0]
            ss = ss.replace(",", "")
        else:
            ss = num_results_text.split(" ")[0]
            ss = ss.replace(",", "")
        print(ss)
        num_page = int(np.ceil(int(ss) / 30))
    else:
        num_page = 40
    print("num page", num_page)

    # change the value inside the range to save more or less reviews
    ihotels = 0
    for i in range(0, num_page):
        print("i = ", i)

        # expand the review
        time.sleep(7)
        #
        # see more button
        seemore = driver.find_elements(By.CLASS_NAME, 'pexOo')
        if len(seemore) > 0:
            seemore[0].click()

        # driver.find_element_by_xpath(".//div[contains(@data-test-target, 'expand-review')]").click()
        container = driver.find_elements(By.XPATH, "//div[@data-locationid]")
        print(len(container))

        for j in range(len(container)):
            print (j, ihotels)

            try:
                elem = container[j].find_element(By.CLASS_NAME, "property_title")
                title = elem.text
                ttt = title.split(".")
                if len(ttt) > 1:
                    title = ttt[1]
                title = title.replace(",", " ")
                href = elem.get_attribute("href")

                id = href.split("/")[-1].split(".")[0]

                reviews = 0
                elem = container[j].find_elements(By.CLASS_NAME, "review_count")
                if len(elem) > 0:
                    txt = elem[0].text
                    txt = txt.replace(",", "")

                    ttt = txt.split(" ")
                    if len(ttt) > 0:
                        reviews = int(ttt[0])


                rating = -1
                elem = container[j].find_elements(By.CLASS_NAME, "ui_bubble_rating")
                if len(elem) > 0:
                    txt = elem[0].get_attribute('alt')
                    ttt = txt.split(" ")
                    if len(ttt) > 0:
                        rating = float(ttt[0])


                hotel_icons = ""
                elem = container[j].find_elements(By.CLASS_NAME, "prw_common_hotel_icons_list")
                if len(elem) > 0:
                    hotel_icons = elem[0].text
                    hotel_icons = hotel_icons.replace("\n", ";")

                if id not in list_ids:
                    list_ids.append(id)
                    print(ihotels, id, title, reviews, rating)
                    ihotels = ihotels + 1
                    csvWriter.writerow(
                        [
                            id,
                            title,
                            href,
                            reviews,
                            rating,
                            hotel_icons
                        ]
                    )
                    csvFile.flush()
            except:
                print ('next next')

        el = driver.find_elements(By.XPATH, "//a[@data-page-number]")
        if len(el) > 2:
            if i == 0:
                el[0].click()
            else:
                el[1].click()

        csvFile.flush()

    driver.quit()
#    except:
#        print ('skip')
#        driver.quit()
# Write your code here :-)
# Write your code here :-)
