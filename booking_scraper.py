import sys
import csv
from selenium import webdriver
import time
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
import pandas as pd
from os.path import exists
import os

# default path to file to store data
path_to_file = "booking_zakinthos.csv"
os.remove(path_to_file)

if exists(path_to_file):
    df  = pd.read_csv(path_to_file, header=None)
    list_ids = df[0].values.tolist()
    print ("Starting with ", len(df), " properties", len(list_ids) )
else:
    list_ids = []
    print ("Starting on empty file")

# default number of scraped pages
num_page = 40

# default tripadvisor website of hotel or things to do (attraction/monument)

urls = [
"https://www.booking.com/searchresults.en-gb.html?ss=Zakynthos%2C+Ionian+Islands%2C+Greece&ssne=Zakynthos&ssne_untouched=Zakynthos&label=gen173nr-1FCAEoggI46AdIM1gEaFyIAQGYAQm4AQfIAQzYAQHoAQH4AQuIAgGoAgO4Aunvjp4GwAIB0gIkNWE0NWYxMTEtODAzMS00OTZmLTg4MzAtZWYzNjM1ZDZlOWFh2AIG4AIB&sid=b8ea07e999a05e717bd0890acdbef409&aid=304142&lang=en-gb&sb=1&src_elem=sb&src=searchresults&dest_id=-831270&dest_type=city&ac_position=1&ac_click_type=b&ac_langcode=xu&ac_suggestion_list_length=5&search_selected=true&search_pageview_id=6d903afee75c02af&ac_meta=GhA2ZDkwM2FmZWU3NWMwMmFmIAEoATICeHU6A1pha0AASgBQAA%3D%3D&checkin=2023-07-01&checkout=2023-07-06&group_adults=2&no_rooms=1&group_children=0&sb_travel_purpose=leisure"
]

pages = [
10
]


# if you pass the inputs in the command line
if (len(sys.argv) == 4):
    path_to_file = sys.argv[1]
    num_page = int(sys.argv[2])
    url = sys.argv[3]

# import the webdriver
#chrome_options.add_argument("--headless")


# open the file to save the review
csvFile = open(path_to_file, 'a', encoding="utf-8")
csvWriter = csv.writer(csvFile)


inew = len(list_ids)
ii = -1
for url in urls:
    print (url)
    ii = ii + 1
#    try:
    chrome_options = Options()
    driver = webdriver.Chrome(options=chrome_options)
    driver.implicitly_wait(5)
    driver.get(url)
    time.sleep(4)
    overlay = driver.find_elements(By.XPATH, '//button[@id="onetrust-accept-btn-handler"]')
    if len(overlay) > 0:
        overlay[0].click()

    # change the value inside the range to save more or less reviews
    num_page = pages[ii]
    for i in range(0, num_page):

        # expand the review
        time.sleep(7)
        #driver.find_element_by_xpath(".//div[contains(@data-test-target, 'expand-review')]").click()

        #container = driver.find_elements_by_xpath("//div[@data-reviewid]")
        container = driver.find_elements(By.XPATH, '//div[@data-testid="property-card"]')
        scores = driver.find_elements(By.XPATH, '//div[@data-testid="review-score"]')
        prices = driver.find_elements(By.XPATH, '//div[@data-testid="price-for-x-nights"]')
        address = driver.find_elements(By.XPATH, '//span[@data-testid="address"]')



         #dates = driver.find_elements_by_xpath(".//div[@class='EftBQ']")
        print ("len", len(container), "scores", len(scores), "prices", len(prices), "address", len(address))
        time.sleep(3)

        for j in range(len(container)):
            try:
                elem = container[j].find_element(By.CLASS_NAME,'e13098a59f')
                name = elem.text
                name = name.replace('Opens in new window', '')
                name = name.replace('\n', '')

                link = elem.get_attribute('href')
                #score = scores[j].text.split("\n")
                price = prices[j].text.split(",")
                addr = address[j].text
                nights = price[0]
                adults = price[1]
                try:
                    selem = container[j].find_element(By.CLASS_NAME, 'fbd1d3018c')
                    money = selem.text
                except:
                    print ('exc')
                    money = "-1"

                txt = ""
                rate = ""
                el = container[j].find_elements(By.CLASS_NAME,'b5cd09854e')
                if len(el) > 1:
                    txt = el[0].text
                    rate = el[1].text
                revs = ""
                el = container[j].find_elements(By.CLASS_NAME, 'db63693c62')
                if len(el) > 0:
                    revs = el[0].text
                    revs = revs.replace(',', '.')

                id  = link.split("?")[0].split(".html")[0].split("/")[-1].split(".")[0]


                if id not in list_ids:
                    print (i, inew, id, name, txt, rate, revs, nights, adults, money, addr)
                    csvWriter.writerow([id, name, txt, rate, revs, nights, adults, money, addr, link])
                    list_ids.append(id)
                    inew = inew + 1
                else:
                    print (name, ' found' )
                    #print (j, name, txt, rate, revs, nights, adults, money, addr)
            except:
                print ('skip')


        el = driver.find_elements(By.XPATH, '//button[@class="fc63351294 a822bdf511 e3c025e003 fa565176a8 f7db01295e e1b7cfea84 f9d6150b8e"]')
        if len(el) == 1:
            print ('next', el[0])
            el[0].click()
        else:
            print ('next 1', el[1])
            el[1].click()

        csvFile.flush()

    driver.quit()
#    except:
#        print ('skip')
#        driver.quit()

