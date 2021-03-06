import time
import random
import re
from selenium import webdriver
from pymouse import PyMouse

browser_position = (0,0)
mouse = PyMouse()

def split_url(url):
    rp = re.compile('http.?://')
    url = rp.sub('', url)
    return url.split('/')[-1:] if url.endswith('/') else url.split('/')

def domain(url):
    return '.'.join(url.split('.')[-2:])

class ImgurSurfer(object):

    url = "http://imgur.com"
    domain = "imgur.com"

    def __init__(self):
        self.alive = True

    def act(self, driver):
        pass

class DefaultSurfer(object):

    url = None
    domain = 'all'

    def __init__(self):
        self.alive = True

    def act(self, driver, url):
        page = driver.get(url)
        time.sleep(3)
        driver.back()


class RedditSurfer(object):

    url = "http://reddit.com"
    domain = 'reddit.com'
    history = []

    def __init__(self):
        self.alive = True

    def act(self, driver, url=None):
        if not url:
            page = driver.get(self.url)

        self.history.append(self.url)
        i = 5
        while i > 0:
            site_content = driver.find_element_by_id("siteTable")
            contents = site_content.find_elements_by_class_name("title")
            comments = site_content.find_elements_by_class_name("comments")
            contents_links = [link.get_attribute('href') for link in contents]
            contents_links = [c for c in contents_links if c]
            comments_links = [link.get_attribute('href') for link in comments]

            for content_link, comment_link in zip(contents_links, comments_links):
                time.sleep(2)
                new_page = driver.get(comment_link)
                self.history.append(comment_link)
                i = 0
                rd = int(15*random.random())
                while True:
                    if rd > 0:
                        rd -= 1
                    else:
                        rd = int(5*random.random())
                    driver.execute_script("window.scrollTo(0, {}*5);".format(i))
                    i += 1
                    time.sleep(0.01)
                    if i == 300:
                        break

                if domain(split_url(content_link)[0]) == 'imgur.com':
                    driver.get(content_link)
                    time.sleep(5)
                    driver.back()

                driver.back()
                self.history.append('BACK')
                print self.history, '\n\n'

    def grab_info(self):
        pass

default = DefaultSurfer()
reddit = RedditSurfer()
imgur = ImgurSurfer()

surfers = {surfer.domain: surfer for surfer in [reddit, imgur, default]}

def run_surfer(surfer):
    profile = webdriver.FirefoxProfile("/home/walrus/.mozilla/firefox/fhittmzv.procastinator/")
    driver = webdriver.Firefox(profile)
    global browser_position
    browser_position = driver.get_window_position()

    while surfers['reddit.com'].alive:
        surfers['reddit.com'].act(driver)

run_surfer(reddit)
