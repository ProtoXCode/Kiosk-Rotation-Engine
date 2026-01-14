import requests
from bs4 import BeautifulSoup


def extract_text_from_url(url: str, timeout: int = 3) -> int:
    """ Returns the number of words extracted from the url """
    try:
        resp = requests.get(
            url,
            timeout=timeout,
            headers={'User-Agent': 'KioskRotationEngine/1.0'}
        )
        resp.raise_for_status()
    except Exception as e:
        raise RuntimeError(f'URL fetch failed: {e}')

    soup = BeautifulSoup(resp.text, 'html.parser')

    # Remove non-content elements
    for tag in soup(
            ['script', 'style', 'noscript', 'nav', 'footer', 'header']):
        tag.decompose()

    # noinspection PyArgumentList
    text = soup.get_text(separator=' ')

    words = [w for w in text.split() if len(w) > 1]

    return len(words)
