import doctest
import sys

import unittest
import os.path


# We do it this way instead of using doctest.DocTestSuite because doctest.DocTestSuite requires modules to be pickled, which python doesn't allow.
# We need tests to be pickleable so that they can be run on a cluster.
class TestDocStrings(unittest.TestCase):

    def test_bed(self):

        old_dir = os.getcwd()
        os.chdir(os.path.dirname(os.path.realpath(__file__)))
        result = doctest.testmod(sys.modules["fastlmm.pyplink.snpreader.Bed"])
        os.chdir(old_dir)
        assert result.failed == 0, "failed doc test: " + __file__


def getTestSuite():
    """
    set up composite test suite
    """

    test_suite = unittest.TestSuite([])
    test_suite.addTests(unittest.TestLoader().loadTestsFromTestCase(TestDocStrings))

    return test_suite


if __name__ == "__main__":

    suites = getTestSuite()
    r = unittest.TextTestRunner(failfast=False)
    ret = r.run(suites)
    assert ret.wasSuccessful()
    print("done")
