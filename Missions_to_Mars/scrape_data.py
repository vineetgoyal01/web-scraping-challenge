from splinter import Browser
from bs4 import BeautifulSoup
import pandas as pd
import time 
from webdriver_manager.chrome import ChromeDriverManager
from time import sleep
#Site Navigation

executable_path = {'executable_path': ChromeDriverManager().install()}
browser = Browser("chrome", **executable_path, headless=False)

# Defining scrape & dictionary
def scrape():
    final_data = {}
    output = marsNews()
    final_data["mars_news"] = output[0]
    final_data["mars_paragraph"] = output[1]
    final_data["mars_image"] = marsImage()
    final_data["mars_facts"] = marsFacts()
    final_data["mars_hemisphere"] = marsHem()

    return final_data

# NASA Mars News

def marsNews():
    # Visit the NASA Mars News Site
    news_url = "https://mars.nasa.gov/news/"
    browser.visit(news_url)
    sleep(1)
    # Results HTML with BeautifulSoup
    html = browser.html
    soup = BeautifulSoup(html, "html.parser")

    # Scrape the latest News Title and latest Paragraph Text
    article = soup.select_one("ul.item_list li.slide")
    news_title = article.find("div", class_="content_title").get_text()
    news_p = article.find("div", class_ ="article_teaser_body").get_text()
    output = [news_title, news_p]
    return output

# JPL Mars Space Images - Featured Image
def marsImage():
    image_url = "https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars"
    browser.visit(image_url)
    html = browser.html
    soup = BeautifulSoup(html, "html.parser")
    image = soup.find("img", class_="thumb")["src"]
    featured_image_url = "https://www.jpl.nasa.gov" + image
    return featured_image_url


#  Mars Facts
def marsFacts():
    
    # Visit the Space Facts website
    facts_url = "https://space-facts.com/mars/"
    browser.visit(facts_url)
    
    # Using Pandas to reas the URL
    mars_data = pd.read_html(facts_url)
    mars_data = pd.DataFrame(mars_data[0])
    mars_data.columns = ["Description", "Value"]
    mars_data = mars_data.set_index("Description")
    mars_facts = mars_data.to_html(index = True, header =True)
    return mars_facts


# # Mars Hemispheres
def marsHem():
    
    # Visit the USGS Astrogeology Science Center Site
    hemispheres_url = "https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars"
    browser.visit(hemispheres_url)
    sleep(2)
    html = browser.html
    soup = BeautifulSoup(html, "html.parser")
    mars_hemisphere = []

    products = soup.find("div", class_ = "result-list" )
    hemispheres = products.find("div", class_="item")

    # Iterate through the List of All Hemispheres
    for hemisphere in hemispheres:
        title = hemisphere.find("h3").text
        title = title.replace("Enhanced", "")
        end_link = hemisphere.find("a")["href"]
        image_link = "https://astrogeology.usgs.gov/" + end_link    
        browser.visit(image_link)
        sleep(1)
        html = browser.html
        soup=BeautifulSoup(html, "html.parser")
        downloads = soup.find("div", class_="downloads")
        image_url = downloads.find("a")["href"]
        dictionary = {"title": title, "img_url": image_url}
        mars_hemisphere.append(dictionary)
    return mars_hemisphere

    # if running from command line, show the scraped data results
if __name__ == "__main__":
    result = scrape()
    print(result)