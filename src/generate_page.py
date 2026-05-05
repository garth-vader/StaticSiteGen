import os
from markdown_blocks import markdown_to_html_node
from extract_title import extract_title_text
def generate_page(from_path, template_path, dest_path):

    print(f"Generating page from {from_path} to {dest_path} using {template_path}")
    with open(from_path, "r", encoding="utf-8") as f:
        src_markdown = f.read()
    
    with open(template_path, "r", encoding="utf-8") as f:
        template_text = f.read()

    content = markdown_to_html_node(src_markdown).to_html()
    title = extract_title_text(src_markdown)
     
    page = template_text.replace(r"{{ Title }}", title).replace(r"{{ Content }}", content)

    if not os.path.exists(os.path.dirname(dest_path)):
        os.makedirs(os.path.dirname(dest_path))

    with open(dest_path, 'w', encoding="utf-8") as f:
        amount_written = f.write(page)

    print(f"wrote {amount_written}") 




