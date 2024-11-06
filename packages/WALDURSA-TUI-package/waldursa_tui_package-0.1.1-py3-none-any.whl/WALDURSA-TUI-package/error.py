from textual.app import ComposeResult
from textual.containers import Container
from textual.widgets import Button, Label
from textual.screen import ModalScreen


class ErrorPopup(ModalScreen):
    "A simple error popup modal."

    def __init__(self, error_message: str, error_type: str) -> None:
        super().__init__()
        self.error_message = error_message
        self.error_type = error_type

    def compose(self) -> ComposeResult:
        # Create the content for the modal (error message and OK button)
        yield Container(
            Label(self.error_type + ":", id="error_type"),
            Label(self.error_message, id="error_message"),  # Display the error message
        )
        yield Container(
            Button.error("OK", id="close_button"),  # OK button to close the popup
            id="center",
        )

    def on_button_pressed(self, event: Button.Pressed) -> None:
        # Close the popup when OK button is pressed
        if event.button.id == "close_button":
            self.app.pop_screen()
