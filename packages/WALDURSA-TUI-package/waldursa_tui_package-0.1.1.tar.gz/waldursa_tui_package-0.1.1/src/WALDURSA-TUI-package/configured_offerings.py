from textual.app import ComposeResult
from textual.widgets import ListView, ListItem, Label, Input
from textual.containers import Container, Vertical


class LabelItem(ListItem):
    def __init__(self, content: str) -> None:
        super().__init__()

        self.content = content

    def compose(self) -> ComposeResult:
        yield Label(self.content, id="side_menu_offerings_button")

    def get_content(self):
        return self.content


class Configured_offerings(Container):
    def __init__(self):
        super().__init__()

        self.list_view_menu = ListView(classes="box", id="side_menu_offerings_listview")
        self.list_view_param = ListView(classes="box", id="params")
        self.search_bar = Input(placeholder="Search...", id="search_bar_offerings")

        self.offerings = []

    def test_menu(self):  # will be removed when actual data is used
        test_list = []
        for i in range(1, 7):
            test_list.append("Offering " + str(i))
        return test_list

    def test_paramaters(self):  # will be removed when actual data is used
        test_list = []
        for i in range(1, 15):
            test_list.append(["Item " + str(i), "value " + str(i)])
        return test_list

    def compose(self) -> ComposeResult:
        with Vertical(id="side_menu_offerings"):
            yield self.search_bar
            yield self.list_view_menu
        yield self.list_view_param

    def on_list_view_selected(self, event: ListView.Selected):
        if event.list_view.id == "side_menu_offerings_listview":
            offering = self.query_one("#params", ListView)
            offering.clear()
            offering.append(
                ListItem(Label("New params from " + str(event.item.get_content())))
            )

    def on_input_submitted(self, event: Input.Submitted):
        input_text = event.value.lower()
        side_menu = self.query_one("#side_menu_offerings_listview", ListView)

        if input_text == "":
            for i in range(len(self.offerings)):
                if self.offerings[i] not in side_menu.children:
                    self.list_view_menu.append(self.offerings[i])
        else:
            for i in range(len(self.offerings)):
                if input_text in self.offerings[i].get_content().lower():
                    if self.offerings[i] not in side_menu.children:
                        side_menu.append(self.offerings[i])
                else:
                    for j in range(len(side_menu.children)):
                        if self.offerings[i] == side_menu.children[j]:
                            side_menu.remove_items(iter([j]))
                            break

    def on_mount(self):
        self.make_listView_menu(self.test_menu())
        self.make_listView_param(self.test_paramaters())

    def make_listView_menu(self, list_buttons):
        for button in list_buttons:
            labelItem_button = LabelItem(button)
            self.list_view_menu.append(labelItem_button)
            self.offerings.append(labelItem_button)

    def make_listView_param(self, list_paramaters):
        for item in list_paramaters:
            self.list_view_param.append(ListItem(Label(item[0] + ": " + item[1])))
