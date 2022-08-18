import os

target_dirpath_dict = {
    os.path.join('target_dir'): 86400 * 30,
    os.path.join('one_else_target_dir'): 86400 * 30,
}

excluded_filenames = [
    '.gitignore'
]
