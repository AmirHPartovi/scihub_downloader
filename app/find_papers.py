import requests
from bs4 import BeautifulSoup

__all__ = ["get_list_of_papers"]
DBLP_DOMAINS = [
    "https://dblp.org/search/publ/api",  # for publication queries
    "https://dblp.org/search/author/api",  # for author queries
    "https://dblp.org/search/venue/api"  # for venue queries
]


def get_list_of_papers(mode: str, input_text: str, num_results: int = 100) -> list:
    """
    Get a list of papers from DBLP based on the input text.

    Args:
        mode (str): The mode of search. Can be 'author', 'title', or 'venue'.
        input_text (str): The text to search for.
        num_results (int): The number of results to return. Default is 100.

    Returns:
        list: A list of dictionaries containing paper details.
    """
    if mode == "publication":
        url = f"{DBLP_DOMAINS[0]}?q=*{input_text}&format=json&h={num_results}"
    elif mode == "author":
        url = f"{DBLP_DOMAINS[1]}?q=*{input_text}&format=json&h={num_results}"
    elif mode == "venue":
        url = f"{DBLP_DOMAINS[2]}?q=*{input_text}&format=json&h={num_results}"
    else:
        raise ValueError(
            "Invalid mode. Choose from 'publication', 'author', or 'venue'.")

    response = requests.get(url, timeout=20)
    if response.status_code != 200:
        raise Exception(
            f"Failed to fetch data from DBLP. Status code: {response.status_code}")

    data = response.json()
    papers = []
    try:
        result = data.get('result', {})
        if isinstance(result, str):
            print(f"Unexpected result format: {result}")
            return []

        hits = result.get('hits', {})
        if isinstance(hits, str):
            print(f"Unexpected hits format: {hits}")
            return []

        hit_list = hits.get('hit', [])
        if not isinstance(hit_list, list):
            return []

        for hit in hit_list:
            info = hit.get('info', {})
            if not isinstance(info, dict):
                continue

            paper = {
                'title': info.get('title', 'Untitled'),
                'year': info.get('year', 'N/A'),
                'venue': info.get('venue', 'N/A'),
                'doi': info.get('doi', ''),
                'url': info.get('url', '')
            }

            # Handle authors which can be either a dict or list
            authors = info.get('authors', {})
            if isinstance(authors, dict):
                author = authors.get('author', [])
                if isinstance(author, dict):
                    paper['authors'] = [author.get('text', '')]
                elif isinstance(author, list):
                    paper['authors'] = [a.get('text', '') for a in author]

            papers.append(paper)

        return papers

    except (KeyError, TypeError, AttributeError) as e:
        print(f"Error parsing response: {str(e)}")
        return []
