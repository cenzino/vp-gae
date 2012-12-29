# -*- coding: utf-8 -*-
import unittest
from application.utils import slugify
from google.appengine.tools.appcfg import verbosity


class UtilsTest(unittest.TestCase):

    def test_slugify(self):
        self.assertEqual(slugify("Primo Post"), "primo-post")
        self.assertEqual(slugify("Google AppEngine"), "google-appengine")
        self.assertEqual(slugify("Perche Linux e meglio?"), "perche-linux-e-meglio")
        self.assertEqual(slugify("Python, Flask e AppEngine"), "python-flask-e-appengine")

if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    suite = unittest.TestLoader().loadTestsFromTestCase(UtilsTest)
    unittest.TextTestRunner(verbosity=2).run(suite)