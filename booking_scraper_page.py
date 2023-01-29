import sys
import csv
import selenium
from selenium import webdriver
import time
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
import pandas as pd

from selenium.common.exceptions import WebDriverException

#
# default path to file to store data
listings_file = "booking_zakinthos.csv"
df = pd.read_csv(listings_file, header=None)
df.columns = ['id', 'name', 'txt', 'rate', 'revs', 'nights', 'adults', 'money', 'addr', 'link']
urls = df.link.tolist()
ids = df.id.tolist()

#
#print("found ", len(urls))
#
path_to_file = "booking_zakinthos_reviews.csv"

#df  = pd.read_csv(path_to_file, header=None)
#print ("Starting with ", len(df), " properties" )

# default number of scraped pages
num_page = 3

# default tripadvisor website of hotel or things to do (attraction/monument)

#urls = ["https://www.booking.com/hotel/gr/chandris-apartments.en-gb.html?label=gen173nr-1FCAEoggI46AdIM1gEaFyIAQGYAQm4AQfIAQzYAQHoAQH4AQOIAgGoAgO4Avjf-50GwAIB0gIkYTliNTQ4OTUtYmNhNC00YWMwLWEyY2YtZmNkNDA4YmUyYzEx2AIF4AIB&sid=6e38c114ad3781f7eced25d3cc6ba450&aid=304142&ucfs=1&arphpl=1&checkin=2023-07-01&checkout=2023-07-06&dest_id=1570&dest_type=region&group_adults=2&req_adults=2&no_rooms=1&group_children=0&req_children=0&hpos=3&hapos=3&sr_order=popularity&srpvid=7b422e74ff87022d&srepoch=1673591787&all_sr_blocks=153151501_348672091_2_2_0&highlighted_blocks=153151501_348672091_2_2_0&matching_block_id=153151501_348672091_2_2_0&sr_pri_blocks=153151501_348672091_2_2_0__33250&from=searchresults&map_fdco=1#hotelTmpl",
#"https://www.booking.com/hotel/gr/nikos-pool-apartments-ground-floor.en-gb.html?aid=304142&label=gen173nr-1FCAEoggI46AdIM1gEaFyIAQGYAQm4AQfIAQzYAQHoAQH4AQyIAgGoAgO4AoDLhJ4GwAIB0gIkM2E5YmQ3ZGEtYTAwYy00NDQ0LThlYjMtMWI4Y2M5MTc1OWRi2AIG4AIB&sid=b8ea07e999a05e717bd0890acdbef409&all_sr_blocks=708963502_366547105_2_0_0;checkin=2023-07-01;checkout=2023-07-06;dest_id=-827992;dest_type=city;dist=0;group_adults=2;group_children=0;hapos=1;highlighted_blocks=708963502_366547105_2_0_0;hpos=1;matching_block_id=708963502_366547105_2_0_0;no_rooms=1;req_adults=2;req_children=0;room1=A%2CA;sb_price_type=total;sr_order=popularity;sr_pri_blocks=708963502_366547105_2_0_0__24840;srepoch=1673602459;srpvid=1d26434c6e82001e;type=total;ucfs=1&#hotelTmpl",
# "https://www.booking.com/hotel/gr/loc-old-town-annunziata.en-gb.html?label=gen173nr-1FCAEoggI46AdIM1gEaFyIAQGYAQm4AQfIAQzYAQHoAQH4AQOIAgGoAgO4Avjf-50GwAIB0gIkYTliNTQ4OTUtYmNhNC00YWMwLWEyY2YtZmNkNDA4YmUyYzEx2AIF4AIB&sid=6e38c114ad3781f7eced25d3cc6ba450&aid=304142&ucfs=1&arphpl=1&checkin=2023-07-01&checkout=2023-07-06&dest_id=1570&dest_type=region&group_adults=2&req_adults=2&no_rooms=1&group_children=0&req_children=0&hpos=5&hapos=5&sr_order=popularity&srpvid=7b422e74ff87022d&srepoch=1673591787&all_sr_blocks=403665307_364319126_2_0_0&highlighted_blocks=403665307_364319126_2_0_0&matching_block_id=403665307_364319126_2_0_0&sr_pri_blocks=403665307_364319126_2_0_0__64750&from_sustainable_property_sr=1&from=searchresults&map_fdco=1#hotelTmpl"]
#urls = [url.split("_")[1] for url in urls]


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

for i in range(len(urls)):
    url = urls[i]
    id = ids[i]
    print (url)
    try:
        chrome_options = Options()
        driver = webdriver.Chrome(options=chrome_options)
        driver.implicitly_wait(5)
        driver.get(url)
        time.sleep(4)
        overlay = driver.find_elements(By.XPATH, '//button[@id="onetrust-accept-btn-handler"]')
        print (len(overlay))
        if len(overlay) > 0:
            overlay[0].click()
        time.sleep(2)


        button = driver.find_elements(By.XPATH, '//button[@data-testid="fr-read-all-reviews"]')
        print ("button", len(button))
        if (len(button) > 0 ):
            button[0].click()
        time.sleep(2)

        ipages = 0
        while True:

            elems = driver.find_elements(By.CLASS_NAME, "review_list_new_item_block")
            print ("comments ", len(elems))
            for i in range(len(elems)):
                elem = elems[i]
                x1 = elem.find_elements(By.CLASS_NAME, "bui-review-score__badge")
                x2 = elem.find_elements(By.CLASS_NAME, "c-review__body")
                x3 = elem.find_elements(By.CLASS_NAME, "bui-avatar-block__title")
                x4 = elem.find_elements(By.CLASS_NAME, "bui-avatar-block__subtitle")
                x5 = elem.find_elements(By.CLASS_NAME, "c-review-block__date")

                xx5 = ""
                if len(x5) > 0:
                    xx5 = x5[0].text

                print (xx5)
                xx1 = ""
                if (len(x1) > 0):
                    print (x1[0].text)
                    xx1 = x1[0].text
                xx2_1 = ""
                xx2_2 = ""
                if (len(x2) > 0):
                    print ('+', x2[0].text)
                    xx2_1 = x2[0].text
                    xx2_1 = xx2_1.replace('\n', ' ')
                    xx2_1 = xx2_1.replace(',', ' ')
                    if (len(x2) > 1):
                        xx2_2 = x2[1].text
                        xx2_2 = xx2_2.replace('\n', ' ')
                        xx2_2 = xx2_2.replace(',', ' ')
                        print ('-', x2[1].text)
                xx3 = ""
                if (len(x3) > 0):
                    print (x3[0].text)
                    xx3 = x3[0].text
                xx4 = ""
                if (len(x4) > 0):
                    print (x4[0].text)
                    xx4 = x4[0].text
                print ("-----")
                csvWriter.writerow([id, xx1, xx2_1, xx2_2, xx3, xx4, xx5])

            next_button = driver.find_elements(By.CLASS_NAME, 'pagenext')
            if len(next_button) > 0:
                next_button[0].click()
                time.sleep(2)
                print ("ipages", ipages)
                ipages = ipages + 1

            else:
                break



        driver.quit()
    except WebDriverException:
        print ("continue")
        driver.quit()
