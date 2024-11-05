from mmget.reporters.ipyreporter import create_ipyreportor
from mmget.reporters.printreporter import PrintReporter


def is_jupyter_environment():
    """
    Check if the code is running inside a Jupyter notebook.

    Returns:
        bool: True if running in Jupyter, False otherwise.
    """
    try:
        from IPython import get_ipython

        if get_ipython() is not None:
            return True
        return False
    except ImportError:
        return False


def has_ipywidget_installed():
    try:
        import ipywidgets  # noqa

        return True
    except ImportError:
        return False


class ReporterFactory:
    @staticmethod
    def create():
        return (
            create_ipyreportor()
            if (is_jupyter_environment() and has_ipywidget_installed())
            else PrintReporter()
        )
