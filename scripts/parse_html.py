import re
from bs4 import BeautifulSoup

with open("/Users/jeevanm/.gemini/antigravity-ide/scratch/audit/page_source.html", "r", encoding="utf-8") as f:
    html = f.read()

soup = BeautifulSoup(html, "html.parser")

print("=== CANONICAL & SEO TAGS ===")
canonical = soup.find_all("link", attrs={"rel": "canonical"})
print("Canonical:", [c.get("href") for c in canonical])

og_url = soup.find_all("meta", attrs={"property": "og:url"})
print("OG URL:", [m.get("content") for m in og_url])

hreflangs = soup.find_all("link", attrs={"rel": "alternate", "hreflang": True})
print("Hreflang count:", len(hreflangs))
for h in hreflangs[:5]:
    print("  hreflang:", h.get("hreflang"), "->", h.get("href"))

title = soup.find("title")
print("Title:", title.text if title else None)

h1s = soup.find_all("h1")
print("H1 count:", len(h1s))
for h in h1s:
    print("  H1:", h.text.strip())

print("\n=== IMAGES WITHOUT ALT ===")
imgs = soup.find_all("img")
print("Total images:", len(imgs))
missing_alt = [img for img in imgs if not img.get("alt")]
print("Images missing alt attribute:", len(missing_alt))
for img in missing_alt[:5]:
    print("  Missing alt img:", img)

print("\n=== PRELOADS & SCRIPTS ===")
preloads = soup.find_all("link", attrs={"rel": "preload"})
for p in preloads:
    print("  Preload:", p.get("as"), p.get("href"), p.get("fetchpriority"))

scripts = soup.find_all("script")
print("Total scripts:", len(scripts))
async_scripts = [s for s in scripts if s.get("src")]
print("External scripts count:", len(async_scripts))
for s in async_scripts[:15]:
    print("  Script src:", s.get("src"), "async:", s.has_attr("async"), "defer:", s.has_attr("defer"))

print("\n=== THIRD PARTY SCRIPTS ===")
third_parties = []
for s in async_scripts:
    src = s.get("src", "")
    if any(tp in src for tp in ["googletagmanager", "clarity", "taboola", "analytics", "facebook", "gtag"]):
        third_parties.append(src)
print("Third party scripts:", third_parties)
