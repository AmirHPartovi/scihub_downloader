import os
import requests
from bs4 import BeautifulSoup
import time
import random
import re
import json

# Update Sci-Hub domains
SCI_HUB_DOMAINS = [
    "https://sci-hub.se/",
    "https://sci-hub.st/",
    "https://sci-hub.ru/",
    "https://sci-hub.wf/",
]

# Create a folder for downloads
DOWNLOAD_DIR = "Downloaded_Papers"
os.makedirs(DOWNLOAD_DIR, exist_ok=True)

# Log files
SUCCESS_LOG = "success.log"
FAILED_LOG = "failed.log"

# Read DOIs from file
DOI_FILE = "./dois/triangulation.txt"
if not os.path.exists(DOI_FILE):
    print(f"❌ DOI file not found: {DOI_FILE}")
    exit(1)

with open(DOI_FILE, "r") as f:
    dois = [line.strip() for line in f.readlines() if line.strip()]


def get_pdf_url(doi):
    """Find PDF URL from DOI using Sci-Hub"""
    for domain in SCI_HUB_DOMAINS:
        try:
            url = domain + doi
            print(f"🔍 Searching in Sci-Hub: {url}")
            response = requests.get(url, timeout=10)
            response.raise_for_status()
            soup = BeautifulSoup(response.text, "html.parser")

            # Check for iframe
            iframe = soup.find("iframe")
            if iframe and "src" in iframe.attrs:
                pdf_url = iframe["src"]
                if pdf_url.startswith("//"):
                    pdf_url = "https:" + pdf_url
                return pdf_url

            # Check for embed
            embed = soup.find("embed")
            if embed and "src" in embed.attrs:
                pdf_url = embed["src"]
                if pdf_url.startswith("//"):
                    pdf_url = "https:" + pdf_url
                return pdf_url

        except requests.RequestException as e:
            print(f"⚠️ Error accessing {domain}: {e}")
            continue
    return None


def get_paper_title(doi):
    """Retrieve paper title from CrossRef"""
    try:
        crossref_url = f"https://api.crossref.org/works/{doi}"
        response = requests.get(crossref_url, timeout=10)
        response.raise_for_status()
        data = response.json()
        title = data["message"]["title"][0]
        return title
    except Exception as e:
        print(f"⚠️ Error retrieving title for {doi}: {e}")
        return doi.replace("/", "_")


def sanitize_filename(filename):
    """Sanitize filename by removing invalid characters"""
    return re.sub(r'[\\/*?:"<>|]', "_", filename)[:100]


def download_pdf(doi):
    """Download PDF for a given DOI"""
    pdf_url = get_pdf_url(doi)
    if not pdf_url:
        print(f"🚫 PDF not found for DOI: {doi}")
        with open(FAILED_LOG, "a") as f:
            f.write(doi + "\n")
        return

    title = get_paper_title(doi)
    safe_title = sanitize_filename(title)
    filename = f"{safe_title}.pdf"
    filepath = os.path.join(DOWNLOAD_DIR, filename)

    try:
        print(f"⬇️ Downloading: {filename}")
        pdf_response = requests.get(pdf_url, timeout=15)
        pdf_response.raise_for_status()
        with open(filepath, "wb") as f:
            f.write(pdf_response.content)

        # Log success
        with open(SUCCESS_LOG, "a") as f:
            f.write(f"{doi} -> {filename}\n")

        print(f"✅ Saved: {filepath}")
    except requests.RequestException as e:
        print(f"❌ Download failed for {doi}: {e}")
        with open(FAILED_LOG, "a") as f:
            f.write(doi + "\n")


# Download all DOIs
for doi in dois:
    download_pdf(doi)
    time.sleep(random.uniform(3, 7))  # Random delay

print("\n🎉 Process complete!")
