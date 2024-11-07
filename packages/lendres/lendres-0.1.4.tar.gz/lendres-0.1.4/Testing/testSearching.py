"""
Created on Febuary 16, 2022
@author: Lance A. Endres
"""
import numpy                                                    as np

from   lendres.algorithms.Search                                import Search
import unittest

# More information at:
# https://docs.python.org/3/library/unittest.html

class TestBoundingBinarySearch(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.points = [1, 3, 5, 8, 11, 14, 18, 22]

    def testIndicesFirstHalf(self):
        result = Search.BoundingBinarySearch(2, self.points, returnedUnits="indices")
        self.assertEqual(result[0], 0)
        self.assertEqual(result[1], 1)


    def testIndicesSecondHalf(self):
        result = Search.BoundingBinarySearch(16, self.points, returnedUnits="indices")
        self.assertEqual(result[0], 5)
        self.assertEqual(result[1], 6)


    def testIndicesOnAPoint(self):
        result = Search.BoundingBinarySearch(5, self.points, returnedUnits="indices")
        self.assertEqual(result[0], 2)
        self.assertEqual(result[1], 2)


    def testValues(self):
        result = Search.BoundingBinarySearch(2, self.points, returnedUnits="values")
        self.assertEqual(result[0], 1)
        self.assertEqual(result[1], 3)


    def testValueTooLow(self):
        result = Search.BoundingBinarySearch(-2, self.points, returnedUnits="values")
        self.assertTrue(result[0] is np.nan)
        self.assertTrue(result[1] is np.nan)


    def testValueTooHigh(self):
        result = Search.BoundingBinarySearch(10000, self.points, returnedUnits="values")
        self.assertTrue(result[0] is np.nan)
        self.assertTrue(result[1] is np.nan)



class TestFindIndicesByValues(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        #                0    1    2    3    4    5    6    7    8    9   10   11   12
        cls.numbers = [  1,   3,  11,  11,   5,   8,   5,  11,  14,  18,  22,   3,   3]
        cls.strings = ["a", "b", "c", "b", "b", "d", "d", "e", "a", "a", "b", "b", "b"]


    def testFindNumbers(self):
        result = Search.FindIndicesByValues(self.numbers, 3)
        self.assertEqual(result[0], 1)
        self.assertEqual(len(result), 3)


    def testFindStrings(self):
        result = Search.FindIndicesByValues(self.strings, "b")
        self.assertEqual(result[5], 12)
        self.assertEqual(len(result), 6)


    def testFindMaxCount(self):
        result = Search.FindIndicesByValues(self.strings, "b", maxCount=4)
        self.assertEqual(result[3], 10)
        self.assertEqual(len(result), 4)


if __name__ == "__main__":
    unittest.main()