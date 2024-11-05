import os
from urllib.parse import parse_qsl, urlparse
from email.message import Message


class URLReader:
    def __init__(self, url):
        self.url = url
        self.parsed_url = urlparse(url)
        self.query_params = dict(parse_qsl(self.parsed_url.query))
        self.is_valid = self._validate_url()
        self.is_dummy = self.parsed_url.scheme == "dummy"
        self.is_civitai = self.parsed_url.netloc == "civitai.com"
        self.is_hf = self.parsed_url.netloc == "huggingface.co"
        self._parse_hf_url()

    def _validate_url(self):
        """Validate the URL based on its scheme and structure."""
        valid_schemes = ["http", "https", "ftp", "dummy"]
        if self.parsed_url.scheme not in valid_schemes:
            return False
        if not self.parsed_url.netloc:
            return False
        return True

    def _parse_hf_url(self):
        self.hf_repo_id = None
        self.hf_filename = None
        self.hf_revision = None

        # Link copied from huggingface web site:
        # https://huggingface.co/google-t5/t5-small/blob/main/README.md

        # Link to download the file:
        # https://huggingface.co/google-t5/t5-small/resolve/main/README.md

        try:
            if self.is_hf:
                path_parts = self.parsed_url.path.strip("/").split("/")
                if len(path_parts) >= 3:
                    self.hf_repo_id = "/".join(path_parts[0:2])
                    remaining = path_parts[2:]
                    remaining.pop(0)
                    self.hf_revision = remaining.pop(0)
                    self.hf_filename = "/".join(remaining)
        except Exception:
            self.hf_filename = None
            self.hf_repo_id = None
            self.hf_revision = None
            self.is_hf = False


class HeaderReader:
    def __init__(self, headers, url):
        self.headers = headers
        self.url = url

    def _get_filename_from_cd(self, cd):
        """
        Get filename from content-disposition
        """
        message = Message()
        message["content-disposition"] = cd
        return message.get_filename()

    def get_filename(self):
        cd = self.headers.get("Content-Disposition")
        if cd is None:
            return os.path.basename(self.url)
        filename = self._get_filename_from_cd(cd)
        if filename is None:
            return os.path.basename(self.url)
        return filename
