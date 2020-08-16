import argparse
import json
from argparse import Namespace


def parse() -> "Namespace":
    parser = argparse.ArgumentParser(
        description="Extract websocket messages from a HAR file"
    )
    parser.add_argument(
        "filepath",
        type=str,
        help="Path to the HAR file to read"
    )
    parser.add_argument(
        "destination",
        type=str,
        nargs="?",
        default="websocket_messages.txt",
        help="Path to write websocket messages"
    )
    return parser.parse_args()


def extract_to_file(filepath: str, destination: str) -> None:
    with open(filepath, "r") as f:
        json_content = json.loads(f.read())
    websocket_entry = next((
        entry for entry in json_content["log"]["entries"]
        if entry["_resourceType"] == "websocket"
    ))
    websocket_messages = websocket_entry["_webSocketMessages"]
    with open(destination, "w") as f:
        f.writelines([
            f"{message['time']},{message['type']},{message['opcode']},{message['data']}\n"
            for message in websocket_messages
        ])


def process(args: "Namespace") -> None:
    extract_to_file(filepath=args.filepath, destination=args.destination)


def main():
    args = parse()
    process(args)


if __name__ == "__main__":
    main()
