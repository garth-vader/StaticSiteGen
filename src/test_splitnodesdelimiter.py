import unittest
from inline_markdown import split_nodes_delimiter, extract_markdown_images, extract_markdown_links
from textnode import TextNode, TextType

class Testsplitnodesdeliter(unittest.TestCase):
    def test_split_nodes_delimiter_code_block(self):
        node = TextNode("This is text with a `code block` word", TextType.TEXT)
        self.assertListEqual(
            split_nodes_delimiter([node], "`", TextType.CODE),
            [
                TextNode("This is text with a ", TextType.TEXT),
                TextNode("code block", TextType.CODE),
                TextNode(" word", TextType.TEXT),
            ],
        )

    def test_split_nodes_delimiter_code_block_multiple_blocks(self):
        node = TextNode("This is text with a `code block` word and a `second block`", TextType.TEXT)
        self.assertListEqual(
            split_nodes_delimiter([node], "`", TextType.CODE),
            [
                TextNode("This is text with a ", TextType.TEXT),
                TextNode("code block", TextType.CODE),
                TextNode(" word and a ", TextType.TEXT),
                TextNode("second block", TextType.CODE),
            ],
        )
        
    def test_split_nodes_delimiter_multiple_nodes(self):
        node1 = TextNode("This is text1 with a `code block` word", TextType.TEXT)
        node2 = TextNode("This is text2 with a `code` word", TextType.TEXT)
        node3 = TextNode("This is bold3 with a `code block` word", TextType.BOLD)
        self.assertListEqual(
            split_nodes_delimiter([node1, node2, node3], "`", TextType.CODE),
            [
                TextNode("This is text1 with a ", TextType.TEXT),
                TextNode("code block", TextType.CODE),
                TextNode(" word", TextType.TEXT),
                TextNode("This is text2 with a ", TextType.TEXT),
                TextNode("code", TextType.CODE),
                TextNode(" word", TextType.TEXT),
                TextNode("This is bold3 with a `code block` word", TextType.BOLD)
            ],
        )
        
    def test_split_nodes_delimiter_italic(self):
        node = TextNode("This is text with an _italic_ word", TextType.TEXT)
        self.assertListEqual(
            split_nodes_delimiter([node], "_", TextType.ITALIC),
            [
                TextNode("This is text with an ", TextType.TEXT),
                TextNode("italic", TextType.ITALIC),
                TextNode(" word", TextType.TEXT),
            ],
        )

    def test_split_nodes_delimiter_bold(self):
        node = TextNode("This is text with a **bold** word", TextType.TEXT)
        self.assertListEqual(
            split_nodes_delimiter([node], "**", TextType.BOLD),
            [
                TextNode("This is text with a ", TextType.TEXT),
                TextNode("bold", TextType.BOLD),
                TextNode(" word", TextType.TEXT),
            ],
        )

    def test_split_nodes_delimiter_not_TEXT(self):
        node = TextNode("This is text with a **bold** word", TextType.BOLD)
        self.assertListEqual(
            split_nodes_delimiter([node], "**", TextType.CODE),
            [
                TextNode("This is text with a **bold** word", TextType.BOLD),
            ],
        )

    def test_delim_bold_and_italic(self):
        node = TextNode("**bold** and _italic_", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "**", TextType.BOLD)
        new_nodes = split_nodes_delimiter(new_nodes, "_", TextType.ITALIC)
        self.assertListEqual(
            [
                TextNode("bold", TextType.BOLD),
                TextNode(" and ", TextType.TEXT),
                TextNode("italic", TextType.ITALIC),
            ],
            new_nodes,
        )
    def test_split_nodes_delimiter_raise_value_error(self):
        #No closing delimiter
        node = TextNode("This is text ^with a  word", TextType.TEXT)
        self.assertRaises(
            ValueError,
            split_nodes_delimiter,
            [node],
            "^", 
            TextType.CODE
        )
           
class Testextractmarkdown(unittest.TestCase):
    def test_extract_markdown_images1(self):
        text = "This is text with a ![rick roll](https://i.imgur.com/aKaOqIh.gif) and ![obi wan](https://i.imgur.com/fJRm4Vk.jpeg)"
        self.assertListEqual([("rick roll", "https://i.imgur.com/aKaOqIh.gif"), ("obi wan", "https://i.imgur.com/fJRm4Vk.jpeg")], extract_markdown_images(text))

    def test_extract_markdown_images2(self):
        matches = extract_markdown_images(
            "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png)"
        )
        self.assertListEqual([("image", "https://i.imgur.com/zjjcJKZ.png")], matches) 
    
    def test_extract_markdown_links(self):
        text = "This is text with a link [to boot dev](https://www.boot.dev) and [to youtube](https://www.youtube.com/@bootdotdev)"
        self.assertListEqual([("to boot dev", "https://www.boot.dev"), ("to youtube", "https://www.youtube.com/@bootdotdev")], 
                             extract_markdown_links(text))