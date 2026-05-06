from copystatic import copy_folder, delete_public
from generate_page import generate_page_recursive
import os
import shutil
import sys

source_path = "./content/"
template_path = "./template.html"
destination_path = "./docs/"
static_path = "./static/"

def main():
    basepath = ""
    if len(sys.argv) > 1:
        basepath = sys.argv[1]
    if basepath == "":
        basepath = '/'
    

    if os.path.exists(destination_path):
        shutil.rmtree(destination_path)
    else:
        print("public is already deleted")
    # delete_public()

    copy_folder(static_path, destination_path)
    generate_page_recursive(source_path, template_path, destination_path, basepath)

main()
