import requests
from bs4 import BeautifulSoup
import pandas as pd
import os
import csv
from seekh_data_scraper.wikipedia_data_scraping.wikipedia_config import BASE_DIR

def scrape_content_url(url):
    response = requests.get(url)
    soup = BeautifulSoup(response.text, "html.parser")

    # Get page title from the new structure
    title_element = soup.find("h1", class_="firstHeading")
    page_title = title_element.find("span", class_="mw-page-title-main").text.strip()

    # Find the main content div with the new class
    content_div = soup.find("div", class_="mw-parser-output")

    titles_to_skip = set([
        "Alternative theories", "References", "Further reading", "Additional Reading",
        "External links", "Footnotes", "See also", "Scientific journals",
        "Citations", "Common subfields", "Sources", "Journals",
        "Explanatory notes", "Sources", "Applied fields", "Notes", "Bibliography",
        "International relations", "Historical publication",
       "Conferences", "Modern references",
        "Books", "Awards", "Gallery", "Notes and references", "Historical references"
    ])

    content_data = []
    current_subtitle = None

    for element in content_div.find_all(["h2", "h3", "p", "ul"]):
        if element.name in ["h2", "h3"]:
            # Find heading in the new structure
            heading_span = element.find("span", class_="mw-headline")
            if heading_span and heading_span.text not in titles_to_skip:
                current_subtitle = heading_span.text
        elif element.name == "p" or element.name == "ul":
            if current_subtitle:
                # Clean up the content by removing reference tags
                for ref in element.find_all("sup", class_="reference"):
                    ref.decompose()
                content = element.get_text(strip=True)
                content_data.append({
                    "url": url,
                    "content": content,
                    "topic": current_subtitle
                })

    return page_title, content_data

def scrape_wikipedia_intro(url):
    response = requests.get(url)
    if response.status_code == 200:
        soup = BeautifulSoup(response.text, 'html.parser')
        # Find the main content in the new structure
        content_div = soup.find('div', class_="mw-parser-output")
        if not content_div:
            return ""
            
        scraped_content = ""
        for p in content_div.find_all('p', recursive=False):
            # Skip empty paragraphs
            if not p.get_text(strip=True):
                continue
                
            # Remove reference tags
            for ref in p.find_all("sup", class_="reference"):
                ref.decompose()
                
            formatted_parts = []
            for part in p.contents:
                if part.name in ['a', 'b', 'i']:
                    formatted_parts.append(part.get_text())
                elif part.name not in ['sup', 'span', 'small']:
                    formatted_parts.append(str(part))
            
            scraped_content += ''.join(formatted_parts)
            
            # Stop when we hit the first heading
            next_heading = p.find_next(["h1", "h2", "h3"])
            if next_heading:
                break
                
        return scraped_content
    return ""

def scrape_see_also(url):
    response = requests.get(url)
    if response.status_code == 200:
        soup = BeautifulSoup(response.content, "html.parser")
        
        # Find "Related pages" section in the new structure
        related_h2 = soup.find("h2", {"id": "Related_pages"})
        if not related_h2:
            # Fall back to "See also" if "Related pages" doesn't exist
            related_h2 = soup.find("span", class_="mw-headline", text="See also")
            
        if related_h2:
            # Find the next unordered list
            ul_tag = related_h2.find_next("ul")
            if ul_tag:
                related_data = []
                li_tags = ul_tag.find_all("li")
                for li_tag in li_tags:
                    a_tag = li_tag.find("a")
                    if a_tag:
                        link_text = a_tag.get_text()
                        href = a_tag.get("href")
                        if href.startswith('/wiki/'):
                            full_url = "https://en.wikipedia.org" + href
                            related_data.append({"title": link_text, "href": full_url})
                return related_data
    return None

def scrape_images(url):
    response = requests.get(url)
    if response.status_code == 200:
        soup = BeautifulSoup(response.content, "html.parser")
        # Find images within the main content area
        content_div = soup.find("div", class_="mw-parser-output")
        if not content_div:
            return []
            
        images = content_div.find_all('img')
        image_data = []
        for img in images:
            src = img.get('src', '')
            if src.startswith('//'):
                src = 'https:' + src
            alt = img.get('alt', '')
            # Filter out tiny images (likely icons)
            width = img.get('width')
            if width and int(width) > 50:
                image_data.append({
                    'src': src,
                    'alt': alt
                })
        return image_data
    return []

def save_data(page_title, content_data, summary_data, see_also_data, image_data):
    # Create directory for this page
    page_dir = os.path.join(BASE_DIR, page_title)
    os.makedirs(page_dir, exist_ok=True)

    # Save content.csv
    with open(os.path.join(page_dir, 'content.csv'), 'w', newline='', encoding='utf-8') as f:
        writer = csv.DictWriter(f, fieldnames=["url", "content", "topic"])
        writer.writeheader()
        writer.writerows(content_data)

    # Save summary.csv
    pd.DataFrame([summary_data]).to_csv(os.path.join(page_dir, 'summary.csv'), index=False)

    # Save see_also_links.csv
    if see_also_data:
        with open(os.path.join(page_dir, 'see_also_links.csv'), 'w', newline='', encoding='utf-8') as f:
            writer = csv.DictWriter(f, fieldnames=["title", "href"])
            writer.writeheader()
            writer.writerows(see_also_data)

    # Save images.csv
    if image_data:
        pd.DataFrame(image_data).to_csv(os.path.join(page_dir, 'images.csv'), index=False)