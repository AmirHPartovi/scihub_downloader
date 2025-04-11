# Sci-Hub Downloader

Sci-Hub Downloader is a simple tool that takes a list of DOIs from a `.txt` file and downloads the corresponding research papers from Sci-Hub.

## Features

- Accepts a `.txt` file containing DOIs (one DOI per line).
- Automatically downloads papers from Sci-Hub.
- Saves downloaded files locally.

## Requirements

- Python 3.x
- Internet connection

## Installation

1. Clone this repository:

   ```bash
   git clone https://github.com/AmirHPartovi/scihub_downloader.git
   cd scihub_downloader
   ```

2. Install the required dependencies:
   ```bash
   pip install -r requirements.txt
   ```

## Usage

1. Create a `*.txt` file containing the DOIs you want to download. Example:

   ```
   10.1000/xyz123
   10.1001/abc456
   ```

2. Run the script:

   ```bash
   python3 index.py
   ```

   - `--input`: Path to the `./dois/doi.txt` file containing DOIs.
   - `--output`: Directory where the downloaded papers will be saved.

## Disclaimer

This tool is for educational purposes only. Use it responsibly and ensure compliance with copyright laws in your jurisdiction.

## License

This project is licensed under the [MIT License](LICENSE).
