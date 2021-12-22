# Get Packages
import pandas as pd
import numpy as np
from bs4 import BeautifulSoup
from datetime import datetime
import yfinance as yf
import matplotlib.pyplot as plt
import argparse

# Import translate function
from translate import translate

# Selenium imports
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
import time
from time import sleep

# Scroll functions
def doScroll(driver, pageLength):
    lastCount = -1
    match = False

    while not match:
        lastCount += 1
        time.sleep(1)

        driver.execute_script(
            "window.scrollTo(0, document.body.scrollHeight);var pageLength=document.body.scrollHeight;return "
            "pageLength;")

        if lastCount == pageLength:
            match = True


# Scraping investing.com
def scrape_investing(tag, numOfPost, translation=False):

    # Prepare dict
    news = {
        "titles" : [],
        "dates" : [],
        "par" : [],
        "font" : [],
        "url" : []
    }

    # Enter the page
    my_url = "https://es.investing.com/search/?tab=news&q=" + tag
    option = Options()
    option.headless = False
    driver = webdriver.Chrome(options=option)
    driver.get(my_url)
    driver.maximize_window()
    
    # Do scroll
    numOfPost = int(numOfPost)
    pageLength = int(numOfPost / 8)
    doScroll(driver, numOfPost)
    
    # Enter every post
    for n in range(numOfPost):
        counter = 0
        while True:
            try:
                xpath = WebDriverWait(driver, 2).until(
                      EC.visibility_of_element_located((By.XPATH,
                      f"/html/body/div[5]/section/div/div[4]/div[3]/div/div[{n+1}]/div/a")))
                href = xpath.get_attribute('href')
                news['url'].append(href)
                driver.get(href)
                sleep(3)

                # Inside the post url, get title, date and content
                print("------------->>> Scraping ", str(href))

                # HTML
                html = BeautifulSoup(driver.page_source, 'html.parser')

                # Get title
                title = html.find(class_="articleHeader").text
                news["titles"].append(title)

                # Get date
                date = html.find(class_="contentSectionDetails").span.text
                news["dates"].append(date)

                # Get content
                content_list = []
                content = html.findAll("p")
                for p in content:
                    if tag in p.text:
                        content_list.append(p.text)
                    else:
                        continue
                news["par"].append(content_list)
                
                news['font'].append("Investing")

                # Get back
                driver.back()
                break
                
            except Exception as exception:
                if counter < 1:
                    print(exception.__class__.__name__)
                    counter += 1
                    sleep(1)
                    continue
                else:
                    break
                    
    
    # Close window
    driver.quit()

    if translation:
        news['titles'] = translate(news['titles'])['to']
        news['par'] = translate(news['par'])['to']
    
    # Return
    return news

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="Scrape news")
    myParser = parser.add_argument_group("Needed arguments")
    myParser.add_argument('-tag', '-t', help="Write a tag for the news search", required=True)
    myParser.add_argument('-numOfPost', '-n', help="How many post news do you want to scrape?", required=True)
    myParser.add_argument('-googleTranslator', '-g', help="Type something if you want to translate all news to english, else ignore", required=False)
    args = parser.parse_args()

    # Make it work!!!
    res = pd.DataFrame(scrape_investing(args.tag, args.numOfPost, args.googleTranslator))
    print(res)