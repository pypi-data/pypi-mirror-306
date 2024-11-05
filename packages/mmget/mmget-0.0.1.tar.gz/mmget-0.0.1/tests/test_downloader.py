import unittest
import os
from mmget.downloader import Downloader


class TestDownloader(unittest.TestCase):
    def setUp(self):
        self.downloader = Downloader()

    def test_dl_adds_task(self):
        self.downloader.dl("dummy://test.txt")
        self.assertEqual(len(self.downloader.tasks), 1)

    def test_dl_chainable(self):
        result = self.downloader.dl("dummy://test1.txt").dl("dummy://test2.txt")
        self.assertEqual(len(self.downloader.tasks), 2)
        self.assertEqual(result, self.downloader)

    def test_dl_with_path(self):
        self.downloader.dl("dummy://test.txt", "test_path")
        self.assertEqual(len(self.downloader.tasks), 1)
        task = self.downloader.tasks[0]
        self.assertEqual(
            task.output_path.absolute_path, os.path.abspath("test_path")
        )

    def test_dl_with_dist_type(self):
        self.downloader.dl("dummy://test.txt", dest_type="a1111")
        self.assertEqual(len(self.downloader.tasks), 1)
        task = self.downloader.tasks[0]
        self.assertEqual(task.output_path.dest_type, "a1111")

    def test_create_tasks_twice_not_allowed(self):
        self.downloader.dl("dummy://test.txt?s=1")
        self.downloader.create_tasks()
        with self.assertRaises(RuntimeError):
            self.downloader.create_tasks()
