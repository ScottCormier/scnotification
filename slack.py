import os
import yaml

from send import Send


class Config:
    def __init__(self, channel):
        self.config_path = "{}/config/slack.yaml".format(os.path.dirname(__file__))
        loaded_config = self._load_file(self.config_path)

        if channel not in loaded_config["Channels"].keys():
            raise ValueError("Channel '{}' not found in config".format(channel))

        self._contents = loaded_config["Channels"][channel]

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
        super(Notify, self).__init__(channel=channel)
        config = self.get_config()
        self.send = Send(config)
