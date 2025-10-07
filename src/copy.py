import os
import shutil

def copy_static(sub_dir=None) :
    full_path = os.path.abspath("./static") if not(sub_dir) else sub_dir
    copy_path = os.path.abspath("./docs")

    if not(os.path.exists(full_path)) :
        return False

    to_copy = os.listdir(full_path)

    if not(len(to_copy)) :
        return False

    to_copy = list(map(lambda x: os.path.join(full_path, x), to_copy))
    to_copy_dirs = [i for i in to_copy if not(os.path.isfile(i))]
    to_copy_files = [i for i in to_copy if os.path.isfile(i)]

    for dir in to_copy_dirs :
        s_dir = dir.split("/")[-1]
        if not os.path.isdir(os.path.join(copy_path, s_dir)) :
            os.mkdir(os.path.join(copy_path, s_dir))
        if len(os.listdir(dir)) :
            copy_static(sub_dir=dir)

    for file in to_copy_files :
        s_file = file.split("/")
        s_file_path = s_file[s_file.index("static"):]
        build_file_path = None if len(s_file_path) < 3 else "/".join(s_file_path[1:-1])
        shutil.copy(file, copy_path if not(build_file_path) else os.path.join(copy_path, build_file_path))

    # whoops not(sub_dir) and shutil.rmtree(full_path)
    return True
