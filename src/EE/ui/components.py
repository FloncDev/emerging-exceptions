"""UI Components"""
from enum import Enum

COMPONENT_DIR = "src/frontend/components"


class Element:
    """Base class for all elements"""

    def __init__(self, title: str, id: str) -> None:
        self.title = title
        self.id = id


class TextType(Enum):
    """Enum for different text types"""

    Small = 0
    Large = 1


class Text(Element):
    """A text input element"""

    def __init__(
        self,
        title: str,
        id: str,
        type: TextType = TextType.Small,
        default: str = "",
    ) -> None:
        super().__init__(title, id)
        self.type = type
        self.default = default

    def html(self) -> str:
        """Return the components HTML"""
        with open(
            COMPONENT_DIR + f"/text_{str(self.type).split('.')[1].lower()}.html"
        ) as f:
            html = f.read()

        return (
            html.replace("{{title}}", self.title)
            .replace("{{id}}", self.id)
            .replace("{{default}}", self.default)
        )


class SelectOption:
    """An option for a Select element"""

    def __init__(self, text: str, id: str) -> None:
        self.text = text
        self.id = id


class Select(Element):
    """A basic select menu"""

    def __init__(
        self, title: str, id: str, options: list[SelectOption], default: str | None
    ) -> None:
        super().__init__(title, id)
        self.options = options
        self.default = default

    def html(self) -> str:
        """Return the components HTML"""
        with open(COMPONENT_DIR + "/select.html") as f:
            html = f.read()

        options = ""
        for option in self.options:
            options += f"<input type='radio' id='{option.id}' name='{self.id}'>\n"
            options += f"<label for='{option.id}'>{option.text}</label><br>\n"

        return html.replace("{{title}}", self.title).replace("{{inputs}}", options)


class Dropdown(Element):
    """
    A dropdown element

    Default option is options[0]
    """

    def __init__(self, title: str, id: str, options: list[SelectOption]) -> None:
        super().__init__(title, id)
        self.options = options

    def html(self) -> str:
        """Return the components HTML"""
        with open(COMPONENT_DIR + "/dropdown.html") as f:
            html = f.read()

        options = ""
        for option in self.options:
            options += f"<option id='{option.id}'>{option.text}</option>\n"

        return (
            html.replace("{{title}}", self.title)
            .replace("{{id}}", self.id)
            .replace("{{inputs}}", options)
        )
