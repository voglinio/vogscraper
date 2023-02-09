# Write your code here :-)
# Write your code here :-)
import sys
import csv
import selenium
from selenium import webdriver
import time
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
import pandas as pd
import numpy as np

from selenium.common.exceptions import WebDriverException

#
# default path to file to store data
listings_file = "tripadvisor_corfu_hotels.csv"
df = pd.read_csv(listings_file, header=None)

df.columns = ['id', 'title', 'href',  'reviews', 'rating', 'hotel_icons']
urls = df.href.tolist()
ids = df.id.tolist()
reviews = df.reviews.tolist()

#
#print("found ", len(urls))
#
path_to_file = "tripadvisor_corfu_hotels_reviews.csv"
csvFile = open(path_to_file, "w", encoding="utf-8")
csvWriter = csv.writer(csvFile)

itotal = 0
for i in range(len(ids)):
    try:
        url = urls[i]
        max_reviews = reviews[i]
        chrome_options = Options()
        chrome_options.add_argument("--headless")
        driver = webdriver.Chrome(options=chrome_options)
        driver.implicitly_wait(2)
        driver.get(url)
        time.sleep(4)

        overlay = driver.find_element(By.ID, "onetrust-accept-btn-handler")
        overlay.click()
        time.sleep(2)

        ipages = 0
        ireviews = 0
        print (i, ids[i], max_reviews, int(np.ceil(max_reviews/10)))

        for jj in range(int(np.ceil(max_reviews/10))):
            container = driver.find_elements(By.XPATH, '//div[@data-test-target="HR_CC_CARD"]')
            print ("loading page ", ipages, ' =>', len(container), '=', ireviews, '<->', max_reviews)
            time.sleep(1)
            for j in range(len(container)):
                try:
                    ireviews = ireviews + 1
                    itotal = itotal + 1
                    title = ""
                    elems = container[j].find_elements(By.CLASS_NAME, 'Qwuub')
                    if len(elems) > 0:
                        title = elems[0].text
                        title = title.replace("\n", " ")

                    body = ""
                    elems = container[j].find_elements(By.CLASS_NAME, 'QewHA')
                    if len(elems) > 0:
                        body = elems[0].text
                        body = body.replace("\n", " ")
                        body = body.replace(",", " ")

                    rating = ""
                    elem = container[j].find_elements(By.CLASS_NAME, 'ui_bubble_rating')
                    if len(elem) > 0:
                        rating = elem[0]
                        rating = rating.get_attribute('class')
                        rating = rating.split(" ")[1]

                    visit_date = ""
                    elem = container[j].find_elements(By.CLASS_NAME, "teHYY")
                    if len(elem) > 0:
                        visit_date = elem[0]
                        visit_date = visit_date.text
                        ttt = visit_date.split(":")
                        if len(ttt) > 0:
                            visit_date = ttt[1]
                            visit_date = visit_date[1:]

                    name = ""
                    elem = container[j].find_elements(By.CLASS_NAME, "ui_header_link")
                    if len(elem) > 0:
                        name = elem[0].text


                    review_date = ""
                    elem = container[j].find_elements(By.CLASS_NAME, "cRVSd")
                    if len(elem) > 0:
                        review_date = elem[0].text
                        review_date = review_date.split("wrote a review")[1]
                        review_date = review_date[1:]

                    print (i, jj, ireviews, itotal, name, title, review_date, visit_date, rating)


                    csvWriter.writerow(
                            [
                                ids[i],
                                name,
                                review_date,
                                title,
                                body,
                                visit_date,
                                rating
                            ]
                        )
                    csvFile.flush()
                except:
                    print ("review level exception")


            el = driver.find_elements(By.CLASS_NAME, "next")
            if len(el) > 0:
                el[0].click()

            time.sleep(4)
            ipages = ipages +1

        driver.quit()
    except:
       print ("property level exception")
       driver.quit()
