#
# config.py
#
# futaba - A Discord Mod bot for the Programming server
# Copyright (c) 2017-2018 Jake Richardson, Ammon Smith, jackylam5
#
# futaba is available free of charge under the terms of the MIT
# License. You are free to redistribute and/or modify it under those
# terms. It is distributed in the hopes that it will be useful, but
# WITHOUT ANY WARRANTY. See the LICENSE file for more details.
#

'''
Loads configuration files from disk
'''

from collections import namedtuple

import toml

from futaba.exceptions import InvalidConfigError

__all__ = [
    'Configuration',
    'load_config',
]

Configuration = namedtuple(
    'Configuration', (
        'token',
        'owner_ids',
        'default_prefix',
        'python_emoji_id',
        'discord_py_emoji_id',
        'database_url',
    ),
)

def _get(config, field, path=None):
    if field not in config:
        if path is None:
            return InvalidConfigError(f"No '{field}' section found in configuration.", config)
        else:
            return InvalidConfigError(f"No '{path}.{field}' field found in configuration.", config)

    return config[field]

def load_config(path):
    with open(path) as fh:
        config = toml.load(fh)

    config_bot = _get(config, 'bot')
    token = _get(config_bot, 'token', 'bot')
    prefix = _get(config_bot, 'prefix', 'bot')

    try:
        owner_ids = [int(id) for id in _get(config_bot, 'owners', 'bot')]
    except ValueError:
        raise InvalidConfigError("Owner IDs must be integers", config)

    config_emoji = _get(config, 'emojis')

    try:
        python_emoji_id = int(_get(config_emoji, 'python', 'emojis'))
        discord_py_emoji_id = int(_get(config_emoji, 'discordpy', 'emojis'))
    except ValueError:
        raise InvalidConfigError("Emoji IDs must be integers", config)

    config_db = _get(config, 'database')
    db_url = _get(config_db, 'url', 'database')

    return Configuration(
        token=token,
        owner_ids=owner_ids,
        default_prefix=prefix,
        python_emoji_id=python_emoji_id,
        discord_py_emoji_id=discord_py_emoji_id,
        database_url=db_url,
    )