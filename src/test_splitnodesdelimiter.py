import unittest
from splitnodesdelimiter import split_nodes_delimiter
from textnode import TextNode, TextType

class Testsplitnodesdeliter(unittest.TestCase):
    def test_split_nodes_delimiter_code_block(self):
        node = TextNode("This is text with a `code block` word", TextType.TEXT)
        self.assertEqual(
            split_nodes_delimiter([node], "`", TextType.CODE),
            [
                TextNode("This is text with a ", TextType.TEXT),
                TextNode("code block", TextType.CODE),
                TextNode(" word", TextType.TEXT),
            ],
        )

    def test_split_nodes_delimiter_code_block_multiple_blocks(self):
        node = TextNode("This is text with a `code block` word and a `second block`", TextType.TEXT)
        self.assertEqual(
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
        self.assertEqual(
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
        self.assertEqual(
            split_nodes_delimiter([node], "_", TextType.ITALIC),
            [
                TextNode("This is text with an ", TextType.TEXT),
                TextNode("italic", TextType.ITALIC),
                TextNode(" word", TextType.TEXT),
            ],
        )

    def test_split_nodes_delimiter_bold(self):
        node = TextNode("This is text with a **bold** word", TextType.TEXT)
        self.assertEqual(
            split_nodes_delimiter([node], "**", TextType.BOLD),
            [
                TextNode("This is text with a ", TextType.TEXT),
                TextNode("bold", TextType.BOLD),
                TextNode(" word", TextType.TEXT),
            ],
        )

    def test_split_nodes_delimiter_not_TEXT(self):
        node = TextNode("This is text with a **bold** word", TextType.BOLD)
        self.assertEqual(
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
           