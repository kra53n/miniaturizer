from time import strftime
from sys import exit

from os import walk
from os import getcwd
import os.path

from yaml import safe_load
from yaml import dump


def get_date():
    return {
        "day": int(strftime("%d")),
        "month": int(strftime("%m")),
    }

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

    def create_file(data, filename):
        """
        Create file with name in lowercase with `.yaml` extension
        Arguments:
            0) data - data that you want to load
            0) name - name of file without extension
        """
        filename = filename.lower() + ".yaml"
        create_file(data, filename)


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

    def update_limiter(self, filename, path=""):
        """
        Arguments:
          0) filename - name of file with extension
          1) path - path where file is lying
        """
        data = open_file(filename)
        date = get_date()
        if (date["day"] - data["day"]) >= data["period"]:
            data["day"] = date["day"]
            if (data["limit"] - data["period"]) > 0:
                data["limit"] = data["limit"] - data["period"]
        create_file(data, filename)
    
    def show_info(self, filename, path=""):
        data = open_file(filename)
        show = (
            "day",
            "limit",
            "period",
            "step",
        )
        for i in show:
            print("{}: {}".format(i.capitalize(), data[i]))

    def __define_changes(self, filename):
        """
        Identify what changes can be in file
        """
        return open_file(filename).keys()

    def edit(self, filename):
        data = open_file(filename)
        # choosing parameter to chage
        data_keys = self.__define_changes(filename)
        data_keys = tuple(data_keys)
        message = "Choose parameter to change:\n"
        for i in range(len(data_keys)):
            message += "  {}. {}\n".format(i+1, data_keys[i].capitalize())
        option = int(input(message + "Your parameter: ")) - 1
        key = data_keys[option]
        print("  {}: {}".format(key.capitalize(), data[key]))
        # working with paremeter
        parameter = input("On what parameter you want change {}: ".format(
            key.capitalize()
        ))
        parameter = type(data[key])(parameter)
        data[key] = parameter
        create_file(data, filename)


class Cli:
    def __init__(self, path):
        self.path = path
        self.progname = "Miniaturizer"
        while 1:
            try:
                self.__menu()
            except KeyboardInterrupt:
                print()
                self.__notify("Exiting from Miniaturizer")
                exit()

    def __show_menu(self):
        message = self.progname
        print(message)
        for count, opt in enumerate(Settings.menu_options_list, start=1):
            print(f" {count}. {opt.capitalize()}")
        print()

    def __menu(self):
        self.__show_menu()
        option =  int(input("Choose your option: "))-1
        options = Settings.menu_options_list
        if options[option] == "edit":
            self.__editing()
        if options[option] == "create":
            self.__creating_file()
        if options[option] == "show info":
            self.__showing_info()

    def __choosing_limiter(self):
        paths, files = Yaml.parse_yaml_extensions(path)
        filename = ""
        if len(files) == 0:
            print("You don`t have any files with `yaml`")
            return 0
        if len(files) > 0:
            print("Choosing limiter:")
            for i in range(len(files)):
                print("  {}. {}".format(i+1, files[i]))
            option = int(input("\nChoose limiter: ")) - 1
            filename = files[option]
            return filename

    def __editing(self):
        self.__notify("Editing mode")
        filename = self.__choosing_limiter()
        Dama().edit(filename)
        self.__notify("Parameter was changed")

    def __creating_file(self):
        self.__notify("Creating file")
        data = Dama().create_file()
        self.__notify("File %s was created" % (
            data["title"].lower() + ".yaml"))
    
    def __showing_info(self):
        """
        Arguments:
         0) path - path to working directory
        """
        filename = self.__choosing_limiter()
        Dama().update_limiter(filename)
        self.__notify("Showing %s" % filename)
        Dama().show_info(filename)
        input("\nTo continue push Enter")

    def __notify(self, text):
        print(":: " + text)


if __name__ == "__main__":
    path = getcwd()
    Cli(path)
