import os
import sys
import time
import pathlib
from datetime import datetime

from cfg import target_dirpath_list, max_file_lifetime_in_seconds, excluded_filenames


class FilesCleaner:

    def __init__(self, target_dirpathes: list, max_file_lifetime_in_secs: int = 60, excluded_filename_list=None):
        """Чистильщик файлов"""

        if excluded_filename_list is None:
            self._excluded_filenames = list()
        elif isinstance(excluded_filename_list, list):
            self._excluded_filenames = excluded_filename_list
        else:
            raise Exception(f'Неверный тип параметра excluded_filenames: {type(excluded_filename_list)}. Нужен list')

        if target_dirpathes is None:
            raise Exception('Назначьте директории, где проводить очистку')
        elif isinstance(target_dirpathes, list):
            self._target_dirpath_list = target_dirpathes
        else:
            raise Exception(f'Неверный тип параметра target_dirpath_list: {type(target_dirpathes)}. Нужен list')

        self._max_file_lifetime_in_seconds = max_file_lifetime_in_secs

    def clear_dirs(self):
        for target_dir in self._target_dirpath_list:
            for filename in os.listdir(target_dir):
                filepath = os.path.join(target_dir, filename)
                if not os.path.isdir(filepath):
                    target_file = pathlib.Path(filepath)
                    if datetime.now().timestamp() - target_file.stat().st_mtime <= self._max_file_lifetime_in_seconds:
                        print('KEEP', filename)
                    else:
                        if filename not in self._excluded_filenames:
                            print('DELETE', filename)
                            os.remove(target_file)

    def set_interval(self, seconds: int):
        while True:
            self.clear_dirs()
            time.sleep(seconds)

    def set_excluded_files(self, files: list):
        self._excluded_filenames = files


if __name__ == '__main__':
    args = sys.argv
    interval_sec = 60 * 60 * 24
    for arg in args:
        if arg.startswith('set_interval_in_days'):
            interval_sec = int(arg.split('=')[1]) * interval_sec
            break

    f_cleaner = FilesCleaner(
        target_dirpathes=target_dirpath_list,
        max_file_lifetime_in_secs=max_file_lifetime_in_seconds,
        excluded_filename_list=excluded_filenames
    )

    f_cleaner.set_interval(interval_sec)
