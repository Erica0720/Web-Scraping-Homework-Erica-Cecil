from splinter import Browser
from bs4 import BeautifulSoup 
import time
import pandas as pd 


def init_browser():
    # @NOTE: Replace the path with your actual path to the chromedriver
    executable_path = {"executable_path": "/usr/local/bin/chromedriver"}
    return Browser("chrome", **executable_path, headless=False)


def scrape_info():
    browser = init_browser()
    mars = {}

    # Visit mars.nasa.gov/news/
    url = "https://mars.nasa.gov/news/"
    browser.visit(url)

    html = browser.html
    news = BeautifulSoup(html, "html.parser")

    mars["news_title"] = news.find('div', class_='content_title').get_text()

    time.sleep(1)

    mars["news_p"] = news.find('div', class_='article_teaser_body').get_text()
    
        

        # Scrape page into jpl.nasa.gov
    url = "https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars"
    browser.visit(url)

    full_image_elem = browser.find_by_id('full_image')
    full_image_elem.click()
    time.sleep(1)

    more_info = browser.find_link_by_partial_text('more info')
    more_info.click()
    # time.sleep(1)


    # Create link
    html = browser.html
    img_soup = BeautifulSoup(html, 'html.parser')

    img_url_rel = img_soup.find('figure', class_='lede').find('img')['src']

    mars["image_url"] = f'https://www.jpl.nasa.gov{img_url_rel}' 
    
   
    # MARS WEATHER TWEET
    url = "https://twitter.com/marswxreport?lang=en"
    browser.visit(url)
    html = browser.html
    news = BeautifulSoup(html, "html.parser")
    

    mars["mars_weather_tweet"] = news.find("p","TweetTextSize").get_text()


    # USGS ASTROGEOLOGY PHOTOS
    # url = "https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars"
    # browser.visit(url)
    # time.sleep(1)
    # hemisphere_image_urls = []

    # links = browser.find_by_tag("h3")

    # for i in range(len(links)):
    #     hemisphere = {}
    #     browser.find_by_tag("h3")[i].click()
    #     sample_elem = browser.find_link_by_text('Sample').first
    #     hemisphere['img_url'] = sample_elem['href']
    #     hemisphere['title'] = browser.find_by_css("h2.title").text
    #     hemisphere_image_urls.append(hemisphere)
    #     browser.back()
    #     time.sleep(1)
    
    # mars["hemisphere_image_urls"] = hemisphere_image_urls
    # print(hemisphere_image_urls)
    #  table 
    df = pd.read_html('http://space-facts.com/mars/')[0]
    df.columns = ['description', 'value']
    df.set_index('description', inplace=True)

    table = df.to_html()
    table = table.replace('\n', '')

    mars['facts'] = table
    
    # Close the browser after scraping
    browser.quit()
    print(mars)
    # Return results
    return mars
