from mmget.tasks.civitaitask import CivitAITask
from mmget.tasks.dummytask import DummyTask
from mmget.tasks.huggingfacetask import HuggingFaceTask
from mmget.tasks.invalidtask import InvalidTask
from mmget.tasks.regularlinktask import RegularLinkTask
from mmget.url import URLReader


class TaskFactory:
    @staticmethod
    def create(
        id,
        url: str,
        reporter,
        output_path,
        hf_token=None,
        civitai_token=None,
        version=None,
    ):
        parser = URLReader(url)
        args = [id, url]
        kwargs = {"reporter": reporter, "output_path": output_path}
        if not parser.is_valid:
            task = InvalidTask(*args, **kwargs, error_message="Invalid URL")
        elif not output_path.is_valid:
            task = InvalidTask(
                *args, **kwargs, error_message=output_path.error_message
            )
        elif parser.is_dummy:
            task = DummyTask(*args, **kwargs)
        elif parser.is_civitai:
            task = CivitAITask(
                *args, **kwargs, civitai_token=civitai_token, version=version
            )
        elif parser.is_hf:
            task = HuggingFaceTask(*args, **kwargs, hf_token=hf_token)
        else:
            task = RegularLinkTask(*args, **kwargs)
        return task
