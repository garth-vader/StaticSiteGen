import unittest
from markdown_blocks import markdown_to_blocks, block_to_block_type, BlockType, markdown_to_html_node
from htmlnode import HTMLNode

class TestMarkdownToHtmlNode(unittest.TestCase):
    def test_paragraphs(self):
        md = """
This is **bolded** paragraph
text in a p
tag here

This is another paragraph with _italic_ text and `code` here

"""

        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><p>This is <b>bolded</b> paragraph text in a p tag here</p><p>This is another paragraph with <i>italic</i> text and <code>code</code> here</p></div>",
        )

    def test_codeblock(self):
        md = """
```
This is text that _should_ remain
the **same** even with inline stuff
```
"""

        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><pre><code>This is text that _should_ remain\nthe **same** even with inline stuff\n</code></pre></div>",
        )



class TestBlockToBlockType(unittest.TestCase):
    def test_block_to_block_types(self):
            block = "# heading"
            self.assertEqual(block_to_block_type(block), BlockType.HEADING)
            block = "```\ncode\n```"
            self.assertEqual(block_to_block_type(block), BlockType.CODE)
            block = "> quote\n> more quote"
            self.assertEqual(block_to_block_type(block), BlockType.QUOTE)
            block = "- list\n- items"
            self.assertEqual(block_to_block_type(block), BlockType.UNORDERED_LIST)
            block = "1. list\n2. items"
            self.assertEqual(block_to_block_type(block), BlockType.ORDERED_LIST)
            block = "paragraph"
            self.assertEqual(block_to_block_type(block), BlockType.PARAGRAPH)

    def test_headings(self):
        self.assertEqual(block_to_block_type("# This is a Heading"), BlockType.HEADING)
        self.assertEqual(block_to_block_type("#This is not a Heading"), BlockType.PARAGRAPH)
        self.assertEqual(block_to_block_type("## This is a Heading"), BlockType.HEADING)
        self.assertEqual(block_to_block_type("### This is a Heading"), BlockType.HEADING)
        self.assertEqual(block_to_block_type("#### This is a Heading"), BlockType.HEADING)
        self.assertEqual(block_to_block_type("##### This is a Heading"), BlockType.HEADING)
        self.assertEqual(block_to_block_type("###### This is a Heading"), BlockType.HEADING)
        self.assertEqual(block_to_block_type("####### This is not a Heading"), BlockType.PARAGRAPH)

    def test_code_blocks(self):
        good_block1 = """```
x = 10 + 10
```"""
        good_block2 = """```

```"""
        good_block3 = """```
somecode```"""
        bad_block2 = """```
"""
        self.assertEqual(block_to_block_type(good_block1), BlockType.CODE)
        self.assertEqual(block_to_block_type(good_block2), BlockType.CODE)
        self.assertEqual(block_to_block_type(good_block3), BlockType.CODE)
        self.assertEqual(block_to_block_type(bad_block2), BlockType.PARAGRAPH)

    def test_quote_block(self):
        quote_block1 = ">quoted text>"
        quote_block2 = "> quoted text> "

        quote_block3 = "bad quoted text>"
        quote_block4 = " >bad quoted text"
        self.assertEqual(block_to_block_type(quote_block1), BlockType.QUOTE)
        self.assertEqual(block_to_block_type(quote_block2), BlockType.QUOTE)
        self.assertEqual(block_to_block_type(quote_block3), BlockType.PARAGRAPH)
        self.assertEqual(block_to_block_type(quote_block4), BlockType.PARAGRAPH)

    def test_unordered_list_block(self):
        ul_block1 = "- list of one"
        ul_block2  = """- one
- two""" 
        ul_block3  = """- one
- two
- three""" 
        ul_block4  = """- one
-two
- three""" 
        self.assertEqual(block_to_block_type(ul_block1), BlockType.UNORDERED_LIST)
        self.assertEqual(block_to_block_type(ul_block2), BlockType.UNORDERED_LIST)
        self.assertEqual(block_to_block_type(ul_block3), BlockType.UNORDERED_LIST)
        self.assertEqual(block_to_block_type(ul_block4), BlockType.PARAGRAPH)

    def test_ordered_list_block(self):
        ol_block1 = "1. list of one"
        ol_block2  = """1. one
2. two""" 
        ol_block3  = """1. one
2. two
3. three""" 
        ol_block4  = """2. one
1. two
3. three""" 
        ol_block5  = """1. one
2.two
3. three""" 
        self.assertEqual(block_to_block_type(ol_block1), BlockType.ORDERED_LIST)
        self.assertEqual(block_to_block_type(ol_block2), BlockType.ORDERED_LIST)
        self.assertEqual(block_to_block_type(ol_block3), BlockType.ORDERED_LIST)
        self.assertEqual(block_to_block_type(ol_block4), BlockType.PARAGRAPH)
        self.assertEqual(block_to_block_type(ol_block5), BlockType.PARAGRAPH)

class TestMarkdownToHTML(unittest.TestCase):
    def test_markdown_to_blocks(self):
        md = """
This is **bolded** paragraph

This is another paragraph with _italic_ text and `code` here
This is the same paragraph on a new line

- This is a list
- with items
"""
        blocks = markdown_to_blocks(md)
        self.assertEqual(
            blocks,
            [
                "This is **bolded** paragraph",
                "This is another paragraph with _italic_ text and `code` here\nThis is the same paragraph on a new line",
                "- This is a list\n- with items",
            ],
        )

    def test_markdown_to_blocks_newlines(self):
        md = """
This is **bolded** paragraph




This is another paragraph with _italic_ text and `code` here
This is the same paragraph on a new line

- This is a list
- with items
"""
        blocks = markdown_to_blocks(md)
        self.assertEqual(
            blocks,
            [
                "This is **bolded** paragraph",
                "This is another paragraph with _italic_ text and `code` here\nThis is the same paragraph on a new line",
                "- This is a list\n- with items",
            ],
        )
    def test_empty_list(self):
        blocks = """




"""
        self.assertEqual(markdown_to_blocks(blocks), [])
        self.assertEqual(markdown_to_blocks(""), [])


if __name__ == "__main__":
    unittest.main()