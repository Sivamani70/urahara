import json
import os
import sys
import re
from PIL import Image
from pyzbar.pyzbar import decode


def eprint(*args, **kwargs):
    print(*args, file=sys.stderr, **kwargs)


class Main:
    url: set[str] = set()

    def __init__(self, file_path: list):
        self.file_path = [path for path in file_path if os.path.exists(path)]
        if os.name == 'nt':
            os.system('cls')
        else:
            os.system('clear')

    def process(self):

        print("Processing files:")
        print("---------------------")
        for f in self.file_path:
            print(f)

        print("Raw Dump:")
        print("---------------------")
        for img in self.file_path:
            image = Image.open(img)
            decoded_obj = decode(image)

            if decoded_obj:
                for obj in decoded_obj:
                    qr_data = obj.data.decode('utf-8')
                    print(qr_data)
                    try:
                        json_data = json.loads(qr_data)
                        self.flat_json(json_data)
                    except (json.JSONDecodeError, TypeError):
                        self.extract_url(qr_data)

    def extract_url(self, data: str):
        pattern = r'\b(?:(?:https?|ftp|file):\/\/|www\.|ftp\.)(?:\([-A-Z0-9+&@#\/%=~_|$?!:,."]*\)|[-A-Z0-9+&@#\/%=~_|$?!:,."])*(?:\([-A-Z0-9+&@#\/%=~_|$?!:,."]*\)|[A-Z0-9+&@#\/%=~_|$"])'
        uri = re.findall(pattern, data, re.IGNORECASE)
        for i in uri:
            self.url.add(i)

    def flat_json(self, obj: dict | list | str):
        if isinstance(obj, dict):
            for v in obj.values():
                self.flat_json(v)
        elif isinstance(obj, list):
            for i in obj:
                self.flat_json(i)
        elif isinstance(obj, str):
            self.extract_url(obj)

    def display(self):
        print("---------------------")
        print("Extracted information:")
        print("---------------------")
        for i in self.url:
            print(i)


if len(sys.argv) == 1:
    eprint("Error: Provide File Path which contains QR")
    sys.exit(1)

main = Main(sys.argv[1:])
main.process()
main.display()
