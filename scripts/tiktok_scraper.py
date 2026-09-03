#!/usr/bin/env python3
"""
JELE CHEWY x KAMU KAMU — TikTok Scraper (yt-dlp)
ดึง views / likes / shares / comments / saves / followers จากลิงก์โพสต์ TikTok
Usage: python3 scripts/tiktok_scraper.py [output_json]
"""

import json
import sys
import subprocess
import time
import random
from datetime import datetime, timezone

# ============================================================
#  MANUAL OVERRIDE — KOL ที่ดึงยอดอัตโนมัติไม่ได้
#  (คลิปถูกจำกัดอายุ / ต้อง login / ลิงก์ตาย)
#  ใส่ยอดที่ดูด้วยตาจาก TikTok แล้วอัปเดตเป็นระยะ
# ============================================================
MANUAL_OVERRIDE = {
    # 'chatangg': {'views': 0, 'likes': 0, 'shares': 0, 'comments': 0, 'saves': 0, 'followers': 0},
}

# ============================================================
#  KOL LINKS — key ต้องตรงกับ key ใน index.html
# ============================================================
KOL_LINKS = {
    # --- คลิปแบรนด์ (Jele Chewy official) ---
    "vdo_teaser": "https://vt.tiktok.com/ZS4PJLMF4/",
    "vdo_launching": "https://vt.tiktok.com/ZS4PJ8yar/",
    "vdo_intro": "https://vt.tiktok.com/ZS4PJ1pox/",
    "vdo_review": "https://vt.tiktok.com/ZS4PJa3Sw/",
    # --- KOL ---
    "chatangg": "https://vt.tiktok.com/ZS4yjnsWB/",
    "100lowteens": "https://vt.tiktok.com/ZS4U6vYTF/",
    "sristories.official": "https://vt.tiktok.com/ZS4UfB9Gu/",
    "foodballstylee": "https://vt.tiktok.com/ZS4U7ftpy/",
}


def scrape_tiktok_video(url, timeout=25):
    """ดึง metadata ของคลิป TikTok ด้วย yt-dlp --dump-json"""
    try:
        result = subprocess.run(
            ['yt-dlp', '--dump-json', '--no-download', '--no-warnings', url],
            capture_output=True, text=True, timeout=timeout
        )

        if result.returncode != 0:
            print(f"    yt-dlp error: {result.stderr.strip()[:160]}")
            return None

        info = json.loads(result.stdout)
        return {
            'url': info.get('webpage_url', url),
            'views': info.get('view_count', 0) or 0,
            'likes': info.get('like_count', 0) or 0,
            'shares': info.get('repost_count', 0) or 0,
            'comments': info.get('comment_count', 0) or 0,
            'saves': (info.get('save_count')
                      or info.get('collect_count')
                      or info.get('favorite_count')
                      or info.get('bookmark_count')
                      or 0),
            'followers': info.get('channel_follower_count', 0) or 0,
        }

    except subprocess.TimeoutExpired:
        print(f"    Timeout scraping {url}")
    except json.JSONDecodeError as e:
        print(f"    JSON parse error: {e}")
    except Exception as e:
        print(f"    Error scraping {url}: {e}")
    return None


def main():
    output_file = sys.argv[1] if len(sys.argv) > 1 else 'scrape_results.json'

    # เก็บผลรอบก่อนไว้ ถ้ารอบนี้ดึงไม่ได้จะได้ไม่กลายเป็น 0
    previous = {}
    try:
        with open(output_file) as f:
            previous = json.load(f)
    except Exception:
        pass

    results = {}
    fresh = 0
    now = datetime.now(timezone.utc).strftime('%Y-%m-%d %H:%M')
    active = {k: v for k, v in KOL_LINKS.items() if v and str(v).strip()}

    print(f"Scraping {len(active)} KOL(s) using yt-dlp...")

    for username, link in active.items():
        if username in MANUAL_OVERRIDE:
            results[username] = dict(MANUAL_OVERRIDE[username], url=link)
            print(f"  @{username} — manual override")
            continue

        print(f"  Scraping @{username}...")
        data = scrape_tiktok_video(link)
        if data:
            data['ok'] = True          # ดึงสดสำเร็จรอบนี้
            data['as_of'] = now
            results[username] = data
            fresh += 1
            print(f"    Views: {data['views']:,} | Likes: {data['likes']:,} | "
                  f"Shares: {data['shares']:,} | Comments: {data['comments']:,} | "
                  f"Saves: {data['saves']:,}")
        else:
            old = previous.get(username)
            if isinstance(old, dict) and old.get('views'):
                old = dict(old)
                old['ok'] = False      # ค่าเก่า ไม่ใช่ยอดรอบนี้
                old.setdefault('as_of', previous.get('_updated'))
                results[username] = old
                print("    Failed — เก็บค่ารอบก่อนไว้แทน (ทำเครื่องหมายว่าค้าง)")
            else:
                print(f"    Failed to scrape @{username}")

        time.sleep(random.uniform(0.5, 1.5))

    # _updated ต้องหมายถึง "ครั้งล่าสุดที่ดึงยอดได้จริง" เท่านั้น
    # ถ้ารอบนี้ล้มทุกลิงก์ ให้คงเวลาเดิมไว้ ไม่งั้นแดชบอร์ดจะโกหกว่าข้อมูลสด
    if fresh > 0:
        results['_updated'] = now
    else:
        results['_updated'] = previous.get('_updated') or now
    results['_last_attempt'] = now
    results['_fresh'] = fresh
    results['_total'] = len(active)

    with open(output_file, 'w') as f:
        json.dump(results, f, indent=2, ensure_ascii=False)

    print(f"\nResults saved to {output_file}")
    print(f"Freshly scraped: {fresh}/{len(active)}"
          f"{'  <-- ALL FAILED, keeping previous values' if fresh == 0 else ''}")
    if fresh == 0:
        print("WARNING: TikTok returned no data this run. Numbers on the dashboard are stale.")


if __name__ == '__main__':
    main()
