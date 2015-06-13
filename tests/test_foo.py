import unittest
import io
import imageprocessor
import vehicle

class TestStringMethods(unittest.TestCase):
  def setUp(self):
    print("Booo")

  def test_imageprocessor(self):
    thr = ImageStreamThreadDouble()

    # Give the stream that represents target on the lest
    thr.stream = self.import_from_file()

    img_pr = imageprocessor.ImageProcessor(thr)
    self.assertEqual(img_pr.get_target_loc(), 'left')

  def import_from_file(self):
    return ''



class ImageStreamThreadDouble:
  def __init__(self):      
      self.stream = io.BytesIO()

  def get_resolution(self):
    return (50, 40)




suite = unittest.TestLoader().loadTestsFromTestCase(TestStringMethods)
unittest.TextTestRunner(verbosity=2).run(suite)
