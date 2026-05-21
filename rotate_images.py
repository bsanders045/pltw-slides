import re
import urllib.request
import urllib.parse
from datetime import datetime

SLIDE_KEYWORDS = {
    "slide2": "art-deco-architecture",
    "slide3": "modern-organic-architecture",
    "slide4": "suspension-bridge-engineering",
    "slide5": "gothic-cathedral-flying-buttress",
    "slide6": "concrete-dam-engineering",
    "slide7_img1": "cable-stayed-bridge",
    "slide7_img2": "burj-khalifa-skyscraper",
}

def get_unsplash_image(query, seed):
    try:
        safe_query = urllib.parse.quote(query)
        url = f"https://images.unsplash.com/featured/1200x800/?{safe_query}&sig={seed}"
        req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
        with urllib.request.urlopen(req, timeout=10) as response:
            return response.geturl().split('?')[0] + "?auto=format&fit=crop&w=1200&q=80"
    except Exception as e:
        print(f"Error fetching: {e}")
        return None

def main():
    html_filename = "index.html"
    epoch_start = datetime(2026, 1, 1)
    days_since_epoch = (datetime.now() - epoch_start).days
    four_week_period = days_since_epoch // 28
    
    with open(html_filename, "r", encoding="utf-8") as f:
        html_content = f.read()

    updates = 0
    for key, query in SLIDE_KEYWORDS.items():
        seed = four_week_period + hash(key) % 100
        img_url = get_unsplash_image(query, seed)
        if img_url:
            pattern = rf'(id="img-{key}"\s+src=")(.*?)(")'
            html_content, count = re.subn(pattern, rf'\1{img_url}\3', html_content, count=1)
            if count > 0:
                print(f"-> Updated {key}")
                updates += 1

    if updates > 0:
        with open(html_filename, "w", encoding="utf-8") as f:
            f.write(html_content)

if __name__ == "__main__":
    main()
