import time
import random
from selenium import webdriver
from pymouse import PyMouse

class TheRobot():

    sites = ["http://reddit.com",
             "http://buzzfeed.com"]

    def __init__(self, profile_filename):
        self.profile_filename = profile_filename
        self.profile = webdriver.FirefoxProfile(self.profile_filename)
        self.world = webdriver.Firefox(self.profile)
        self.browser_position = self.world.get_window_position()
        self.attention = PyMouse()
        self.born_place = random.choice(self.__class__.sites)
        self.alive = False

    def live(self):
        self.born_time = time.time()
        self.alive = True
        self.wander_to(self.born_place)

        while self.alive:
            self.thought = self.choose()
            self.wander_to(self.thought)
            self.think()

    def choose(self):
        objects_to_look_at = self.world.find_elements_by_tag_name('a') or random.choice(self.__class__.sites)
        self.attention_focus = random.choice(objects_to_look_at)
        return self.attention_focus.get_attribute('href')

    def think(self):
        self.time_to_think = 1 + 1*random.random()
        self.started_wonder_at = time.time()
        self.is_thinking = True
        while self.is_thinking:
            time_now = time.time()
            if time_now - self.started_wonder_at > self.time_to_think:
                self.is_thinking = False

    def wander_to(self, place):
        self.world.get(place)

me = TheRobot("/home/walrus/.mozilla/firefox/fhittmzv.procastinator/")
me.live()
