import sys
import csv
from selenium import webdriver
import time
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
import pandas as pd
from os.path import exists
import json


# default path to file to store data
path_to_file = "aibnb_corfu_coords.csv"

if exists(path_to_file):
    df = pd.read_csv(path_to_file, header=None)
    list_ids = df[0].astype("string").values.tolist()
    print("Starting with ", len(df), " properties", len(list_ids))
else:
    list_ids = []
    print("Starting on empty file")

# default number of scraped pages
num_page = 15

# default tripadvisor website of hotel or things to do (attraction/monument)

urls = [
     "https://www.airbnb.com/s/Corfu--Greece/homes?place_id=ChIJfwotqt1eWxMR0CErp-YUlAE&refinement_paths%5B%5D=%2Fhomes&flexible_trip_dates%5B%5D=february&flexible_trip_dates%5B%5D=march&flexible_trip_dates%5B%5D=april&flexible_trip_dates%5B%5D=may&flexible_trip_lengths%5B%5D=one_week&date_picker_type=flexible_dates&search_type=filter_change&tab_id=home_tab&query=Corfu%2C%20Greece&price_filter_input_type=0&price_filter_num_nights=5&source=structured_search_input_header",
     "https://www.airbnb.com/s/Kerkira--Corfu--Greece/homes?refinement_paths%5B%5D=%2Fhomes&flexible_trip_dates%5B%5D=april&flexible_trip_dates%5B%5D=february&flexible_trip_dates%5B%5D=march&flexible_trip_dates%5B%5D=may&flexible_trip_lengths%5B%5D=one_week&date_picker_type=flexible_dates&search_type=autocomplete_click&tab_id=home_tab&query=Kerkira%2C%20Corfu&price_filter_input_type=0&price_filter_num_nights=5&place_id=ChIJd3V-rehbWxMRHuBSyk-6Hhg&source=structured_search_input_header",
     "https://www.airbnb.com/s/Gouvia--Corfu/homes?place_id=ChIJ94-dHZJbWxMR7u9uIMVDTr4&refinement_paths%5B%5D=%2Fhomes&flexible_trip_dates%5B%5D=february&flexible_trip_dates%5B%5D=march&flexible_trip_dates%5B%5D=april&flexible_trip_dates%5B%5D=may&flexible_trip_lengths%5B%5D=one_week&date_picker_type=flexible_dates&search_type=autocomplete_click&tab_id=home_tab&query=Gouvia%2C%20Corfu&price_filter_input_type=0&price_filter_num_nights=5&source=structured_search_input_header"

  #   "https://www.airbnb.com/s/Ag.-Georgios-Pagon--Greece/homes?refinement_paths%5B%5D=%2Fhomes&flexible_trip_dates%5B%5D=august&flexible_trip_dates%5B%5D=july&flexible_trip_dates%5B%5D=june&flexible_trip_dates%5B%5D=september&flexible_trip_lengths%5B%5D=one_week&date_picker_type=flexible_dates&search_type=autocomplete_click&tab_id=home_tab&query=Ag.%20Georgios%20Pagon%2C%20Greece&price_filter_input_type=0&price_filter_num_nights=5&source=structured_search_input_header&place_id=ChIJberIu-pRWxMR8xcilAttI_Q",
#     "https://www.airbnb.com/s/Perama--Perama--Corfu--Greece/homes?refinement_paths%5B%5D=%2Fhomes&flexible_trip_dates%5B%5D=august&flexible_trip_dates%5B%5D=july&flexible_trip_dates%5B%5D=june&flexible_trip_dates%5B%5D=september&flexible_trip_lengths%5B%5D=one_week&date_picker_type=flexible_dates&search_type=autocomplete_click&tab_id=home_tab&query=Perama%2C%20Perama%2C%20Corfu&price_filter_input_type=0&price_filter_num_nights=5&place_id=ChIJ_4f7_FFeWxMRfrhdXyEEHhk&source=structured_search_input_header",
#     "https://www.airbnb.com/s/Ipsos--Corfu--Greece/homes?tab_id=home_tab&refinement_paths%5B%5D=%2Fhomes&flexible_trip_lengths%5B%5D=one_week&price_filter_input_type=0&price_filter_num_nights=5&query=Ipsos%2C%20Corfu&place_id=ChIJX16PEUFbWxMRa_lNZ-q_5Hc&date_picker_type=flexible_dates&flexible_trip_dates%5B%5D=june&flexible_trip_dates%5B%5D=july&flexible_trip_dates%5B%5D=august&flexible_trip_dates%5B%5D=september&source=structured_search_input_header&search_type=autocomplete_click",
#     "https://www.airbnb.com/s/Liapades--Corfu--Greece/homes?tab_id=home_tab&refinement_paths%5B%5D=%2Fhomes&flexible_trip_lengths%5B%5D=one_week&price_filter_input_type=0&price_filter_num_nights=5&query=Liapades%2C%20Corfu&date_picker_type=flexible_dates&flexible_trip_dates%5B%5D=august&flexible_trip_dates%5B%5D=july&flexible_trip_dates%5B%5D=june&flexible_trip_dates%5B%5D=september&source=structured_search_input_header&search_type=autocomplete_click&place_id=ChIJnTxRibpQWxMR8AK64iy9AAU",
#     "https://www.airbnb.com/s/Moraitika--Corfu--Greece/homes?tab_id=home_tab&refinement_paths%5B%5D=%2Fhomes&flexible_trip_lengths%5B%5D=one_week&price_filter_input_type=0&price_filter_num_nights=5&query=Moraitika%2C%20Corfu&date_picker_type=flexible_dates&flexible_trip_dates%5B%5D=august&flexible_trip_dates%5B%5D=july&flexible_trip_dates%5B%5D=june&flexible_trip_dates%5B%5D=september&source=structured_search_input_header&search_type=autocomplete_click&place_id=ChIJjyd2mMehXBMRt5B0xxtZJa8",
#     "https://www.airbnb.com/s/Ag.-Mattheos--Greece/homes?tab_id=home_tab&refinement_paths%5B%5D=%2Fhomes&flexible_trip_lengths%5B%5D=one_week&price_filter_input_type=0&price_filter_num_nights=5&query=Ag.%20Mattheos%2C%20Greece&date_picker_type=flexible_dates&flexible_trip_dates%5B%5D=august&flexible_trip_dates%5B%5D=july&flexible_trip_dates%5B%5D=june&flexible_trip_dates%5B%5D=september&source=structured_search_input_header&search_type=autocomplete_click&place_id=ChIJldR02SKhXBMR3JHGu-7HSYY",
#     "https://www.airbnb.com/s/Pelekas--Corfu--Greece/homes?refinement_paths%5B%5D=%2Fhomes&flexible_trip_dates%5B%5D=august&flexible_trip_dates%5B%5D=july&flexible_trip_dates%5B%5D=june&flexible_trip_dates%5B%5D=september&flexible_trip_lengths%5B%5D=one_week&date_picker_type=flexible_dates&adults=1&search_type=autocomplete_click&tab_id=home_tab&query=Pelekas%2C%20Corfu&price_filter_input_type=0&price_filter_num_nights=5&source=structured_search_input_header&place_id=ChIJC6U8XOJYWxMRA8NZvWN1yuc",
#     "https://www.airbnb.com/s/Corfu--Greece/homes?place_id=ChIJfwotqt1eWxMR0CErp-YUlAE&refinement_paths%5B%5D=%2Fhomes&checkin=2023-07-10&checkout=2023-07-14&date_picker_type=flexible_dates&adults=1&search_type=filter_change&tab_id=home_tab&query=Corfu%2C%20Greece&flexible_trip_lengths%5B%5D=one_week&price_filter_input_type=0&price_filter_num_nights=5&flexible_trip_dates%5B%5D=august&flexible_trip_dates%5B%5D=july&source=structured_search_input_header",
#     "https://www.airbnb.com/s/Corfu--Greece/homes?place_id=ChIJfwotqt1eWxMR0CErp-YUlAE&refinement_paths%5B%5D=%2Fhomes&flexible_trip_dates%5B%5D=august&flexible_trip_dates%5B%5D=july&flexible_trip_dates%5B%5D=june&flexible_trip_dates%5B%5D=september&flexible_trip_lengths%5B%5D=one_week&date_picker_type=flexible_dates&adults=1&search_type=filter_change&tab_id=home_tab&query=Corfu%2C%20Greece&price_filter_input_type=0&price_filter_num_nights=5&source=structured_search_input_header",
#     "https://www.airbnb.com/s/Palaiokastritsa--Corfu--Greece/homes?refinement_paths%5B%5D=%2Fhomes&flexible_trip_dates%5B%5D=august&flexible_trip_dates%5B%5D=july&flexible_trip_dates%5B%5D=june&flexible_trip_dates%5B%5D=september&flexible_trip_lengths%5B%5D=one_week&date_picker_type=flexible_dates&adults=1&search_type=autocomplete_click&tab_id=home_tab&query=Palaiokastritsa%2C%20Corfu&price_filter_input_type=0&price_filter_num_nights=5&place_id=ChIJxZVuN5NQWxMRoJS54iy9AAQ&source=structured_search_input_header",
#     "https://www.airbnb.com/s/Kassiopi--Corfu--Greece/homes?refinement_paths%5B%5D=%2Fhomes&flexible_trip_dates%5B%5D=august&flexible_trip_dates%5B%5D=july&flexible_trip_dates%5B%5D=june&flexible_trip_dates%5B%5D=september&flexible_trip_lengths%5B%5D=one_week&date_picker_type=flexible_dates&adults=1&search_type=autocomplete_click&tab_id=home_tab&query=Kassiopi%2C%20Corfu&price_filter_input_type=0&price_filter_num_nights=5&source=structured_search_input_header&place_id=ChIJWQRpFYtBWxMRcBe74iy9AAU",
#     "https://www.airbnb.com/s/Lefkimmi--Corfu--Greece/homes?refinement_paths%5B%5D=%2Fhomes&flexible_trip_dates%5B%5D=august&flexible_trip_dates%5B%5D=july&flexible_trip_dates%5B%5D=june&flexible_trip_dates%5B%5D=september&flexible_trip_lengths%5B%5D=one_week&date_picker_type=flexible_dates&adults=1&search_type=autocomplete_click&tab_id=home_tab&query=Lefkimmi%2C%20Corfu&price_filter_input_type=0&price_filter_num_nights=5&source=structured_search_input_header&place_id=ChIJzxkogOqbXBMRgJS54iy9AAQ",
#     "https://www.airbnb.com/s/Sidari--Corfu--Greece/homes?refinement_paths%5B%5D=%2Fhomes&flexible_trip_dates%5B%5D=august&flexible_trip_dates%5B%5D=july&flexible_trip_dates%5B%5D=june&flexible_trip_dates%5B%5D=september&flexible_trip_lengths%5B%5D=one_week&date_picker_type=flexible_dates&adults=1&search_type=autocomplete_click&tab_id=home_tab&query=Sidari%2C%20Corfu&price_filter_input_type=0&price_filter_num_nights=5&source=structured_search_input_header&place_id=ChIJ-Z6H3-NOWxMR0CW74iy9AAU",
#     "https://www.airbnb.com/s/Dasia--Corfu/homes?refinement_paths%5B%5D=%2Fhomes&flexible_trip_dates%5B%5D=august&flexible_trip_dates%5B%5D=july&flexible_trip_dates%5B%5D=june&flexible_trip_dates%5B%5D=september&flexible_trip_lengths%5B%5D=one_week&date_picker_type=flexible_dates&adults=1&search_type=search_query&tab_id=home_tab&price_filter_input_type=0&price_filter_num_nights=5&source=structured_search_input_header",
#     "https://www.airbnb.com/s/Benitses--Corfu--Greece/homes?tab_id=home_tab&refinement_paths%5B%5D=%2Fhomes&flexible_trip_lengths%5B%5D=one_week&price_filter_input_type=0&price_filter_num_nights=5&query=Benitses%2C%20Corfu%2C%20Greece&date_picker_type=flexible_dates&flexible_trip_dates%5B%5D=august&flexible_trip_dates%5B%5D=july&flexible_trip_dates%5B%5D=june&flexible_trip_dates%5B%5D=september&source=structured_search_input_header&search_type=autocomplete_click&place_id=ChIJe3BB9IhfWxMRxK0Am3INW4c",
#     "https://www.airbnb.com/s/Gouvia--Corfu--Greece/homes?tab_id=home_tab&refinement_paths%5B%5D=%2Fhomes&flexible_trip_lengths%5B%5D=one_week&price_filter_input_type=0&price_filter_num_nights=5&query=Gouvia%2C%20Corfu&place_id=ChIJ94-dHZJbWxMR7u9uIMVDTr4&date_picker_type=flexible_dates&flexible_trip_dates%5B%5D=june&flexible_trip_dates%5B%5D=july&flexible_trip_dates%5B%5D=august&flexible_trip_dates%5B%5D=september&source=structured_search_input_header&search_type=autocomplete_click",
]


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


inew = len(list_ids) + 1

for url in urls:
    print(url)
    try:
        chrome_options = Options()
        driver = webdriver.Chrome(options=chrome_options)
        driver.implicitly_wait(5)
        driver.get(url)
        time.sleep(5)

        # change the value inside the range to save more or less reviews
        for i in range(0, num_page):
            print("page", i)
            # expand the review
            driver.refresh()
            time.sleep(7)
            res = driver.find_elements(By.XPATH, ".//script[@data-deferred-state]")

            data = json.loads(res[0].get_attribute("innerHTML"))
            listings = data["niobeMinimalClientData"][0][1]["data"]["presentation"][
                "explore"
            ]["sections"]["sectionIndependentData"]["staysSearch"]["searchResults"]
            print("len", len(listings))

            for j in range(len(listings)):

                listi = listings[j]["listing"]
                if listi["id"] not in list_ids:

                    list_ids.append(listi["id"])

                    tmp = listi["avgRatingLocalized"]
                    if tmp is not None:

                        tmp = tmp.split(" ")
                        rating = "-1"
                        if len(tmp) > 0:
                            rating = tmp[0]
                        num_reviews = "-1"
                        if len(tmp) > 1:
                            num_reviews = tmp[1][1:-1]
                    else:
                        rating = "-1"
                        num_reviews = "-1"

                    beds = ""
                    primaryLine = listi['structuredContent']['primaryLine']
                    if len(primaryLine) > 0:
                        beds = primaryLine[0]['body']

                    title = listi["title"]
                    title = title.replace("\n", " ")
                    title = title.replace(",", " ")

                    print(inew, len(list_ids), listi["id"], title, beds, rating, num_reviews, listi["coordinate"])

                    csvWriter.writerow(
                        [
                            listi["id"],
                            listi["name"],
                            title,
                            listi["city"],
                            listi["localizedCityName"],
                            title,
                            beds,
                            rating,
                            num_reviews,
                            listi["listingObjType"],
                            listi["coordinate"]["longitude"],
                            listi["coordinate"]["latitude"],
                            listi["roomTypeCategory"],
                        ]
                    )
                    inew = inew + 1
                else:
                    print("found", listi["id"], listi["name"])

            time.sleep(5)
            el = driver.find_elements(By.CLASS_NAME, "_1bfat5l")
            if len(el) > 0:
                el[0].click()

            csvFile.flush()

        driver.quit()
    except:
       print("skip")
       driver.quit()
