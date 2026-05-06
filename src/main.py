from copystatic import copy_folder, delete_public
from generate_page import generate_page_recursive

import sys

source_path = "./content/"
template_path = "./template.html"
destination_path = "./docs/"
static_path = "./static/"

def main():
    basepath = sys.argv
    if basepath == "":
        basepath = '/'
    
    # delete_public()

    copy_folder(static_path, destination_path)
    generate_page_recursive(source_path, template_path, destination_path, basepath)

main()
