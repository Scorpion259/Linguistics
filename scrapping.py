import time
from selenium.webdriver.firefox.options import Options
from bs4 import BeautifulSoup
from scriptsDB import insert_document, find_document, delete_document
from pymongo import MongoClient
from Connection import ConnectionString
from selenium import webdriver
from selenium.common.exceptions import TimeoutException

options = Options()
options.set_preference('permissions.default.image', 2)
options.set_preference('dom.ipc.plugins.enabled.libflashplayer.so', False)

# Create the client
client = MongoClient(ConnectionString, 1488)
# Connect to our database
db = client['ling']
# Fetch our series collection
articles_collection = db['news']


def getArticles(url):
    # Setup the driver. This one uses firefox with some options and a path to the geckodriver
    driver = webdriver.Firefox(options=options, executable_path='C:\\geckodriver.exe')
    # implicitly_wait tells the driver to wait before throwing an exception
    driver.implicitly_wait(30)
    # driver.get(url) opens the page
    driver.get(url)
    # This starts the scrolling by passing the driver and a timeout
    scroll(driver, 5)
    # Once scroll returns bs4 parsers the page_source
    soup_a = BeautifulSoup(driver.page_source, 'lxml')
    # Them we close the driver as soup_a is storing the page source
    driver.close()

    # Looping through all the a elements in the page source
    for article in soup_a.find_all('div', class_='matter'):
        title = article.find('div', class_='title').get_text(strip=True)
        lead = article.find('div', class_='lead').get_text(strip=True)
        rubric = article.find('a', class_='rubric').get_text(strip=True)
        link = article.find('a', class_='img', href=True)['href']

        print(str(title) + '\n' + str(lead) + '\n' + str(rubric) + '\n' + str(link) + '\n\n')

        url_of_article = 'https://novostivolgograda.ru' + link
        print(url_of_article)
        driver = webdriver.Firefox(options=options, executable_path='C:\\geckodriver.exe')
        driver.set_page_load_timeout(2)

        try:
            driver.get(url_of_article)
            soup = BeautifulSoup(driver.page_source, 'html.parser')
            for block in soup.find_all('section', class_='cols'):
                full_text = block.find('div', class_='content-blocks').get_text(strip=True)
            print("URL successfully Accessed")
            new_article = {
                "title": str(title),
                "lead": str(lead),
                "rubric": str(rubric),
                "link": str(link),
                "full_text": str(full_text)
            }
            insert_document(articles_collection, new_article)
            driver.quit()
        except TimeoutException as e:
            print("Page load Timeout Occurred. Quitting !!!")
            soup = BeautifulSoup(driver.page_source, 'html.parser')
            for block in soup.find_all('section', class_='cols'):
                full_text = block.find('div', class_='content-blocks').get_text(strip=True)
            new_article = {
                "title": str(title),
                "lead": str(lead),
                "rubric": str(rubric),
                "link": str(link),
                "full_text": str(full_text)
            }
            insert_document(articles_collection, new_article)
            driver.quit()


def scroll(driver, timeout):
    scroll_pause_time = timeout

    # Get scroll height
    last_height = driver.execute_script("return document.body.scrollHeight")

    while True:
        # Scroll down to bottom
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")

        # Wait to load page
        time.sleep(scroll_pause_time)

        # Calculate new scroll height and compare with last scroll height
        new_height = driver.execute_script("return document.body.scrollHeight")
        if new_height == last_height:
            # If heights are the same it will exit the function
            break
        last_height = new_height


if __name__ == '__main__':
    print(getArticles('https://novostivolgograda.ru/news'))
