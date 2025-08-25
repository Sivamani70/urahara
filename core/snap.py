import time
import os
from datetime import datetime
from urllib.parse import urlparse
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from logger.log import CustomLogger


class Snap:
    URL_GUI_ENDPOINT: str = "https://www.virustotal.com/gui/url/"

    def __init__(self, driver_path: str, data: list[dict[str, str]]):
        self._logger = CustomLogger()
        self._data = data
        self._chrome_options: Options = Options()
        # self.chrome_options.add_argument("--headless")
        self._service: Service = Service(driver_path)
        self._driver = webdriver.Chrome(
            service=self._service, options=self._chrome_options, keep_alive=True)
        self._driver.maximize_window()

    def load_url_and_take_screenshot(self, url: str, name: str) -> bool:
        status: bool = False
        try:
            self._driver.get(url)
            time.sleep(5)
            file_name = f"{name}_{datetime.now().strftime('%Y_%m_%d_%H_%M_%S')}.png"
            folder_name = "generated_images"
            destination_folder = os.path.join(os.getcwd(), folder_name)
            os.makedirs(destination_folder, exist_ok=True)
            full_path = os.path.join(destination_folder, file_name)
            self._logger.info(
                "Attempting to save the file at the following location")
            self._logger.info(full_path)
            status = self._driver.save_screenshot(full_path)
        except Exception as err:
            self._logger.error(f"{err}")

        return status

    def get_screenshots(self):
        for d in self._data:
            total = d["total"]
            final_url = self.URL_GUI_ENDPOINT + d["url_id"]
            domain = ((urlparse(d["url_from_response"])
                       ).netloc).replace(".", "_")
            self._logger.info(
                f"Refer the below link for the domain: {domain}\nVirusTotal reputation score is: {total}\nVT URL: {final_url}")
            status = self.load_url_and_take_screenshot(final_url, domain)
            if status:
                self._logger.success("File successfully saved")
            else:
                self._logger.error("Error: Failed to save file.")
