import pandas as pd
from splinter import Browser
from bs4 import BeautifulSoup
import time
from webdriver_manager.chrome import ChromeDriverManager


def scrape_info():
    # Splinter setup
    executable_path = {'executable_path': ChromeDriverManager().install()}
    browser = Browser('chrome', **executable_path, headless=False)

    # Visit URL
    url = ('https://redplanetscience.com/')
    browser.visit(url)

    html = browser.html
    soup = BeautifulSoup(html, 'html.parser')

    # Scrape news title
    news_title = soup.find_all('div', class_='content_title')[0].text

    # Scarpe news paragraph

    news_p = soup.find_all('div', class_='article_teaser_body')[0].text

    # Visit URL
    url = 'https://spaceimages-mars.com/'
    browser.visit(url)

    html = browser.html
    soup = BeautifulSoup(html, 'html.parser')

    partial_url = soup.find_all('a',class_="showimg")[0]['href']
    featured_image_url = url + partial_url

    # Mars Facts table
    url = 'https://galaxyfacts-mars.com/'

    mars_facts = pd.read_html(url)

    mars_facts_df = mars_facts[0]
    header_row = 0
    mars_facts_df.columns = mars_facts_df.iloc[header_row]
    mars_facts_df = mars_facts_df.drop(header_row)
    mars_facts_df = mars_facts_df.reset_index(drop=True)

    mars_facts_html = mars_facts_df.to_html(index=False, classes="table table-striped table-responsive")

    # Visit URL
    url = 'https://marshemispheres.com/'
    browser.visit(url)

    soup = BeautifulSoup(browser.html, 'html.parser')

    titles = soup.find_all('h3')[:-1]

    title_ls = []
    for title in titles:
        title_ls.append(title.text)
    
    url_ls = []

    for title in title_ls:
        url = 'https://marshemispheres.com/'
        browser.visit(url)
        browser.click_link_by_partial_text(title)
        html = browser.html
        soup = BeautifulSoup(browser.html, 'html.parser')
        image_url = soup.find_all('li')[0].a["href"]
        dictionary = {"title": title,"image_url":url + image_url}
        url_ls.append(dictionary)

    # Store data in a dictionary
    mars_data = {
        "NewsTitle": news_title,
        "NewsPara": news_p,
        "FeaturedImg": featured_image_url,
        "MarsFacts": mars_facts_html,
        "Hemispheres": url_ls,
    }

    # Close the browser after scraping
    browser.quit()

    # Return results
    return mars_data