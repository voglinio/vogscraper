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
listings_file = "tripadvisor_zakynthos_restaurants.csv"
df = pd.read_csv(listings_file, header=None)
df.columns = ['id', 'title', 'href',  'reviews', 'cuisine', 'money', 'stars']
urls = df.href.tolist()
ids = df.id.tolist()
reviews = df.reviews.tolist()

#
#print("found ", len(urls))
#
path_to_file = "tripadvisor_zakynthos_restaurants_reviews.csv"
csvFile = open(path_to_file, "w", encoding="utf-8")
csvWriter = csv.writer(csvFile)


for i in range(len(ids)):
    try:
        url = urls[i]
        max_reviews = reviews[i]
        chrome_options = Options()
        driver = webdriver.Chrome(options=chrome_options)
        driver.implicitly_wait(5)
        driver.get(url)
        time.sleep(4)

        overlay = driver.find_element(By.ID, "onetrust-accept-btn-handler")
        overlay.click()
        time.sleep(2)

        ipages = 0
        ireviews = 0
        print (i, ids[i], max_reviews, int(np.ceil(max_reviews/15)))

        for jj in range(int(np.ceil(max_reviews/15))):

            container = driver.find_elements(By.XPATH, '//div[@class="review-container"]')
            print ("loading page ", ipages, ' =>', len(container), '=', ireviews)

            for j in range(len(container)):
                txt = container[j].text
                splits = txt.split("\n")
                name = splits[0]
                review_date = splits[2]
                review_date = review_date.replace('Reviewed ', '')
                title = container[j].find_element(By.CLASS_NAME, 'noQuotes')
                title = title.text
                title = title.replace(",", " ")

                body = container[j].find_element(By.CLASS_NAME, 'prw_reviews_text_summary_hsx')
                body = body.text
                body = body.replace(",", " ")

                visit_date = container[j].find_element(By.CLASS_NAME, "prw_reviews_stay_date_hsx")
                visit_date = visit_date.text
                visit_date = visit_date.replace('Date of visit: ', '')

                rating = container[j].find_element(By.CLASS_NAME, 'ui_bubble_rating')
                rating = rating.get_attribute('class')
                rating = rating.split(" ")[1]


                print (ireviews, name, review_date, title, body, visit_date, rating)
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
                ireviews = ireviews + 1
                pass

            el = driver.find_elements(By.XPATH, "//a[@data-page-number]")
            if len(el) > 2:
                if ipages == 0:
                    el[0].click()
                else:
                    el[1].click()

            time.sleep(3)
            ipages = ipages +1

        driver.quit()
    except:
        print ("pass")
        driver.quit()
