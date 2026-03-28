import asyncio
import json
import os
from playwright.async_api import async_playwright

async def scrape_ekantipur():
    async with async_playwright() as p:
        # Launch browser
        browser = await p.chromium.launch(headless=True)
        context = await browser.new_context(
            user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36"
        )
        page = await context.new_page()

        try:
            # Task 1: Extract Entertainment News
            print("Navigating to Entertainment section...")
            await page.goto("https://ekantipur.com/entertainment", wait_until="domcontentloaded", timeout=60000)
            
            print("Waiting for articles to load...")
            await page.wait_for_selector(".category", timeout=15000)
            
            # Extract top 5 unique articles
            articles_elements = await page.locator(".category").all()
            
            entertainment_news = []
            seen_titles = set()
            print(f"Found {len(articles_elements)} articles. Extracting top 5 unique...")
            
            for i, element in enumerate(articles_elements):
                if len(entertainment_news) >= 5:
                    break
                    
                try:
                    # Title: .category-description h2 a
                    title_el = element.locator(".category-description h2 a").first
                    title = (await title_el.inner_text()).strip()
                    
                    # Skip if we've already seen this title (avoids duplicates)
                    if title in seen_titles:
                        continue
                    seen_titles.add(title)
                    
                    # Image: .category-image img
                    image_el = element.locator(".category-image img").first
                    image_url = await image_el.get_attribute("data-src") or await image_el.get_attribute("src")
                    
                    # Author: .author-name p a
                    # Note: "कान्तिपुर संवाददाता" is a generic name used by the site 
                    # when a specific journalist is not named.
                    author_el = element.locator(".author-name p a").first
                    author = await author_el.inner_text() if await author_el.count() > 0 else None
                    
                    entertainment_news.append({
                        "title": title,
                        "image_url": image_url,
                        "category": "मनोरञ्जन",
                        "author": author.strip() if author else None
                    })
                    print(f"  - Extracted: {title[:40]}...")
                except Exception as e:
                    print(f"  - Error extracting article {i+1}: {e}")

            # Task 2: Extract Cartoon of the Day
            print("Navigating to Cartoon section...")
            await page.goto("https://ekantipur.com/cartoon", wait_until="domcontentloaded", timeout=60000)
            
            print("Waiting for cartoons to load...")
            await page.wait_for_selector(".cartoon-wrapper", timeout=15000)
            
            # Extract the first (latest) cartoon
            cartoon_element = page.locator(".cartoon-wrapper").first
            
            cartoon_data = {
                "title": None,
                "image_url": None,
                "author": None
            }

            if await cartoon_element.count() > 0:
                try:
                    # Image: .cartoon-image img
                    image_el = cartoon_element.locator(".cartoon-image img").first
                    cartoon_data["image_url"] = await image_el.get_attribute("data-src") or await image_el.get_attribute("src")
                    
                    # Title: Use the 'alt' attribute of the image for the dynamic title
                    cartoon_data["title"] = await image_el.get_attribute("alt")
                    
                    # Author: Extract from .cartoon-description p (e.g., "गजब छ बा! - अविन")
                    desc_el = cartoon_element.locator(".cartoon-description p").first
                    full_desc = await desc_el.inner_text() if await desc_el.count() > 0 else ""
                    
                    # Split to get the author (the part after " - ")
                    if " - " in full_desc:
                        parts = full_desc.split(" - ")
                        cartoon_data["author"] = parts[1].strip()
                        # If alt was missing, fallback to the first part of the description
                        if not cartoon_data["title"]:
                            cartoon_data["title"] = parts[0].strip()
                    
                    if not cartoon_data["title"]:
                        cartoon_data["title"] = "व्यंग्यचित्र"
                        
                    print(f"  - Cartoon found: {cartoon_data['title']} by {cartoon_data['author']}")
                except Exception as e:
                    print(f"  - Error extracting cartoon: {e}")
            else:
                print("  - Cartoon wrapper not found on page.")

            # Final Data Structure
            output = {
                "entertainment_news": entertainment_news,
                "cartoon_of_the_day": cartoon_data
            }

            with open("output.json", "w", encoding="utf-8") as f:
                json.dump(output, f, ensure_ascii=False, indent=4)
            
            print("Scraping completed successfully. Data saved to output.json")

        except Exception as e:
            print(f"CRITICAL ERROR: {e}")
            await page.screenshot(path="error_screenshot.png")
        finally:
            await browser.close()

if __name__ == "__main__":
    asyncio.run(scrape_ekantipur())
