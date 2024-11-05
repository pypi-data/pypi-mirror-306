import unittest
from unittest.mock import patch
from mmget.downloadspeedestimator import DownloadSpeedEstimator


class TestDownloadSpeedEstimator(unittest.TestCase):
    def setUp(self):
        self.estimator = DownloadSpeedEstimator()

    def test_add_first_progress(self):
        self.estimator.add(10)
        self.assertIsNotNone(self.estimator.start_time)
        self.assertEqual(len(self.estimator.records), 1)
        self.assertEqual(self.estimator.records[0].progress, 10)

    @patch("time.time", side_effect=[1000, 1000.3, 1000.5, 1003])
    def test_add_progress_within_threshold(self, mock_time):
        self.estimator.add(10)
        initial_time = self.estimator.records[0].time
        self.estimator.add(20)
        self.estimator.add(30)
        self.assertEqual(len(self.estimator.records), 2)
        self.assertEqual(self.estimator.records[0].progress, 10)
        self.assertEqual(self.estimator.records[0].time, initial_time)
        self.assertEqual(self.estimator.records[1].progress, 30)
        self.assertEqual(self.estimator.records[1].time, 1000.5)
        self.estimator.add(40)
        self.assertEqual(len(self.estimator.records), 3)

    @patch("time.time", side_effect=[1000, 1001.1])
    def test_eta_calculation(self, mock_time):
        self.estimator.add(10)
        self.estimator.add(20)
        self.assertIsNotNone(self.estimator.eta)
        self.assertAlmostEqual(self.estimator.eta, 8.8, places=1)

    def test_completion(self):
        self.estimator.add(100)
        self.assertEqual(self.estimator.eta, 0)
        self.assertIsNotNone(self.estimator.completed_time)

    def test_get_formatted_eta(self):
        self.estimator.eta = 3661  # 1 hour, 1 minute, and 1 second
        self.assertEqual(self.estimator.get_formatted_eta(), "01:01:01")
        self.estimator.eta = 61  # 1 minute and 1 second
        self.assertEqual(self.estimator.get_formatted_eta(), "01:01")
        self.estimator.eta = 59  # 59 seconds
        self.assertEqual(self.estimator.get_formatted_eta(), "00:59")
