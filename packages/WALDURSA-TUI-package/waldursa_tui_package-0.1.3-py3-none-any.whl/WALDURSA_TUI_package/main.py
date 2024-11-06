from textual.app import App, ComposeResult
from textual.widgets import TabbedContent, TabPane
import configured_offerings
import dashboard
import logs

from quit import QuitScreen
from error import ErrorPopup


class WaldurSATUIApp(App):
    CSS_PATH = "main.tcss"
    BINDINGS = [("q", "request_quit", "Quit"), ("e", "request_error", "Error Showcase")]

    def compose(self) -> ComposeResult:
        with TabbedContent(initial="dashboard"):
            with TabPane("Dashboard", id="dashboard"):
                yield dashboard.Dashboard()
            with TabPane("Logs", id="logs"):
                yield logs.Logs()
            with TabPane("Configured offerings", id="configured_offerings"):
                yield configured_offerings.Configured_offerings()

    def action_show_tab(self, tab: str) -> None:
        self.get_child_by_type(TabbedContent).active = tab

    def action_request_quit(self) -> None:
        """Action to display the quit dialog."""

        def check_quit(quit: bool) -> None:
            """Called when QuitScreen is dismissed."""
            if quit:
                self.exit()

        self.push_screen(QuitScreen(), check_quit)

    def action_request_error(self) -> None:
        # show error message
        self.app.push_screen(ErrorPopup("An unexpected error occurred!", "Test error"))


if __name__ == "__main__":
    app = WaldurSATUIApp()
    app.run()
