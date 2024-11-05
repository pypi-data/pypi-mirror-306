import os
import unittest
from mmget.outputpathvalidator import OutputPathValidator


class TestOutputPathValidator(unittest.TestCase):
    def test_default_path(self):
        validator = OutputPathValidator(None)
        self.assertEqual(validator.absolute_path, os.path.abspath(os.getcwd()))
        self.assertTrue(validator.is_valid)

    def test_valid_dist_type(self):
        validator = OutputPathValidator(".", dest_type="a1111")
        self.assertTrue(validator.is_valid)
        self.assertEqual(validator.dest_type, "a1111")

    def test_invalid_dist_type(self):
        validator = OutputPathValidator(".", dest_type="invalid")
        self.assertFalse(validator.is_valid)

    def test_directory_check(self):
        validator = OutputPathValidator(".")
        self.assertTrue(validator.is_directory)
        self.assertTrue(validator.is_exists)

    def test_nonexistent_path(self):
        validator = OutputPathValidator("nonexistent_path")
        self.assertFalse(validator.is_exists)
        self.assertFalse(validator.is_directory)

    def test_dist_type_set_but_output_is_not_existed(self):
        validator = OutputPathValidator("file-not-existed", dest_type="a1111")
        self.assertFalse(validator.is_exists)
        self.assertFalse(validator.is_valid)
