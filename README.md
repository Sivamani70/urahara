# Urahara: A Comprehensive Tool for QR Phishing Investigation

Inspired by **Kisuke Urahara**, a character whose true motives and plans are always concealed, this tool is designed to uncover the hidden threats lurking behind QR codes.

**This is an automated Python tool for Security Operations Center (SOC) analysts to quickly investigate QR code phishing attempts and generate comprehensive documentation for Root Cause Analysis (RCA).**

## 🛡️ End-to-End Workflow

This script streamlines the investigative process by automating several key tasks:

1. **QR Code Data Extraction:** Decodes QR codes from images (`.jpg`, `.png`, etc.) and extracts embedded data.

2. **URL Discovery:** Intelligently identifies and extracts URLs from both simple text and complex, nested JSON payloads within the QR code.

3. **VirusTotal Analysis:** Submits the extracted URLs to the VirusTotal API for immediate security analysis.

4. **Evidence Capture:** Automates the browser to navigate to the VirusTotal report page and capture a full-page screenshot of the analysis results.

5. **RCA Documentation:** Automatically generates a formatted Microsoft Word document (`.docx`) that includes the malicious URL, a summary of the VirusTotal findings, and the screenshot as evidence.

## 📋 Prerequisites

To run this script, you must have Python installed. This project also requires the following Python libraries:

- `Pillow`
- `pyzbar`
- `requests`
- `selenium`
- `python-docx`

In addition, `pyzbar` has a system-level dependency on `libzbar`. You'll need to install this separately depending on your operating system:

- **For Fedora (using dnf):**

```
sudo dnf install zbar
```

- **For Ubuntu (using apt):**

```
sudo apt update
sudo apt install libzbar0
```

- **For Windows:**  
  The necessary DLLs are typically included when you install `pyzbar` via `pip`. However, you may need to install the **Visual C++ Redistributable Packages for Visual Studio 2013** if you encounter errors. This is a common requirement for many Python libraries with C-based dependencies on Windows. You can download it directly from the Microsoft website.

```
  You also need:
    A VirusTotal API Key: Obtain a free API key by registering on the VirusTotal website.
    A Browser Driver: The script uses Selenium, which requires a browser driver (e.g., chromedriver for Google Chrome). Ensure the driver executable is in your system's PATH.
```

## 💻 WebDriver Setup

This project uses Selenium to automate a browser. You need to download the appropriate WebDriver for the browser you want to use (e.g., Chrome or Edge). As of now, this script is written to use the Chrome browser only, so only the ChromeDriver is needed. The script is easily migratable to other browsers with minor changes to the driver initialization.

Download the WebDriver:

- **For Chrome:** Visit the [ChromeDriver downloads](https://googlechromelabs.github.io/chrome-for-testing/) page and download the version that matches your Chrome browser.
- **For Edge:** Visit the [Microsoft Edge WebDriver](https://developer.microsoft.com/en-us/microsoft-edge/tools/webdriver/) downloads page and download the version that matches your Edge browser.

## 🌐 Environment Variables

- This script requires two environment variables to be configured: `VT_API_KEY` and `CHROME_DRIVER_PATH`.

### On Windows

1. **GUI Method (Permanent):**
   - Go to "Environment Variables" by searching for it in the Start Menu.
   - In the "System variables" or "User variables" section, click New... to add each variable.
   - For `VT_API_KEY`, set the value to your VirusTotal API key.
   - For `CHROME_DRIVER_PATH`, set the value to the **complete path, including the executable file**.
     - **Example:** `C:\path\to\chromedriver.exe`
   - **Important:** You must restart your terminal or IDE for the changes to take effect.
2. **Command Prompt (Temporary):**
   - To set a variable for the current session, use the `set` command.

```
        set VT_API_KEY=YOUR_API_KEY
        set CHROME_DRIVER_PATH=C:\path\to\chromedriver.exe
```

### On Linux / macOS

1. **Shell Profile (Permanent):**

   - Open your shell's profile file (e.g., `.bashrc`, `.zshrc`, or `.bash_profile`) in a text editor.
   - Add the following lines to the end of the file: [After that Save the file and then apply the changes by running source ~/.bashrc (or your corresponding shell file).]

```
    export VT_API_KEY="YOUR_API_KEY"
    export CHROME_DRIVER_PATH="/path/to/chromedriver"
```

2. **Terminal (Temporary):**
   - To set a variable for the current terminal session, use the `export` command.

```
    export VT_API_KEY="YOUR_API_KEY"
    export CHROME_DRIVER_PATH="/path/to/chromedriver"
```

**Installation**

1. Clone the repository:

```
git clone https://github.com/Sivamani70/urahara.git
cd urahara
```

2. Set up the virtual environment and install dependencies:

**On macOS/Linux**

```
python3 -m venv venv
source venv/bin/activate
```

**On Windows**

```
py -m venv venv
venv\Scripts\activate
```

3. Install Python libraries:

```
pip install -r requirements.txt
```

## ⚙️ Configuration

Before running the script, you must configure your `VirusTotal API key` and `ChromeDriver` to use VirusTotal submission and Evidence Capture modules.

## 🚀 Usage

Run the script from the command line, providing the path to one or more QR code image files.

```
python main.py path/to/qr_image1.png path/to/qr_image2.jpg
```

The script will automatically perform the analysis and generate a .docx report for each URL identified.

## 📈 Project Status

The current development status of the project is outlined below, detailing both completed milestones and tasks that are presently in progress.

**Phase 1: QR Data Acquisition and Parsing**

[x] Completed: Decoding of QR code images.

[x] Completed: Extraction of data payloads.

[x] Completed: Parsing of URLs from JSON and plain text.

**Phase 2: Automated Analysis and Documentation**

[x] Completed: Integration with the VirusTotal API.

[x] Completed: Automated capture of VirusTotal report screenshots.

[x] Completed: Automated generation of RCA documentation.

## 🤝 Contributing

As a tool for the security community, contributions are highly encouraged. Whether it's improving the URL regex, adding support for other threat intelligence platforms, or enhancing the documentation, your input is valuable. Please open an issue or submit a pull request.
