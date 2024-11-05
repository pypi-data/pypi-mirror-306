import unittest
from mmget.url import URLReader


class TestURLParser(unittest.TestCase):
    def test_valid_http_url(self):
        parser = URLReader("http://example.com/path?param=value")
        self.assertTrue(parser.is_valid)
        self.assertFalse(parser.is_dummy)
        self.assertEqual(parser.parsed_url.scheme, "http")
        self.assertEqual(parser.parsed_url.netloc, "example.com")
        self.assertEqual(parser.parsed_url.path, "/path")
        self.assertEqual(parser.query_params, {"param": "value"})

    def test_valid_https_url(self):
        parser = URLReader("https://example.com")
        self.assertTrue(parser.is_valid)
        self.assertFalse(parser.is_dummy)

    def test_valid_ftp_url(self):
        parser = URLReader("ftp://ftp.example.com/file.txt")
        self.assertTrue(parser.is_valid)
        self.assertFalse(parser.is_dummy)

    def test_valid_dummy_url(self):
        parser = URLReader("dummy://example.com/path?s=5")
        self.assertTrue(parser.is_valid)
        self.assertTrue(parser.is_dummy)
        self.assertEqual(parser.query_params, {"s": "5"})

    def test_invalid_scheme(self):
        parser = URLReader("invalid://example.com")
        self.assertFalse(parser.is_valid)
        self.assertFalse(parser.is_dummy)

    def test_missing_netloc(self):
        parser = URLReader("http:///path")
        self.assertFalse(parser.is_valid)

    def test_complex_url(self):
        parser = URLReader(
            "https://user:pass@example.com:8080/path/to/file.html?param1=value1&param2=value2#fragment"  # noqa
        )
        self.assertTrue(parser.is_valid)
        self.assertEqual(parser.parsed_url.scheme, "https")
        self.assertEqual(parser.parsed_url.netloc, "user:pass@example.com:8080")
        self.assertEqual(parser.parsed_url.path, "/path/to/file.html")
        self.assertEqual(
            parser.query_params, {"param1": "value1", "param2": "value2"}
        )
        self.assertEqual(parser.parsed_url.fragment, "fragment")

    def test_no_url(self):
        parser = URLReader("not-url")
        self.assertFalse(parser.is_valid)
        self.assertFalse(parser.is_dummy)
        self.assertEqual(parser.parsed_url.scheme, "")
        self.assertEqual(parser.parsed_url.netloc, "")
        self.assertEqual(parser.parsed_url.path, "not-url")
        self.assertEqual(parser.query_params, {})

    def test_empty_url(self):
        parser = URLReader("")
        self.assertFalse(parser.is_valid)
        self.assertFalse(parser.is_dummy)
        self.assertEqual(parser.parsed_url.scheme, "")
        self.assertEqual(parser.parsed_url.netloc, "")
        self.assertEqual(parser.parsed_url.path, "")
        self.assertEqual(parser.query_params, {})

    def test_url_with_only_scheme(self):
        parser = URLReader("http://")
        self.assertFalse(parser.is_valid)
        self.assertFalse(parser.is_dummy)
        self.assertEqual(parser.parsed_url.scheme, "http")
        self.assertEqual(parser.parsed_url.netloc, "")
        self.assertEqual(parser.parsed_url.path, "")
        self.assertEqual(parser.query_params, {})

    def test_huggingface_url(self):
        parser = URLReader(
            "https://huggingface.co/black-forest-labs/FLUX.1-dev/blob/main/model/flux1-dev.safetensors"  # noqa
        )
        self.assertTrue(parser.is_valid)
        self.assertTrue(parser.is_hf)
        self.assertEqual(parser.hf_repo_id, "black-forest-labs/FLUX.1-dev")
        self.assertEqual(parser.hf_filename, "model/flux1-dev.safetensors")

    def test_non_huggingface_url(self):
        parser = URLReader(
            "https://example.com/datasets/username/dataset/resolve/main/file.txt"
        )
        self.assertTrue(parser.is_valid)
        self.assertFalse(parser.is_hf)
        self.assertIsNone(parser.hf_repo_id)
        self.assertIsNone(parser.hf_filename)

    def test_invalid_huggingface_url(self):
        parser = URLReader("https://huggingface.co/invalid/path")
        self.assertTrue(parser.is_valid)
        self.assertTrue(parser.is_hf)
        self.assertIsNone(parser.hf_repo_id)
        self.assertIsNone(parser.hf_filename)


if __name__ == "__main__":
    unittest.main()
