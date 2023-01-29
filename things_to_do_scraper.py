import sys
import csv
from selenium import webdriver
import time
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By

# default path to file to store data
path_to_file = "reviews_acropolis.csv"

# default number of scraped pages
num_page = 50

# default tripadvisor website of hotel or things to do (attraction/monument)
url = "https://www.tripadvisor.com/Attraction_Review-g189400-d198706-Reviews-Acropolis-Athens_Attica.html"

# if you pass the inputs in the command line
if (len(sys.argv) == 4):
    path_to_file = sys.argv[1]
    num_page = int(sys.argv[2])
    url = sys.argv[3]

# import the webdriver
chrome_options = Options()
#chrome_options.add_argument("--headless")

driver = webdriver.Chrome(options=chrome_options)
driver.implicitly_wait(5)
driver.get(url)
time.sleep(4)

overlay = driver.find_element(By.ID, "onetrust-accept-btn-handler")
overlay.click()
time.sleep(2)

# open the file to save the review
csvFile = open(path_to_file, 'w', encoding="utf-8")
csvWriter = csv.writer(csvFile)
inew = 1
# change the value inside the range to save more or less reviews
for i in range(0, num_page):

    # expand the review
    time.sleep(5)
    #driver.find_element_by_xpath(".//div[contains(@data-test-target, 'expand-review')]").click()

    #container = driver.find_elements_by_xpath("//div[@data-reviewid]")
    container = driver.find_elements(By.XPATH, '//*[@id="tab-data-qa-reviews-0"]')
    container = driver.find_elements(By.CLASS_NAME, "_c")
    #dates = driver.find_elements_by_xpath(".//div[@class='EftBQ']")
    print ("len", len(container))

    for j in range(len(container)-1):
	
       if len(container[j+1].find_elements(By.CLASS_NAME, "yCeTE")) > 0:
           title = container[j+1].find_elements(By.CLASS_NAME, "yCeTE")[0]
           title = title.text
           review  = container[j+1].find_elements(By.CLASS_NAME, "yCeTE")[1]
           review = review.text
           review = review.replace('\n', ' ')
           review = review.replace(',', ' ')
           rating = container[j+1].find_elements(By.CLASS_NAME, "UctUV")[0].get_attribute("aria-label")
           rating = rating.split(" ")[0]
           date = container[j+1].find_elements(By.CLASS_NAME, "TreSq")[0]
           date = date.text
           date = date.split("\n")[0]
           date = date[8:]
           elems = date.split(' ')
           month = elems[0]
           date = elems[1][:-1]
           year = elems[2]
           print (inew, title, review, rating, month, date, year)
           inew = inew + 1
           csvWriter.writerow([month, date, year, rating, title, review])

    # change the page
    time.sleep(4)
    csvFile.flush()

    el = driver.find_elements(By.CLASS_NAME, "xkSty")[0]
    el = el.find_elements(By.XPATH, '//a[@data-smoke-attr="pagination-next-arrow"]')
    if len(el) > 0:
        el[0].click()

driver.quit()
