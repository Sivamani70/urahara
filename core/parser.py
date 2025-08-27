import json
import os
import re
import sys
from logger.log import CustomLogger
from PIL import Image
from pyzbar.pyzbar import decode


class Qr:
    """
    The Qr class is designed to process image files containing QR codes.
    It extracts data from the codes, filters for URLs, and handles both
    raw data and nested JSON structures to find all URLs.
    """

    VALID_EXTENSIONS = ('.png', '.jpg', '.jpeg', '.bmp', '.gif')
    urls: set[str] = set()
    file_path: list[str] = []

    def __init__(self, file_path: list[str]):
        """
        Initializes the Qr object, clearing the console and validating
        the provided file paths. It only accepts supported image file types
        and logs errors for invalid paths or extensions.

        Args:
            file_path (list[str]): A list of file paths to image files.
        """

        # Unblock the below line to clear the terminal
        # if os.name == 'nt':
        #     os.system('cls')
        # else:
        #     os.system('clear')

        self._logger = CustomLogger()
        for path in file_path:
            if os.path.exists(path):
                extension = os.path.splitext(path)[1].lower()
                if extension in self.VALID_EXTENSIONS:
                    self.file_path.append(path)
                else:
                    self._logger.error(
                        f"Wrong extension skipped {path} as it is not a supported image file type.")
            else:
                self._logger.info(
                    f"Skipping '{path}' as the file does not exist.")

    @property
    def _urls(self) -> set[str]:
        """
        Provides a public-facing property to get the set of extracted URLs.
        It also logs the extracted URLs to the console with de-fanged
        characters for security.

        Returns:
            set[str]: A set of unique URLs extracted from the QR codes.
        """
        self._logger.info(
            "\n---------------------\nExtracted information:\n---------------------")
        for i in self.urls:
            self._logger.info((i.replace(".", "[.]")).replace(":", "[:]"))

        return self.urls

    def extract_url(self, data: str):
        """
        Uses a regular expression to find and extract URLs from a given string.

        Args:
            data (str): The string content to search for URLs.
        """
        pattern = r'\b(?:(?:https?|ftp|file):\/\/|www\.|ftp\.)(?:\([-A-Z0-9+&@#\/%=~_|$?!:,."]*\)|[-A-Z0-9+&@#\/%=~_|$?!:,."])*(?:\([-A-Z0-9+&@#\/%=~_|$?!:,."]*\)|[A-Z0-9+&@#\/%=~_|$"])'
        uri = re.findall(pattern, data, re.IGNORECASE)
        for i in uri:
            self.urls.add(i)

    def flat_json(self, obj: dict | list | str):
        """
        Recursively flattens a JSON object (dict or list) to extract all string values.
        It calls `extract_url` on each string found.

        Args:
            obj (dict | list | str): The JSON object to be flattened.
        """
        if isinstance(obj, dict):
            for v in obj.values():
                self.flat_json(v)
        elif isinstance(obj, list):
            for i in obj:
                self.flat_json(i)
        elif isinstance(obj, str):
            self.extract_url(obj)

    def process(self):
        """
        Main method to process the image files. It decodes the QR codes,
        attempts to parse JSON data, and extracts URLs from all string content.
        It handles cases where the QR data is not valid JSON.
        """
        if len(self.file_path) == 0:
            self._logger.error("No files to process")
            sys.exit(0)

        self._logger.info("Processing files:")
        for f in self.file_path:
            self._logger.info(f)

        self._logger.info(f"\nRaw Dump:\n---------------------")
        for img in self.file_path:
            image = Image.open(img)
            decoded_obj = decode(image)

            if decoded_obj:
                for obj in decoded_obj:
                    qr_data = obj.data.decode('utf-8')
                    self._logger.info(
                        (qr_data.replace(".", "[.]")).replace(":", "[:]"))
                    try:
                        json_data = json.loads(qr_data)
                        self.flat_json(json_data)
                    except (json.JSONDecodeError, TypeError):
                        self.extract_url(qr_data)
