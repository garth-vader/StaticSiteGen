import os
import shutil

def copy_folder_to_public(folder_name):
    current_directory = os.getcwd() 
    path_public = os.path.join(current_directory, "public/") 
    path_source = os.path.join(current_directory, folder_name)
    copy(path_source, path_public)


def copy(src, dst):
    if os.path.isfile(src):
        print(f"copy {src} to {dst}")
        shutil.copy(src, dst)
        return

    print(f"making {dst}")
    os.mkdir(dst)
    #src is a folder
    for file_name in os.listdir(src):
        src_path = os.path.join(src, file_name)
        dst_path = os.path.join(dst, file_name)
        copy(src_path, dst_path)
    return

def delete_public():
    current_directory = os.getcwd() 
    path_public = os.path.join(current_directory, "public/") 
    if os.path.exists(path_public):
        shutil.rmtree(path_public)
    else:
        print("public is already deleted")