import os
import requests
from urllib.parse import urljoin
from html.parser import HTMLParser

class SoundEffectHTMLParser(HTMLParser):
    def __init__(self):
        super().__init__()
        self.links = []

    def handle_starttag(self, tag, attrs):
        if tag == 'a':
            href = dict(attrs).get('href')
            if href and (href.endswith('.mp3') or href.endswith('.wav')):
                self.links.append(href)

def fetch_page_content(url):
    try:
        response = requests.get(url)
        response.raise_for_status()
        return response.text
    except requests.RequestException as e:
        print(f"Failed to fetch page content: {e}")
        return None

def download_file(url, folder):
    try:
        filename = os.path.basename(url)
        filepath = os.path.join(folder, filename)
        with requests.get(url, stream=True) as response:
            response.raise_for_status()
            with open(filepath, 'wb') as f:
                for chunk in response.iter_content(chunk_size=8192):
                    f.write(chunk)
        print(f"Downloaded: {filename}")
    except requests.RequestException as e:
        print(f"Failed to download file: {e}")

def main():
    base_url = "https://elements.envato.com/sound-effects"
    download_folder = os.path.join(os.getcwd(), "downloads")

    if not os.path.exists(download_folder):
        os.makedirs(download_folder)

    html_content = fetch_page_content(base_url)
    if not html_content:
        return

    parser = SoundEffectHTMLParser()
    parser.feed(html_content)

    for link in parser.links:
        full_url = urljoin(base_url, link)
        download_file(full_url, download_folder)

if __name__ == "__main__":
    main()
