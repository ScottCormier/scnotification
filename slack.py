import os
import yaml

from send import Send


class Config:
    def __init__(self):
        self.config_path = "{}/config/slack.yaml".format(os.path.dirname(__file__))
        loaded_config = self._load_file(self.config_path)
        self._contents = loaded_config["Channels"]

    def _load_file(self, config_file):
        with open(config_file, "r") as config:
            contents = yaml.safe_load(config)
        return contents

    def get_config(self):
        return self._contents


class Notify(Config):
    def __init__(self, channel=None):
        if not channel:
            channel = "Default"
        super(Notify, self).__init__()

        config = self.get_config()
        if channel not in config.keys():
            raise ValueError("Channel '{}' not found in config".format(channel))

        self.name = config[channel]["attributes"]["name"]
        self.verbose = config[channel]["attributes"]["verbose"]
        self.url = config[channel]["url"]
        self.send = Send(config[channel])


if __name__ == "__main__":
    config = Notify("ScFiles")
    print(config.channels)
