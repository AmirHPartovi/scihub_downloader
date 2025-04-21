
import requests
from bs4 import BeautifulSoup
import re
import webbrowser  # Add this import at the top with other imports

ــall__ = ["get_pdf_url", "get_paper_title", "sanitize_filename", "download_pdf"]
# Update Sci-Hub domains
SCI_HUB_DOMAINS = [
    "https://sci-hub.se/",
    "https://sci-hub.st/",
    "https://sci-hub.ru/",
    "https://sci-hub.wf/",
]


# Log files
SUCCESS_LOG = "success.log"
FAILED_LOG = "failed.log"




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
        return False

    # Open PDF URL directly in browser
    try:
        print(f"🌐 Opening PDF in browser: {pdf_url}")
        webbrowser.open_new_tab(pdf_url)
        return pdf_url
    except Exception as e:
        print(f"❌ Failed to open PDF in browser: {e}")
        with open(FAILED_LOG, "a") as f:
            f.write(f"{doi} (browser open failed) -> {str(e)}\n")
        return None


