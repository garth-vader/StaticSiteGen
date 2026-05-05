from enum import Enum
import re

from htmlnode import HTMLNode, ParentNode, LeafNode
from textnode import TextNode, TextType, text_node_to_html_node
from inline_markdown import text_to_textnodes


class BlockType(Enum):
    PARAGRAPH = "paragraph"
    HEADING = "heading"
    CODE = "code"
    QUOTE = "quote"
    UNORDERED_LIST = "unordered_list"
    ORDERED_LIST = "ordered_list"

def markdown_to_html_node(markdown):
    blocks = markdown_to_blocks(markdown)
    children = []
    for block in blocks:
        html_node = text_to_children(block)
        children.append(html_node)        

    return ParentNode("div", children)


def text_to_children(text):
    block_type = block_to_block_type(text)

    match block_type:
        case BlockType.CODE:
            block_text = text.replace("```", "")
            #remove the first white space
            return  ParentNode("pre", [LeafNode("code", block_text[1:])])
        case BlockType.QUOTE:
            tag = "blockquote"
            html_children = []
            lines = []
            for line in text.split("\n"):
                line = line[1:]
                if len(line) > 0 and line[0] == ' ':
                    line = line[1:]
                lines.append(line)
            sanitized_text = " ".join(lines) 
            text_nodes = text_to_textnodes(sanitized_text)
            for text_node in text_nodes:
                html_children.append(text_node_to_html_node(text_node))
            return ParentNode(tag, html_children)

        case BlockType.UNORDERED_LIST:
            tag = "ul"
            html_children = []
            for line in text.split('\n'):
                text_nodes = text_to_textnodes(line[1:].strip())
                list_nodes = []
                for text_node in text_nodes:
                    list_nodes.append(text_node_to_html_node(text_node))
                html_node = ParentNode("li", list_nodes)
                html_children.append(html_node)

            return ParentNode(tag, html_children) 
        case BlockType.ORDERED_LIST:
            tag = "ol"
            html_children = []
            for line in text.split('\n'):
                text_nodes = text_to_textnodes(line[2:].strip())
                list_nodes = []
                for text_node in text_nodes:
                    list_nodes.append(text_node_to_html_node(text_node))
                html_node = ParentNode("li", list_nodes)
                html_children.append(html_node)
            return ParentNode(tag, html_children) 
        case BlockType.HEADING:
            return text_to_heading_node(text)
        case BlockType.PARAGRAPH:
            tag = 'p'
            block_text = text.strip().replace("\n", " ")
            children = text_to_textnodes(block_text)
            html_nodes_children = list(map(text_node_to_html_node, children))
            return ParentNode(tag, html_nodes_children)
        case _:
            raise ValueError("Blocktype enum doesn't exists")
        
def text_to_heading_node(text):
            count = 0
            for i in range(6):
                if text[i] != '#':
                    break
                count += 1
            tag = f"h{count}"
            html_children = list(map(text_node_to_html_node, text_to_textnodes(text[count+1:])))
            return ParentNode(f"h{count}", html_children)

def block_to_block_type(block):
    if re.match(r"(^#{1,6} )", block):
        return BlockType.HEADING

    is_quote_block = True
    for line in block.split('\n'):

        if re.match(r"(^>)(.*)", block) is None:
            is_quote_block = False
            break
    if is_quote_block:
        return BlockType.QUOTE

    is_unordered_list = True 
    for line in block.split('\n'):
        if re.match(r"(^- ).*", line) is None:
            is_unordered_list = False
            break
    if is_unordered_list: 
        return BlockType.UNORDERED_LIST

    is_ordered_list = True
    count = 1
    for line in block.split('\n'):
        reg = r"^" + str(count) + r"\. .*"
        if re.match(reg, line) is None:
            is_ordered_list = False
            break
        count += 1
    if is_ordered_list:
        return BlockType.ORDERED_LIST

    if re.match(r"(^`{3}\n)[\s\S]*(`{3}$)", block):
        return BlockType.CODE
    
    return BlockType.PARAGRAPH

def markdown_to_blocks(markdown):
    list_of_blocks = []
    for block in markdown.split("\n\n"):
        s = block.strip()
        if s == "":
            continue
        list_of_blocks.append(s)

    return list_of_blocks