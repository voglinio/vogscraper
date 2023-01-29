import sys
import csv
from selenium import webdriver
import time
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
import pandas as pd
from os.path import exists


# default path to file to store data
path_to_file = "aibnb_corfu_gouvia.csv"

if exists(path_to_file):
    df  = pd.read_csv(path_to_file, header=None)
    list_ids = df[0].values.tolist()
    print ("Starting with ", len(df), " properties", len(list_ids) )
else:
    list_ids = []
    print ("Starting on empty file")

# default number of scraped pages
num_page = 17

# default tripadvisor website of hotel or things to do (attraction/monument)

urls = [
"https://www.airbnb.com/s/Gouvia--Corfu--Greece/homes?tab_id=home_tab&refinement_paths%5B%5D=%2Fhomes&flexible_trip_lengths%5B%5D=one_week&price_filter_input_type=0&price_filter_num_nights=5&query=Gouvia%2C%20Corfu&place_id=ChIJ94-dHZJbWxMR7u9uIMVDTr4&date_picker_type=flexible_dates&flexible_trip_dates%5B%5D=june&flexible_trip_dates%5B%5D=july&flexible_trip_dates%5B%5D=august&flexible_trip_dates%5B%5D=september&source=structured_search_input_header&search_type=autocomplete_click"
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


inew = 1

for url in urls:
    print (url)
    try:
        chrome_options = Options()
        driver = webdriver.Chrome(options=chrome_options)
        driver.implicitly_wait(5)
        driver.get(url)

        # change the value inside the range to save more or less reviews
        for i in range(0, num_page):

            # expand the review
            time.sleep(7)
            #driver.find_element_by_xpath(".//div[contains(@data-test-target, 'expand-review')]").click()

            #container = driver.find_elements_by_xpath("//div[@data-reviewid]")
            container = driver.find_elements(By.CLASS_NAME, "c4mnd7m")
            #dates = driver.find_elements_by_xpath(".//div[@class='EftBQ']")
            print ("len", len(container))

            for j in range(len(container)):

                z = container[j].find_elements(By.CLASS_NAME, "t1jojoys")
                if len(z) >= 1:
                    title = z[0].text
                    title = title.replace('\n', ' ')
                    title = title.replace(',', ' ')

                    x = container[j].find_elements(By.CLASS_NAME, "s1cjsi4j")
                    if len(x) >= 3:
                        desc = x[1].text
                        desc = desc.replace('\n', ' ')
                        desc = desc.replace(',', ' ')

                        beds  = x[2].text
                        dates = x[3].text

                        y = container[j].find_elements(By.CLASS_NAME, "t5eq1io")
                        yy = container[j].find_elements(By.CLASS_NAME, "p11pu8yw")
                        if len(y) >= 1:
                            rating = y[0].text
                            price = yy[0].text
                            split_price = price.split(" ")
                            if len(split_price) > 1:
                                price = split_price[1]



                            rr = rating.split(" ")
                            if len(rr) > 1:
                                rate = rating.split(" ")[0]
                                count = rating.split(" ")[1]
                                count = count[1:-1]
                            else:
                                rate = rating
                                count = 0

                            p = container[j].find_elements(By.CLASS_NAME, "bn2bl2p")
                            if len(p) >= 1:
                                id = p[0].get_attribute('target')

                                if id not in list_ids:
                                    print (len(list_ids) , id, title, desc, beds, dates, rate, count, price)
                                    csvWriter.writerow([id, title, desc, beds, dates, rate, count, price])
                                    list_ids.append(id)
                                    inew = inew + 1


            el = driver.find_elements(By.CLASS_NAME, "_1bfat5l")[0]
            el.click()

            csvFile.flush()

        driver.quit()
    except:
        print ('skip')
        driver.quit()

