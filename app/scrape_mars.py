# Import dependencies

from bs4 import BeautifulSoup as bs
import requests
import pandas as pd
from splinter import Browser
import pymongo
from flask import Flask, render_template, redirect
from flask_pymongo import PyMongo
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager

# Import Splinter and set the chromedriver path
executable_path = {
    "executable_path": ChromeDriverManager().install()}
browser = Browser("chrome", **executable_path, headless=False)


def scrape():

    # In[28]:
    mars_info_dict = dict()

    # Visit the following URL
    url = "https://mars.nasa.gov/news/"
    browser.visit(url)

    # In[29]:
    html = browser.html
    soup = bs(html, "html.parser")

    # NASA Mars News

    # In[30]:
    news_title = soup.find('div', class_="content_title")

    news_title = news_title.text.strip()

    mars_info_dict['news_titles'] = news_title

    # In[31]:
    news_paragraphs = soup.find('div', class_="article_teaser_body")
    news_paragraphs = news_paragraphs.text.strip()
    mars_info_dict['news_paragraph'] = news_paragraphs

    # JPL Mars Space Images - Featured Image

    # In[83]:
    # Visit the following URL
    url_2 = "https://data-class-jpl-space.s3.amazonaws.com/JPL_Space/index.html"
    browser.visit(url_2)

    # In[84]:
    html = browser.html
    soup = bs(html, "html.parser")

    # In[85]:
    featured_image = soup.find('img',class_ = 'thumbimg').get('src')

    # In[90]:
    featured = featured_image['data-fancybox-href']

    # In[91]:
    featured_image_url = "https://data-class-jpl-space.s3.amazonaws.com/JPL_Space/index.html" + featured

    mars_info_dict['featured_image_urls'] = featured_image_url

    # Mars Facts
    # In[78]:
    mars_facts = pd.read_html('https://space-facts.com/mars/')
    mars_facts_df = mars_facts[0]

    # In[79]:
    mars_facts_html = mars_facts_df.to_html(buf=None, columns=None, col_space=None, header=True, index=True, na_rep='NaN', formatters=None, float_format=None, sparsify=None,
                                            index_names=True, justify=None, bold_rows=True, classes=None, escape=True, max_rows=None, max_cols=None, show_dimensions=False, notebook=False)

    mars_info_dict['mars_facts_htmls'] = mars_facts_html

    # Mars Hemispheres

    # In[50]:
    url_hemispherecerberus = 'https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars'
    browser.visit(url_hemispherecerberus)
    html = browser.html
    soup = bs(html, 'html.parser')

    # In[51]:

    image_cerberus = soup.find_all("img", class_='wide-image')
    for image in image_cerberus:
        img_cerberus = "https://astrogeology.usgs.gov"+image['src']

    # In[52]:

    url_hemisphereschiaparelli = 'https://astrogeology.usgs.gov/search/map/Mars/Viking/schiaparelli_enhanced'
    browser.visit(url_hemisphereschiaparelli)
    html = browser.html
    soup = bs(html, 'html.parser')

    # In[54]:

    image_schiaparelli = soup.find_all("img", class_='wide-image')
    for image in image_schiaparelli:
        img_schiaparelli = "https://astrogeology.usgs.gov"+image['src']

    # In[58]:

    url_hemispheresyrtis = 'https://astrogeology.usgs.gov/search/map/Mars/Viking/syrtis_major_enhanced'
    browser.visit(url_hemispheresyrtis)
    html = browser.html
    soup = bs(html, 'html.parser')

    # In[59]:

    image_syrtis = soup.find_all("img", class_='wide-image')
    for image in image_syrtis:
        img_syrtis = "https://astrogeology.usgs.gov"+image['src']

    # In[68]:

    url_hemispheremarineris = 'https://astrogeology.usgs.gov/search/map/Mars/Viking/valles_marineris_enhanced'
    browser.visit(url_hemispheremarineris)
    html = browser.html
    soup = bs(html, 'html.parser')

    # In[69]:

    image_marineris = soup.find_all("img", class_='wide-image')
    for image in image_marineris:
        img_marineris = "https://astrogeology.usgs.gov"+image['src']

    # In[80]:

    hemisphere_image_urls = [
        {"title": "Valles Marineris Hemisphere", "img_url": img_marineris},
        {"title": "Cerberus Hemisphere", "img_url": img_cerberus},
        {"title": "Schiaparelli Hemisphere", "img_url": img_schiaparelli},
        {"title": "Syrtis Major Hemisphere", "img_url": img_syrtis}
    ]

    # In[81]:

    mars_info_dict['hemisphere_images'] = hemisphere_image_urls

    complete_mars_dict = {
        "News_Title": mars_info_dict["news_titles"],
        "News_Summary": mars_info_dict["news_paragraph"],
        "Featured_Image": mars_info_dict["featured_image_urls"],
        "Facts_Table": mars_facts_html,
        "Hemisphere_Image_urls": hemisphere_image_urls
    }

    return complete_mars_dict
