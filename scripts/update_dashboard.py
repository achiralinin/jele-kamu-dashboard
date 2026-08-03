#!/usr/bin/env python3
"""
เขียนผล scrape ลงบล็อก LIVE DATA ใน index.html
Usage: python3 scripts/update_dashboard.py scrape_results.json index.html
"""

import json
import re
import sys

START = '/* === LIVE DATA START === ห้ามแก้มือ · GitHub Actions เขียนทับทุก 30 นาที === */'
END = '/* === LIVE DATA END === */'


def main():
    results_file = sys.argv[1] if len(sys.argv) > 1 else 'scrape_results.json'
    html_file = sys.argv[2] if len(sys.argv) > 2 else 'index.html'

    with open(results_file) as f:
        data = json.load(f)

    html = open(html_file, encoding='utf-8').read()
    if START not in html or END not in html:
        print('ERROR: ไม่พบ LIVE DATA marker ใน index.html — ยกเลิก')
        sys.exit(1)

    block = f"{START}\nconst LIVE = {json.dumps(data, ensure_ascii=False, indent=2)};\n{END}"
    new_html = re.sub(
        re.escape(START) + r'.*?' + re.escape(END),
        lambda _: block,
        html,
        flags=re.DOTALL,
    )

    if new_html == html:
        print('ไม่มีอะไรเปลี่ยน')
        return

    with open(html_file, 'w', encoding='utf-8') as f:
        f.write(new_html)

    n = len([k for k in data if not k.startswith('_')])
    print(f'อัปเดต {html_file} แล้ว — {n} KOL · stamp {data.get("_updated", "-")}')


if __name__ == '__main__':
    main()
