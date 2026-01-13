from pathlib import Path
from bs4 import BeautifulSoup


def extract_text_from_html(path: Path) -> str:
    """
    Extracts readable text from an HTML file.

    This is intentionally simple:
     - Strip scripts, styles
     - Ignores layout
     - Return human-readable text only
    """

    html = path.read_text(encoding='utf-8', errors='ignore')
    soup = BeautifulSoup(html, 'html.parser')

    # Remove non-content elements
    for tag in soup(['script', 'style', 'noscript']):
        tag.decompose()

    # noinspection PyArgumentList
    text = soup.get_text(separator=' ')

    # Normalize whitespace
    return ' '.join(text.split())
