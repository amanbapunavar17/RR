import urllib.request
import os
import pypdf

os.makedirs('d:/RR/data_downloads', exist_ok=True)

headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)'}

urls = {
    'released': 'https://www.iplt20.com/cms/files/jot2qw8s50z1/3gFAJ4z1USxcXYhaZVl65L/2a463a9c02a5bb7fd12fa3fbe91cc299/TATA_IPL_2027-_Release_Player_List.pdf',
    'retained': 'https://www.iplt20.com/cms/files/jot2qw8s50z1/1YiPT45UgZ1olwgjsAjlG4/923c2a85f32a8e6b054a4b553ed98fe0/TATA_IPL_2027_-_Retained_Player_List.pdf'
}

for key, url in urls.items():
    dest = f'd:/RR/data_downloads/{key}_2027.pdf'
    print(f"Downloading {key} from {url} to {dest}...")
    req = urllib.request.Request(url, headers=headers)
    with urllib.request.urlopen(req, timeout=20) as resp, open(dest, 'wb') as f:
        f.write(resp.read())
    print(f"Downloaded {dest}, size: {os.path.getsize(dest)} bytes")

# Now extract text from both PDFs
for key in ['released', 'retained']:
    pdf_path = f'd:/RR/data_downloads/{key}_2027.pdf'
    reader = pypdf.PdfReader(pdf_path)
    print(f"\n--- {key.upper()} PDF: {len(reader.pages)} pages ---")
    full_text = []
    for idx, page in enumerate(reader.pages):
        text = page.extract_text()
        print(f"Page {idx+1} length: {len(text)}")
        full_text.append(f"--- PAGE {idx+1} ---\n" + text)
    
    txt_dest = f'd:/RR/data_downloads/{key}_2027.txt'
    with open(txt_dest, 'w', encoding='utf-8') as f:
        f.write('\n'.join(full_text))
    print(f"Saved full text to {txt_dest}")

