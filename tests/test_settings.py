import os.path
import unittest

from textboxify import settings


class TestSettings(unittest.TestCase):

    def test_file_exists(self):
        self.assertTrue(os.path.isfile(settings.DEFAULT_INDICATOR["file"]))
        self.assertTrue(os.path.isfile(settings.DEFAULT_PORTRAIT["file"]))

    def test_path_exists(self):
        self.assertTrue(os.path.exists(settings.BASE_DIR))
        self.assertTrue(os.path.exists(settings.DATA_DIR))
        self.assertTrue(os.path.exists(settings.BORDER_DIR))
        self.assertTrue(os.path.exists(settings.INDICATOR_DIR))
        self.assertTrue(os.path.exists(settings.PORTRAIT_DIR))
        self.assertTrue(os.path.exists(settings.DEFAULT_INDICATOR["file"]))
        self.assertTrue(os.path.exists(settings.DEFAULT_PORTRAIT["file"]))

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
        self.assertEqual(os.path.basename(settings.DEFAULT_INDICATOR["file"]), "idle.png")
        self.assertEqual(os.path.basename(settings.DEFAULT_PORTRAIT["file"]), "placeholder.png")

    def test_file_paths(self):
        self.assertEqual(os.path.split(os.path.dirname(settings.DEFAULT_INDICATOR["file"]))[1], "indicator")
        self.assertEqual(os.path.split(os.path.dirname(settings.DEFAULT_PORTRAIT["file"]))[1], "portrait")
