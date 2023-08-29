from slack import Notify

# Initialize the notification and set what channel to send to
notify = Notify(channel="MayaServer")

# send a basic message to the channel
notify.send.message("sometitle", "somemessage")

# send a batch of messages
notify.send.message("sometitle", ["somemessage", "someothermessage"])

# send an error message
notify.send.error("someerrortitle", "someerrormessage")

# send a warning message
notify.send.warning("somewarningtitle", "somewarningmessage")

# example usage of message collection
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
notify.send.warning("Error", failed)
notify.send.error("Error", failed)

# Alternative usage of message collection, sending individual explicit warnings
for message in failed:
    notify.send.warning("Warning", message)

# Example usage of the exposed config attributes
for message in range(0, 10):
    if notify.send.verbose:
        notify.send.error("Verbose Error", "Message {}".format(message))