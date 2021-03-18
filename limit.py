from os import walk
from time import strftime

from yaml import load
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
        date = load(f)
    return date


class Cli:
    def __init__(self):
        data = self.__process_file()
        if data:
            print("I have data")
        if not data:
            print("I create data")

    def __parse_yaml_extensions(self):
        pass

    def __process_file(self):
        try:
            return open_file()
        except FileNotFoundError:
            data = get_date()
            data.update(self.__setup_config())
            self.filename = data["title"]
            create_file(data, filename=self.filename)
            return 0

    def __setup_config(self):
        title = input("What title of limit you want? ")
        limit = int(input("What the maximum in your limit? "))
        step = int(input("What the step that will reduce your limit? "))
        period = int(input("What period it will be changed? "))
        return {
        "title": title,
        "limit": limit,
        "step": step,
        "period":period,
        }


if __name__ == "__main__":
    Cli()
