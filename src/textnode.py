from enum import Enum

class TextType(Enum):
    PLAIN = "plain"
    BOLD = "**Bold text**"
    ITALIC = "_Italic text_"
    CODE = "`Code text`"
    LINK = "link"
    IMAGE = "![alt text](url)"

class TextNode():
    def __init__(self, text, text_type, url):
        self.text = text
        self.text_type = text_type
        if not url:
            self.url = None
        else: 
            self.url = url

    def __eq__(self, other):
        return self.text == other.text and self.text_type == other.text_type and self.url == other.url

    def __repr__(self):

        return f"TextNode({self.text}, {self.text_type.value}, {self.url})"
    