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


# default path to file to store data
path_to_file = "tripadvisor_zakynthos_restaurants.csv"

if exists(path_to_file):
    df = pd.read_csv(path_to_file, header=None)
    list_ids = df[0].values.tolist()
    print("Starting with ", len(df), " properties", len(list_ids))
else:
    list_ids = []
    print("Starting on empty file")

# default number of scraped pages
num_page = 17

# default tripadvisor website of hotel or things to do (attraction/monument)

urls = ["https://www.tripadvisor.com/Restaurants-g189462-Zakynthos_Ionian_Islands.html"]
tagakia = ["Excellent", "Very good", "Average", "Poor", "Terrible"]

# if you pass the inputs in the command line
if len(sys.argv) == 4:
    path_to_file = sys.argv[1]
    num_page = int(sys.argv[2])
    url = sys.argv[3]

# import the webdriver
# chrome_options.add_argument("--headless")

# open the file to save the review
csvFile = open(path_to_file, "a", encoding="utf-8")
csvWriter = csv.writer(csvFile)


inew = 1

for url in urls:
    print(url)
    # try:
    chrome_options = Options()
    driver = webdriver.Chrome(options=chrome_options)
    driver.implicitly_wait(5)
    driver.get(url)
    time.sleep(4)

    overlay = driver.find_element(By.ID, "onetrust-accept-btn-handler")
    overlay.click()
    time.sleep(2)

    num_results_span = driver.find_elements(By.CLASS_NAME, "SgeRJ")
    print(num_results_span)
    if len(num_results_span) > 0:
        num_results_text = num_results_span[0].text
        ss = num_results_text.split(" ")[0]
        print(ss)
        num_page = int(np.ceil(int(ss) / 30))
    else:
        num_page = 40
    print("num page", num_page)

    # change the value inside the range to save more or less reviews
    for i in range(0, num_page):
        print("i = ", i)

        # expand the review
        time.sleep(7)
        # driver.find_element_by_xpath(".//div[contains(@data-test-target, 'expand-review')]").click()
        container = driver.find_elements(By.XPATH, "//div[@data-test]")
        print(len(container))

        for j in range(len(container)):
            try:
                elem = container[j].find_element(By.CLASS_NAME, "RfBGI")
                title = elem.text
                ttt = title.split(".")
                if len(ttt) > 1:
                    title = ttt[1]
                title = title.replace(",", " ")

                elem = container[j].find_element(By.CLASS_NAME, "Lwqic")
                href = elem.get_attribute("href")

                elem = container[j].find_element(By.CLASS_NAME, "IiChw")
                reviews = elem.text.split(" ")[0]
                reviews = reviews.replace(",", "")

                elems = container[j].find_elements(By.CLASS_NAME, "qAvoV")
                cuisine = ""
                money = ""
                if len(elems) > 3:
                    cuisine = elems[2].text
                    cuisine = cuisine.replace(",", "-")
                    money = elems[3].text

                elem = container[j].find_element(By.CLASS_NAME, "UctUV")
                stars = elem.get_attribute("aria-label")

                id = href.split("/")[-1].split(".")[0]
                if id not in list_ids:

                    print(inew, id, title, href, reviews, cuisine, money, stars)
                    inew = inew + 1
                    csvWriter.writerow(
                        [
                            id,
                            title,
                            href,
                            reviews,
                            cuisine,
                            money,
                            stars,
                        ]
                    )
                    csvFile.flush()

            except:
                print("nope!", title)
                pagedriver.quit()

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
