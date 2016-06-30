import os
import yaml
from gitcd.Exceptions import GitcdFileNotFoundException


class Parser:

    yaml = {}

    def load(self, filename: str):
        # raise exception if no .gitcd in current working dir
        if not os.path.isfile(filename):
            raise GitcdFileNotFoundException("File %s not found" % filename)

        # open and load .gitcd
        with open(filename, 'r') as stream:
            self.yaml = yaml.safe_load(stream)

        return self.yaml

    def write(self, filename: str, config: dict):
        with open(filename, "w") as outfile:
            outfile.write(yaml.dump(config, default_flow_style=False))
