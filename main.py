import os
import sys
from core.vt import VTReport
from core.snap import Snap, Reference
from core.parser import Qr
from logger.log import CustomLogger
from core.evidence import RCA


def confirm_submission(msg: str) -> bool:
    """
    Prompts the user for confirmation and returns True or False.
    """
    logger = CustomLogger()
    yes = ["yes", "y"]

    while True:
        logger.info(
            f"{msg}")
        response = input("Enter (Y)es/(N)o:\t").lower()
        if response in yes:
            return True
        elif response in ["no", "n"]:
            return False
        else:
            logger.error("Invalid input. Please enter 'yes' or 'no'.")


def main() -> int:
    """
    Main function to orchestrate the program's workflow.
    Returns 0 on successful completion, or a non-zero exit code on failure.
    """

    logger = CustomLogger()

    # --- Step 1: Validate command-line arguments ---
    if len(sys.argv) == 1:
        logger.error(
            "Provide the file path(s) that contains QR codes.")
        return 1

    # --- Step 2: Process QR codes and get URLs ---
    qr: Qr = Qr(sys.argv[1:])
    qr.process()
    urls: set[str] = qr._urls

    if len(urls) == 0:
        logger.error("No URLs to submit")
        return 1

    # --- Step 3: Confirm URL submission to VirusTotal ---
    if not confirm_submission("Would you like to submit the above URLs to VirusTotal and get the reports?"):
        logger.success("Terminating program.")
        return 0

    # --- Step 4: Validate environment variables ---
    logger.info("Checking for the VirusTotal API key and Chrome Driver Path")
    api_key = os.environ.get("VT_API_KEY")
    driver_path = os.environ.get("CHROME_DRIVER_PATH")

    if api_key is None:
        logger.error("problem in finding API key")
        return 1

    if driver_path is None:
        logger.error("problem in finding Driver Path")
        return 1

    # --- Step 5: Get analysis reports from VirusTotal ---
    logger.success("VirusTotal API key and Chrome Driver Path found")
    vt_report: VTReport = VTReport(urls, api_key)
    data: list[dict[str, str]] = vt_report.analysis_reports()

    if not data:
        logger.info("No analysis data received. No screenshots will be taken.")
        logger.success("Program execution concluded.")
        return 0

    # --- Step 6: Capture screenshots ---
    snap: Snap = Snap(driver_path, data)
    reference: list[Reference] = snap.get_screenshots()

    if len(reference) == 0:
        logger.error("No Screenshots to Document the findings")
        return 1

    if not confirm_submission("Would you like to Document the findings?"):
        logger.success("Terminating program.")
        return 0

    rca: RCA = RCA(reference)
    rca.document_findings()
    logger.success("Program execution completed successfully.")
    return 0


if __name__ == "__main__":
    # [Entry Point] Call the main function and use its return value as the exit code.
    sys.exit(main())
