# Ekantipur Web Scraper

A robust Python web scraper built with **Playwright** and **uv** to extract entertainment news and the daily cartoon from [ekantipur.com](https://ekantipur.com).

## 🚀 Features

- **Entertainment News**: Extracts the top 5 unique articles (Title, Image URL, Category, Author).
- **Cartoon of the Day**: Extracts the latest cartoon with dynamic title (from `alt` tag) and author.
- **Lazy Loading Support**: Handles `data-src` attributes to ensure images are correctly captured.
- **Robust Navigation**: Implements `domcontentloaded` and `networkidle` strategies with extended timeouts.
- **Error Handling**: Automatically saves an `error_screenshot.png` on failure for easy debugging.
- **UTF-8 Support**: Correctly preserves Devanagari (Nepali) characters in the output.

## 🛠️ Tech Stack

- **Python**: Core logic.
- **Playwright**: Browser automation and scraping.
- **uv**: Modern Python package and environment management.
- **React**: (Optional) Dashboard for visualizing the extracted data.

## 📦 Installation

1. Ensure you have [uv](https://github.com/astral-sh/uv) installed.
2. Clone the repository:
   ```bash
   git clone <your-repo-url>
   cd ekantipur-scraper
   ```
3. Install dependencies and Playwright browsers:
   ```bash
   uv sync
   uv run playwright install chromium
   ```

## 🖥️ Usage

Run the scraper using `uv`:

```bash
uv run python scraper.py
```

The extracted data will be saved to `output.json` in the root directory.

## 📊 Output Format

```json
{
    "entertainment_news": [
        {
            "title": "Article Title",
            "image_url": "https://...",
            "category": "मनोरञ्जन",
            "author": "Author Name"
        }
    ],
    "cartoon_of_the_day": {
        "title": "Cartoon Title",
        "image_url": "https://...",
        "author": "Artist Name"
    }
}
```

## 📝 Assignment Prompts

A list of prompts used during the development and debugging of this project can be found in `prompts.txt`.
