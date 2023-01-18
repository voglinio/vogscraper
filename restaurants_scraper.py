import sys
import csv
from selenium import webdriver
import time

# default path to file to store data
path_to_file = "reviews_restaurant_araliki.csv"

# default number of scraped pages
num_page = 10

# default tripadvisor website of restaurant
url = "https://www.tripadvisor.com/Restaurant_Review-g60763-d802686-Reviews-Hard_Rock_Cafe-New_York_City_New_York.html"
url = "https://www.tripadvisor.com/Restaurant_Review-g662629-d8045266-Reviews-La_Tavola_Calda-Corfu_Town_Corfu_Ionian_Islands.html"
url = "https://www.tripadvisor.com/Restaurant_Review-g662629-d6124735-Reviews-The_Venetian_Well-Corfu_Town_Corfu_Ionian_Islands.html"
url = "https://www.tripadvisor.com/Restaurant_Review-g189417-d6513925-Reviews-Peskesi-Heraklion_Crete.html"
url = "https://www.tripadvisor.com/Restaurant_Review-g664630-d1155453-Reviews-Flamingo-Skala_Kefalonia_Ionian_Islands.html"
url = "https://www.tripadvisor.com/Restaurant_Review-g189484-d7008097-Reviews-Gemelos_Tavern-Corinth_Corinthia_Region_Peloponnese.html"
url = "https://www.tripadvisor.com/Restaurant_Review-g189471-d7020210-Reviews-To_Araliki-Kavala_Kavala_Region_East_Macedonia_and_Thrace.html"

# if you pass the inputs in the command line
if (len(sys.argv) == 4):
    path_to_file = sys.argv[1]
    num_page = int(sys.argv[2])
    url = sys.argv[3]

# Import the webdriver
driver = webdriver.Chrome()
driver.implicitly_wait(4)
driver.get(url)

# Open the file to save the review
csvFile = open(path_to_file, 'a', encoding="utf-8")
csvWriter = csv.writer(csvFile)

# change the value inside the range to save more or less reviews
for i in range(0, num_page):
    
    # expand the review 
    time.sleep(5)
    driver.find_element_by_xpath("//span[@class='taLnk ulBlueLinks']").click()

    container = driver.find_elements_by_xpath(".//div[@class='review-container']")

    for j in range(len(container)):

        title = container[j].find_element_by_xpath(".//span[@class='noQuotes']").text
        date = container[j].find_element_by_xpath(".//span[contains(@class, 'ratingDate')]").get_attribute("title")
        rating = container[j].find_element_by_xpath(".//span[contains(@class, 'ui_bubble_rating bubble_')]").get_attribute("class").split("_")[3]
        review = container[j].find_element_by_xpath(".//p[@class='partial_entry']").text.replace("\n", " ")

        csvWriter.writerow([date, rating, title, review]) 

    # change the page
    driver.find_element_by_xpath('.//a[@class="nav next ui_button primary"]').click()

driver.close()
