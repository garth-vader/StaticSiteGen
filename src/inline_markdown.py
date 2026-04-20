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

def split_nodes_image(old_nodes):
    result = []
    for node in old_nodes:
        images = extract_markdown_images(node.text)
        if len(images) == 0 or node.text_type != TextType.TEXT:
            result.append(node)
        else:
            s = node.text
            for image_alt, image_link in images:
                before_image, rest = s.split(f"![{image_alt}]({image_link})", 1)
                if len(before_image) > 0:
                    result.append(TextNode(before_image, TextType.TEXT))
                result.append(TextNode(image_alt, TextType.IMAGE, image_link))
                s = rest 
            if len(s) > 0:
                result.append(TextNode(s, TextType.TEXT))
    return result
            


def split_nodes_link(old_nodes):
    result = []
    for node in old_nodes:
        links = extract_markdown_links(node.text)
        if len(links) == 0 or node.text_type != TextType.TEXT:
            result.append(node)
        else:
            s = node.text
            for link_text, link_url in links:
                before_image, rest = s.split(f"[{link_text}]({link_url})", 1)
                if len(before_image) > 0:
                    result.append(TextNode(before_image, TextType.TEXT))
                result.append(TextNode(link_text, TextType.LINK, link_url))
                s = rest 
            if len(s) > 0:
                result.append(TextNode(s, TextType.TEXT))
    return result

def extract_markdown_images(text):
    return re.findall(r"!\[([^\[\]]*)\]\(([^\(\)]*)\)", text)

def extract_markdown_links(text):
    return re.findall(r"(?<!!)\[([^\[\]]*)\]\(([^\(\)]*)\)", text)

