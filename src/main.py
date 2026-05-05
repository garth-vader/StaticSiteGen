from copystatic import copy_folder, delete_public
from generate_page import generate_page
def main():
    delete_public()
    copy_folder("./static/", "./public/")
    generate_page("./content/index.md", "./template.html", "./public/index.html")

main()
