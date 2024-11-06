# Perse

[![PyPI version](https://badge.fury.io/py/zf-perse.svg)](https://badge.fury.io/py/zf-perse)

<p align="center">
  <img src="https://zf-static.s3.us-west-1.amazonaws.com/perse-logo128.png" alt="Perse"/>
</p>

Perse converts `HTML` to `JSON` using a mix of traditional html parsing and LLM based data extraction.

### Features

It's core features includes:

- Identify important fields to extract from html
- Building a JSON schemas that handles nested fields
- Process html tokens and fill the JSON schema object

You can install Perse using pip:

```bash
pip install zf-perse
export PERSE_OPENAI_API_KEY="your-openai-api-key"
```

And run it from CLI:

```bash
perse --url https://google.com
```

### Optimizations

It performs a few optimizations after fetching the html while preventing any accidental removal of important data.

These optimizations includes:

- Removal of styling, scripting and svg tags
- Collapsing Tags (e.g. divs) with only one child

## Comparison

There are a few other libraries but none of them provide a solution for reliable data extraction from html.

### HTML to JSON

[html2json](https://pypi.org/project/html-to-json/) library is a simple html to json converter that doesn't handle nested fields, nor does it remove unnecessary tags.

When ran on exactly the same html, Perse provides a more structured and cleaner output and at least 50% less verbose output.

<table>
<tr>
<th>HTML to JSON</th>
<th>Perse</th>
</tr>
<tr>
<td>
    <img src="https://zf-static.s3.us-west-1.amazonaws.com/perse-output-htmltojson.png" width="250px" alt="rate_1.0">
</td>
<td>
    <img src="https://zf-static.s3.us-west-1.amazonaws.com/perse-output-perse.png" width="250px" alt="rate_1.0">
</td>
</tr>
</table>

### HTML to Markdown

[Reader-LM](https://jina.ai/news/reader-lm-small-language-models-for-cleaning-and-converting-html-to-markdown/) is a language model that converts html to markdown. It doesn't provide a json output catering only to the reader mode which is not suitabel for data extraction, analysis and automations.

## Usage

**Process HTML content and get a Dictionary**

```python
html_content = "<html>...</html>"
json_dict = perse(html_content)
print(json_dict)
```

**Process HTML content and get a JSON string**

```python
html_content = "<html>...</html>"
json_string = perses(html_content)
print(json_string)
```

**Exclude specific tags from the JSON output**

```python
html_content = "<html>...</html>"
json_dict = perse(html_content, exclude_tags={"script", "style"})
print(json_dict)
```

**Clean up the HTML content for side usage**

```python
html_content = "<html>...</html>"
clean_soup = simmer(html_content) # or use simmers for a string output
print(clean_soup.prettify())
```

## Examples

## Google's Homepage

```bash
$ perse --url https://google.com

{
  "image": "/images/branding/googleg/1x/googleg_standard_color_128dp.png",
  "title": "Google",
  "search_form": {
    "action": "/search",
    "method": "GET",
    "autocomplete": "off",
    "query": "",
    "buttons": [
      {
        "button_1": {
          "label": "Google Search",
          "value": "Google Search"
        },
        "button_2": {
          "label": "I'm Feeling Lucky",
          "value": "I'm Feeling Lucky"
        }
      }
    ]
  }
}
```

### Zeff Muks's Homepage

```bash
$ perse --url https://zeffmuks.com

{
  "title": "Zeff Muks",
  "description": "Antifragile Entropy Assassin \ud83e\udd77",
  "og_data": {
    "type": "website",
    "title": "Zeff Muks",
    "description": "Antifragile Entropy Assassin \ud83e\udd77",
    "url": "https://zeffmuks.com/",
    "image": "https://www.zeffmuks.com/images/ZeffMuks-1920.png",
    "site_name": "Zeff Muks"
  },
  "twitter_data": {
    "card": "summary_large_image",
    "site": "@zeffmuks",
    "title": "Zeff Muks",
    "description": "Antifragile Entropy Assassin \ud83e\udd77",
    "image": "https://www.zeffmuks.com/images/ZeffMuks-1920.png"
  },
  "user_section": {
    "header": {
      "profile_image_url": "/images/ZeffMuks-6912.png",
      "title": "Antifragile Entropy Assassin \ud83e\udd77",
      "signature": ""
    },
    "builds": [
      {
        "date": "08/30/2024",
        "name": "Cursor Git",
        "description": "Enhanced Git for Cursor AI Editor",
        "download_link": "https://zf-static.s3.us-west-1.amazonaws.com/cursor-git-0.1.12.vsix",
        "preview_image": "https://zf-static.s3.us-west-1.amazonaws.com/cursor-git-logo128.png",
        "alternative_link": ""
      },
      {
        "date": "08/18/2024",
        "name": "PyZF",
        "description": "Enhancements for Python",
        "download_link": "https://pypi.org/project/PyZF",
        "preview_image": "https://zf-static.s3.us-west-1.amazonaws.com/pyzf-logo128.png",
        "alternative_link": ""
      },
      {
        "date": "08/05/2024",
        "name": "Xanthus",
        "description": "X (formerly Twitter) Assistant",
        "download_link": "https://pypi.org/project/zf-xanthus",
        "preview_image": "https://zf-static.s3.us-west-1.amazonaws.com/xanthus-logo128.png",
        "alternative_link": ""
      },
      {
        "date": "07/24/2024",
        "name": "Jenga",
        "description": "Fast JSON5 Python Library",
        "download_link": "https://pypi.org/project/zf-jenga",
        "preview_image": "",
        "alternative_link": ""
      },
      {
        "date": "07/12/2024",
        "name": "Pegasus",
        "description": "Next Generation Tech Stack",
        "download_link": "https://zf-static.s3.us-west-1.amazonaws.com/pegasus.zip",
        "preview_image": "https://zf-static.s3.us-west-1.amazonaws.com/pegasus-logo128.png",
        "alternative_link": ""
      },
      ...
      {
        "date": "11/01/2023",
        "name": "Z",
        "description": "Next Generation Content Platform",
        "download_link": "https://x.com/zeffmuks/status/1718507463321010429",
        "preview_image": "https://zf-static.s3.us-west-1.amazonaws.com/z-logo128.png",
        "alternative_link": "https://alpha.thez.ai/try"
      }
    ]
  }
}
```

## License

[MIT License](./LICENSE)

