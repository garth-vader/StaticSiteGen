from copystatic import copy_folder_to_public, delete_public

def main():
    delete_public()
    copy_folder_to_public("static/")

main()
