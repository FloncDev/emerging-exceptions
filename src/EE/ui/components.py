"""UI Components"""
from enum import Enum


class Element:
    """Base class for all elements"""

    def __init__(self, title: str, id: str) -> None:
        self.title = title
        self.id = id


class TextType(Enum):
    """Enum for different text types"""

    Large = 0
    Small = 0


class Text(Element):
    """A text input element"""

    def __init__(
        self,
        title: str,
        id: str,
        default: str,
        type: TextType = TextType.Small,
    ) -> None:
        super().__init__(title, id)
        self.default = default
        self.type = type


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


class Dropdown(Element):
    """
    A dropdown element

    Default option is options[0]
    """

    def __init__(self, title: str, id: str, options: list[SelectOption]) -> None:
        super().__init__(title, id)
        self.options = options
