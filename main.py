import json
import os
import re
import sys
from PIL import Image
from pyzbar.pyzbar import decode
from core.vt import VTReport
from core.snap import Snap
from logger.log import CustomLogger


class Main:
    VALID_EXTENSIONS = ('.png', '.jpg', '.jpeg', '.bmp', '.gif')
    urls: set[str] = set()
    file_path: list[str] = []

    def __init__(self, file_path: list[str]):
        if os.name == 'nt':
            os.system('cls')
        else:
            os.system('clear')

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

    def process(self):

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

    def extract_url(self, data: str):
        pattern = r'\b(?:(?:https?|ftp|file):\/\/|www\.|ftp\.)(?:\([-A-Z0-9+&@#\/%=~_|$?!:,."]*\)|[-A-Z0-9+&@#\/%=~_|$?!:,."])*(?:\([-A-Z0-9+&@#\/%=~_|$?!:,."]*\)|[A-Z0-9+&@#\/%=~_|$"])'
        uri = re.findall(pattern, data, re.IGNORECASE)
        for i in uri:
            self.urls.add(i)

    def flat_json(self, obj: dict | list | str):
        if isinstance(obj, dict):
            for v in obj.values():
                self.flat_json(v)
        elif isinstance(obj, list):
            for i in obj:
                self.flat_json(i)
        elif isinstance(obj, str):
            self.extract_url(obj)

    @property
    def _urls(self) -> set[str]:
        self._logger.info(
            "\n---------------------\nExtracted information:\n---------------------")
        for i in self.urls:
            self._logger.info((i.replace(".", "[.]")).replace(":", "[:]"))

        return self.urls


def confirm_submission() -> bool:
    logger = CustomLogger()
    yes = ["yes", "y"]

    while True:
        logger.info(
            "\nWould you like to submit the above URLs to VirusTotal and get the reports?")
        response = input("Enter (Y)es/(N)o:\t").lower()
        if response in yes:
            return True
        elif response in ["no", "n"]:
            return False
        else:
            logger.error("Invalid input. Please enter 'yes' or 'no'.")


def run():
    logger = CustomLogger()

    if len(sys.argv) == 1:
        logger.error(
            "Provide the file path(s) that contains QR codes.")
        sys.exit(1)

    main: Main = Main(sys.argv[1:])
    main.process()
    urls: set[str] = main._urls

    if len(urls) == 0:
        logger.error("No URLs to submit")
        sys.exit(1)

    if not confirm_submission():
        logger.success("Terminating program.")
        sys.exit(0)

    logger.info("Checking for the VirusTotal API key and Chrome Driver Path")
    api_key = os.environ.get("VT_API_KEY")
    driver_path = os.environ.get("CHROME_DRIVER_PATH")

    if api_key is None:
        logger.error("problem in finding API key")
        sys.exit(1)

    if driver_path is None:
        logger.error("problem in finding Driver Path")
        sys.exit(1)

    logger.success("VirusTotal API key and Chrome Driver Path found")
    vt_report: VTReport = VTReport(urls, api_key)
    data: list[dict[str, str]] = vt_report.analysis_reports()
    if data:
        snap: Snap = Snap(driver_path, data)
        snap.get_screenshots()
    else:
        logger.info("No analysis data received. No screenshots will be taken.")
        logger.success("Program execution concluded.")


if __name__ == "__main__":
    run()
