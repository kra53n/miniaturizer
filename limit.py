from pathlib import Path
from time import strftime
from os import walk, getcwd
from yaml import safe_load, dump


MENU_OPTS = (
    "edit",
    "create",
    "show files",
    "exit",
)


def get_date():
    return {
        "day": int(strftime("%d")),
        "month": int(strftime("%m")),
    }


class Yaml:
    """
    Working with yaml file formats
    """
    ext = ".yaml"

    @staticmethod
    def create_file(data, filename):
        filename = filename if '.yaml' in filename else f'{filename}{Yaml.ext}'
        with open(filename, "w") as f:
            dump(data, f)

    @staticmethod
    def open_file(filename):
        return safe_load(Path(filename).read_text())

    def __parse_files(path):
        """
        Arguments:
            path - path to directory
        """
        skip_dirs = (".git")

        # add to path and fls paths and files without files of skip_dirs
        paths, fls = [], []
        for root, dirs, files in walk(path):
            if not any((skip_item in root[len(path):] for skip_item in skip_dirs)):
                for fl in files:
                    paths.append(str(Path(root) / fl))
                    fls.append(fl)
        return paths, fls

    def parse_yaml_extensions(path):
        """
        Arguments:
            path - path to directory
        """
        paths, files = Yaml.__parse_files(path)
        paths = [i for i in paths if i[len(i)-len(Yaml.ext):] == Yaml.ext]
        files = [i for i in files if i[len(i)-len(Yaml.ext):] == Yaml.ext]
        return paths, files


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
        title = input("Title: ")
        limit = int(input("Maximum in limit: "))
        step = float(input("Reduction step: "))
        period = int(input("Period(days): "))

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
        data = Yaml.open_file(filename)
        date = get_date()
        if date["day"] - data["day"] >= data["period"]:
            data["day"] = date["day"]
            if data["limit"] - data["period"] > 0:
                data["limit"] = data["limit"] - data["period"]
        Yaml.create_file(data, filename)
    
    def show_info(self, filename, path=""):
        data = Yaml.open_file(filename)
        show = ("day", "limit", "period", "step")
        for elem in show:
            print("{}: {}".format(elem.capitalize(), data[elem]))

    def __define_changes(self, filename):
        """
        Identify what changes can be in file
        """
        return Yaml.open_file(filename).keys()

    def edit(self, filename):
        data = Yaml.open_file(filename)
        # choosing parameter to chage
        data_keys = tuple(self.__define_changes(filename))
        message = "Choose parameter to change:\n"
        for i in range(len(data_keys)):
            message += "  {}. {}\n".format(i+1, data_keys[i].capitalize())

        option = int(input(message + "Your parameter: ")) - 1
        key = data_keys[option]
        print("  {}: {}".format(key.capitalize(), data[key]))
        # working with paremeter
        parameter = input("On what parameter you want change {}: ".format(key.capitalize()))
        parameter = type(data[key])(parameter)
        data[key] = parameter
        Yaml.create_file(data, filename)


class Cli:
    def __init__(self, path):
        self.path = path
        self.progname = "Miniaturizer"

        while True:
            try:
                self.__menu()
            except KeyboardInterrupt:
                self.__exit()

    def __exit(self):
        self.__notify("Exit")
        exit()

    def __show_menu(self):
        message = self.progname
        print(message)
        for count, opt in enumerate(MENU_OPTS, start=1):
            print(f" {count}. {opt.capitalize()}")
        print()

    def __menu(self):
        self.__show_menu()
        opt =  int(input("Choose your option: ")) - 1

        match MENU_OPTS[opt]:
            case "edit":
                self.__editing()
            case "create":
                self.__creating_file()
            case "show info":
                self.__showing_info()
            case "exit":
                self.__exit()

    def __choosing_limiter(self):
        paths, files = Yaml.parse_yaml_extensions(path)
        filename = ""

        match len(files):
            case 0:
                print("You don`t have any files with `yaml`")
                return 0
            case _:
                print("Choosing limiter:")
                for i in range(len(files)):
                    print("  {}. {}".format(i+1, files[i]))
                opt = int(input("\nChoose limiter: ")) - 1
                filename = files[opt]
                return filename

    def __editing(self):
        self.__notify("Editing mode")
        filename = self.__choosing_limiter()
        Dama().edit(filename)
        self.__notify("Parameter was changed")

    def __creating_file(self):
        self.__notify("Creating file")
        data = Dama().create_file()
        filename = data["title"].lower() + Yaml.ext
        self.__notify(f"File {filename} was created")
    
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
