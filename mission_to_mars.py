# Dependencies
from bs4 import BeautifulSoup as bs
from splinter import Browser
import time
import pandas as pd
import requests
import pymongo

# ## Step 1 - Scraping
# - Complete your initial scraping using Jupyter Notebook, BeautifulSoup, Pandas, and Requests/Splinter.
# - Create a Jupyter Notebook file called mission_to_mars.ipynb and use this to complete all of your scraping and analysis tasks. The following outlines what you need to scrape.

def init_browser():
    executable_path = {'executable_path': '/usr/local/Cellar/chromedriver/2.35/bin/chromedriver'}
    return Browser('chrome', **executable_path, headless=False)

def scrape():

    # #### NASA Mars News
    # Scrape the [NASA Mars News Site](https://mars.nasa.gov/news/) and collect the latest News Title and Paragragh Text. Assign the text to variables that you can reference later.

    # URL of page to be scraped
    nasaURL = 'https://mars.nasa.gov/news/'

    # Retrieve page with the requests module
    nasaResponse = requests.get(nasaURL)
    # Create BeautifulSoup object; parse with 'html.parser'
    nasaSoup = bs(nasaResponse.text, 'html.parser')

    newsTitle = nasaSoup.find('div', {'class' : 'content_title'}).find('a').get_text().strip()
    newsP = nasaSoup.find('div', {'class' : 'rollover_description_inner'}).get_text().strip()


    # #### JPL Mars Space Images - Featured Image
    # - Visit the url for JPL's Featured Space Image [here](https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars).
    # - Use splinter to navigate the site and find the image url for the current - Featured Mars Image and assign the url string to a variable called featured_image_url.
    # - Make sure to find the image url to the full size .jpg image.
    # - Make sure to save a complete url string for this image.


    # Set paths
    browser = init_browser()
    jplURL = 'https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars'

    # Retrieve page with the requests module
    nasaResponse = requests.get(nasaURL)
    # Create BeautifulSoup object; parse with 'html.parser'
    nasaSoup = bs(nasaResponse.text, 'html.parser')

    # Navigate to article page
    browser.visit(jplURL)
    browser.click_link_by_partial_text('FULL IMAGE')
    time.sleep(3)
    browser.click_link_by_partial_text('more info')

    # Get HTML from final page
    featureArticle = browser.html

    # Create BeautifulSoup object; parse with 'html.parser'
    jplSoup = bs(featureArticle,'html.parser')

    # Find image source tag
    featuredImg = jplSoup.find('figure', {'class' : 'lede'}).find('img')
    featuredImgSrc = featuredImg['src']

    # Create full URL
    featuredImgURL = 'https://www.jpl.nasa.gov' + featuredImgSrc


    # #### Mars Weather
    # Visit the Mars Weather twitter account [here](https://twitter.com/marswxreport?lang=en) and scrape the latest Mars weather tweet from the page. Save the tweet text for the weather report as a variable called mars_weather.

    # URL of page to be scraped
    twitterURL = 'https://twitter.com/marswxreport'

    # Retrieve page with the requests module
    twitterResponse = requests.get(twitterURL)
    # Create BeautifulSoup object; parse with 'html.parser'
    twitterSoup = bs(twitterResponse.text, 'html.parser')

    newsTitle = nasaSoup.find('div', {'class' : 'content_title'}).find('a').get_text().strip()
    newsP = nasaSoup.find('div', {'class' : 'rollover_description_inner'}).get_text().strip()


    marsWeather = twitterSoup.find('li', {'class' : 'stream-item'}).find('div', {'class' : 'js-tweet-text-container'}).get_text().strip()

    # #### Mars Facts
    # - Visit the Mars Facts webpage [here](http://space-facts.com/mars/) and use Pandas to scrape the table containing facts about the planet including Diameter, Mass, etc.
    # - Use Pandas to convert the data to a HTML table string.

    # Read URL Tables using pandas
    factsURL = 'https://space-facts.com/mars/'
    tables = pd.read_html(factsURL)

    # Make it into a dataframe
    df = tables[0]
    df.columns = ['Profile','Fact']

    factsDict = df.to_dict('records')

    # #### Mars Hemisperes
    # - Visit the USGS Astrogeology site [here](https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars) to obtain high resolution images for each of Mar's hemispheres.
    # - You will need to click each of the links to the hemispheres in order to find the image url to the full resolution image.
    # - Save both the image url string for the full resolution hemipshere image, and the Hemisphere title containing the hemisphere name. Use a Python dictionary to store the data using the keys img_url and title.
    # - Append the dictionary with the image url string and the hemisphere title to a list. This list will contain one dictionary for each hemisphere.

    usgsURL = 'https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars'

    # Retrieve page with the requests module
    usgsResponse = requests.get(usgsURL)
    # Create BeautifulSoup object; parse with 'html.parser'
    usgsSoup = bs(usgsResponse.text, 'html.parser')

    # Find hemisphere listings
    usgsResults = usgsSoup.find_all('div', {'class' : 'item'})

    hemispherePhotos = []
    # Iterate through results and get hemisphere name and high-res image url
    for result in usgsResults:
        # Create detail page URL
        src = result.a['href']
        url = 'https://astrogeology.usgs.gov' + src

        # Retrieve page with the requests module
        response = requests.get(url)
        # Create BeautifulSoup object; parse with 'html.parser'
        soup = bs(response.text, 'html.parser')

        # Get Hemisphere name
        hemisphere = soup.find('div', {'class' : 'content'}).h2.get_text().strip()
        hemisphereName = hemisphere[:-9]

        # Get high-res image URL
        downloads = soup.find('div', {'class' : 'downloads'}).find_all('li')
        link = downloads[0].a['href']

        hemispherePhotos.append({'title' : hemisphereName,
                                 'img_url' : link})

    marsinfo = {}

    marsinfo['latestnews'] = {'title' : newsTitle, 'subtitle': newsP}
    marsinfo['featuredimage'] = featuredImgURL
    marsinfo['weather'] = marsWeather
    marsinfo['planetfacts'] = factsDict
    marsinfo['hemispheres'] = hemispherePhotos

    return marsinfo


# post = scrape()
#
# pp = pprint.PrettyPrinter(indent=4)
# pp.pprint(post)

# # The default port used by MongoDB is 27017
# # https://docs.mongodb.com/manual/reference/default-mongodb-port/
# conn = 'mongodb://localhost:27017/'
# client = pymongo.MongoClient(conn)
#
# # Define the database in Mongo
# db = client.mars_db
# # Declare the collection
# collection = db.information
#
# post = scrape()
# db.collection.insert_one(post)
