import sys
import csv
from selenium import webdriver
import time
from selenium.webdriver.chrome.options import Options

# default path to file to store data
path_to_file = "reviews_achilleion.csv"

# default number of scraped pages
num_page = 50

# default tripadvisor website of hotel or things to do (attraction/monument) 
url = "https://www.tripadvisor.com/Hotel_Review-g60763-d1218720-Reviews-The_Standard_High_Line-New_York_City_New_York.html"
url = "https://www.tripadvisor.com/Hotel_Review-g189458-d23182681-Reviews-Angsana_Corfu_Resort_Spa-Corfu_Ionian_Islands.html"
#url = "https://www.tripadvisor.com/Attraction_Review-g187791-d192285-Reviews-Colosseum-Rome_Lazio.html"
#url = "https://www.tripadvisor.com/Attraction_Review-g187497-d190166-Reviews-Basilica_de_la_Sagrada_Familia-Barcelona_Catalonia.html"
url = "https://www.tripadvisor.com/Attraction_Review-g187497-d191052-Reviews-Casa_Batllo-Barcelona_Catalonia.html"
url = "https://www.tripadvisor.com/Attraction_Review-g776017-d523868-Reviews-Paleokastritsa_Beach-Paleokastritsa_Corfu_Ionian_Islands.html"
url = "https://www.tripadvisor.com/Attraction_Review-g662629-d8498696-Reviews-Corfu_Old_Town-Corfu_Town_Corfu_Ionian_Islands.html"
url = "https://www.tripadvisor.com/Attraction_Review-g662629-d4696311-Reviews-Old_Fortress_Corfu-Corfu_Town_Corfu_Ionian_Islands.html"
url = "https://www.tripadvisor.com/Attraction_Review-g676295-d2469814-Reviews-Canal_D_Amour-Sidari_Corfu_Ionian_Islands.html"
url = "https://www.tripadvisor.com/Attraction_Review-g1188103-d523820-Reviews-Achilleion_Museum-Gastouri_Corfu_Ionian_Islands.html"

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

# open the file to save the review
csvFile = open(path_to_file, 'a', encoding="utf-8")
csvWriter = csv.writer(csvFile)

# change the value inside the range to save more or less reviews
for i in range(0, num_page):

    # expand the review 
    time.sleep(5)
    #driver.find_element_by_xpath(".//div[contains(@data-test-target, 'expand-review')]").click()

    #container = driver.find_elements_by_xpath("//div[@data-reviewid]")
    container = driver.find_elements_by_xpath('//*[@id="tab-data-qa-reviews-0"]')
    container = driver.find_elements_by_class_name("_c")
    #dates = driver.find_elements_by_xpath(".//div[@class='EftBQ']")
    print ("len", len(container))

    for j in range(len(container)-1):
	
       if len(container[j+1].find_elements_by_class_name("yCeTE")) > 0:
           title = container[j+1].find_elements_by_class_name("yCeTE")[0]
           title = title.text
           review  = container[j+1].find_elements_by_class_name("yCeTE")[1]
           review = review.text
           review = review.replace('\n', ' ')
           rating = container[j+1].find_elements_by_class_name("UctUV")[0].get_attribute("aria-label")
           rating = rating.split(" ")[0]
           date = container[j+1].find_elements_by_class_name("TreSq")[0]
           date = date.text
           date = date.split("\n")[0]
           date = date[8:]
           print (j+1, title, review, rating, date)
        
           csvWriter.writerow([date, rating, title, review])
        
    # change the page            
    time.sleep(2)

    #driver.find_element_by_xpath('.//a[@class="ui_button nav next primary "]').click()
    #driver.find_element_by_xpath('//*[@id="tab-data-qa-reviews-0"]/div/div[5]/div[11]/div[1]/div/div[1]/div[2]/div/a').click()
    el = driver.find_elements_by_class_name("xkSty")[0]
    el = el.find_elements_by_class_name("BrOJk")[0]
    el.click()

driver.quit()
