import os.path
import unittest

from textboxify import settings


class TestSettings(unittest.TestCase):

    def test_file_exists(self):
        self.assertTrue(os.path.isfile(settings.DEFAULT_CORNER))
        self.assertTrue(os.path.isfile(settings.DEFAULT_SIDE))
        self.assertTrue(os.path.isfile(settings.DEFAULT_INDICATOR))
        self.assertTrue(os.path.isfile(settings.DEFAULT_PORTRAIT))

    def test_path_exists(self):
        self.assertTrue(os.path.exists(settings.BASE_DIR))
        self.assertTrue(os.path.exists(settings.DATA_DIR))
        self.assertTrue(os.path.exists(settings.BORDER_DIR))
        self.assertTrue(os.path.exists(settings.INDICATOR_DIR))
        self.assertTrue(os.path.exists(settings.PORTRAIT_DIR))
        self.assertTrue(os.path.exists(settings.DEFAULT_CORNER))
        self.assertTrue(os.path.exists(settings.DEFAULT_SIDE))
        self.assertTrue(os.path.exists(settings.DEFAULT_INDICATOR))
        self.assertTrue(os.path.exists(settings.DEFAULT_PORTRAIT))

    def test_dir_names(self):
        self.assertEqual(os.path.basename(settings.BASE_DIR), "textboxify")
        self.assertEqual(os.path.basename(settings.DATA_DIR), "data")
        self.assertEqual(os.path.basename(settings.BORDER_DIR), "border")
        self.assertEqual(os.path.basename(settings.INDICATOR_DIR), "indicator")
        self.assertEqual(os.path.basename(settings.PORTRAIT_DIR), "portrait")

    def test_dir_paths(self):
        self.assertListEqual(settings.DATA_DIR.split("/")[-2:], ['textboxify', 'data'])
        self.assertListEqual(settings.BORDER_DIR.split("/")[-2:], ['data', 'border'])
        self.assertListEqual(settings.INDICATOR_DIR.split("/")[-2:], ['data', 'indicator'])
        self.assertListEqual(settings.PORTRAIT_DIR.split("/")[-2:], ['data', 'portrait'])

    def test_file_names(self):
        self.assertEqual(os.path.basename(settings.DEFAULT_CORNER), "corner.png")
        self.assertEqual(os.path.basename(settings.DEFAULT_SIDE), "side.png")
        self.assertEqual(os.path.basename(settings.DEFAULT_INDICATOR), "idle.png")
        self.assertEqual(os.path.basename(settings.DEFAULT_PORTRAIT), "placeholder.png")

    def test_file_paths(self):
        self.assertListEqual(settings.DEFAULT_CORNER.split("/")[-3:], ['border', 'default', 'corner.png'])
        self.assertListEqual(settings.DEFAULT_SIDE.split("/")[-3:], ['border', 'default', 'side.png'])
        self.assertListEqual(settings.DEFAULT_INDICATOR.split("/")[-2:], ['indicator', 'idle.png'])
        self.assertListEqual(settings.DEFAULT_PORTRAIT.split("/")[-2:], ['portrait', 'placeholder.png'])
