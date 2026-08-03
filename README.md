# JELE CHEWY × KAMU KAMU — Campaign Dashboard

แดชบอร์ดแคมเปญ JELE Chewy × KAMU KAMU (ก.ค.–ส.ค. 2026) · Facebook + TikTok

**Live:** https://achiralinin.github.io/jele-kamu-dashboard/

## ระบบทำงานยังไง

GitHub Actions รันทุก 30 นาที → `scripts/tiktok_scraper.py` ดึงยอดจากลิงก์โพสต์ TikTok ด้วย yt-dlp
→ `scripts/update_dashboard.py` เขียนผลลงบล็อก `LIVE DATA` ใน `index.html` → commit + push
→ GitHub Pages เสิร์ฟหน้าใหม่อัตโนมัติ

ยอด views จะไปเติมช่อง **View Actual** และ likes+comments+shares+saves ไปเติม **Engagement Actual**
ของ KOL แต่ละราย แล้วรวมขึ้นไปเป็นยอดกลุ่มและการ์ดบนสุดให้เอง

## เพิ่ม / แก้ลิงก์โพสต์ KOL

แก้ `KOL_LINKS` ใน `scripts/tiktok_scraper.py` — key ต้องตรงกับ `key` ของ KOL ใน `index.html`

```python
KOL_LINKS = {
    "chatangg": "https://vt.tiktok.com/ZS4yjnsWB/",
}
```

## กรอกผลจริงที่ดึงอัตโนมัติไม่ได้ (Facebook / AWO / VDO)

แก้ในบล็อก `GROUPS` ของ `index.html` โดยตรง แต่ละแถวมี 3 ช่อง

| ช่อง | ความหมาย |
|---|---|
| `ar` | Reach จริง |
| `av` | View จริง |
| `ae` | Engagement จริง |

ใส่ตัวเลขทับ `null` — ยอดรวมรายกลุ่ม การ์ดบนสุด และ % ความสำเร็จคำนวณต่อให้เอง
งบที่ใช้จริงแก้ที่ `ACTUAL_SPEND`

> อย่าแก้บล็อกระหว่าง `LIVE DATA START` / `LIVE DATA END` — Actions เขียนทับทุกรอบ

## ถ้าคลิปไหนดึงไม่ได้

TikTok บางคลิปติด age-restrict หรือ login gate ให้ใส่ยอดที่ดูด้วยตาลงใน `MANUAL_OVERRIDE`
ที่หัวไฟล์ `scripts/tiktok_scraper.py` แล้วระบบจะใช้ค่านั้นแทนการ scrape

ถ้ารอบไหน scrape ล้มเหลว สคริปต์จะเก็บค่ารอบก่อนหน้าไว้ ไม่รีเซ็ตเป็น 0

## รันเองแบบ manual

Actions → Auto Update Dashboard → Run workflow

หรือในเครื่อง:

```bash
pip install -U yt-dlp
python3 scripts/tiktok_scraper.py scrape_results.json
python3 scripts/update_dashboard.py scrape_results.json index.html
```

## ที่มาข้อมูล

`Client_Sheet_JELE CHEWY X KAMU KAMU — June2026.xlsx` (ชีต KPI · Working · KOL List · Timeline)
