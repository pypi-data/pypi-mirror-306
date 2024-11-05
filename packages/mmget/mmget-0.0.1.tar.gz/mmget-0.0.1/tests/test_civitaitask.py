import unittest
from unittest.mock import patch, MagicMock
from mmget.tasks.civitaitask import CivitAITask
from mmget.outputpathvalidator import OutputPathValidator


class TestCivitAITask(unittest.TestCase):
    def setUp(self):
        self.output_path = OutputPathValidator(".")
        self.reporter = MagicMock()
        self.task = CivitAITask(
            1,
            "https://civitai.com/models/1234",
            self.reporter,
            self.output_path,
        )

    def test_initialization(self):
        self.assertEqual(self.task.id, 1)
        self.assertEqual(self.task.url, "https://civitai.com/models/1234")
        self.assertIsNotNone(self.task.reporter)
        self.assertEqual(self.task.output_path, self.output_path)

    @patch("mmget.tasks.civitaitask.CivitAITask.submit_worker")
    def test_run_submits_worker(self, mock_submit):
        self.task.run()
        mock_submit.assert_called_once()
        self.assertIsNotNone(self.task.future)

    @patch("requests.get")
    @patch("mmget.partedfilewriter.PartedFileWriter")
    def test_worker_handle_single_version(self, mock_writer, mock_get):
        options = {
            "metadata": {
                "modelVersions": [
                    {
                        "name": "v1.0",
                        "downloadUrl": "https://example.com/model.safetensors",
                        "images": [],
                    }
                ],
                "type": "Checkpoint",
            }
        }

        mock_response = MagicMock()
        mock_response.headers = {
            "content-disposition": "attachment; filename=model.safetensors"
        }
        mock_get.return_value = mock_response
        self.task.worker(options)
        mock_get.assert_called_once_with(
            "https://example.com/model.safetensors", stream=True
        )
