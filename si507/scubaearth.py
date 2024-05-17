# SI 507, Fall 2019 - final project
# Developed by Gui Ruggiero

import requests
import json
from bs4 import BeautifulSoup
import sqlite3
import os
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import time

# # # # # # # # # # # # # # # # # # # #
#   Part 1: Scraping ScubaEarth.com   #
# # # # # # # # # # # # # # # # # # # #

class Site():
    def __init__(self, name, country):
        self.created_by = 1
        
        self.name = name
        self.country = country

        self.lat = 0.0
        self.lgn = 0.0
        self.max_depth = 0.0
        self.notes = "notes"
        self.water = "water"
        self.salinity = "salinity"

    def __str__(self):
        return self.name + " @ " + self.country

# Caching file/dictionary
CACHE_FNAME = "cache.json"
try:
    cache_file = open(CACHE_FNAME, "r")
    cache_contents = cache_file.read()
    CACHE_DICTION = json.loads(cache_contents)
    cache_file.close()
except:
    CACHE_DICTION = {}

# Scraping with cache
def scraping_using_cache(url): 
    if url in CACHE_DICTION:
        # print("Getting cached data...")
        return CACHE_DICTION[url]
    
    else:
        # print("Making a request for new data...")
        CACHE_DICTION[url] = requests.get(url).text
        dumped_json_cache = json.dumps(CACHE_DICTION)
        fw = open(CACHE_FNAME, "w")
        fw.write(dumped_json_cache)
        fw.close()
        return CACHE_DICTION[url]

def scrape_scubaearth():
    # # Initializing Selenium browser - Chrome OS (not entirely figured out)
    # os.chmod("/home/guilhermeruggiero/chromedriver", 755)
    # driver = webdriver.Chrome(executable_path="/home/guilhermeruggiero/chromedriver")

    # # Initializing Selenium browser - Windows (working alternative)
    # os.chmod(r"C:\Users\gui\Downloads\chromedriver.exe", 755)
    # driver = webdriver.Chrome(executable_path=r"C:\Users\gui\Downloads\chromedriver.exe")

    # # Country to be searched
    # country = "USA"
    
    # # Search page
    # driver.get("http://www.scubaearth.com/dive-site/dive-site-profile-search.aspx")
    # time.sleep(2)
    # print("Page opened\n")

    # # Typing country into the right field
    # field_location = driver.find_element_by_id("location")
    # field_location.clear()
    # field_location.send_keys(country)
    # time.sleep(2)
    # print("Country typed on field\n")

    # # Clicking search button        
    # button_search = driver.find_element_by_link_text("Search")
    # button_search.click()
    # time.sleep(7)
    # print("Clicked search button - this is fun!\n")
    
    # # Getting page source code
    # # results = driver.find_element_by_id("sites-tabs-result").get_attribute('innerText')
    # results = driver.page_source
    # results_json = json.dumps(results)
    # driver.close()
    # print("Got results page source code\n")

# #     Storing source code a file (Windows <> Chrome OS development)       
#     with open("page.json", "w") as file:
#         file.write(results_json)
    
#     Reading source code from JSON file (Windows <> Chrome OS development)
    results_file = open("page.json", "r")
    results_json = results_file.read()

    results_soup = BeautifulSoup(results_json, "html.parser")
    # print(results_soup.prettify())

    # Finding div with results
    sites_div = results_soup.find(id='\\"sites-tabs-result\\"')
    # print(sites_div)
    site_list = sites_div.find_all("div")
    # print(site_list)

    # Going through every result and creating site objects
    sites = []
    i = 1
    for site_result in site_list:
        # print(site_result)
        # print(site_result.attrs)
        # print(site_result["class"])

        if site_result["class"] == ['\\"activity-module']:
            site_name = site_result.find("span").text.strip()
            # print(site_name)
            new_site = Site(site_name, country)
            
            # print(i)
            i += 1

        elif site_result["class"] == ['\\"dive-site-search-btns\\"']:
            site_url = "http://www.scubaearth.com" + site_result.find("a")["href"][2:-2]
            # print(site_url)

            # Fetching dive site page and details
            site_details = scraping_using_cache(site_url)
            # print(site_details)
            site_details_soup = BeautifulSoup(site_details, "html.parser")
            # print(site_details_soup.prettify())
            content_div = site_details_soup.find(class_="general-content-module dive-site-overview-module")
            # print(content_div)

            site_notes = content_div.find("span").text.strip()
            # print(site_notes)
            new_site.notes = site_notes

            data_table = content_div.find_all("tr")
            # print(data_table)
            for row in data_table:
                if row.find(class_="td-title").text.strip() == "Maximum Depth":
                    site_max_depth = row.find("span").text.strip()
                    try:
                        site_max_depth = int(site_max_depth)
                    except:
                        site_max_depth = 0
                    # print(site_max_depth)

                elif row.find(class_="td-title").text.strip() == "Water Environment Type":
                    site_water = row.find("span").text.strip()
                    # print(site_water)

                elif row.find(class_="td-title").text.strip() == "Salinity":
                    site_salinity = row.find("span").text.strip()
                    # print(site_salinity)

            new_site.max_depth = site_max_depth
            new_site.water = site_water
            new_site.salinity = site_salinity

            # print(i)
            i += 1

        else:
            data = site_result.text
            # print(data)
            site_lat = float(data[data.find(":") + 2:data.find(":") + 10])
            # print(site_lat)
            site_lgn = float(data[data.find("g") + 3:data.find("g") + 11])
            # print(site_lgn)
            new_site.lat = site_lat
            new_site.lgn = site_lgn

            # print(i)
            i += 1
        
        if i > 3:
            i = 1
            # print(new_site)
            sites.append(new_site)
            # print(sites)
            # print("="*50)
        
    print("Scraped results page and all its dive sites pages - total: " + str(len(sites)) + "\n")

    # Storing in database
    conn = sqlite3.connect('divelog.db')
    cur = conn.cursor()

    # Dropping table
    statement = "DROP TABLE IF EXISTS 'Sites';"
    cur.execute(statement)
    conn.commit()
    print("Table 'Sites' dropped (if present)\n")

    # Creating table
    statement = """
        CREATE TABLE 'Sites' (
            'id' INTEGER PRIMARY KEY AUTOINCREMENT,
            'created_by' INTEGER,
            'name' TEXT NOT NULL,
            'country' TEXT NOT NULL,
            'lat' REAL,
            'lgn' REAL,
            'max_depth' REAL,
            'notes' TEXT,
            'water' TEXT,
            'salinity' TEXT
        );
    """
    cur.execute(statement)
    conn.commit()
    print("Table 'Sites' created\n")

    # Inserting data
    i = 0
    for site in sites:
        insertion = (None, 1, site.name, site.country, site.lat, site.lgn, site.max_depth,
            site.notes, site.water, site.salinity)
        statement = "INSERT INTO 'Sites' "
        statement += "VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)"
        cur.execute(statement, insertion)
        i += 1

    conn.commit()
    if i == len(sites):
        print("Data inserted into table 'Sites' - rows: " + str(i) + " (as expected, heck yeah!)\n")
    else:
        print("Data inserted into table 'Sites' - rows: " + str(i) + "\n")

    conn.close()

# Only runs when this file is run directly
if __name__=="__main__":
    scrape_scubaearth()
    pass