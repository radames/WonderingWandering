import time
import random
import logging
import os
import re
import numpy as np
from sys import argv
from selenium import webdriver
import bs4
from pymouse import PyMouse

def readable(element):
    if element.parent.name in ['style', 'script', '[document]', 'head', 'title']:
        return False
    elif isinstance(element, bs4.element.Comment):
        return False
    return True

class MakeMove():
    NPTS = 100

    def linear_bezier(self, point1, point2, t):
        return (1.0 - t) * point1 + t * point2

    def interpolate_control_points(self, points, t):
        return [
            self.linear_bezier(point1, point2, t)
            for point1, point2 in zip(points, points[1:])]

    def bezier(self, control_points, t, stoplevel=2):
        points = self.points_as_arrays(control_points)
        while len(points) > stoplevel:
            points = self.interpolate_control_points(points, t)
            return self.linear_bezier(points[0], points[1], t)

    def points_as_arrays(self, point_tuples):
        return [np.array(point) for point in point_tuples]

    def getPoints(self, startx, starty, endx, endy):
        p0 = (startx, starty)
        p1 = (endx, endy)
        control_points = [p0, (p0[0]/1.5,p0[0]/1.5), p1, p1]
        times = np.linspace(0, 1, num=self.NPTS)
        curve = np.array([self.bezier(control_points, t) for t in times]).T
        bzPos = zip(*curve.tolist())
        return bzPos

class TheRobot():

    sites = ["http://reddit.com",
             "http://9gag.com",
             "http://youtube.com",
             "http://bbc.co.uk"]

    def __init__(self, profile_filename):
        # Where all the unconsciousness will exist
        lifes = os.listdir('ids')
        self.actual_life = 'ids/life-{}'.format(len(lifes) + 1)
        # And there was light...
        os.mkdir(self.actual_life)
        self.biography_title = self.actual_life + '/my_life'
        self.biography = open(self.biography_title, 'w')
        self.profile_filename = profile_filename
        self.profile = webdriver.FirefoxProfile(self.profile_filename)
        # And the world was created
        self.world = webdriver.Firefox(self.profile)
        self.world.maximize_window()
        # What is the world's border size?
        self.world_border = self.world.get_window_size()['height'] - self.world.find_element_by_tag_name('html').rect['height']
        # In some place of the universe
        self.world_position = self.world.get_window_position()
        # And one day, something will look at it
        self.attention_focus = PyMouse()
        # Something that will appears in someplace
        self.born_place = random.choice(self.__class__.sites)
        # But for now, there is no life
        self.alive = False
        # And of course, no memories
        self.memories = 0
        self.short_time_memory = set()
        self.makemove = MakeMove()
        # Not borde yet, but one day it will be
        self.boredness = 0
        # Normality? Nature vs. Nurture
        self.environment = 'NORMALITY'
        self.start_your_memory()

    def start_your_memory(self):
        self.memory = logging
        self.memory.basicConfig(filename=self.biography_title, level=logging.INFO, format='%(asctime)s %(message)s')

    def get_environment(self, url):
        p = re.compile('.*//([^!]*?)(?=/)')
        environment_match = p.match(url)
        if environment_match:
            environment = environment_match.group(1)
        else:
            environment = 'NORMALITY'
        return '.'.join(environment.split('.')[-3:])

    def create_masks(self):
        self.masks = {}
        self.masks['youtube.com'] = self.behave_in_youtube

    def behave_in(self, environment):
        if self.masks.has_key(environment):
            self.masks[environment]()
        else:
            self.default_behaviour()

    def default_behaviour(self):
        self.time_to_think = 1 + 3*random.random()
        self.started_wonder_at = time.time()
        self.is_thinking = True
        while self.is_thinking:
            time_now = time.time()
            if time_now - self.started_wonder_at > self.time_to_think:
                self.is_thinking = False

    def wait(self, wait_time):
        self.time_to_think = wait_time
        self.started_wonder_at = time.time()
        self.is_thinking = True
        while self.is_thinking:
            time_now = time.time()
            if time_now - self.started_wonder_at > self.time_to_think:
                self.is_thinking = False

    def behave_in_youtube(self):
        if 'watch' in self.world.current_url:
            self.wait(random.random()*36)
        else:
            self.default_behaviour()

    def live(self):
        # And so we created it
        self.born_time = time.time()
        self.memory.info('I was born in {}.'.format(self.born_time))
        # And there was wander...
        self.alive = True
        # Beginning from someplace
        self.memory.info('Everything started at {}.'.format(self.born_place))
        self.wander_to(self.born_place)
        # And let's have some instincts
        self.create_masks()

        while self.alive:
            # Choose what to do
            if self.boredness < 5:
                self.thought = self.choose()
            else:
                self.memory.info('I am bored! I want to go to another place...')
                self.thought = random.choice(self.__class__.sites)
                self.boredness = 0

            self.verbal_thought = '{}'.format(self.thought if type(self.thought) == str else self.thought.get_attribute('href'))
            self.memory.info('I thought that going to {} would be a good idea.'.format(self.verbal_thought))
            new_environment = self.get_environment(self.verbal_thought) if self.verbal_thought else 'NORMALITY'

            # Everyone loves a change... sometimes
            if new_environment == self.environment:
                self.boredness += 1
                print self.get_environment(self.verbal_thought)
            else:
                self.boredness = 0

            self.environment = new_environment

            # Pay attention for what you decided
            self.look_around()
            self.attention(self.thought)
            # And follow it, try not to miss it
            self.wander_to(self.thought)
            # Specially try to not forget it
            #self.memorize()
            # And when you are there, think, think... think
            self.think()
            # And maybe you will get bored, But don't despair, you always can one more time...

    def look_around(self):
        self.world_height = self.world.find_element_by_tag_name('body').rect['height']
        self.looking_around = True
        self.looking_around_time = random.random()*10
        self.start_looking_time = time.time()
        self.small_thought_time = self.start_looking_time
        while self.looking_around:
            time_now = time.time()
            if time_now - self.start_looking_time > self.looking_around_time:
                self.world.execute_script("window.scrollTo({top: 0, behavior: 'smooth'})")
                break

            if time_now - self.small_thought_time > 0.4:
                self.world.execute_script("window.scrollTo({{top: {}, behavior: 'smooth'}})".format(random.random()*self.world_height))
                self.small_thought_time = time.time()


    def choose(self):
        # What exist around you?
        all_objects = self.world.find_elements_by_tag_name('a')
        objects_to_look_at = []
        for obj in all_objects:
            try:
                # But what objectively exists?
                if obj.is_displayed():
                    objects_to_look_at.append(obj)
            except:
                pass
        # Don't still know where to look at?
        if not objects_to_look_at:
            # Go for the places that you already know better.
            objects_to_look_at = self.__class__.sites
        choice = random.choice(objects_to_look_at)
        return choice

    def think(self):
       self.behave_in(self.environment)

    def attention(self, thought):
        # Is it a concrete thought?
        if type(thought) != str:
            # Find a small window to thw world to look at
            window_to_world = thought.rect
            looking_x, looking_y = self.attention_focus.position()

            correct_point_of_view = window_to_world['y'] + self.world_border

            if window_to_world['y'] > self.world.get_window_size()['height']:
                self.world.execute_script("window.scrollTo({{top: {}, behavior: 'smooth'}})".format(window_to_world['y'] + 40))
                correct_point_of_view = 40 + self.world_border
                time.sleep(1)
            error_x = window_to_world['width']*random.random()
            error_y = window_to_world['height']*random.random()

            pts = self.makemove.getPoints(looking_x, looking_y, window_to_world['x'] + error_x, correct_point_of_view + error_y)

            for p in pts:
                self.attention_focus.move(p[0],p[1])
                time.sleep(1.0/100)

    def memorize(self):
        # To remember is to be alive
        new_memory = self.actual_life + '/memory-{}.jpg'.format(self.memories)
        #self.world.save_screenshot(new_memory)
        self.biography.write(self.verbal_thought)
        self.biography.flush()
        self.memories += 1

    def wander_to(self, place):
        # Do you know where the place is?
        if type(place) != str:
            # Get the direction to the place
            place = place.get_attribute('href')
        try:
            # Wander to the place
            self.world.get(place)
        except:
            # Don't know where to go, what to do? Start from beginning...
            self.world.get(self.born_place)

the_profile = argv[1] if len(argv) > 1 else "/home/walrus/.mozilla/firefox/fhittmzv.procastinator/"
me = TheRobot(the_profile)
# And so it begins...
me.live()
