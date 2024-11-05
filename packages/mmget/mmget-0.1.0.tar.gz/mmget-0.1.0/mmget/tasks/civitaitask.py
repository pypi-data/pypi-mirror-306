import asyncio
import requests
import re
import os
from enum import Enum

from mmget.partedfilewriter import PartedFileWriter
from mmget.types import DistType
from mmget.url import HeaderReader
from mmget.tasks.task import Task
from mmget.errors import NetworkError
from mmget.reporters.reporter import ReporterItemState


class CivitaiAIModelType(str, Enum):
    Checkpoint = "Checkpoint"
    Lora = "LORA"
    TextualInversion = "TextualInversion"
    VAE = "VAE"


class SoftwareType(str, Enum):
    A1111 = "a1111"
    ComfyUI = "comfyui"


class ComfyUIPaths:
    @staticmethod
    def resolve(base_path: str, type: str):
        mapping = {
            CivitaiAIModelType.Checkpoint.value: "checkpoints",
            CivitaiAIModelType.Lora.value: "loras",
            CivitaiAIModelType.VAE.value: "vae",
            CivitaiAIModelType.TextualInversion.value: "embeddings",
        }
        return (
            os.path.join(base_path, "models", mapping[type])
            if type in mapping
            else base_path
        )


class A1111Paths:
    @staticmethod
    def resolve(base_path: str, type: str):
        mapping = {
            CivitaiAIModelType.Checkpoint.value: "Stable-diffusion",
            CivitaiAIModelType.Lora.value: "Lora",
            CivitaiAIModelType.VAE.value: "VAE",
            CivitaiAIModelType.TextualInversion.value: "embeddings",
        }
        return (
            os.path.join(base_path, "models", mapping[type])
            if type in mapping
            else base_path
        )


class CivitAIAPIClient:
    def __init__(self, token=None):
        self.host = "https://civitai.com/"
        self.token = token

    def get_model_id_from_url(self, model_url):
        text = model_url.replace("https://civitai.com/models/", "")
        pattern = re.compile(r"(\d+)")
        model_id = pattern.search(text).group()
        return model_id

    def get_model_json_url_from_id(self, model_id):
        return f"{self.host}/api/v1/models/{model_id}"

    def request_model_metadata(self, model_url):
        model_id = self.get_model_id_from_url(model_url)
        url = self.get_model_json_url_from_id(model_id)
        res = requests.get(url)
        if res.status_code != 200:
            raise NetworkError(res.text)
        return res.json()

    def normalize_download_url(self, url):
        if self.token and self.token.strip():
            url = f"{url}?token={self.token.strip()}"
        return url


class CivitAIMetadataReader:
    def __init__(self, model_info):
        self.model_info = model_info

    def find_latest_model_version_name(self):
        if not self.model_info or "modelVersions" not in self.model_info:
            return None

        latest_version = max(
            self.model_info["modelVersions"],
            key=lambda version: version.get("createdAt", ""),
        )
        return latest_version.get("name")

    def has_version(self, version: str):
        if not self.model_info or "modelVersions" not in self.model_info:
            return False

        return any(
            item["name"] == version for item in self.model_info["modelVersions"]
        )

    def get_model_versions(self):
        return [m["name"] for m in self.model_info["modelVersions"]]

    def get_model_version(self, selected_model_version):
        return next(
            modelVersionData
            for modelVersionData in self.model_info["modelVersions"]
            if modelVersionData["name"] == selected_model_version
        )

    def get_model_version_download_url(self, selected_model_version):
        return self.get_model_version(selected_model_version)["downloadUrl"]

    def get_model_version_image_url(self, selected_model_version):
        images = self.get_model_version(selected_model_version)["images"]
        if len(images) == 0:
            return None
        return images[0]["url"]

    def get_model_type(self):
        return self.model_info["type"]


class CivitAITask(Task):
    def __init__(
        self, id, url, reporter, output_path, civitai_token=None, version=None
    ):
        super().__init__(id, url, reporter, output_path)
        self.civitai_token = civitai_token
        self.version = version

    def worker(self, options):
        metadata = options.get("metadata", None)
        version = (
            self.version
            if self.version is not None
            else options.get("version", None)
        )

        try:
            api_client = CivitAIAPIClient(token=self.civitai_token)

            if metadata is None:
                self.reporter.set_title(self.id, self.url)
                metadata = api_client.request_model_metadata(self.url)

            reader = CivitAIMetadataReader(metadata)
            model_versions = reader.get_model_versions()

            if version is not None and not reader.has_version(version):
                self.reporter.set_error(
                    self.id, f"{self.version} not available"
                )
                self.future.set_result(None)
                return

            if len(model_versions) > 1 and version is None:
                if self.reporter.can_ask_options():

                    def on_option_selected(value):
                        new_options = {
                            **(options or {}),
                            "metadata": metadata,
                            "version": value,
                        }
                        self.run(new_options)

                    self.reporter.ask_options(
                        self.id,
                        "Select a version",
                        model_versions,
                        on_option_selected,
                    )
                else:
                    self.reporter.show_message(
                        self.id,
                        (
                            f"Multiple model versions available: {model_versions}. "
                            "Please specify which version to download using "
                            "the `version` parameter."
                        ),
                    )
                    self.future.set_result(None)
                return

            if version is None and len(model_versions) == 1:
                version = model_versions[0]
            download_url = reader.get_model_version_download_url(version)
            download_url = api_client.normalize_download_url(download_url)
            model_type = reader.get_model_type()

            response = requests.get(download_url, stream=True)
            response.raise_for_status()

            output = self.output_path.absolute_path

            if self.output_path.is_directory:
                header_reader = HeaderReader(response.headers, self.url)
                filename = header_reader.get_filename()
                if self.output_path.dest_type == DistType.A1111.value:
                    output = os.path.join(
                        A1111Paths.resolve(output, model_type), filename
                    )
                elif self.output_path.dest_type == DistType.ComfyUI.value:
                    output = os.path.join(
                        ComfyUIPaths.resolve(output, model_type), filename
                    )
                else:
                    output = os.path.join(output, filename)
            self.reporter.set_title(self.id, os.path.basename(output))

            file_manager = PartedFileWriter.get_instance()

            with file_manager.open(output) as file:
                file_manager.transfer_response_to_file(
                    response,
                    file,
                    self.id,
                    self.reporter,
                )
            self.future.set_result(None)
        except Exception as e:
            exception = e
            error_message = str(exception)
            self.reporter.set_error(self.id, error_message)
            self.future.set_result(exception)

    def run(self, options=None) -> "asyncio.Future":
        options = options or {}

        self.reporter.set_state(self.id, ReporterItemState.Pending)
        self.submit_worker(self.worker, options)
        return self.future
