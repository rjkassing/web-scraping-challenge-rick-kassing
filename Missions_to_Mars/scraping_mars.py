from splinter import Browser
from bs4 import BeautifulSoup
from webdriver_manager.chrome import ChromeDriverManager
import pandas as pd 
import requests
import pymongo


def init_browser():
    executable_path = {"executable_path": "/Users/derek/Downloads/chromedriver_win32/chromedriver"}
    return Browser("chrome", **executable_path, headless=False)


def scrape():
    browser = init_browser()
    mars_dict = {}
### NASA Mars News
    url = 'https://mars.nasa.gov/news/'
    browser.visit(url)
# HTML object
    html = browser.html
# Parse HTML with Beautiful Soup
    soup = BeautifulSoup(html, 'html.parser')

    step1=soup.find('ul', class_='item_list')
    step2=step1.find("li", class_='slide')
    step3=step2.find("div", class_="content_title")
    news_title = step3.text

    step4=step2.find("div", class_="article_teaser_body")
    news_p=step4.text

### JPL Mars Space Images - Featured Image

    url = 'https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars'
    browser.visit(url)
##Push "buttons" to get to desired page
    browser.links.find_by_partial_text('FULL IMAGE').click()
    browser.links.find_by_partial_text('more info').click()

# HTML object
    html = browser.html
# Parse HTML with Beautiful Soup
    soup = BeautifulSoup(html, 'html.parser') 
    featured_image_url=soup.find("figure", class_="lede").a["href"]
    featured_image_url 

### Mars Facts
    url = 'https://space-facts.com/mars/'
    browser.visit(url)
    tables = pd.read_html(url)
    type(tables)
    df = tables[0]
    df.head()
### Mars Hemispheres
    url = 'https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars'
    browser.visit(url)

    sidebar = soup.find(class_='itemLink product-item')

    titles_url = []
    for x in range(4):
        browser.links.find_by_partial_text('Enhanced')[x].click()
        html=browser.html
        imagesoup= BeautifulSoup(html, 'html.parser')
        image_url=imagesoup.find("li").a["href"]
        print (image_url)
        image_title=browser.find_by_css("h2.title").text
        titles_url.append({"title":image_title, "image_url":image_url})
        browser.back()
    print(titles_url)

    mars_dict["news_title"]=news_title
    mars_dict["news_p"]= news_p
    mars_dict["featured_image_url"]= featured_image_url
    mars_dict["titles_url"]= titles_url

    return mars_dict
