import unittest

from roboter.models import robot


class TestRobot(unittest.TestCase):
    def test_robot_init(self):
        r = robot.Robot(name='test robot')
        self.assertEqual(r.name, 'test robot')
