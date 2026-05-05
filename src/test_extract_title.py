import unittest
from extract_title import extract_title_text, extract_title


class TestExtractTitle(unittest.TestCase):
    def test_extract(self):
        self.assertEqual(extract_title("./content/index.md"), "Tolkien Fan Club")
    def test_extract_title_text(self):
        text = """# Tolkien Fan Club

![JRR Tolkien sitting](/images/tolkien.png)
"""
        self.assertEqual(extract_title_text(text), "Tolkien Fan Club")
        self.assertEqual(extract_title_text("# title"), "title")
        self.assertRaises(ValueError, extract_title_text, "somestring")