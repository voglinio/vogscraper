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
path_to_file = "tripadvisor_zakynthos_v4.csv"

if exists(path_to_file):
    #df = pd.read_csv(path_to_file, header=None)
    #list_ids = df[0].values.tolist()
    #print("Starting with ", len(df), " properties", len(list_ids))
#else:
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
            #try:
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
            reviews = reviews.replace(",", ".")

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
                pagedriver = webdriver.Chrome(options=chrome_options)
                pagedriver.implicitly_wait(5)
                pagedriver.get(href)
                time.sleep(4)
                overlay = pagedriver.find_element(By.ID, "onetrust-accept-btn-handler")
                overlay.click()
                time.sleep(2)
                ratings = pagedriver.find_elements(By.CLASS_NAME, "DzMcu")
                vals = ["", "", "", ""]
                for k in range(len(ratings)):
                    type = ratings[k].find_element(By.CLASS_NAME, "BPsyj")
                    type = type.text
                    value = ratings[k].find_element(
                        By.CLASS_NAME, "ui_bubble_rating"
                    )
                    value = value.get_attribute("class")
                    value = value.split(" ")[1]
                    vals[k] = value
                    print("--> ", type, value)

                coords = pagedriver.find_elements(
                    By.XPATH, "//span[@data-test-target]"
                )
                lat = long = -1
                if len(coords) > 0:
                    imgs = coords[0].find_elements(By.TAG_NAME, "img")
                    if len(imgs) > 0:
                        img = imgs[0].get_attribute("src")
                        lat = float(img.split("|")[1].split("&")[0].split(",")[0])
                        long = float(img.split("|")[1].split("&")[0].split(",")[1])
                        print("--> ", lat, long)

                tparams = pagedriver.find_elements(
                    By.XPATH, '//div[@data-param="trating"]'
                )
                travel_ratings = tparams[0].find_elements(By.CLASS_NAME, "row_num")
                temp = [-1, -1, -1, -1, -1]
                if len(travel_ratings) == 5:
                    for k in range(len(travel_ratings)):
                        print(tagakia[k], travel_ratings[k].text)
                        tttt = travel_ratings[k].text.replace(',', '')
                        temp[k] = int(tttt)


                #
                # Get Languages:
                # Step 1: Click on more languages
                lang_dict = {"English": 0, "Greek":0, "German":0, "Italian":0, "French": 0, "Russian":0, "Other": 0}

                el = pagedriver.find_elements(By.XPATH, '//div[@data-param="filterLang"]')
                print ("====> el")
                if len(el) > 0:
                   taLinks = el[0].find_elements(By.CLASS_NAME, 'taLnk')
                   if len(taLinks) > 0:
                       taLinks[0].click()
                       time.sleep(1)
                       print ("Clicked")
                       #
                       # Step 2: Once clicked get languages
                       el = pagedriver.find_elements(By.CLASS_NAME, 'more-options')
                       if len(el) > 0:
                           print (el[0].text)
                           #
                           # Step 3: Close the overlay window_height
                           el = pagedriver.find_elements(By.CLASS_NAME, 'ui_close_x')
                           if len(el) > 0:
                               el[1].click()
                               time.sleep(2)
                               print ("ui_close_x")

                #
                # Get Loops:
                # Step 1: Click on ALL languages
                el = pagedriver.find_elements(By.ID, 'filters_detail_language_filterLang_ALL')
                if len(el) > 0:
                    el[0].click()
                    time.sleep(3)
                    #
                    # Step 2: Loop Traveler Type
                    ttypes = ["Families", "Couples", "Solo", "Business", "Friends"]


                    #
                    # Step 3: Loop Time of year
                    ttypes = ["Mar-May", "Jun-Aug", "Sep-Nov", "Dec-Feb"]
                    data_ttypes = np.zeros((4, 5))
                    try:
                        ii = 0
                        for ttype in ttypes:
                            print("======> ", ttype)
                            ii = ii + 1
                            search_string= '//label[@for="filters_detail_checkbox_filterSeasons__'+str(ii)+'"]'
                            clikme = pagedriver.find_elements(By.XPATH, search_string)
                            if len(clikme) > 0:
                                clikme[0].click()
                                time.sleep(2)

                            tparams = pagedriver.find_elements(By.XPATH, '//div[@data-param="trating"]' )

                            travel_ratings = tparams[0].find_elements(By.CLASS_NAME, "row_num")
                            temp = [-1, -1, -1, -1, -1]
                            if len(travel_ratings) == 5:
                                for k in range(len(travel_ratings)):
                                    #print(tagakia[k], travel_ratings[k].text)
                                    tttt = travel_ratings[k].text.replace(',', '')
                                    temp[k] = int(tttt)
                                    data_ttypes[ii-1, k] = temp[k]

                            clikme = pagedriver.find_elements(By.XPATH, search_string)
                            if len(clikme) > 0:
                                clikme[0].click()
                                time.sleep(2)
                    except:
                        print('next time')


                print (data_ttypes)
                pagedriver.quit()

                print(inew, id, title, href, reviews, cuisine, money, stars)
                inew = inew + 1
                csvWriter.writerow(
                    [
                        id,
                        title,
                        lat,
                        long,
                        href,
                        reviews,
                        cuisine,
                        money,
                        stars,
                        vals[0],
                        vals[1],
                        vals[2],
                        vals[3],
                        temp[0],
                        temp[1],
                        temp[2],
                        temp[3],
                        temp[4],
                    ]
                )
                csvFile.flush()

            #except:
            #    print("nope!", title)
            #    pagedriver.quit()

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
