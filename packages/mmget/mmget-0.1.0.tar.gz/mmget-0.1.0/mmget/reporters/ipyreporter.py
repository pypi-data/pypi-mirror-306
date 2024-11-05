from typing import Union
from mmget.formatter import Formatter
from mmget.downloadspeedestimator import DownloadSpeedEstimator
import asyncio
from mmget.reporters.reporter import Reporter, ReporterItemState


class ReportItem:
    def __init__(
        self,
        title,
        progress_bar,
        message,
        dropdown,
        dropdown_hbox,
        dropdown_confirm_button,
        dropdown_label,
        speed_estimator,
        state,
    ):
        self.title = title
        self.progress_bar = progress_bar
        self.message = message
        self.dropdown = dropdown
        self.dropdown_hbox = dropdown_hbox
        self.dropdown_confirm_button = dropdown_confirm_button
        self.dropdown_label = dropdown_label
        self.speed_estimator = speed_estimator
        self.state = state


def create_ipyreportor():
    import ipywidgets as widgets
    from IPython.display import display

    class IPYReporter(Reporter):
        def __init__(self):
            self.status_bar = widgets.HTML(
                value="<b>Status:</b> Initializing..."
            )
            self.rows = []
            self.progress_list = widgets.VBox()
            self.main_container = widgets.VBox(
                [self.status_bar, self.progress_list],
                layout=widgets.Layout(padding="4px", min_height="200px"),
            )
            self.display_handle = None
            self._timer_task = None

        def add_report_item(self) -> int:
            id = len(self.rows)
            title = widgets.Label(
                f"{id}",
                layout=widgets.Layout(
                    width="auto",
                    margin="0px",
                    padding="0px",
                    min_height="22px",
                    align_items="center",
                ),
            )
            progress_bar = widgets.FloatProgress(
                value=0,
                min=0,
                max=100,
                description="",
                bar_style="info",
                style={"description_width": "initial"},
                orientation="horizontal",
                layout=widgets.Layout(
                    width="auto", margin="0px", padding="0px", height="20px"
                ),
            )
            message = widgets.HTML(
                "",
                layout=widgets.Layout(
                    height="20px",
                    margin="0px",
                    padding="0px",
                    align_items="center",
                    justify_content="center",
                ),
            )
            message.style = {"font_size": "12px"}
            dropdown_label = widgets.Label(
                "",
                layout=widgets.Layout(
                    width="auto", margin="0px", padding="0px", min_width="50px"
                ),
            )
            dropdown = widgets.Dropdown(
                options=[],
                value=None,
                description="",
                disabled=False,
                layout=widgets.Layout(width="auto"),
            )
            dropdown_confirm_button = widgets.Button(
                description="Confirm",
            )
            dropdown_hbox = widgets.HBox(
                [dropdown_label, dropdown, dropdown_confirm_button],
                layout=widgets.Layout(display="none"),
            )
            spacer = widgets.HTML(
                value="<hr>", layout=widgets.Layout(margin="0px", height="10px")
            )
            self.rows.append(
                ReportItem(
                    title=title,
                    progress_bar=progress_bar,
                    message=message,
                    dropdown=dropdown,
                    dropdown_hbox=dropdown_hbox,
                    dropdown_confirm_button=dropdown_confirm_button,
                    dropdown_label=dropdown_label,
                    speed_estimator=DownloadSpeedEstimator(),
                    state=ReporterItemState.Pending,
                )
            )
            self.progress_list.children += (
                spacer,
                title,
                progress_bar,
                message,
                dropdown_hbox,
            )
            return id

        def set_title(self, id: int, title: str):
            if 0 <= id < len(self.rows):
                self.rows[id].title.value = f"{title}"

        def set_state(self, id: int, state: ReporterItemState):
            if 0 <= id < len(self.rows):
                self.rows[id].state = state
                message = self.rows[id].message
                if state == ReporterItemState.Pending:
                    message.value = "<i>Pending...</i>"
                elif state == ReporterItemState.AlreadyDownloaded:
                    message.value = "<i>File already existed</i>"
                elif state == ReporterItemState.Completed:
                    message.value = "<b>Completed</b>"

        def set_progress(self, id: int, bytes_received: int, total_bytes: int):
            completed = bytes_received / total_bytes * 100
            if 0 <= id < len(self.rows):
                self.rows[id].progress_bar.value = completed
                self.rows[id].speed_estimator.add(completed)
                self.rows[id].state = ReporterItemState.Downloading
                received_unit = Formatter.format_bytes(bytes_received)
                total_unit = Formatter.format_bytes(total_bytes)

                text = f"{received_unit} of {total_unit} ({completed:05.1f}%)"

                if completed < 100:
                    eta = self.rows[id].speed_estimator.get_formatted_eta()
                    if eta:
                        text += f"- {eta} remaining"
                self.rows[id].message.value = text
                self.rows[id].progress_bar.layout.display = "flex"
                self.rows[id].message.layout.display = "block"
                self.rows[id].title.layout.display = "block"

        def can_ask_options(self):
            return True

        def ask_options(self, id: int, message: str, options, callback):
            if 0 <= id < len(self.rows):
                dropdown = self.rows[id].dropdown
                dropdown_hbox = self.rows[id].dropdown_hbox
                progress_bar = self.rows[id].progress_bar
                message_box = self.rows[id].message
                dropdown_label = self.rows[id].dropdown_label
                dropdown_confirm_button = self.rows[id].dropdown_confirm_button
                dropdown.options = options
                dropdown_label.value = message
                dropdown_hbox.layout.display = "flex"
                progress_bar.layout.display = "none"
                message_box.layout.display = "none"

                def on_confirm_button_clicked(b):
                    if dropdown.value is None:
                        return
                    callback(dropdown.value)
                    dropdown_hbox.layout.display = "none"

                dropdown_confirm_button.on_click(on_confirm_button_clicked)

        async def _update_estimators(self):
            while True:
                for row in self.rows:
                    if (
                        row.state == ReporterItemState.Downloading
                        and row.progress_bar.value > 0
                    ):
                        row.speed_estimator.add(row.progress_bar.value)
                        if row.progress_bar.value < 100:
                            eta = row.speed_estimator.get_formatted_eta()
                            if eta:
                                text = f"{row.progress_bar.value:05.1f}% (ETA: {eta})"
                                row.message.value = text
                await asyncio.sleep(10)

        def start(self):
            self.set_status("Downloading...")
            self.display_handle = display(self.main_container, display_id=True)
            loop = asyncio.get_event_loop()
            self._timer_task = loop.create_task(self._update_estimators())

        def stop(self, message: str = None):
            if message:
                self.set_status(message)
            else:
                self.set_status("Completed")
            if self._timer_task:
                self._timer_task.cancel()

        def set_error(self, id: int, error: Union[str, Exception]):
            if 0 <= id < len(self.rows):
                error_message = str(error)
                self.rows[id].message.value = (
                    f"<span style='color: red;'><b>Error:</b> {error_message}</span>"  # noqa
                )
                self.rows[id].message.style = {"font_size": "14px"}
                self.rows[id].progress_bar.layout.display = "none"
                self.rows[id].message.layout.display = "block"
                self.rows[id].title.layout.display = "block"
                self.rows[id].state = ReporterItemState.Error

        def show_message(self, id: int, message: str):
            if 0 <= id < len(self.rows):
                self.rows[id].message.value = f"<i>{message}</i>"

        def set_status(self, message: str):
            self.status_bar.value = f"<b>Status:</b> {message}"

    return IPYReporter()
