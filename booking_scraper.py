import sys
import csv
from selenium import webdriver
import time
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
import pandas as pd
from os.path import exists


# default path to file to store data
path_to_file = "booking_zakinthos_v3.csv"

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

urls = ["https://www.booking.com/searchresults.html?label=gen173nr-1FCAEoggI46AdIM1gEaFyIAQGYAQm4AQfIAQzYAQHoAQH4AQuIAgGoAgO4Atishp4GwAIB0gIkMDM3OTdjNzUtYzZmZS00ZGYyLThmOTctZjg2YmExZTM0M2Vi2AIG4AIB&sid=7653fd0ad7a5ac380149dda7f5677a12&aid=304142&checkin=2023-08-01&checkout=2023-08-06&dest_id=1570&dest_type=region&group_adults=2&req_adults=2&no_rooms=1&group_children=0&req_children=0&order=upsort_bh",
"https://www.booking.com/searchresults.en-gb.html?ss=Corfu%2C+Greece&ssne=Corfu+Town&ssne_untouched=Corfu+Town&label=gen173nr-1FCAEoggI46AdIM1gEaFyIAQGYAQm4AQfIAQzYAQHoAQH4AQuIAgGoAgO4Atishp4GwAIB0gIkMDM3OTdjNzUtYzZmZS00ZGYyLThmOTctZjg2YmExZTM0M2Vi2AIG4AIB&sid=7653fd0ad7a5ac380149dda7f5677a12&aid=304142&lang=en-gb&sb=1&src_elem=sb&src=searchresults&dest_id=1570&dest_type=region&ac_position=0&ac_click_type=b&ac_langcode=en&ac_suggestion_list_length=5&search_selected=true&search_pageview_id=1d2e7bb4767b026d&ac_meta=GhAxZDJlN2JiNDc2N2IwMjZkIAAoATICZW46BUNvcmZ1QABKAFAA&checkin=2023-08-01&checkout=2023-08-06&group_adults=2&no_rooms=1&group_children=0&sb_travel_purpose=leisure",
"https://www.booking.com/searchresults.en-gb.html?label=gen173nr-1FCAEoggI46AdIM1gEaFyIAQGYAQm4AQfIAQzYAQHoAQH4AQuIAgGoAgO4Atishp4GwAIB0gIkMDM3OTdjNzUtYzZmZS00ZGYyLThmOTctZjg2YmExZTM0M2Vi2AIG4AIB&lang=en-gb&sid=7653fd0ad7a5ac380149dda7f5677a12&sb=1&sb_lp=1&src=index&src_elem=sb&error_url=https%3A%2F%2Fwww.booking.com%2Findex.en-gb.html%3Flabel%3Dgen173nr-1FCAEoggI46AdIM1gEaFyIAQGYAQm4AQfIAQzYAQHoAQH4AQuIAgGoAgO4Atishp4GwAIB0gIkMDM3OTdjNzUtYzZmZS00ZGYyLThmOTctZjg2YmExZTM0M2Vi2AIG4AIB%26sid%3D7653fd0ad7a5ac380149dda7f5677a12%26sb_price_type%3Dtotal%26%26&ss=Corfu+Town&is_ski_area=0&ssne=Corfu+Town&ssne_untouched=Corfu+Town&dest_id=-820069&dest_type=city&checkin_year=2023&checkin_month=8&checkin_monthday=1&checkout_year=2023&checkout_month=8&checkout_monthday=6&efdco=1&group_adults=2&group_children=0&no_rooms=1&b_h4u_keep_filters=&from_sf=1",
"https://www.booking.com/searchresults.en-gb.html?efdco=1&checkin_monthday=1&b_h4u_keep_filters=&from_sf=1&auth_success=1&sb_lp=1&label=gen173nr-1FCAEoggI46AdIM1gEaFyIAQGYAQm4AQfIAQzYAQHoAQH4AQOIAgGoAgO4Avjf-50GwAIB0gIkYTliNTQ4OTUtYmNhNC00YWMwLWEyY2YtZmNkNDA4YmUyYzEx2AIF4AIB&is_ski_area=&src_elem=sb&lang=en-gb&group_adults=2&dest_type=region&sb=1&error_url=https%3A%2F%2Fwww.booking.com%2Findex.en-gb.html%3Flabel%3Dgen173nr-1FCAEoggI46AdIM1gEaFyIAQGYAQm4AQfIAQzYAQHoAQH4AQOIAgGoAgO4Avjf-50GwAIB0gIkYTliNTQ4OTUtYmNhNC00YWMwLWEyY2YtZmNkNDA4YmUyYzEx2AIF4AIB%26sid%3D6e38c114ad3781f7eced25d3cc6ba450%26sb_price_type%3Dtotal%26%26&ss=Corfu%2C+Greece&group_children=0&no_rooms=1&sid=6e38c114ad3781f7eced25d3cc6ba450&src=index&checkout_monthday=6&checkout_month=7&search_pageview_id=747479fc4933010e&dest_id=1570&search_selected=true&checkin_year=2023&checkout_year=2023&checkin_month=7",
"https://www.booking.com/searchresults.en-gb.html?ss=Corfu&ssne=Corfu&ssne_untouched=Corfu&label=gen173nr-1FCAEoggI46AdIM1gEaFyIAQGYAQm4AQfIAQzYAQHoAQH4AQuIAgGoAgO4AvvngJ4GwAIB0gIkOTcwOTIwNjYtOGU1Mi00ODBlLTlkZTktYjIxZjhiYzIyNTlk2AIG4AIB&sid=7653fd0ad7a5ac380149dda7f5677a12&aid=304142&lang=en-gb&sb=1&src_elem=sb&src=searchresults&dest_id=1570&dest_type=region&checkin=2023-07-01&checkout=2023-07-06&group_adults=2&no_rooms=1&group_children=0&sb_travel_purpose=leisure"]



urls = [
"https://www.booking.com/searchresults.en-gb.html?ss=Lefkada%2C+Greece&ssne=Corfu&ssne_untouched=Corfu&label=gen173nr-1FCAEoggI46AdIM1gEaFyIAQGYAQm4AQfIAQzYAQHoAQH4AQuIAgGoAgO4Atishp4GwAIB0gIkMDM3OTdjNzUtYzZmZS00ZGYyLThmOTctZjg2YmExZTM0M2Vi2AIG4AIB&sid=7653fd0ad7a5ac380149dda7f5677a12&aid=304142&lang=en-gb&sb=1&src_elem=sb&src=searchresults&dest_id=2805&dest_type=region&ac_position=0&ac_click_type=b&ac_langcode=en&ac_suggestion_list_length=5&search_selected=true&search_pageview_id=ecbb7ea40a9a0586&ac_meta=GhBlY2JiN2VhNDBhOWEwNTg2IAAoATICZW46A0xlZkAASgBQAA%3D%3D&checkin=2023-08-01&checkout=2023-08-06&group_adults=2&no_rooms=1&group_children=0&sb_travel_purpose=leisure",
"https://www.booking.com/searchresults.en-gb.html?ss=Lefkada%2C+Ionian+Islands%2C+Greece&ssne=Lefkada+Town&ssne_untouched=Lefkada+Town&label=gen173nr-1FCAEoggI46AdIM1gEaFyIAQGYAQm4AQfIAQzYAQHoAQH4AQuIAgGoAgO4Atishp4GwAIB0gIkMDM3OTdjNzUtYzZmZS00ZGYyLThmOTctZjg2YmExZTM0M2Vi2AIG4AIB&sid=7653fd0ad7a5ac380149dda7f5677a12&aid=304142&lang=en-gb&sb=1&src_elem=sb&src=searchresults&dest_id=-822235&dest_type=city&ac_position=1&ac_click_type=b&ac_langcode=xu&ac_suggestion_list_length=5&search_selected=true&search_pageview_id=44c20d34535b012e&ac_meta=GhA0NGMyMGQzNDUzNWIwMTJlIAEoATICeHU6AkxlQABKAFAA&checkin=2023-08-01&checkout=2023-08-06&group_adults=2&no_rooms=1&group_children=0&sb_travel_purpose=leisure",
"https://www.booking.com/searchresults.en-gb.html?ss=Nydri&ssne=Nydri&ssne_untouched=Nydri&label=gen173nr-1FCAEoggI46AdIM1gEaFyIAQGYAQm4AQfIAQzYAQHoAQH4AQuIAgGoAgO4Atishp4GwAIB0gIkMDM3OTdjNzUtYzZmZS00ZGYyLThmOTctZjg2YmExZTM0M2Vi2AIG4AIB&aid=304142&lang=en-gb&sb=1&src_elem=sb&src=searchresults&dest_id=-824809&dest_type=city&checkin=2023-08-01&checkout=2023-08-06&group_adults=2&no_rooms=1&group_children=0&sb_travel_purpose=leisure",
"https://www.booking.com/searchresults.en-gb.html?ss=Vasiliki%2C+Ionian+Islands%2C+Greece&ssne=Nydri&ssne_untouched=Nydri&label=gen173nr-1FCAEoggI46AdIM1gEaFyIAQGYAQm4AQfIAQzYAQHoAQH4AQuIAgGoAgO4Atishp4GwAIB0gIkMDM3OTdjNzUtYzZmZS00ZGYyLThmOTctZjg2YmExZTM0M2Vi2AIG4AIB&aid=304142&lang=en-gb&sb=1&src_elem=sb&src=searchresults&dest_id=-830143&dest_type=city&ac_position=1&ac_click_type=b&ac_langcode=en&ac_suggestion_list_length=5&search_selected=true&search_pageview_id=19b60f7d109801e7&ac_meta=GhAxOWI2MGY3ZDEwOTgwMWU3IAEoATICZW46B1Zhc2lsaWtAAEoAUAA%3D&checkin=2023-08-01&checkout=2023-08-06&group_adults=2&no_rooms=1&group_children=0&sb_travel_purpose=leisure"
]

urls = [
"https://www.booking.com/searchresults.en-gb.html?label=gen173nr-1FCAEoggI46AdIM1gEaFyIAQGYAQm4AQfIAQzYAQHoAQH4AQuIAgGoAgO4Aunvjp4GwAIB0gIkNWE0NWYxMTEtODAzMS00OTZmLTg4MzAtZWYzNjM1ZDZlOWFh2AIG4AIB&lang=en-gb&sid=b8ea07e999a05e717bd0890acdbef409&sb=1&sb_lp=1&src=index&src_elem=sb&error_url=https%3A%2F%2Fwww.booking.com%2Findex.en-gb.html%3Flabel%3Dgen173nr-1FCAEoggI46AdIM1gEaFyIAQGYAQm4AQfIAQzYAQHoAQH4AQuIAgGoAgO4Aunvjp4GwAIB0gIkNWE0NWYxMTEtODAzMS00OTZmLTg4MzAtZWYzNjM1ZDZlOWFh2AIG4AIB%26sid%3Db8ea07e999a05e717bd0890acdbef409%26sb_price_type%3Dtotal%26%26&ss=Zakynthos%2C+Greece&is_ski_area=&ssne=Vasiliki&ssne_untouched=Vasiliki&checkin_year=2023&checkin_month=7&checkin_monthday=1&checkout_year=2023&checkout_month=7&checkout_monthday=6&efdco=1&group_adults=2&group_children=0&no_rooms=1&b_h4u_keep_filters=&from_sf=1&ss_raw=Zak&ac_position=0&ac_langcode=en&ac_click_type=b&ac_meta=GhA4OGVjM2FmNWMzYTYwMjMwIAAoATICZW46A1pha0AASgBQAA%3D%3D&dest_id=1663&dest_type=region&place_id_lat=37.78129&place_id_lon=20.848534&search_pageview_id=88ec3af5c3a60230&search_selected=true&region_type=island&search_pageview_id=88ec3af5c3a60230&ac_suggestion_list_length=5&ac_suggestion_theme_list_length=0",
"https://www.booking.com/searchresults.en-gb.html?ss=Zakynthos%2C+Ionian+Islands%2C+Greece&ssne=Zakynthos&ssne_untouched=Zakynthos&label=gen173nr-1FCAEoggI46AdIM1gEaFyIAQGYAQm4AQfIAQzYAQHoAQH4AQuIAgGoAgO4Aunvjp4GwAIB0gIkNWE0NWYxMTEtODAzMS00OTZmLTg4MzAtZWYzNjM1ZDZlOWFh2AIG4AIB&sid=b8ea07e999a05e717bd0890acdbef409&aid=304142&lang=en-gb&sb=1&src_elem=sb&src=searchresults&dest_id=-831270&dest_type=city&ac_position=1&ac_click_type=b&ac_langcode=xu&ac_suggestion_list_length=5&search_selected=true&search_pageview_id=6d903afee75c02af&ac_meta=GhA2ZDkwM2FmZWU3NWMwMmFmIAEoATICeHU6A1pha0AASgBQAA%3D%3D&checkin=2023-07-01&checkout=2023-07-06&group_adults=2&no_rooms=1&group_children=0&sb_travel_purpose=leisure"
]

pages = [40, 10]


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
                score = scores[j].text.split("\n")
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

                txt = score[0]
                rate = score[1]
                revs = score[2]
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
        
