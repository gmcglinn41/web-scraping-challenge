from splinter import Browser
from bs4 import BeautifulSoup as bs
import time
import pandas as pd

def init_browser():
    # @NOTE: Replace the path with your actual path to the chromedriver
    executable_path = {"executable_path": "/usr/local/bin/chromedriver"}
    return Browser("chrome", **executable_path, headless=False)

def scrape_info():
    browser = init_browser()

    # Url page to be scrapped
  
    url_1 = "https://mars.nasa.gov/news/"
    
    browser.visit(url_1)

    time.sleep(5)

    # HTML object
    html = browser.html
 

    # Scrape page into Soup
    html = browser.html
    #Parse html 
    soup = bs(html, "html.parser")

    #Scrape first title
    list_items = soup.select_one('ul.item_list li.slide')
    first_title = list_items.find('div',class_='content_title').get_text()
    first_title

   
    #Scrape first paragraph
    first_paragraph= list_items.find('div',class_='article_teaser_body').get_text()
    print(first_title)
    print(first_paragraph)

    #Nasa Mars Space Images - Featured Image
    nasa_image_url = "https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars"
    browser.visit(nasa_image_url)
    
    time.sleep(5)
    full_image = browser.find_by_id('full_image')
    full_image.click()
    browser.is_element_present_by_text('more info',wait_time=1)
    browser.links.find_by_partial_text('more info').click()
    html = browser.html
    soup = bs(html, 'html.parser')
    image2 = soup.select_one("figure.lede a img").get("src")
    image2

    
    #Scraping the Mars Facts using Pandas
    mars =  "https://space-facts.com/mars/"
    mars_facts = pd.read_html(mars)
    mars_facts

    #Find the Mars Facts DataFrame in the list
    mars_df = mars_facts[0]

    #Create the dataFrame
    mars_df = mars_df.rename(columns={0: "Description", 1: "Mars"})

    #Set the index to Description
    mars_df.set_index("Description", inplace=True)
    mars_df

   
    #Convert Pandas table to html
    mars_html_table = mars_df.to_html()
    mars_html_table = mars_html_table.replace('\n', '')

    #Mars Hemispheres
    #Scrape Mars hemisphere title and image
    astro_url = "https://astrogeology.usgs.gov/"
    hemis_url = "https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars"
    browser.visit(hemis_url)
    html = browser.html
    soup = bs(html, "html.parser") 

    #Extract Item elements
    mars_hems = soup.find("div", class_="collapsible results")
    mars_item = mars_hems.find_all("div", class_="item")
    image_urls = []


    #looping through hemisphere item
    for item in mars_item:
        # Error handling
        try:
            #Extract title
            hem = item.find("div", class_="description")
            hem_title = hem.h3.text
            #Image url
            hem_image_url = hem.a["href"]
            browser.visit(astro_url+hem_image_url)
            html = browser.html
            soup = bs(html, "html.parser")
            image_src = soup.find('li').a['href']
            if (hem_title and image_src):
                print("-----------------------------")
                print(hem_title)
                print(image_src)
                hem_dict = {
                "Title" : hem_title,
                "Image Url" : image_src}
            
            image_urls.append(hem_dict)
        except Exception as e:
            print(e)
 
    #Create dictionary for all the record
   
    mars_dict = {
        "news_title" : first_title,
        "news_body" : first_paragraph,
        "jpl_image" : image2,
        "table" : mars_html_table,
        "hemisphere" : image_urls
    }

    #close the browser
    browser.quit()

    return mars_dict