import os.path
import unittest

import textboxify
from textboxify.borders import *


class TestBorders(unittest.TestCase):

    def test_that_borders_have_tests(self):

        # Currently tested borders.
        # Append name of border to the list when tests are written for it.
        tested_borders = ["DEFAULT", "DARK", "LIGHT", "BLINK", "BARBER_POLE"]

        # All existing borders included in the package.
        self.all_borders = []

        for border in dir(textboxify.borders):
            if not border.startswith("__") and border.isupper():
                self.all_borders.append(border)

        # Exclude imported variable from settings.
        self.all_borders.remove("BORDER_DIR")

        for border in self.all_borders:
            self.assertIn(border, tested_borders)

    def test_dir_names(self):

        self.assertEqual(os.path.split(os.path.dirname(DEFAULT["corner"]))[1], "default")
        self.assertEqual(os.path.split(os.path.dirname(DEFAULT["side"]))[1], "default")

        self.assertEqual(os.path.split(os.path.dirname(DARK["corner"]))[1], "dark")
        self.assertEqual(os.path.split(os.path.dirname(DARK["side"]))[1], "dark")

        self.assertEqual(os.path.split(os.path.dirname(LIGHT["corner"]))[1], "light")
        self.assertEqual(os.path.split(os.path.dirname(LIGHT["side"]))[1], "light")

        self.assertEqual(os.path.split(os.path.dirname(BLINK["corner"]))[1], "blink")
        self.assertEqual(os.path.split(os.path.dirname(BLINK["side"]))[1], "blink")

        self.assertEqual(os.path.split(os.path.dirname(BARBER_POLE["corner"]))[1], "barber_pole")
        self.assertEqual(os.path.split(os.path.dirname(BARBER_POLE["side"]))[1], "barber_pole")

    def test_path_exists(self):

        self.assertTrue(os.path.exists(DEFAULT["corner"]))
        self.assertTrue(os.path.exists(DEFAULT["side"]))

        self.assertTrue(os.path.exists(DARK["corner"]))
        self.assertTrue(os.path.exists(DARK["side"]))

        self.assertTrue(os.path.exists(LIGHT["corner"]))
        self.assertTrue(os.path.exists(LIGHT["side"]))

        self.assertTrue(os.path.exists(BLINK["corner"]))
        self.assertTrue(os.path.exists(BLINK["side"]))

        self.assertTrue(os.path.exists(BARBER_POLE["corner"]))
        self.assertTrue(os.path.exists(BARBER_POLE["side"]))

    def test_border_files_exists(self):
        self.assertTrue(os.path.isfile(DEFAULT["corner"]))
        self.assertTrue(os.path.isfile(DEFAULT["side"]))

        self.assertTrue(os.path.isfile(DARK["corner"]))
        self.assertTrue(os.path.isfile(DARK["side"]))

        self.assertTrue(os.path.isfile(LIGHT["corner"]))
        self.assertTrue(os.path.isfile(LIGHT["side"]))

        self.assertTrue(os.path.isfile(BLINK["corner"]))
        self.assertTrue(os.path.isfile(BLINK["side"]))

        self.assertTrue(os.path.isfile(BARBER_POLE["corner"]))
        self.assertTrue(os.path.isfile(BARBER_POLE["side"]))

    def test_border_size(self):
        self.assertListEqual(DEFAULT["size"], [10, 10])
        self.assertListEqual(DARK["size"], [10, 10])
        self.assertListEqual(LIGHT["size"], [5, 5])
        self.assertListEqual(BLINK["size"], [15, 15])
        self.assertListEqual(BARBER_POLE["size"], [20, 20])

    def test_border_colorkey(self):
        self.assertIsNone(DEFAULT["colorkey"], (0, 255, 38))
        self.assertTupleEqual(DARK["colorkey"], (0, 255, 38))
        self.assertTupleEqual(LIGHT["colorkey"], (0, 255, 38))
        self.assertTupleEqual(BLINK["colorkey"], (11, 219, 6))
        self.assertTupleEqual(BARBER_POLE["colorkey"], (11, 219, 6))

    def test_border_animate_boolean_value(self):
        self.assertFalse(DEFAULT["animate"])
        self.assertFalse(DARK["animate"])
        self.assertFalse(LIGHT["animate"])
        self.assertTrue(BLINK["animate"])
        self.assertTrue(BARBER_POLE["animate"])
