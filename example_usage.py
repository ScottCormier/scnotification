import random

from slack import Notify

# Initialize the notification and set what channel to send to
notify = Notify(channel="MayaServer")


def basic_usage():
    # send a basic message to the channel
    response = notify.send.message("basic_usage()", "example of a single message being sent.")
    print("| Response::basic_usage: {}".format(response))

    # send a batch of message
    response = notify.send.message("basic_usage()", ["example of multiple messages being sent", "to a channel =]"])
    print("| Response::basic_usage: {}".format(response))


def send_warnings():
    original_state = notify.send.send_warnings
    response = notify.send.warning("send_warnings() 1/2", ["example of a warning being sent",
                                                           "two of these are sent but only one should get through",
                                                           "notify.send_warning is {}".format(
                                                               notify.send.send_warnings)])
    print("| Response::send_warnings()::1/2:notify.send_warning={}: {}".format(notify.send.send_warnings, response))
    notify.send.send_warnings = not notify.send.send_warnings
    response = notify.send.warning("send_warnings() 2/2", ["example of a warning being send",
                                                           "two of these are sent but only one should get through",
                                                           "notify.send_warning is {}".format(
                                                               notify.send.send_warnings)])
    print("| Response::send_warnings()::2/2:notify.send_warning={}: {}".format(notify.send.send_warnings, response))
    notify.send.send_warnings = original_state


def send_errors():
    original_state = notify.send.send_errors
    response = notify.send.error("send_errors() 1/2", ["example of an error being sent",
                                                       "two of these are sent but only one should get through",
                                                       "notify.send_errors is {}".format(notify.send.send_errors)])
    print("| Response::send_errors()::1/2: notify.send_error={}: {}".format(notify.send.send_errors, response))
    notify.send.send_errors = not notify.send.send_errors
    response = notify.send.error("send_errors() 2/2", ["example of an error being sent",
                                                       "two of these are sent but only one should get through",
                                                       "notify.send_errors is {}".format(notify.send.send_errors)])
    print("| Response::send_errors()::2/2: notify.send_error={}: {}".format(notify.send.send_errors, response))
    notify.send.send_errors = original_state


def filter_message():
    message = ["\n", "{}", "sync", "example of a message getting filtered"]
    message.append("unfiltered message: {}".format(str(message)))
    message.append("the messages '\n', '{}', 'sync', should have been removed =]")
    response = notify.send.message("filter_message()", message)
    print("| Response::filter_message(): filtered: {}".format(response))

    additional_filters = ["lol", "foo", "bar"]
    notify.send.filters.extend(additional_filters)

    # You can add new filters dynamically (these wont be written to the config)
    message = ["lol", "foo", "bar",
               "example of adding filters",
               "adding: 'lol', 'foo', 'bar'",
               "new filters: {}".format(str(notify.send.filters)),
               "the first three messages (lol, foo, bar) should not appear in this message."]

    response = notify.send.message("filter_message()", message)
    print("| Response::filter_message(): added and filtered: {}".format(response))


def message_collection_example():
    count = 0
    success = []
    failed = []

    # example usage of message collection
    while count < 10:
        count += 1
        if random.getrandbits(1):
            success.append("{} Succeeded".format(count))
            continue
        failed.append("{} Failed".format(count))

    response = notify.send.warning("Warning", failed)
    print("| Response::message_collection_example(): {}".format(response))
    response = notify.send.error("Error", failed)
    print("| Response::message_collection_example(): collection of errors {}".format(response))

    # Alternative usage of message collection, sending individual explicit warnings
    responses = []
    for message in failed:
        responses.append(notify.send.warning("Warning", message))
    print("| Response::message_collection_example(): explicit single{}".format(responses))


def misc_examples():
    # Example usage of the exposed config attributes
    # color overrides for different types of messages
    response = notify.send.message("misc_examples(): message color override: named",
                                   ["example of a named color override for a message"], color="info")
    print("| Response::misc_examples(): color override: named color {}".format(response))
    response = notify.send.message("misc_examples(): message color override: hex",
                                   ["example of a hex color override for a message"], color="#990099")
    print("| Response::misc_examples(): {}".format(response))
    response = notify.send.error("misc_examples(): error color override: named",
                                 ["example of a named color override for an error"], color="info")
    print("| Response::misc_examples(): color override: errors {}".format(response))
    response = notify.send.warning("misc_examples(): warning color override: named",
                                   ["example of a named color override for a warning"], color="info")
    print("| Response::misc_examples(): color override: errors {}".format(response))

    # verbosity validation allowing message suppression
    message_range = range(0, 10)
    response = None
    message_collection = ["example of message verbosity controlling which messages get sent",
                          "verbosity is set {} for this channel".format(notify.send.verbose)]

    for integer in message_range:
        if notify.send.verbose:
            message_collection.append("message {}/{}".format(integer + 1, len(message_range)))
        else:
            message_collection.append(["suppressing the following {} message/s.".format(len(message_range))])
            break

    if message_collection:
        response = notify.send.message("misc_examples(): verbose", message_collection)
        print("| Response::misc_examples(): verbose {}".format(response))

    if not response and not message_collection:
        print("| Response::misc_examples(): verbose: {}".format(
            "no messages collected or sent, something may have gone wrong."))


if __name__ == "__main__":
    print("Notifying URL: {}".format(notify.send.url))
    print("Config Path: {}".format(notify.config_path))
    print("Verbosity is: {}".format(notify.send.verbose))
    print("Send Warnings: {}".format(notify.send.send_warnings))
    print("Send Errors: {}".format(notify.send.send_errors))
    print("Filters: {}".format(notify.send.filters))
    print("Available Colors: {}".format(notify.send.colors))
    print("-" * 10)
    basic_usage()
    print("-" * 10)
    send_warnings()
    print("-" * 10)
    send_errors()
    print("-" * 10)
    filter_message()
    print("-" * 10)
    message_collection_example()
    print("-" * 10)
    misc_examples()
    print("FIN")
