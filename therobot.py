import time
import random
import os
from selenium import webdriver
from pymouse import PyMouse

class TheRobot():

    sites = ["http://reddit.com",
             "http://buzzfeed.com"]

    def __init__(self, profile_filename):
        lifes = os.listdir('ids')
        self.actual_life = 'ids/life-{}'.format(len(lifes) + 1)
        # And there was light...
        os.mkdir(self.actual_life)
        self.profile_filename = profile_filename
        self.profile = webdriver.FirefoxProfile(self.profile_filename)
        self.world = webdriver.Firefox(self.profile)
        self.world_position = self.world.get_window_position()
        self.attention_focus = PyMouse()
        self.born_place = random.choice(self.__class__.sites)
        self.alive = False
        self.memories = 0

    def live(self):
        self.born_time = time.time()
        # And there was wander...
        self.alive = True
        self.wander_to(self.born_place)

        while self.alive:
            self.thought = self.choose()
            self.attention(self.thought)
            self.wander_to(self.thought)
            self.memorize()
            self.think()

    def choose(self):
        all_objects = self.world.find_elements_by_tag_name('a')
        objects_to_look_at = []
        for obj in all_objects:
            try:
                if obj.is_displayed():
                    objects_to_look_at.append(obj)
            except:
                pass
        if not objects_to_look_at:
            objects_to_look_at = self.__class__.sites
        choice = random.choice(objects_to_look_at)
        return choice

    def think(self):
        self.time_to_think = 1 + 1*random.random()
        self.started_wonder_at = time.time()
        self.is_thinking = True
        while self.is_thinking:
            time_now = time.time()
            if time_now - self.started_wonder_at > self.time_to_think:
                self.is_thinking = False

    def attention(self, thought):
        if type(thought) != str:
            window_to_world = thought.rect
            looking_x, looking_y = self.attention_focus.position()
            change_x = (looking_x - window_to_world['x'])/10.0
            change_y = (looking_y - window_to_world['y'])/10.0
            steps = 10
            while steps > 0:
                looking_x += change_x
                looking_y += change_y
                time.sleep(0.005)
                steps -= 1
                self.attention_focus.move(int(looking_x), int(looking_y))

    def memorize(self):
        new_memory = self.actual_life + '/memory-{}.jpg'.format(self.memories)
        self.world.save_screenshot(new_memory)
        self.memories += 1

    def wander_to(self, place):
        if type(place) != str:
            place = place.get_attribute('href')
        try:
            self.world.get(place)
        except:
            self.world.get(self.born_place)

me = TheRobot("/home/walrus/.mozilla/firefox/fhittmzv.procastinator/")
me.live()
