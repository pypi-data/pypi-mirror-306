from textual.widgets import DataTable
from textual.app import ComposeResult
from textual.containers import Container, Vertical, Horizontal
from textual_plotext import PlotextPlot
from rich.text import Text


class Dashboard(Container):
    def __init__(self):
        super().__init__()

        self.test_list = [
            ("Service", "Uptime", "Last contact", "Status"),
            ("Waldur Mastermind", "100h", "1 minute ago", Text("OK", style="green")),
            ("Waldur Site Agent", "0m", "1 minute ago", Text("FAIL", style="red")),
        ]

    def compose(self) -> ComposeResult:
        with Vertical():
            yield DataTable()
            with Horizontal():
                yield PlotextPlot(id="plot1")
                yield PlotextPlot(id="plot2")

    def on_mount(self) -> None:
        table = self.query_one(DataTable)
        table.cursor_type = "none"
        table.add_columns(*self.test_list[0])
        for row in self.test_list[1:]:
            table.add_row(*row)

        plt = self.query_one("#plot1").plt
        y = plt.sin()
        plt.plot(y)
        plt.title("Example 1")

        plt2 = self.query_one("#plot2").plt
        y = plt2.sin()
        plt2.plot(y)
        plt2.title("Example 2")
