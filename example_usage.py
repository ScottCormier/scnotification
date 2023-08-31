import random

from slack import Notify

# Initialize the notification and set what channel to send to
notify = Notify(channel="MayaServer")


def basic_usage():
    # send a basic message to the channel
    response = notify.slack.message("basic_usage()", "example of a single message being sent.")
    print("| Response::basic_usage: {}".format(response))

    # send a batch of message
    response = notify.slack.message("basic_usage()", ["example of multiple messages being sent", "to a channel =]"])
    print("| Response::basic_usage: {}".format(response))


def send_warnings():
    original_state = notify.slack.send_warnings
    response = notify.slack.warning("send_warnings() 1/2", ["example of a warning being sent",
                                                            "two of these are sent but only one should get through",
                                                            "notify.send_warning is {}".format(
                                                                notify.slack.send_warnings)])
    print("| Response::send_warnings()::1/2:notify.send_warning={}: {}".format(notify.slack.send_warnings, response))
    notify.slack.send_warnings = not notify.slack.send_warnings
    response = notify.slack.warning("send_warnings() 2/2", ["example of a warning being send",
                                                            "two of these are sent but only one should get through",
                                                            "notify.send_warning is {}".format(
                                                                notify.slack.send_warnings)])
    print("| Response::send_warnings()::2/2:notify.send_warning={}: {}".format(notify.slack.send_warnings, response))
    notify.slack.send_warnings = original_state


def send_errors():
    original_state = notify.slack.send_errors
    response = notify.slack.error("send_errors() 1/2", ["example of an error being sent",
                                                        "two of these are sent but only one should get through",
                                                        "notify.send_errors is {}".format(notify.slack.send_errors)])
    print("| Response::send_errors()::1/2: notify.send_error={}: {}".format(notify.slack.send_errors, response))
    notify.slack.send_errors = not notify.slack.send_errors
    response = notify.slack.error("send_errors() 2/2", ["example of an error being sent",
                                                        "two of these are sent but only one should get through",
                                                        "notify.send_errors is {}".format(notify.slack.send_errors)])
    print("| Response::send_errors()::2/2: notify.send_error={}: {}".format(notify.slack.send_errors, response))
    notify.slack.send_errors = original_state


def filter_message():
    message = ["\n", "{}", "sync", "example of a message getting filtered"]
    message.append("unfiltered message: {}".format(str(message)))
    message.append("the messages '\n', '{}', 'sync', should have been removed =]")
    response = notify.slack.message("filter_message()", message)
    print("| Response::filter_message(): filtered:{}".format(response))

    new_filter_message = ["lol", "foo", "bar"]
    notify.slack.filters.extend(new_filter_message)

    # You can add new filters dynamically (these wont be written to the config)
    message = ["lol", "foo", "bar",
               "example of adding filters",
               "adding: 'lol', 'foo', 'bar'",
               "new filters: {}".format(str(notify.slack.filters)),
               "the first three messages (lol, foo, bar) should not appear in this message."]

    response = notify.slack.message("filter_message()", message)
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

    notify.slack.message("Succeeded", success, color="success")
    notify.slack.message("Error", failed, color="danger")
    notify.slack.warning("Error", failed)
    notify.slack.error("Error", failed)

    # Alternative usage of message collection, sending individual explicit warnings
    for message in failed:
        notify.slack.warning("Warning", message)


def dynamic_config_example():
    # Example usage of the exposed config attributes
    message_range = range(0, 10)
    message_collection = ["Verbosity is {}".format(notify.slack.verbose)]

    for integer in message_range:
        if notify.slack.verbose:
            message_collection.append("Message {}/{}".format(integer + 1, len(message_range)))
        else:
            message_collection.append("Suppressing the following {} message/s.".format(len(message_range)))
            break

    if message_collection:
        response = notify.slack.message("Verbosity: {}".format(notify.slack.verbose), message_collection)
        print("| Response::dynamic_config_examples(): Verbose {}".format(response))


if __name__ == "__main__":
    print("Notifying URL: {}".format(notify.slack.url))
    print("Verbosity is: {}".format(notify.slack.verbose))
    print("Send Warnings: {}".format(notify.slack.send_warnings))
    print("Send Errors: {}".format(notify.slack.send_errors))
    print("Filters: {}".format(notify.slack.filters))
    print("Available Colors: {}".format(notify.slack.colors))
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
    dynamic_config_example()
    print("FIN")
