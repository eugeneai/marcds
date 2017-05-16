from nose.tools import nottest

from random import choice
from pyknow import *


class Light(Fact):
    """Info about the traffic light."""
    pass


class RobotCrossStreet(KnowledgeEngine):
    @Rule(Light(color='green'))
    def green_light(self):
        print("Walk")

    @Rule(Light(color='red'))
    def red_light(self):
        print("Don't walk")

    @Rule('light' << Light(color=L('yellow') | L('blinking-yellow')))
    def cautious(self, light):
        print("Be cautious because light is", light["color"])


def test_roborules():
    engine = RobotCrossStreet()
    engine.reset()
    engine.declare(
        Light(color=choice(['green', 'yellow', 'blinking-yellow', 'red'])))
    engine.run()
    # Be cautious becau
