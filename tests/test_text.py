import unittest

import pygame

from textboxify.text import Text


class TestText(unittest.TestCase):
    def setUp(self):
        pygame.font.init()
        pygame.display.init()
        pygame.display.set_mode((1, 1))
        self.font_size = 1
        self.message = "TESTING"
        self.text = Text(self.message, size=self.font_size)

    def test_get_position(self):
        self.assertTupleEqual(self.text.position, (0, 0))

    def test_set_position(self):
        self.text.position = (10, 10)
        self.assertTupleEqual(self.text.position, (10, 10))

    def test_get_linesize(self):
        linesize = pygame.font.Font(None, self.font_size).get_linesize()
        self.assertEqual(self.text.linesize, linesize)

    def test_get_size(self):
        font = pygame.font.Font(None, self.font_size)
        image = font.render(self.message, 1, (255, 255, 255), None)
        rect = image.get_rect()
        self.assertTupleEqual(self.text.size, rect.size)
        self.assertEqual(self.text.width, rect.width)
        self.assertEqual(self.text.height, rect.height)
