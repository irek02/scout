import unittest
import components

class TestStringMethods(unittest.TestCase):
  def test_TargetLocator(self):
    resolution = (50, 40)
    locator = components.TargetLocator(resolution)

    location = locator.get_target_loc('tests/images/up.jpg')
    self.assertEqual(location, "up")

    location = locator.get_target_loc('tests/images/right.jpg')
    self.assertEqual(location, "right")

    location = locator.get_target_loc('tests/images/down.jpg')
    self.assertEqual(location, "down")

    location = locator.get_target_loc('tests/images/left.jpg')
    self.assertEqual(location, "left")

    location = locator.get_target_loc('tests/images/center.jpg')
    self.assertEqual(location, "center")


suite = unittest.TestLoader().loadTestsFromTestCase(TestStringMethods)
unittest.TextTestRunner(verbosity=2).run(suite)


# @Todo testVehicleComponentInterface for implementing shutdown method.