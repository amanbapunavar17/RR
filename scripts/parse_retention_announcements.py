import urllib.request
import re
from html.parser import HTMLParser
import json

headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)'}

def fetch_url(url):
    req = urllib.request.Request(url, headers=headers)
    with urllib.request.urlopen(req, timeout=15) as resp:
        return resp.read().decode('utf-8', errors='ignore')

print("Fetching IPL announcement...")
try:
    ipl_html = fetch_url('https://www.iplt20.com/news/article/tata-ipl-2027-player-retentions-announced')
    print(f"IPL page fetched: {len(ipl_html)} chars")
    
    # Search for all links with pdf or text
    pdf_urls = re.findall(r'https?://[^\s"\'<>]+\.pdf[^\s"\'<>]*', ipl_html, re.I)
    print("Found PDF URLs in IPL page:", pdf_urls)
    
    # Also look for any hrefs containing pdf
    href_pdfs = re.findall(r'href=[\'"]([^\'"]*?\.pdf[^\'"]*)[\'"]', ipl_html, re.I)
    print("Found href PDFs:", href_pdfs)

    # Let's see all href links
    all_hrefs = re.findall(r'href=[\'"]([^\'"]+)[\'"]', ipl_html)
    relevant_hrefs = [h for h in all_hrefs if any(k in h.lower() for k in ['pdf', 'release', 'retain', 'retention', 'player'])]
    print("Relevant hrefs:", relevant_hrefs[:20])

except Exception as e:
    print(f"Error fetching IPL announcement: {e}")

print("\nFetching RR announcement...")
try:
    rr_html = fetch_url('https://www.rajasthanroyals.com/latest-news/ipl-2027-rr-players-retention-list-retained-released')
    print(f"RR page fetched: {len(rr_html)} chars")
    
    pdf_urls_rr = re.findall(r'https?://[^\s"\'<>]+\.pdf[^\s"\'<>]*', rr_html, re.I)
    print("Found PDF URLs in RR page:", pdf_urls_rr)
    
except Exception as e:
    print(f"Error fetching RR announcement: {e}")

