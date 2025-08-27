import time
import os
from datetime import datetime
from urllib.parse import urlparse
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.common.exceptions import WebDriverException
from logger.log import CustomLogger
from core.constants import FolderName


class Reference:
    """
    A simple data class to hold the results for a single finding.
    """

    def __init__(self, heading: str, score: str, path: str):
        self.heading = heading
        self.score = score
        self.path = path


class Snap:
    """
    The Snap class is responsible for using a Selenium WebDriver to navigate to
    VirusTotal report URLs and capture screenshots. These screenshots are then
    saved and organized for a final document.
    """

    URL_GUI_ENDPOINT: str = "https://www.virustotal.com/gui/url/"

    def __init__(self, driver_path: str, data: list[dict[str, str]]):
        """
        Initializes the Snap class with the ChromeDriver path and a list of
        analysis reports. It sets up the Selenium WebDriver instance.

        Args:
            driver_path (str): The path to the ChromeDriver executable.
            data (list[dict[str, str]]): A list of dictionaries containing
            VirusTotal analysis report data.
        """

        self._logger = CustomLogger()
        self._data = data
        self._chrome_options: Options = Options()
        # self.chrome_options.add_argument("--headless")
        self._service: Service = Service(driver_path)
        self._driver = webdriver.Chrome(
            service=self._service, options=self._chrome_options, keep_alive=True)
        self._driver.maximize_window()

    def load_url_and_take_screenshot(self, url: str, name: str) -> tuple[bool, str]:
        """
        Navigates to a given URL and takes a screenshot of the page.

        Args:
            url (str): The URL to navigate to.
            name (str): The name to be used for the screenshot file.

        Returns:
            tuple[bool, str]: A tuple containing a boolean status (True for success)
            and the full path to the saved screenshot file.
        """
        status: bool = False
        full_path = ""
        try:
            self._driver.get(url)
            time.sleep(5)
            file_name = f"{name}_{datetime.now().strftime('%Y_%m_%d_%H_%M_%S')}.png"
            folder_name = FolderName.IMG_FOLDER_NAME.value
            destination_folder = os.path.join(os.getcwd(), folder_name)
            os.makedirs(destination_folder, exist_ok=True)
            full_path = os.path.join(destination_folder, file_name)
            self._logger.info(
                "Attempting to save the file at the following location")
            self._logger.info(full_path)
            status = self._driver.save_screenshot(full_path)
        except WebDriverException as err:
            self._logger.error(f"{err}")
        except Exception as err:
            self._logger.error(f"An unexpected error occurred: {err}")

        return (status, full_path)

    def get_screenshots(self) -> list[Reference]:
        """
        Iterates through the provided analysis data, constructs the VirusTotal
        report URLs, takes a screenshot of each report, and creates a list
        of `Reference` objects.

        Returns:
            list[Reference]: A list of `Reference` objects containing the
            heading, score, and file path for each screenshot.

        Raises:
            Exception: If any screenshot fails to be captured.
        """
        reference = []
        for d in self._data:
            total = d["total"]
            final_url = self.URL_GUI_ENDPOINT + d["url_id"]
            domain = ((urlparse(d["url_from_response"])
                       ).netloc).replace(".", "_")
            score = f"VirusTotal reputation score is: {total}"
            self._logger.info(
                f"Refer the below link for the domain: {domain}\nVT URL: {final_url}\n{score}")
            status, full_path = self.load_url_and_take_screenshot(
                final_url, domain)
            if status:
                self._logger.success("File successfully saved")
                self._logger.success(f"{full_path}")
                reference.append(Reference(domain, score, full_path))
            else:
                self._logger.error("Failed to save file.")
                self._logger.error(f"{full_path}")
                raise Exception(f"Failed to capture screenshot: {full_path}")
        self._driver.quit()
        return reference
