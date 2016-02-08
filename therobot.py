import time
import random
import os
from sys import argv
from selenium import webdriver
from pymouse import PyMouse

class TheRobot():

    sites = ["http://reddit.com",
             "http://9gag.com",
             "http://youtube.com",
             "https://en.wikipedia.org/wiki/Special:Random"]

    def __init__(self, profile_filename):
        # Where all the unconsciousness will exist
        lifes = os.listdir('ids')
        self.actual_life = 'ids/life-{}'.format(len(lifes) + 1)
        # And there was light...
        os.mkdir(self.actual_life)
        self.biography = open(self.actual_life + '/my_life', 'w')
        self.profile_filename = profile_filename
        self.profile = webdriver.FirefoxProfile(self.profile_filename)
        # And the world was created
        self.world = webdriver.Firefox(self.profile)
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

    def live(self):
        # And so we created it
        self.born_time = time.time()
        # And there was wander...
        self.alive = True
        # Beginning from someplace
        self.wander_to(self.born_place)

        while self.alive:
            # Choose what to do
            self.thought = self.choose()
            self.verbal_thought = '{}\n'.format(self.thought if type(self.thought) == str else self.thought.get_attribute('href'))
            # Pay attention for what you decided
            self.attention(self.thought)
            # And follow it, try not to miss it
            self.wander_to(self.thought)
            # Specially try to not forget it
            self.memorize(self.thought)
            # And when you are there, think, think... think
            self.think()
            # And maybe you will get bored, But don't despair, you always can one more time...

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
        # For now, to think is to exist, just let the time flows. What is "to wonder"?
        self.time_to_think = 1 + 1*random.random()
        self.started_wonder_at = time.time()
        self.is_thinking = True
        while self.is_thinking:
            time_now = time.time()
            if time_now - self.started_wonder_at > self.time_to_think:
                self.is_thinking = False

    def attention(self, thought):
        # Is it a concrete thought?
        if type(thought) != str:
            # Find a small window to thw world to look at
            window_to_world = thought.rect
            looking_x, looking_y = self.attention_focus.position()

            correct_point_of_view = window_to_world['y']
            if window_to_world['y'] > self.world.get_window_size()['height']:
                self.world.execute_script("window.scrollTo({{top: {}, behavior: 'smooth'}})".format(window_to_world['y'] + 40))
                correct_point_of_view = 40

            change_x = -(looking_x - window_to_world['x'])/10.0
            change_y = -(looking_y  - 97 - correct_point_of_view)/10.0

            #print looking_x, looking_y, window_to_world, change_x, change_y
            steps = 10
            # And move your eye to it!
            while steps > 0:
                looking_x += change_x
                looking_y += change_y
                #print looking_x, looking_y, window_to_world, change_x, change_y
                time.sleep(0.05)
                steps -= 1
                self.attention_focus.move(int(looking_x), int(looking_y))

    def memorize(self, tought):
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
