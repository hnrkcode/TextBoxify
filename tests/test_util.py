import unittest

import pygame

from textboxify import settings, util


class TestLoadImage(unittest.TestCase):

    def setUp(self):
        pygame.display.init()
        pygame.display.set_mode((1, 1))

    def test_load_image_none_existing_file(self):

        fakefile = "fakefile.png"

        with self.assertRaises(SystemExit) as err:
            util.load_image(fakefile)

        message = f"load_image: Couldn't open {fakefile}"
        self.assertEqual(err.exception.code, message)

    def test_load_image_empty_string(self):

        with self.assertRaises(SystemExit) as err:
            util.load_image("")

        message = "load_image: SDL_RWFromFile(): No file or no mode specified"
        self.assertEqual(err.exception.code, message)

    def test_load_image_set_colorkey(self):
        colorkey = (0, 0, 0)
        test = util.load_image(settings.DEFAULT_PORTRAIT, colorkey)
        self.assertTupleEqual(test.get_colorkey(), (0, 0, 0, 255))

    def test_load_image_colorkey_none(self):
        test = util.load_image(settings.DEFAULT_PORTRAIT)
        self.assertEqual(test.get_colorkey(), None)


class TestSpriteSlice(unittest.TestCase):

    def setUp(self):
        self.w, self.h = util.load_image(settings.DEFAULT_PORTRAIT).get_size()

    def test_number_slices_from_image(self):
        frames = len(util.sprite_slice(settings.DEFAULT_PORTRAIT, (50, 50)))
        self.assertEqual(frames, self.w // 50)

    def test_scale_size_with_ints(self):
        scale = (100, 100)
        frames = util.sprite_slice(settings.DEFAULT_PORTRAIT, (50, 50), scale=scale)

        for frame in frames:
            self.assertTupleEqual(frame.get_size(), scale)

    def test_scale_size_with_floats(self):
        scale = (13.6, 10.6)
        frames = util.sprite_slice(settings.DEFAULT_PORTRAIT, (50, 50), scale=scale)

        for frame in frames:
            size = int(scale[0]), int(scale[1])
            self.assertTupleEqual(frame.get_size(), size)


class TestAnimateSprite(unittest.TestCase):

    def setUp(self):

        self.fps = 30
        self.delay = 1
        self.obj = util.AnimateSprite(fps=self.fps, delay=self.delay)

    def test_images_is_none(self):
        self.assertIsNone(self.obj._images)

    def test_fps_is_set_with_argument_value(self):
        self.assertEqual(self.obj._fps, self.fps)

    def test_delay_is_set_with_argument_values_quotient(self):
        self.assertEqual(self.obj._delay, self.delay / self.fps)

    def test_last_update_is_set_to_zero(self):
        self.assertEqual(self.obj._last_update, 0)

    def test_frame_is_set_to_zero(self):
        self.assertEqual(self.obj._frame, 0)

    def test_animate_method(self):
        self.obj._images = [i for i in range(1234)]

        for i in range(10):
            current_frame = self.obj._frame
            self.obj.animate(i)

            if i - self.obj._last_update > self.obj._delay:
                self.assertNotEqual(current_frame, self.obj._frame)

            if self.obj._frame >= len(self.obj._images):
                self.assertEqual(self.obj._frame, 0)

            self.assertEqual(i, self.obj._last_update)


class TestCustomSprite(unittest.TestCase):

    def setUp(self):
        self.w, self.h = (50, 50)
        self.sprite = util.CustomSprite(settings.DEFAULT_PORTRAIT, (self.w, self.h), delay=0.001)

    def test_that_animate_loop_frames(self):

        for i in range(len(self.sprite._images) * 3):
            pygame.time.Clock().tick(60)
            self.assertIs(self.sprite.image, self.sprite._images[self.sprite._frame])
            self.sprite.animate(pygame.time.get_ticks())

    def test_width(self):
        self.assertEqual(self.sprite.width, self.w)

    def test_height(self):
        self.assertEqual(self.sprite.height, self.h)
