import os
import re
import json
from PIL import Image

SITE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
BASE_DIR = os.path.dirname(SITE_DIR)
SOURCES_DIR = os.path.join(BASE_DIR, "sources", "mulearn")
DOCS_DIR = os.path.join(SITE_DIR, "docs")
MANIFEST_PATH = os.path.join(DOCS_DIR, "ASSET_MANIFEST.json")

def check_contact_sheet():
    print("=== CHECKING ASSET-REVIEW.HTML ===")
    html_path = os.path.join(DOCS_DIR, "asset-review.html")
    with open(html_path, "r", encoding="utf-8") as f:
        content = f.read()
    srcs = re.findall(r'<img src="([^"]+)"', content)
    print(f"Total <img> tags in contact sheet: {len(srcs)}")
    missing = 0
    for s in srcs:
        full = os.path.normpath(os.path.join(DOCS_DIR, s))
        if not os.path.exists(full):
            print(f"  ❌ Broken image: {s} -> {full}")
            missing += 1
    print(f"Broken image references in contact sheet: {missing}")
    return missing == 0

def check_content_data():
    print("\n=== CHECKING CONTENT DATA FILES ===")
    # 1. Events
    events_path = os.path.join(SITE_DIR, "data", "events.js")
    with open(events_path, "r", encoding="utf-8") as f:
        events_txt = f.read()
    
    # Check Web Slingers
    has_ws_date = ("27th October" in events_txt) or ("27 October" in events_txt)
    has_ws_time = ("4:00 PM – 5:15 PM" in events_txt) or ("4:00–5:15 PM" in events_txt)
    has_ws_venue = "SDPK" in events_txt
    print(f"Web Slingers 27 October: {has_ws_date}, 4:00–5:15 PM: {has_ws_time}, SDPK: {has_ws_venue}")
    
    # Check that uncertain years remain unstated (either null or omitted, never invented)
    b_year_unstated = ("year: null" in events_txt) or ("Year is not printed" in events_txt)
    u_year_unstated = ("year: null" in events_txt) or ("Year is not printed" in events_txt)
    ws_year_unstated = ("year: null" in events_txt) or ("Year is not printed" in events_txt)
    print(f"Unconfirmed years kept unstated: Buildathon={b_year_unstated}, Useless={u_year_unstated}, WebSlingers={ws_year_unstated}")
    
    # 2. Team
    team_path = os.path.join(SITE_DIR, "data", "team.js")
    with open(team_path, "r", encoding="utf-8") as f:
        team_txt = f.read()
    
    # Count team entries (supports both object notation and constructor call M(n, ...))
    team_ids = re.findall(r'id:\s*"(team-\d+-[^"]+)"', team_txt)
    if not team_ids:
        team_ids = re.findall(r'M\(\s*(\d+),', team_txt)
    print(f"Team members in team.js: {len(team_ids)}")
    
    # Key roles
    expected_roles = [
        "Lead Enabler",
        "Campus Co-Lead",
        "Operational Lead",
        "IG Lead – AI",
        "IG Lead – UI/UX",
        "IG Lead – Cyber Security",
        "IG Lead – Web",
        "IG Lead – Entrepreneurship"
    ]
    for r in expected_roles:
        present = r in team_txt
        print(f"  Role '{r}' present: {present}")
    
    # 3. Links
    links_path = os.path.join(SITE_DIR, "data", "links.js")
    with open(links_path, "r", encoding="utf-8") as f:
        links_txt = f.read()
    
    expected_urls = [
        ("Register", "https://app.mulearn.org/register"),
        ("Discord", "https://discord.gg/DfnDfBhGha"),
        ("LinkedIn", "https://www.linkedin.com/company/gtech-mulearn-cec/"),
        ("Instagram", "https://www.instagram.com/mulearn.chn/"),
        ("Email", "mailto:gtechmulearncec@gmail.com"),
        ("µLearn Org", "https://mulearn.org/"),
        ("Interest Groups", "https://mulearn.org/interest-groups"),
        ("Careers", "https://mulearn.org/careers")
    ]
    for label, url in expected_urls:
        present = url in links_txt
        print(f"  URL '{label}' verified: {present}")

if __name__ == "__main__":
    check_contact_sheet()
    check_content_data()
