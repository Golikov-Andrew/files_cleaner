import os
import sys
import time
import pathlib
from datetime import datetime


class FilesCleaner:

    def __init__(self, target_dirpathes_dict: dict, excluded_filename_list=None,
                 is_logging_enabled=False, log_filepath='files_cleaner.log'):
        """Чистильщик файлов"""

        if excluded_filename_list is None:
            self.__excluded_filenames = list()
        elif isinstance(excluded_filename_list, list):
            self.__excluded_filenames = excluded_filename_list
        else:
            raise Exception(f'Неверный тип параметра excluded_filenames: {type(excluded_filename_list)}. Нужен list')

        if target_dirpathes_dict is None:
            raise Exception('Назначьте директории, где проводить очистку')
        elif isinstance(target_dirpathes_dict, dict):
            self.__target_dirpath_dict = target_dirpathes_dict
        else:
            raise Exception(f'Неверный тип параметра target_dirpathes_dict: {type(target_dirpathes_dict)}. Нужен dict')

        self.__count_of_deleted_files = 0
        self.__is_logging_enabled = is_logging_enabled
        self.__log_filepath = log_filepath

    def log(self, *messages):
        result_text = [str(datetime.now())]
        result_text.extend([*messages])
        result_text = [str(i) for i in result_text]
        text = '\t'.join(result_text)
        print(text)
        if self.__is_logging_enabled:
            with open(self.__log_filepath, 'a') as f:
                f.write(text + '\n')

    def clear_dirs(self):
        for target_dir, lifetime_in_seconds in self.__target_dirpath_dict.items():
            for filename in os.listdir(target_dir):
                filepath = os.path.join(target_dir, filename)
                if not os.path.isdir(filepath):
                    target_file = pathlib.Path(filepath)
                    if datetime.now().timestamp() - target_file.stat().st_mtime > lifetime_in_seconds:
                        if filename not in self.__excluded_filenames:
                            self.log('delete file ->', filepath)
                            os.remove(target_file)
                            self.__count_of_deleted_files += 1

    def set_interval(self, seconds: int):
        self.log(f'interval_sec={interval_sec}',)
        while True:
            self.log('start iteration',)
            self.reset_count_of_deleted_files()
            self.clear_dirs()
            self.log('total files deleted ->', self.get_count_of_deleted_files())
            time.sleep(seconds)

    def set_excluded_files(self, files: list):
        self.__excluded_filenames = files

    def reset_count_of_deleted_files(self):
        self.__count_of_deleted_files = 0

    def get_count_of_deleted_files(self):
        return self.__count_of_deleted_files


if __name__ == '__main__':
    from cfg import target_dirpath_dict, excluded_filenames, is_logging_enabled, log_filepath

    args = sys.argv
    interval_sec = 60 * 60 * 24
    for arg in args:
        if arg.startswith('set_interval_in_seconds'):
            interval_sec = int(float(arg.split('=')[1]))
            break

    f_cleaner = FilesCleaner(
        target_dirpathes_dict=target_dirpath_dict,
        excluded_filename_list=excluded_filenames,
        is_logging_enabled=is_logging_enabled,
        log_filepath=log_filepath
    )

    f_cleaner.set_interval(interval_sec)
