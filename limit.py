from time import strftime

from os import walk
from os import getcwd
import os.path

from yaml import safe_load
from yaml import dump


def get_date():
    date = {}
    date["day"] = strftime("%d")
    date["week"] = strftime("%m")
    return date

def create_file(data, filename):
    with open(filename, "w") as f:
        dump(data, f)

def open_file(filename):
    with open(filename, "r") as f:
        date = safe_load(f)
    return date

def matrix_to_list(matrix):
    lst = []
    for i in matrix:
        lst.extend(i)
    return lst


class Yaml:
    """
    Working with yaml file formats
    """
    def __parse_files(path):
        """
        Arguments:
            path - path to directory
        """
        # names of dirs that you want to skip
        skip_dir = (
            ".git",
        )
        paths = []
        for root, dirs, files in walk(path):
            skip = False
            for skip_item in skip_dir:
                if skip_item in root[len(path):]:
                    skip = True
            if not skip:
                for fl in files:
                    paths.append(os.path.join(root, fl))
        return paths

    def parse_yaml_extensions(path):
        """
        Arguments:
            path - path to directory
        """
        ext = ".yaml"
        files = Yaml.__parse_files(path)
        files = [i for i in files if i[len(i)-len(ext):] == ext]
        return files


class Data:
    """
    Manipulation with data from `*.yaml` files
    """
    pass


class Cli:
    def __init__(self, path):
        data = self.__processing_file(path)
        if data:
            print(data)
        if not data:
            data = self.__processing_file(path)
            self.__notify("File %s was created" % (
                data["title"].lower() + ".yaml"))

    def __notify(self, text):
        print(":: " + text)

    def __processing_file(self, path):
        try:
            files = Yaml.parse_yaml_extensions(path)
            filename = ""
            if len(files) == 1:
                fl = files[0]
                print("Choose option:")
                message = "1. Open {}\n".format(fl)
                message += "2. Create new limiter\n"
                option = int(input(message + "Enter your option: "))
                if option == 1:
                    self.__notify("Open %s file" % (fl + ".yaml"))
                    filename = fl
                if option == 2:
                    self.__create_file()
            if len(files) > 1:
                print("Choose enter:")
                [print("\t".format(i+1, files[i])) for i in range(len(files))]
                filename = files[int(input(print("Your enter: "))) - 1]
            return open_file(filename)
        except FileNotFoundError:
            self.__create_file()

    def __create_file(self):
        data = get_date()
        data.update(self.__setup_config())
        self.filename = data["title"].lower() + ".yaml"
        create_file(data, filename=self.filename)

    def __setup_config(self):
        title = input("What title of limit you want? ")
        limit = int(input("What the maximum in your limit? "))
        step = int(input("What the step that will reduce your limit? "))
        period = int(input("What period it will be changed?(days) "))
        return {
        "title": title,
        "limit": limit,
        "step": step,
        "period":period,
        }


if __name__ == "__main__":
    path = getcwd()
    Cli(path)
