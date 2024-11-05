from argparse import ArgumentParser

from loguru import logger
from playwright.sync_api import sync_playwright

from perse.perse import perses
from perse.version import __version__


def fetch_html_content(url: str) -> str | None:
    try:
        with sync_playwright() as pw:
            browser = pw.chromium.launch()
            page = browser.new_page()
            page.goto(url)
            full_html = page.content()
            browser.close()
        return full_html
    except Exception as e:
        logger.error(f"Error fetching HTML content: {e}")
        return None


def main():
    parser = ArgumentParser(description="Convert HTML to JSON")
    parser.add_argument("--url", type=str, help="URL to extract data from")
    parser.add_argument("--file", type=str, help="HTML file to extract data from")
    parser.add_argument("--version", action="store_true", help="Show version information")
    args = parser.parse_args()

    if args.version:
        print(f"perse v{__version__}")
        return

    if not args.url and not args.file:
        logger.error("Either --url or --file must be provided")
        return

    content = None
    if args.url:
        if not args.url.startswith("http"):
            logger.error("Unknown scheme in URL")
            return
        content = fetch_html_content(args.url)
    elif args.file:
        with open(args.file, "r", encoding="utf-8") as f:
            content = f.read()

    if not content:
        logger.error("No HTML content found")
        return

    print(perses(content))


if __name__ == "__main__":
    main()
