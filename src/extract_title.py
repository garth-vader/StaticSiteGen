import os

# Takes in a file with a h1 heading in the markdown file.
# Raises error if there is no h1 header
# Returns value of h1 header (no # and no leading or trailing whitespace)
def extract_title(markdown_file):
    with open(markdown_file, 'r', encoding="utf-8") as f:
        title = f.read()
    return extract_title_text(title)



def extract_title_text(markdown_text):
    if markdown_text is None or not markdown_text.startswith("# "):
        raise ValueError("Must start with h1 markdown")
    
    text = markdown_text[1:]
    text = text.split('\n', 1)[0].strip()
    return text
