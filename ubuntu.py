"""
Ubuntu-Inspired Image Fetcher
"I am because we are"

This program fetches images from the internet, saves them locally,
and ensures respect for the community by handling errors gracefully,
avoiding duplicates, and checking HTTP headers.
"""

import os
import requests
from urllib.parse import urlparse
import hashlib

# Directory where images will be stored
IMAGE_DIR = "Fetched_Images"
os.makedirs(IMAGE_DIR, exist_ok=True)


def get_filename_from_url(url):
    """
    Extract filename from URL or generate one if not available.
    """
    parsed_url = urlparse(url)
    filename = os.path.basename(parsed_url.path)

    # If no filename in URL, generate one
    if not filename:
        filename = hashlib.md5(url.encode()).hexdigest() + ".jpg"

    return filename


def is_duplicate(file_path, content):
    """
    Prevent duplicate downloads by comparing file hashes.
    """
    if not os.path.exists(file_path):
        return False

    # Compare hash of existing file vs new content
    with open(file_path, "rb") as f:
        existing_content = f.read()

    return hashlib.md5(existing_content).hexdigest() == hashlib.md5(content).hexdigest()


def fetch_image(url):
    """
    Fetch an image from a URL and save it locally if valid.
    """
    try:
        response = requests.get(url, timeout=10)

        # Respect: check HTTP status
        response.raise_for_status()

        # Precaution: verify content type is image
        content_type = response.headers.get("Content-Type", "")
        if not content_type.startswith("image/"):
            print(f"⚠️ Skipping {url} — Not an image (Content-Type: {content_type})")
            return

        # Generate filename
        filename = get_filename_from_url(url)
        file_path = os.path.join(IMAGE_DIR, filename)

        # Check for duplicates
        if is_duplicate(file_path, response.content):
            print(f"🔁 Duplicate found, skipping: {filename}")
            return

        # Save file
        with open(file_path, "wb") as f:
            f.write(response.content)

        print(f"✅ Saved: {filename}")

    except requests.exceptions.RequestException as e:
        print(f"❌ Failed to fetch {url} — {e}")


def main():
    """
    Main function: prompt user for multiple URLs and fetch images.
    """
    print("🌍 Ubuntu Image Fetcher: 'I am because we are'")
    print("Enter multiple image URLs separated by spaces:")

    urls = input(">> ").strip().split()

    for url in urls:
        fetch_image(url)


if __name__ == "__main__":
    main()
