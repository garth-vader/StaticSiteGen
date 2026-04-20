import unittest
from inline_markdown import split_nodes_delimiter, extract_markdown_images, extract_markdown_links, split_nodes_image, split_nodes_link, text_to_textnodes
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
    
    def test_extract_markdown_links_not_links(self):
        text = "This is text with a link ![to boot dev](https://www.boot.dev) and [to youtube](https://www.youtube.com/@bootdotdev)"
        self.assertListEqual([("to youtube", "https://www.youtube.com/@bootdotdev")], 
                             extract_markdown_links(text))

class Testsplitimages(unittest.TestCase):
    
    def test_split_image(self):
        node = TextNode(
            "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png)",
            TextType.TEXT,
        )
        new_nodes = split_nodes_image([node])
        self.assertListEqual(
            [
                TextNode("This is text with an ", TextType.TEXT),
                TextNode("image", TextType.IMAGE, "https://i.imgur.com/zjjcJKZ.png"),
            ],
            new_nodes,
        )

    def test_split_links(self):
        node = TextNode(
            "This is text with an [link to google](https://www.google.com)",
            TextType.TEXT,
        )
        new_nodes = split_nodes_link([node])
        self.assertListEqual(
            [
                TextNode("This is text with an ", TextType.TEXT),
                TextNode("link to google", TextType.LINK, "https://www.google.com"),
            ],
            new_nodes,
        )
    def test_split_images(self):
        node = TextNode(
            "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png) and another ![second image](https://i.imgur.com/3elNhQu.png)",
            TextType.TEXT,
        )
        new_nodes = split_nodes_image([node])
        self.assertListEqual(
            [
                TextNode("This is text with an ", TextType.TEXT),
                TextNode("image", TextType.IMAGE, "https://i.imgur.com/zjjcJKZ.png"),
                TextNode(" and another ", TextType.TEXT),
                TextNode(
                    "second image", TextType.IMAGE, "https://i.imgur.com/3elNhQu.png"
                ),
            ],
            new_nodes,
        )

    def test_split_links(self):
        node = TextNode(
            "This is text with an [link to google](https://www.google.com) and another [link to boot.dev](https://www.boot.dev)",
            TextType.TEXT,
        )
        new_nodes = split_nodes_link([node])
        self.assertListEqual(
            [
                TextNode("This is text with an ", TextType.TEXT),
                TextNode("link to google", TextType.LINK, "https://www.google.com"),
                TextNode(" and another ", TextType.TEXT),
                TextNode(
                    "link to boot.dev", TextType.LINK, "https://www.boot.dev"
                ),
            ],
            new_nodes,
        )
    
    def test_split_image_link(self):
        node = TextNode(
            "This is text with an [link to google](https://www.google.com) and another ![second image](https://i.imgur.com/3elNhQu.png)",
            TextType.TEXT,
        )
        new_nodes = split_nodes_link([node])
        new_nodes = split_nodes_image(new_nodes)
        self.assertListEqual(
            [
                TextNode("This is text with an ", TextType.TEXT),
                TextNode("link to google", TextType.LINK, "https://www.google.com"),
                TextNode(" and another ", TextType.TEXT),
                TextNode(
                    "second image", TextType.IMAGE, "https://i.imgur.com/3elNhQu.png"),
            ],
            new_nodes,
        )

class Testtexttotextnodes(unittest.TestCase):

    def test_text_to_textnodes(self):
        text = "This is **text** with an _italic_ word and a `code block` and an ![obi wan image](https://i.imgur.com/fJRm4Vk.jpeg) and a [link](https://boot.dev)"

        self.assertListEqual(
            [
                TextNode("This is ", TextType.TEXT),
                TextNode("text", TextType.BOLD),
                TextNode(" with an ", TextType.TEXT),
                TextNode("italic", TextType.ITALIC),
                TextNode(" word and a ", TextType.TEXT),
                TextNode("code block", TextType.CODE),
                TextNode(" and an ", TextType.TEXT),
                TextNode("obi wan image", TextType.IMAGE, "https://i.imgur.com/fJRm4Vk.jpeg"),
                TextNode(" and a ", TextType.TEXT),
                TextNode("link", TextType.LINK, "https://boot.dev"),
            ],
            text_to_textnodes(text),
        )