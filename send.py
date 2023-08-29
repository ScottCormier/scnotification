import requests


class Send:
    def __init__(self, config):
        super(Send, self).__init__()

        self.url = config["url"]
        self.headers = {'Content-Type': 'application/json'}

        self.verbose = config["attributes"]["verbose"]
        self.post_errors = config["attributes"]["post_errors"]
        self.post_warnings = config["attributes"]["post_warnings"]
        self.colors = config["attributes"]["colors"]
        self.filter_messages = config["attributes"]["filter_messages"]
        self.filters = config["attributes"]["filters"]

    def _build(self, title: str, messages: list, color: str) -> dict:
        """
        Builds and returns the payload for the title's notification
        :param title: str
        :param messages: list
        :param color: str
        :return: dict
        """
        title = self._get_header(title)
        messages = self._get_attachments(messages, color)
        return {"blocks": title, "attachments": [messages]}

    def _get_text(self, text: str) -> dict:
        """
        Takes a text input and returns a filled text template.
        :param text:
        :return:
        """
        return {"type": "plain_text", "text": text}

    def _get_section(self, text: str) -> dict:
        """
        Takes a text input and returns a filled section template.
        :param text: str
        :return: dict
        """
        return {"type": "section", "text": self._get_text(text)}

    def _get_header(self, title: str) -> list:
        """
        Takes the title and returns a filled header template
        :param title: str
        :return: dict
        """
        return [{"type": "header", "text": self._get_text(title)}]

    def _get_attachments(self, messages: list, color: str) -> dict:
        """
        Gets the attachments for a list of messages
        :param messages:
        :param color:
        :return:
        """
        filled_templates = []
        for message in messages:
            filled_templates.append(self._get_section(message))
        return {"color": color, "blocks": filled_templates}

    def _flatten_list(self, messages: list) -> list:
        """
        Recursively flattens a list down to a list of strings
        :param messages: list
        :return: list
        """
        flat_messages = []
        for message in messages:
            if isinstance(message, list):
                self._flatten_list(message)
            else:
                flat_messages.append(str(message))
        return flat_messages

    def _filter_messages(self, messages: list) -> list:
        """
        Filters message lists, notifies with a warning if warning posts are True
        :param messages: list
        :return: list
        """
        valid = []
        invalid = []
        for message in messages:
            if not self._validate_message(message):
                invalid.append(message)
                continue
            valid.append(message)
        return [valid, invalid]

    def _validate_message(self, message: str) -> bool:
        if message in self.filters:
            return False
        return True

    def _send(self, payload: dict, url=None, headers=None):
        """
        Sends a payload to the platform url
        :param payload: dict
        :param url: None
        :param headers: None
        :return: response
        """
        # print(payload)
        if not url:
            url = self.url
        if not headers:
            headers = self.headers
        response = requests.post(url, data=str(payload), headers=headers)
        return response

    def _validate_response(self, response) -> bool:
        """
        Validates a requests.status_code as not being 400
        :param response: requests
        :return: bool
        """
        if response.status_code == 200:
            return True
        return False

    def warning(self, title: str, warnings: list | str, color=None) -> requests.models.Response | str:
        if not color:
            color = self.colors["warning"]
        response = self.messages(title, warnings, color)
        return response

    def error(self, title: str, errors: list | str, color=None) -> requests.models.Response | str:
        if not color:
            color = self.colors["danger"]
        response = self.messages(title, errors, color)
        return response

    def messages(self, title: str, messages: list | str, color=None) -> requests.models.Response | str:
        """
        Sends a list of strings to the notification platform
        :param title: str
        :param messages: list
        :param color: None
        :return: response
        """

        if isinstance(messages, str):
            messages = [messages]

        # recursively flatten message list to a list of strings
        messages = self._flatten_list(messages)

        if self.filter_messages:
            messages, filtered = self._filter_messages(messages)
            if len(filtered) > 0 and self.post_warnings:
                filter_message = []
                for filtered_message in filtered:
                    filter_message.append("Filtered character {} from message".format(repr(filtered_message)))
                    print(filter_message)
                self.messages("Warning", filter_message)

        if not color:
            color = self.colors["default"]
        else:
            if color in self.colors.keys():
                color = self.colors[color]

        if not len(messages) > 0:
            return "Filtered messages resulted in 0 messages to send, ending notification request early"

        payload = self._build(title, messages, color)
        response = self._send(payload)

        if not self._validate_response(response) and self.post_errors:
            self.messages("Error sending messages:", messages)
        return response

    def message(self, title: str, message: str, color=None) -> requests.models.Response | str:
        """
        Sends a single message string to the notification platform
        :param title: str
        :param message: str
        :param color: None
        :return: response
        """
        return self.messages(title, message, color)
