from textnode import TextNode, TextType, text_node_to_html_node
import re

def split_nodes_delimiter(old_nodes, delimiter, text_type):
    result = []
    for node in old_nodes:
        if node.text_type is not TextType.TEXT:
            result.append(TextNode(node.text, node.text_type))
            continue
        
        if node.text.count(delimiter) % 2 != 0:
            raise ValueError("Missing matching delimiter")
        
        in_block = False
        for section in node.text.split(delimiter):
            if in_block:
                if len(section) > 0:
                    result.append(TextNode(section, text_type))
                in_block = False
            else:
                if len(section) > 0:
                    result.append(TextNode(section, TextType.TEXT))
                in_block = True 

    return result

def extract_markdown_images(text):
    return re.findall(r"!\[([^\[\]]*)\]\(([^\(\)]*)\)", text)

def extract_markdown_links(text):
    return re.findall(r"(?<!!)\[([^\[\]]*)\]\(([^\(\)]*)\)", text)