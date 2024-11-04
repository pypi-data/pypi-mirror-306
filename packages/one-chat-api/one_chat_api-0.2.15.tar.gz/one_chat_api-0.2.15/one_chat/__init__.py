# one_chat/__init__.py

from .one_chat import OneChat

one_chat_instance = None
default_to = None
default_bot_id = None


def init(authorization_token, to=None, bot_id=None):
    global one_chat_instance, default_to, default_bot_id
    one_chat_instance = OneChat(authorization_token)
    default_to = to
    default_bot_id = bot_id


def send_message(to=None, bot_id=None, message=None, custom_notification=None):
    if one_chat_instance is None:
        raise Exception(
            "OneChat is not initialized. Call init(authorization_token, to, bot_id) first."
        )

    to = to or default_to
    bot_id = bot_id or default_bot_id

    if not to or not bot_id:
        raise ValueError(
            "Both 'to' and 'bot_id' must be provided either during initialization or when calling this method."
        )

    return one_chat_instance.send_message(to, bot_id, message, custom_notification)


def send_file(to=None, bot_id=None, file_path=None, custom_notification=None):
    if one_chat_instance is None:
        raise Exception(
            "OneChat is not initialized. Call init(authorization_token, to, bot_id) first."
        )

    to = to or default_to
    bot_id = bot_id or default_bot_id

    if not to or not bot_id:
        raise ValueError(
            "Both 'to' and 'bot_id' must be provided either during initialization or when calling this method."
        )

    return one_chat_instance.send_file(to, bot_id, file_path, custom_notification)

def send_webview(to=None, bot_id=None, url=None, custom_notification=None):
    if one_chat_instance is None:
        raise Exception(
            "OneChat is not initialized. Call init(authorization_token, to, bot_id) first."
        )

    to = to or default_to
    bot_id = bot_id or default_bot_id

    if not to or not bot_id:
        raise ValueError(
            "Both 'to' and 'bot_id' must be provided either during initialization or when calling this method."
        )

    return one_chat_instance.send_webview(to, bot_id, url, custom_notification)


def broadcast_message(bot_id=None, to=None, message=None):
    if one_chat_instance is None:
        raise Exception(
            "OneChat is not initialized. Call init(authorization_token, to, bot_id) first."
        )

    to = to or default_to
    bot_id = bot_id or default_bot_id

    if not to or not bot_id:
        raise ValueError(
            "Both 'to' and 'bot_id' must be provided either during initialization or when calling this method."
        )

    return one_chat_instance.broadcast_message(bot_id, [to], message)


def send_location(
    to=None,
    bot_id=None,
    latitude=None,
    longitude=None,
    address=None,
    custom_notification=None,
):
    if one_chat_instance is None:
        raise Exception(
            "OneChat is not initialized. Call init(authorization_token, to, bot_id) first."
        )

    to = to or default_to
    bot_id = bot_id or default_bot_id

    if not to or not bot_id:
        raise ValueError(
            "Both 'to' and 'bot_id' must be provided either during initialization or when calling this method."
        )

    return one_chat_instance.send_location(
        to, bot_id, latitude, longitude, address, custom_notification
    )


def send_sticker(to=None, bot_id=None, sticker_id=None, custom_notification=None):
    if one_chat_instance is None:
        raise Exception(
            "OneChat is not initialized. Call init(authorization_token, to, bot_id) first."
        )

    to = to or default_to
    bot_id = bot_id or default_bot_id

    if not to or not bot_id:
        raise ValueError(
            "Both 'to' and 'bot_id' must be provided either during initialization or when calling this method."
        )

    return one_chat_instance.send_sticker(to, bot_id, sticker_id, custom_notification)


def fetch_friends_and_groups(bot_id=None):
    if one_chat_instance is None:
        raise Exception(
            "OneChat is not initialized. Call init(authorization_token, to, bot_id) first."
        )

    bot_id = bot_id or default_bot_id

    if not bot_id:
        raise ValueError(
            "Bot ID must be provided either during initialization or when calling this method."
        )

    return one_chat_instance.fetch_friends_and_groups(bot_id)


def list_all_friends(bot_id=None):
    if one_chat_instance is None:
        raise Exception(
            "OneChat is not initialized. Call init(authorization_token, to, bot_id) first."
        )

    bot_id = bot_id or default_bot_id

    if not bot_id:
        raise ValueError(
            "Bot ID must be provided either during initialization or when calling this method."
        )

    return one_chat_instance.list_all_friends(bot_id)


def list_friend_ids(bot_id=None):
    if one_chat_instance is None:
        raise Exception(
            "OneChat is not initialized. Call init(authorization_token, to, bot_id) first."
        )

    bot_id = bot_id or default_bot_id

    if not bot_id:
        raise ValueError(
            "Bot ID must be provided either during initialization or when calling this method."
        )

    return one_chat_instance.list_friend_ids(bot_id)


def list_all_groups(bot_id=None):
    if one_chat_instance is None:
        raise Exception(
            "OneChat is not initialized. Call init(authorization_token, to, bot_id) first."
        )

    bot_id = bot_id or default_bot_id

    if not bot_id:
        raise ValueError(
            "Bot ID must be provided either during initialization or when calling this method."
        )

    return one_chat_instance.list_all_groups(bot_id)


def list_group_ids(bot_id=None):
    if one_chat_instance is None:
        raise Exception(
            "OneChat is not initialized. Call init(authorization_token, to, bot_id) first."
        )

    bot_id = bot_id or default_bot_id

    if not bot_id:
        raise ValueError(
            "Bot ID must be provided either during initialization or when calling this method."
        )

    return one_chat_instance.list_group_ids(bot_id)
