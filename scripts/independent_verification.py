import os
import re
import json
from PIL import Image

BASE_DIR = r"D:\mulearn\website"
SOURCES_DIR = os.path.join(BASE_DIR, "sources", "mulearn")
SITE_DIR = os.path.join(BASE_DIR, "mulearn-chn")
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
    has_ws_date = "27th October" in events_txt
    has_ws_time = "4:00 PM – 5:15 PM" in events_txt
    has_ws_venue = "SDPK" in events_txt
    print(f"Web Slingers 27th October: {has_ws_date}, 4:00 PM - 5:15 PM: {has_ws_time}, SDPK: {has_ws_venue}")
    
    # Check that uncertain years remain unstated
    # Buildathon year
    b_year_null = "year: null, // Year unconfirmed on supplied poster" in events_txt
    # Useless Projects year
    u_year_null = "year: null, // Year unconfirmed on poster" in events_txt
    # Web Slingers year
    ws_year_null = "year: null" in events_txt
    print(f"Unconfirmed years kept null: Buildathon={b_year_null}, Useless={u_year_null}, WebSlingers={ws_year_null}")
    
    # 2. Team
    team_path = os.path.join(SITE_DIR, "data", "team.js")
    with open(team_path, "r", encoding="utf-8") as f:
        team_txt = f.read()
    
    # Count team entries (id: "team-...")
    team_ids = re.findall(r'id:\s*"team-[^"]+"', team_txt)
    print(f"Team members in team.js: {len(team_ids)}")
    
    # Check specific role labels
    roles_checked = {
        "Lead Enabler": "Lead Enabler" in team_txt,
        "Campus Co-Lead": "Campus Co-Lead" in team_txt,
        "Operational Lead": "Operational Lead" in team_txt,
        "IG Lead – AI": "IG Lead – AI" in team_txt,
        "IG Lead – UI/UX": "IG Lead – UI/UX" in team_txt,
        "IG Lead – Cyber Security": "IG Lead – Cyber Security" in team_txt,
        "IG Lead – Web": "IG Lead – Web" in team_txt,
        "IG Lead – Entrepreneurship": "IG Lead – Entrepreneurship" in team_txt
    }
    for r, exists in roles_checked.items():
        print(f"  Role '{r}' present: {exists}")
        
    # 3. Links
    links_path = os.path.join(SITE_DIR, "data", "links.js")
    with open(links_path, "r", encoding="utf-8") as f:
        links_txt = f.read()
    urls_checked = {
        "Register": "https://app.mulearn.org/register" in links_txt,
        "Discord": "https://discord.gg/DfnDfBhGha" in links_txt,
        "LinkedIn": "https://www.linkedin.com/company/gtech-mulearn-cec/" in links_txt,
        "Instagram": "https://www.instagram.com/mulearn.chn/" in links_txt,
        "Email": "mailto:gtechmulearncec@gmail.com" in links_txt,
        "µLearn Org": "https://mulearn.org/" in links_txt,
        "Interest Groups": "https://mulearn.org/interest-groups" in links_txt,
        "Careers": "https://mulearn.org/careers" in links_txt
    }
    for label, ok in urls_checked.items():
        print(f"  URL '{label}' verified: {ok}")

if __name__ == "__main__":
    check_contact_sheet()
    check_content_data()
