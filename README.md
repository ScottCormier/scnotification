# Slack Notification Library
## About
This is a Slack notification library that simplifies message assembly and includes some quality of life features. It enables sending single messages, lists of messages as a single message, errors, and warnings.

Each message type allows for color overrides in the message attachment. Any hexadecimal value can be passed, but there is also a configurable dictionary that translates hex values to more human-readable strings. Default colors included are: 'default', 'success', 'info', 'warning', 'danger'.

There is a degree of validation, so if something goes wrong with the message assembly, an attempt to send an error notification will be made, wrapping and sending the initial payload.

## Setup
### Required Python Packages
* PyYAML==6.0.1
* Requests==2.31.0

You will need to set up incoming webhooks on each channel you want to send notifications to. After that, you need to declare the channels in the configuration.

The config uses Anchors and Aliases to produce a channel's configuration. You can learn more about anchors and aliases [here](https://www.educative.io/blog/advanced-yaml-syntax-cheatsheet). For our purposes, the general idea is to declare a base default template that can be overridden per channel.

### Default Channel Config
```yaml
Channels:
  Default:
    url: &url "{INCOMING WEBHOOKS URL}"
    attributes: &attributes
      verbose: False # Verbose toggle, used for validating if all messages should be sent
      post_errors: False # Error toggle, used to control if errors should be sent
      post_warnings: False # Warning toggle, used to control if warnings should be sent
      filter_messages: True # Filter toggle, used to control if messages will be filterd
      colors: &colors # Color dict, declares the human-readable -> hex values, others can be added here if needed
        default: "#0275d8"
        success: "#5cb85c"
        info: "#5bc0de"
        warning: "#f0ad4e"
        danger: "#C83E2D"
      filters: &filters [ "{}", "\n", "sync" ] # Filter list, list of messages to ignore
```
### Channel Configuration Override
From the default, you can merge the attributes and redeclare the values you wish to change. This will merge the default template with the new channel declaration.

```yaml
  MayaServer:
    url: "{DIFFERENT URL HERE}"
    attributes:
      <<: *attributes
      verbose: True
      post_errors: True
      post_warnings: True
      colors:
        <<: *colors
        success: "#FFFFFF"
      filters: *filters
```
Once you've declared some channels in the config, you should be able to send messages to your channels.

## Usages
```python
from slack import Notify

# Initialize the notification and set the channel to send to
notify = Notify(channel="MayaServer")

# Send a basic message to the channel
notify.send.message("sometitle", "somemessage")

# Send a batch of messages
notify.send.message("sometitle", ["somemessage", "someothermessage"])

# Send an error message
notify.send.error("someerrortitle", "someerrormessage")

# Send a warning message
notify.send.warning("somewarningtitle", "somewarningmessage")

# Example usage of message collection
import random
count = 0
success = []
failed = []

while count < 10:
    count += 1
    if random.getrandbits(1):
        success.append("{} Succeeded".format(count))
        continue
    failed.append("{} Failed".format(count))

notify.send.messages("Succeeded", success, color="success")
notify.send.messages("Error", failed, color="danger")
notify.send.error("Error", failed)

# Alternative usage of message collection, explicitly sending individual warnings
for message in failed:
    notify.send.warning("Warning", message)
```
## Send Attributes
Most of the following are extensions of the config and are available for easier in-place usage:

* `Notify.send.message`: Send a message string.
* `Notify.send.messages`: Send a list of messages in one message.
* `Notify.send.error`: Explicitly send an error notification.
* `Notify.send.warning`: Explicitly send a warning notification.
* `Notify.send.url`: The URL the current instance is sending notifications to.
* `Notify.send.filters`: List of messages to be filtered.
* `Notify.send.filter_messages`: Boolean config value to show if a channel is filtering messages.
* `Notify.send.colors`: Dictionary of color key-value pairs.
* `Notify.send.post_warnings`: Boolean config attribute to control if a channel is ignoring warnings.
* `Notify.send.post_errors`: Boolean config attribute to control if a channel is ignoring errors.
* `Notify.send.verbose`: Boolean config attribute to show if a channel is sending verbose messages.

Example usage of the exposed config attributes:

```python
for message in range(0, 10):
    if notify.send.verbose:
        notify.send.error("Verbose Error", "Message {}".format(message))
```

# Known Issues/bugs
* Trying to use `notify.send.error()` and pass a list as the message results in a weirdly formatted batch message

