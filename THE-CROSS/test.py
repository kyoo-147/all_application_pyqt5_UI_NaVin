import unittest
import cv2

import ImageDetector
import ImageUtils


class Test_ImageUtils(unittest.TestCase):

    def test_resizeCVIMG(self):
        # Preparing images for Unit Test
        test_img = cv2.imread('Images/camera_no_signal.png')

        # Test Method
        test_img = ImageUtils.resizeCVIMG(test_img)
        _, result, __ = test_img.shape

        # Evaluation : width of Resized image must be 150
        expect = 150
        self.assertEqual(expect, result)

    def test_sort_rectPos(self):
        # Preparing Spots of Square
        test_square_spots = [[30, 30],
                             [0, 30],
                             [0, 0],
                             [30, 50]]

        # Test Method
        result = ImageUtils.sort_rectPos(test_square_spots)

        # Evaluation : Sorted Spots ( = Arrange the square dots counterclockwise )
        expect = [2, 1, 3, 0]

        self.assertListEqual(expect, result)

    def test_isOneSpotInRect(self):
        # Preparing Spots of Square
        test_square_spots_1 = [[0, 0],
                               [0, 100],
                               [100, 100],
                               [100, 0]]

        test_square_spots_2 = [[0, 0],
                               [0, 30],
                               [30, 30],
                               [30, 50]]

        # Preparing Dot Spots
        test_dots = [[[50, 50]], [[30, 50]], [[0, 50]], [[200, 50]]]

        # Test Method
        result_1_1 = ImageUtils.isAnyObjectInRect(test_square_spots_1, test_dots[0], False)
        result_1_2 = ImageUtils.isAnyObjectInRect(test_square_spots_1, test_dots[1], False)
        result_1_3 = ImageUtils.isAnyObjectInRect(test_square_spots_1, test_dots[2], False)
        result_1_4 = ImageUtils.isAnyObjectInRect(test_square_spots_1, test_dots[3], False)

        result_2_1 = ImageUtils.isAnyObjectInRect(test_square_spots_2, test_dots[0], False)
        result_2_2 = ImageUtils.isAnyObjectInRect(test_square_spots_2, test_dots[1], False)
        result_2_3 = ImageUtils.isAnyObjectInRect(test_square_spots_2, test_dots[2], False)
        result_2_4 = ImageUtils.isAnyObjectInRect(test_square_spots_2, test_dots[3], False)

        # Evaluation
        expect_1_1 = True  # (50,50) must be in the Rect
        expect_1_2 = True  # (30,50) must be in the rect
        expect_1_3 = False  # (0, 50) must be on the rect boundary
        expect_1_4 = False  # (200, 50) must be out of the rect

        expect_2_1 = False  # (50,50) must be out of the square
        expect_2_2 = False  # (30,50) must be on the square boundary
        expect_2_3 = False  # (0,50) must be out of the square
        expect_2_4 = False  # (200,50) must be out of the square

        self.assertEqual(expect_1_1, result_1_1)
        self.assertEqual(expect_1_2, result_1_2)
        self.assertEqual(expect_1_3, result_1_3)
        self.assertEqual(expect_1_4, result_1_4)

        self.assertEqual(expect_2_1, result_2_1)
        self.assertEqual(expect_2_2, result_2_2)
        self.assertEqual(expect_2_3, result_2_3)
        self.assertEqual(expect_2_4, result_2_4)


class Test_Detector(unittest.TestCase):

    def test_Detector(self):
        # Preparing images for Unit Test
        testImg = cv2.imread('Images/Test/test_detector.png')

        # Test Method
        pos_result = ImageDetector.Detector(testImg)
        result = len(pos_result)

        # Evaluation : Detector must find 2 people
        expect = 2

        self.assertEqual(expect, result)

    def test_CustomDetector(self):
        # Preparing images for Unit Test
        testImg = cv2.imread('Images/Test/test_custom_detector.jpg')

        # Test Method
        pos_result = ImageDetector.CustomDetector(testImg)
        result = len(pos_result[0])
        print(pos_result[0])

        # Evaluation : Custom Detector must find 1 wheelchair
        expect = 1

        self.assertEqual(expect, result)
