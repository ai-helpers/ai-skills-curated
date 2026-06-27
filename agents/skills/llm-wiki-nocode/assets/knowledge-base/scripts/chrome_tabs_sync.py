import sys
import subprocess
import os
import json
from datetime import datetime

def classify_tab(title, url):
    url_lower = url.lower()
    # 1. Email & Communication
    if any(pattern in url_lower for pattern in ["mail.google.com", "web.whatsapp.com", "chat.google.com", "slack.com"]):
        return "Email & Communication"
    # 2. Airflow DAGs
    elif "airflow" in url_lower and ("/dags/" in url_lower or "grid" in url_lower or "graph" in url_lower or "tree" in url_lower):
        return "Airflow DAGs"
    # 3. Databricks & Analytics
    elif "databricks.com" in url_lower:
        return "Databricks & Analytics"
    # 4. AWS & Cloud Infrastructure
    elif "aws.amazon.com" in url_lower or "awsapps.com" in url_lower:
        return "AWS & Cloud Infrastructure"
    # 5. Google Services (excluding Email/Communication)
    elif "google.com" in url_lower or "google.fr" in url_lower:
        # drive, docs, slides, calendar, groups, contacts
        return "Google Services"
    # 6. GitHub Repositories
    elif "github.com" in url_lower:
        return "GitHub Repositories"
    # 7. Data Platforms & Tools
    elif any(pattern in url_lower for pattern in ["atlassian.net", "atlassian.com", "collibra", "collibra.com", "collibra.be"]):
        return "Data Platforms & Tools"
    # 8. Articles & Reading
    elif any(pattern in url_lower for pattern in ["medium.com", "substack.com", "blogspot.com", "wikipedia.org", "dev.to", "github.io", "readthedocs", "towardsdatascience.com", "towardsdataengineering.com", "uber.com/blog"]):
        return "Articles & Reading"
    else:
        return "Other"

def main():
    if len(sys.argv) < 2:
        print("Usage: python3 chrome_tabs_sync.py <notebook_path>", file=sys.stderr)
        sys.exit(1)

    notebook_path = sys.argv[1]
    notebook_file = os.path.basename(notebook_path)
    
    # Strip extension
    notebook_name, _ = os.path.splitext(notebook_file)
    
    # Clean name for filename: e.g. "130 - Team - Staff" -> "130-team-staff"
    clean_name = notebook_name.lower().strip()
    # Replace " - " with "-"
    clean_name = clean_name.replace(" - ", "-")
    # Replace spaces with "-"
    clean_name = clean_name.replace(" ", "-")
    # Replace multiple dashes with single dash
    while "--" in clean_name:
        clean_name = clean_name.replace("--", "-")

    # Current date
    date_str = datetime.now().strftime("%Y-%m-%d")
    output_filename = f"{clean_name}-{date_str}.md"
    output_dir = "memory/bookmarks/snapshots"
    output_path = os.path.join(output_dir, output_filename)

    # 1. Fetch tabs using AppleScript
    applescript = """
    set output to ""
    tell application "Google Chrome"
    	set winList to every window
    	repeat with win in winList
    		set tabList to every tab of win
    		repeat with t in tabList
    			set output to output & (title of t) & "|||" & (URL of t) & "\n"
    		end repeat
    	end repeat
    end tell
    return output
    """

    print("Retrieving open tabs from Google Chrome...", file=sys.stderr)
    res = subprocess.run(["osascript", "-e", applescript], capture_output=True, text=True)
    if res.returncode != 0:
        print(f"Error running AppleScript: {res.stderr}", file=sys.stderr)
        sys.exit(1)

    lines = res.stdout.strip().split("\n")
    tabs = []
    for idx, line in enumerate(lines, start=1):
        if "|||" in line:
            parts = line.split("|||")
            if len(parts) >= 2:
                title = parts[0].strip()
                url = parts[1].strip()
                tabs.append({
                    "index": idx,
                    "title": title,
                    "url": url
                })

    total_tabs = len(tabs)
    print(f"Captured {total_tabs} open tabs.", file=sys.stderr)

    # Categorize tabs
    categories = {
        "Google Services": [],
        "AWS & Cloud Infrastructure": [],
        "Databricks & Analytics": [],
        "Airflow DAGs": [],
        "GitHub Repositories": [],
        "Data Platforms & Tools": [],
        "Email & Communication": [],
        "Articles & Reading": [],
        "Other": []
    }

    for tab in tabs:
        cat = classify_tab(tab["title"], tab["url"])
        categories[cat].append(tab)

    # Generate Markdown
    md_lines = []
    md_lines.append(f"# Chrome Tabs Snapshot: {notebook_name}")
    md_lines.append(f"**Date:** {date_str}  ")
    md_lines.append(f"**Profile:** {notebook_name}  ")
    md_lines.append(f"**Total Tabs:** {total_tabs}\n")

    md_lines.append("## Table of Contents\n")
    for cat in categories.keys():
        anchor = cat.lower().replace(" ", "-").replace("&", "-").replace("--", "-")
        # clean any dangling dashes
        anchor = anchor.strip("-")
        md_lines.append(f"- [{cat}](#{anchor})")
    md_lines.append("\n---\n")

    for cat, cat_tabs in categories.items():
        anchor = cat.lower().replace(" ", "-").replace("&", "-").replace("--", "-").strip("-")
        md_lines.append(f"## {cat}\n")
        if not cat_tabs:
            md_lines.append("*No open tabs in this category.*\n")
        else:
            md_lines.append("| # | Title | URL |")
            md_lines.append("|---|-------|-----|")
            for t in cat_tabs:
                md_lines.append(f"| {t['index']} | {t['title']} | {t['url']} |")
            md_lines.append("")
        md_lines.append("---")
        md_lines.append("")

    # Add timestamp
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M UTC+2")
    md_lines.append(f"**Snapshot captured:** {timestamp}")

    # Ensure snapshots directory exists
    os.makedirs(output_dir, exist_ok=True)

    # Write Markdown output
    with open(output_path, "w", encoding="utf-8") as f:
        f.write("\n".join(md_lines) + "\n")

    print(f"Snapshot successfully written to {output_path}", file=sys.stderr)
    print(f"Total Tabs: {total_tabs}")
    for cat, cat_tabs in categories.items():
        print(f"- {cat}: {len(cat_tabs)} tabs")

if __name__ == "__main__":
    main()
