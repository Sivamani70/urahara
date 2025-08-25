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

- **Later:**

```
  You also need:
    A VirusTotal API Key: Obtain a free API key by registering on the VirusTotal website.
    A Browser Driver: The script uses Selenium, which requires a browser driver (e.g., chromedriver for Google Chrome). Ensure the driver executable is in your system's PATH.
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

## ⚙️ Configuration [Later Still in implementation]

Before running the script, you must configure your `VirusTotal API key`. Pass the VirusTotal API Key to `main.py` file as an commandline argument with your actual key.

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

[ ] Work in progress: Automated generation of RCA documentation.

## 🤝 Contributing

As a tool for the security community, contributions are highly encouraged. Whether it's improving the URL regex, adding support for other threat intelligence platforms, or enhancing the documentation, your input is valuable. Please open an issue or submit a pull request.
