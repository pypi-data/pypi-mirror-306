from loguru import logger

from perse.perse import reduce_html_content

with open("tests/input.html", "r") as f:
    content = f.read()

logger.info(f"Before: {len(content)}")

exclude_tags = {"script", "style", "svg", "iframe"}
reduced = reduce_html_content(content, exclude_tags)
logger.info(f"After: {len(reduced)}: {reduced}")