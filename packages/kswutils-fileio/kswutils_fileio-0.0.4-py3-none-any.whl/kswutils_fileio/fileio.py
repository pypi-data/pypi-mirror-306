import os
import pickle
import logging
from datetime import datetime


# Path vs Directory
# Path is the directory to an object (a file)
# Path: Obj
# Directory: Folder


class FileIO:

    @staticmethod
    def get_subdirectories(dir, **kwargs):
        """get sub-directories / sub-paths

        Args:
            dir (string or list): target directory(ies).
            skips (optional): default: ['.DS_Store', '__pycache__', '.ipynb_checkpoints']

        Returns:
            list: (1d list): a *sorted* list of subdirectories / subpaths.
        """

        _skips_ = [".DS_Store", "__pycache__", ".ipynb_checkpoints"]

        skips = kwargs.get("skips", _skips_)

        if not isinstance(dir, list):
            dir_ls = [dir]

        sub_dir_ls_all = []

        for each_dir in dir_ls:
            sub_dir_ls = os.listdir(each_dir)

            for d in sub_dir_ls:
                if os.path.basename(d) in skips:
                    continue

                sub_dir_ls_all.append(os.path.join(each_dir, d))

        # try:
        #     from natsort import natsorted
        #     # print("\nUsing natsorted(), Beware of file names containing numbers!\n")
        #     return natsorted(sub_dir_ls_all)
        # except:
        # print("\nUsing sorted(), Beware of file names containing numbers!\n")
        # return sorted(sub_dir_ls_all)  # Capital letter --> Small letter

        # == Note == #
        # I don't think it is a good idea to sort the files at the first place.
        # The files should be sorted project-wised, depending on the applications.
        # NOTE This change will affect some previous development!

        return sub_dir_ls_all

    @staticmethod
    def create_logger():
        dir_path = os.path.join(os.getcwd(), "log")
        filename = "{:%Y-%m-%d_%H-%M-%S}".format(datetime.now()) + ".log"

        logging.captureWarnings(True)
        formatter = logging.Formatter("%(asctime)s %(levelname)s %(message)s")
        logger = logging.getLogger("py.warnings")
        logger.setLevel(logging.INFO)

        if not os.path.exists(dir_path):
            os.makedirs(dir_path)

        fileHandler = logging.FileHandler(dir_path + "/" + filename, "w", "utf-8")
        fileHandler.setFormatter(formatter)
        logger.addHandler(fileHandler)

        consoleHandler = logging.StreamHandler()
        consoleHandler.setLevel(logging.DEBUG)
        consoleHandler.setFormatter(formatter)
        logger.addHandler(consoleHandler)

        return logger

    @staticmethod
    def read_pickle(path):
        with open(path, "rb") as f:
            obj = pickle.load(f)
        return obj

    @staticmethod
    def write_pickle(obj, **kwargs):
        """write object to pickle

        Args:
            obj: object to save as pickle
            savepath: opt. default './new.pickle'

        Returns:
            None
        """
        _savepath = kwargs.get("savepath", "./new.pickle")

        with open(_savepath, "wb") as f:
            pickle.dump(obj, f)
        # In Python 2 document, while serializing, use '.pkl'
        # In Python 3 document, while serializing, use '.pickle'
        return None

    @staticmethod
    def make_dir(dir):
        try:
            os.makedirs(dir)
        except:
            return False
        return True

    @staticmethod
    def is_exsit(dir):
        return os.path.exists(dir)

    @staticmethod
    def get_name_with_extion(dir):
        return os.path.basename(dir)

    @staticmethod
    def get_name_without_extion(dir):
        return os.path.basename(dir).split(".")[0]
