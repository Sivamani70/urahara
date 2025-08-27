import requests
from logger.log import CustomLogger


class VTReport:
    """
    This class is designed to interact with the VirusTotal API. It handles
    the submission of URLs for analysis and the retrieval of detailed
    analysis reports, which include a reputation score.
    """
    URL_END_POINT: str = "https://www.virustotal.com/api/v3/urls"
    ANALYSIS_ENDPOINT: str = "https://www.virustotal.com/api/v3/analyses/"

    def __init__(self, urls: set[str], api_key: str):
        """
        Initializes the VTReport instance.

        Args:
            urls (set[str]): A set of unique URLs to be submitted for analysis.
            api_key (str): The API key for authenticating with the VirusTotal API.
        """
        self._logger = CustomLogger()
        self.urls = urls
        self.session = requests.Session()
        self.session.headers.update({
            "accept": "application/json",
            "x-apikey": api_key
        })

    def _submit(self) -> list[str]:
        """
        Submits each URL to the VirusTotal API for analysis.

        Returns:
            list[str]: A list of analysis IDs for each submitted URL.
        """
        ids: list[str] = []
        post_headers = {"content-type": "application/x-www-form-urlencoded"}

        try:
            for url in self.urls:
                payload: dict[str, str] = {"url": url}
                response: requests.Response = self.session.post(url=self.URL_END_POINT,
                                                                data=payload, headers=post_headers)
                self._logger.info(f"Status code: {response.status_code}")
                response.raise_for_status()
                self._logger.success(f"Status code: {response.status_code}")
                data = response.json()
                id: str = data["data"]["id"]
                self._logger.info(id)
                ids.append(id)
        except requests.exceptions.RequestException as err:
            self._logger.error(f"{err}")

        return ids

    def analysis_reports(self) -> list[dict[str, str]]:
        """
        Retrieves the analysis reports for each submitted URL using their IDs.
        It parses the response to extract relevant data, including the reputation score.

        Returns:
            list[dict[str, str]]: A list of dictionaries, each containing
            the URL, its ID, and the final reputation score.
        """
        analysis_data: list[dict[str, str]] = []
        ids: list[str] = self._submit()
        try:
            for id in ids:
                final_url = self.ANALYSIS_ENDPOINT + id
                analysis_response: requests.Response = self.session.get(
                    final_url)
                self._logger.info(
                    f"Status code: {analysis_response.status_code}")
                analysis_response.raise_for_status()
                self._logger.success(
                    f"Status code: {analysis_response.status_code}")
                analyzed_data = analysis_response.json()

                # Organized response data
                url_id: str = analyzed_data["meta"]["url_info"]["id"]
                url_from_response: str = analyzed_data["meta"]["url_info"]["url"]
                malicious: int = int(
                    analyzed_data["data"]["attributes"]["stats"]["malicious"])
                suspicious: int = int(
                    analyzed_data["data"]["attributes"]["stats"]["suspicious"])
                undetected: int = int(
                    analyzed_data["data"]["attributes"]["stats"]["undetected"])
                harmless: int = int(
                    analyzed_data["data"]["attributes"]["stats"]["harmless"])
                malicious_count: int = malicious + suspicious
                total_count: int = malicious + suspicious + undetected + harmless
                total: str = str(malicious_count) + "/" + str(total_count)
                analysis_data.append(
                    {
                        "url_id": url_id,
                        "url_from_response": url_from_response,
                        "total": total
                    }
                )
        except requests.exceptions.RequestException as err:
            self._logger.error(f"{err}")

        return analysis_data
