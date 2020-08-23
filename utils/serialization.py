from typing import Dict


def camel_to_snake(s):
    # https://stackoverflow.com/questions/1175208/elegant-python-function-to-convert-camelcase-to-snake-case
    return "".join(["_" + c.lower() if c.isupper() else c for c in s]).lstrip("_")


def keys_to_snake(data: Dict) -> Dict:
    result = {}
    for key, value in data.items():
        if isinstance(value, dict):
            value = keys_to_snake(value)
        if isinstance(key, str):
            key = camel_to_snake(key)
        result[key] = value

    return result
