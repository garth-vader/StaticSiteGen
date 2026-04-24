from enum import Enum
import re

class BlockType(Enum):
    PARAGRAPH = "paragraph"
    HEADING = "heading"
    CODE = "code"
    QUOTE = "quote"
    UNORDERED_LIST = "unordered_list"
    ORDERED_LIST = "ordered_list"



def block_to_block_type(block):
    if re.match(r"(^#{1,6} )", block):
        return BlockType.HEADING

    if re.match(r"(^`{3}\n)(.*)(\s*`{3}$)", block):
        return BlockType.CODE
        
    if re.match(r"(^>)(.*)", block):
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

    return BlockType.PARAGRAPH

def markdown_to_blocks(markdown):
    list_of_blocks = []
    for block in markdown.split("\n\n"):
        s = block.strip()
        if s == "":
            continue
        list_of_blocks.append(s)

    return list_of_blocks