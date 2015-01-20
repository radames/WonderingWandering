import time

from selenium import webdriver

def split_url(url):
    url = url.replace('http://','')
    return url.split('/')[-1:] if url.endswith('/') else url.split('/')

def domain(url):
    return '.'.join(url.split('.')[-2:])

class RedditSurfer(object):

    url = "http://reddit.com"
    alive = True
    history = []

    def __init__(self):
        pass

    def act(self, driver):
        page = driver.get(self.url)
        self.history.append(self.url)
        i = 5
#        action = webdriver.ActionChains(driver)
        while i > 0:
            site_content = driver.find_element_by_id("siteTable")
            comments_links = site_content.find_elements_by_class_name("comments")

            links = [link.get_attribute('href') for link in comments_links]
            for link in links:
                time.sleep(2)
                new_page = driver.get(link)
                self.history.append(link)
                i = 0
                while True:
                    driver.execute_script("window.scrollTo(0, {}*200);".format(i))
                    i += 1
                    time.sleep(1)
#                    action.move_by_offset(i*10, i*10)
#                    driver.mouse_move(i*10, i*20)
                    if i == 5:
                        break
#                action.perform()
#                time.sleep(3)
                driver.back()
                self.history.append('BACK')
                print self.history, '\n\n'

    def grab_info(self):
        pass

reddit = RedditSurfer()

def run_surfer(surfer):
    driver = webdriver.Firefox()

    while surfer.alive:
        surfer.act(driver)

run_surfer(reddit)
