#!/usr/bin/env python3
"""Hangman example
"""
from json import loads, dumps
from urllib.request import urlopen, Request
from tiramisu_json_api import Config
from tiramisu_cmdline_parser import TiramisuCmdlineParser


class RemoteConfig(Config):
    def __init__(self,
                 url):
        json = loads(urlopen(url).read())
        super().__init__(json)
        self.url = url

    def send_data(self,
                  updates):
        request = Request(self.url, dumps(updates).encode(), method='POST')
        return loads(urlopen(request).read())


def main():
    config = RemoteConfig('http://localhost:8000')
    parser = TiramisuCmdlineParser(config)
    parser.parse_args()
    config = parser.get_config()
    print(config.value.dict())


if __name__ == "__main__":
    main()
