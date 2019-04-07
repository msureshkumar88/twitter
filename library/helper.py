import logging

import re

class Helper:
    @classmethod
    def validate_string(cls, word):
        word = word.strip()
        return re.search('^[a-zA-Z]+$', word)