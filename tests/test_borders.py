import os.path
import unittest

from textboxify.borders import DARK, LIGHT


class TestBorders(unittest.TestCase):

    def test_dir_names(self):
        self.assertEqual(os.path.split(os.path.dirname(DARK["corner"]))[1], "dark")
        self.assertEqual(os.path.split(os.path.dirname(DARK["side"]))[1], "dark")
        self.assertEqual(os.path.split(os.path.dirname(LIGHT["corner"]))[1], "light")
        self.assertEqual(os.path.split(os.path.dirname(LIGHT["side"]))[1], "light")

    def test_dark_path_exists(self):
        self.assertTrue(os.path.exists(DARK["corner"]))
        self.assertTrue(os.path.exists(DARK["side"]))

    def test_light_path_exists(self):
        self.assertTrue(os.path.exists(LIGHT["corner"]))
        self.assertTrue(os.path.exists(LIGHT["side"]))

    def test_dark_border_files_exists(self):
        self.assertTrue(os.path.isfile(DARK["corner"]))
        self.assertTrue(os.path.isfile(DARK["side"]))

    def test_light_border_files_exists(self):
        self.assertTrue(os.path.isfile(LIGHT["corner"]))
        self.assertTrue(os.path.isfile(LIGHT["side"]))
