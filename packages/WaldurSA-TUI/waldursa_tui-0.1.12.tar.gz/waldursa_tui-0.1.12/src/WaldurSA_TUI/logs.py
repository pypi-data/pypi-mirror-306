from textual.app import ComposeResult
from textual.widgets import ListView, ListItem, Label, Input, DataTable, Button, Rule
from textual.containers import Container, Vertical, Horizontal
from textual_datepicker import DateSelect
import os


class LabelItem(ListItem):
    def __init__(self, content: str) -> None:
        super().__init__()

        self.content = content

    def compose(self) -> ComposeResult:
        yield Label(self.content, id="side_menu_logs_button")

    def get_content(self):
        return self.content


class Logs(Container):
    def __init__(self):
        super().__init__()

        self.list_view_menu = ListView(classes="box", id="side_menu_logs")
        self.search_bar = Input(placeholder="Search...", id="search_bar_logs")
        self.logs = []

    def test_menu(
        self,
    ):  # if there are more than these three options, it will be removed/changed
        test_list = []
        test_list.append("Processing Orders")
        test_list.append("User Membership Synchronization")
        test_list.append("Usage Reporting")
        return test_list

    def test_logs(self):  # will be removed when actual data is used
        test_list = [
            ("17:15:47 - 03.10.2024", "INFO", "User logged in"),
            ("17:15:47 - 03.10.2024", "INFO", "User made made an order"),
            ("17:15:47 - 03.10.2024", "INFO", "User checked membership"),
            ("17:15:47 - 03.10.2024", "INFO", "User logged out"),
        ]
        return test_list

    def compose(self) -> ComposeResult:
        yield self.list_view_menu
        with Vertical(id="logdates"):
            with Horizontal(classes="height-auto"):
                yield DateSelect(
                    placeholder="From date",
                    format="YYYY-MM-DD",
                    picker_mount="#logdates",
                    classes="column",
                )
                yield DateSelect(
                    placeholder="To date",
                    format="YYYY-MM-DD",
                    picker_mount="#logdates",
                    classes="column",
                )
            yield self.search_bar
            with Horizontal(classes="height-auto width-full right-align"):
                yield Button("Refreshing in ?s", id="refresh")
                yield Button(
                    "Export", id="export", classes="margin-left-1"
                )  # OK button to close the popup
            yield Rule(line_style="heavy")
            yield DataTable()

    def on_list_view_selected(self, event: ListView.Selected):
        if event.list_view.id == "side_menu_logs":
            side_menu_text = event.item.get_content()
            table = self.query_one(DataTable).clear()
            self.logs.clear()
            logs = self.test_logs()
            log = ["17:15:47 - 03.10.2024", "INFO", f"Logs of {side_menu_text}"]
            logs.insert(0, log)
            for log in logs:
                table.add_row(*log)
                self.logs.append(log)

    def on_input_submitted(self, event: Input.Submitted):
        input_text = event.value.lower()
        log_text = self.query_one(DataTable)
        log_text.clear()
        self.logs.clear()
        for log in self.test_logs():
            if input_text in log[2].lower():
                log_text.add_row(*log)
                self.logs.append(log)

    def on_button_pressed(self, event: Button.Pressed) -> None:
        if event.button.id == "export":
            newpath = "src/test_export_logs"
            if not os.path.exists(newpath):
                os.makedirs(newpath)
            for nr, log in enumerate(self.logs):
                file = open("src/test_export_logs/log_" + str(nr + 1) + ".txt", "w")
                for item in log:
                    file.write(item + "\n")
                file.close()

    def on_mount(self):
        self.make_listView_menu(self.test_menu())
        table = self.query_one(DataTable)
        table.add_columns("Date", "Status", "Log")
        for log in self.test_logs():
            table.add_row(*log)
            self.logs.append(log)

    def make_listView_menu(self, list_buttons):
        for button in list_buttons:
            labelItem_button = LabelItem(button)
            self.list_view_menu.append(labelItem_button)
