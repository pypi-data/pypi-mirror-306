import unittest
from unittest.mock import Mock

from mmget.outputpathvalidator import OutputPathValidator
from mmget.tasks.taskfactory import TaskFactory
from mmget.tasks.civitaitask import CivitAITask
from mmget.tasks.dummytask import DummyTask
from mmget.tasks.huggingfacetask import HuggingFaceTask
from mmget.tasks.invalidtask import InvalidTask
from mmget.tasks.regularlinktask import RegularLinkTask


class TestTaskFactory(unittest.TestCase):
    def setUp(self):
        self.reporter = Mock()
        self.output_path = Mock()

    def test_create_invalid_task(self):
        task = TaskFactory.create(
            0, "invalid://url", self.reporter, self.output_path
        )
        self.assertIsInstance(task, InvalidTask)

    def test_create_invalid_task_with_invalid_path(self):
        output_path = OutputPathValidator(
            "directory-not-existed", dest_type="a1111"
        )
        task = TaskFactory.create(
            0, "dummy://file.txt", self.reporter, output_path
        )
        self.assertIsInstance(task, InvalidTask)
        self.assertEqual(
            task.error_message, "The output path is not a valid a1111 folder"
        )

    def test_create_dummy_task(self):
        task = TaskFactory.create(
            0, "dummy://file.txt", self.reporter, self.output_path
        )
        self.assertIsInstance(task, DummyTask)

    def test_create_civitai_task(self):
        task = TaskFactory.create(
            0,
            "https://civitai.com/models/1234",
            self.reporter,
            self.output_path,
            civitai_token="token123",
            version="v1",
        )
        self.assertIsInstance(task, CivitAITask)
        self.assertEqual(task.civitai_token, "token123")
        self.assertEqual(task.version, "v1")

    def test_create_huggingface_task(self):
        task = TaskFactory.create(
            0,
            "https://huggingface.co/model",
            self.reporter,
            self.output_path,
            hf_token="token456",
        )
        self.assertIsInstance(task, HuggingFaceTask)
        self.assertEqual(task.hf_token, "token456")

    def test_create_regular_link_task(self):
        task = TaskFactory.create(
            0, "https://example.com/file.txt", self.reporter, self.output_path
        )
        self.assertIsInstance(task, RegularLinkTask)
