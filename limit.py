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


class Settings:
    menu_options_list = (
        "edit",
        "create",
        "show info",
    )


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
        fls = []
        for root, dirs, files in walk(path):
            skip = False
            for skip_item in skip_dir:
                if skip_item in root[len(path):]:
                    skip = True
            if not skip:
                for fl in files:
                    paths.append(os.path.join(root, fl))
                    fls.append(fl)
        return paths, fls

    def parse_yaml_extensions(path):
        """
        Arguments:
            path - path to directory
        """
        ext = ".yaml"
        paths, files = Yaml.__parse_files(path)
        paths = [i for i in paths if i[len(i)-len(ext):] == ext]
        files = [i for i in files if i[len(i)-len(ext):] == ext]
        return paths, files

    def create_file(data, name):
        """
        Create file with name in lowercase with `.yaml` extension
        Arguments:
            0) data - data that you want to load
            0) name - name of file without extension
        """
        name = name.lower() + ".yaml"
        create_file(data, name)


class Dama:
    """
    Dama - data manipulation
    Manipulation with data from `*.yaml` files
    """
    def create_file(self):
        data = get_date()
        data.update(self.setup_config())
        Yaml.create_file(data, data["title"])
        return data

    def setup_config(self):
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

    def show_info(self, path):
        """
        Arguments:
         0) path - path to working directory
        """
        paths, files = Yaml.parse_yaml_extensions(path)
        filename = ""
        if len(files) == 0:
            print("You don`t have any `yaml` files")
            return 0
        if len(files) > 0:
            print("Choose limiter:")
            for i in range(len(files)):
                print("\t{}. {}".format(i+1, files[i]))


class Cli:
    def __init__(self, path):
        self.path = path
        self.__menu()
        #data = self.__processing_file(path)
        #if data == "update":
        #    data = self.__processing_file(path)
        #if data:
        #    print(data)

    def __show_menu(self):
        message = "miniaturizer\n".capitalize()
        options = Settings.menu_options_list
        print(message)
        [print("  {}. ".format(i+1), options[i]) for i in range(len(options))]

    def __menu(self):
        self.__show_menu()
        option =  int(input("Choose your option: "))-1
        options = Settings.menu_options_list
        if options[option] == "edit":
            pass
        if options[option] == "create":
            #Dama().create_file()
            self.__creating_file()
        if options[option] == "show info":
            Dama().show_info(self.path)

    def __creating_file(self):
        self.__notify("Creating file")
        data = Dama().create_file()
        self.__notify("File %s was created" % (
            data["title"].lower() + ".yaml"))

    def __notify(self, text):
        print(":: " + text)

    #def __show_info(self, path):
    #    """
    #    Arguments:
    #     0) path - path to working directory
    #    """
    #    paths, files = Yaml.parse_yaml_extensions(path)
    #    filename = ""
    #    if len(files) == 0:
    #        print("You don`t have any `yaml` files")
    #        return 0
    #    if len(files) > 0:
    #        print("Choose limiter:")
    #        for i in range(len(files)):
    #            print("\t{}. {}".format(i+1, files[i]))
    #        option = int(input("Enter your option: "))
    #        if option == (len(files) + 1):
    #            self.__create_file()
    #            return "update"
    #        path = paths[option-1]
    #    return open_file(path)


if __name__ == "__main__":
    path = getcwd()
    Cli(path)
