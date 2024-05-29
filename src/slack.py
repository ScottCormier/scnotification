import os
import yaml

from scnotification.src.send import Send


class Config:
    def __init__(self):
        self.config_path = "{}/config/slack.yaml".format(os.path.dirname(__file__))
        loaded_config = self._load_file(self.config_path)
        self.channels = loaded_config["Channels"].keys()
        self._contents = loaded_config["Channels"]

    def _load_file(self, config_file):
        with open(config_file, "r") as config:
            contents = yaml.safe_load(config)
        return contents

    def get_config(self):
        return self._contents


class Notify(Config):
    def __init__(self, channel=None, broadcast=False):
        if not channel:
            channel = "Default"
        super(Notify, self).__init__()
        print("=" * 10)
        print("Registering Channel: {}".format(channel))
        config = self.get_config()
        if channel not in config.keys():
            raise ValueError("Channel '{}' not found in config".format(channel))

        self.name = config[channel]["attributes"]["name"]
        self.verbose = config[channel]["attributes"]["verbose"]
        self.url = config[channel]["url"]
        self.send = Send(config[channel])

        print("|----Name: {}".format(self.name))
        print("|----Config: {}".format(self.config_path))
        print("|----URL: {}".format(self.url))
        print("|----Send Object: {}".format(self.send))
        print("|----Verbose: {}".format(self.verbose))
        print("|----Errors: {}".format(config[channel]["attributes"]["send_errors"]))
        print("|----Warnings: {}".format(config[channel]["attributes"]["send_warnings"]))
        print("|----Filter: {}".format(config[channel]["attributes"]["filter_messages"]))
        print("|----Filters: {}".format(config[channel]["attributes"]["filters"]))
        print("|----Colors: {}".format(config[channel]["attributes"]["colors"]))



if __name__ == "__main__":
    config = Notify("ScFiles")
    loaded = config.get_config()
    print(config.channels)
