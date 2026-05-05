import os
import shutil


def copy_folder(src, dst):
    if os.path.isfile(src):
        print(f"copy {src} to {dst}")
        shutil.copy(src, dst)
        return

    os.mkdir(dst)
    #src is a folder
    for file_name in os.listdir(src):
        src_path = os.path.join(src, file_name)
        dst_path = os.path.join(dst, file_name)
        copy_folder(src_path, dst_path)
    return

def delete_public():
    current_directory = os.getcwd() 
    path_public = os.path.join(current_directory, "public/") 
    if os.path.exists(path_public):
        shutil.rmtree(path_public)
    else:
        print("public is already deleted")