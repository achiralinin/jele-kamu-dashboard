# JELE CHEWY × KAMU KAMU — Campaign Dashboard

แดชบอร์ดแคมเปญ JELE Chewy × KAMU KAMU (ก.ค.–ส.ค. 2026) · Facebook + TikTok

**Live:** https://achiralinin.github.io/jele-kamu-dashboard/

## ระบบทำงานยังไง

GitHub Actions รันทุก 30 นาที → `scripts/tiktok_scraper.py` ดึงยอดจากลิงก์โพสต์ TikTok ด้วย yt-dlp
→ commit ทับ `scrape_results.json` ไฟล์เดียว → `index.html` fetch ไฟล์นั้นตอนเปิดหน้า

**Actions ไม่แตะ `index.html` เลย** ดีไซน์กับข้อมูลสดแยกไฟล์กันชัดเจน แก้หน้าเว็บด้วยมือได้ทุกเมื่อ
โดยไม่ต้องกลัว merge conflict กับรอบ auto-update

ยอด views จะไปเติมช่อง **View Actual** และ likes+comments+shares+saves ไปเติม **Engagement Actual**
แล้วรวมขึ้นไปเป็นยอดกลุ่มและการ์ดบนสุดให้เอง

ตอนนี้ดึงอัตโนมัติ 8 คลิป — คลิปแบรนด์ 4 (Teaser / Launching / Introduction / Review) + KOL 4

## เพิ่ม / แก้ลิงก์โพสต์ TikTok

แก้ `KOL_LINKS` ใน `scripts/tiktok_scraper.py` — key ต้องตรงกับ `key` ของแถวนั้นใน `index.html`

```python
KOL_LINKS = {
    "vdo_teaser": "https://vt.tiktok.com/ZS4PJLMF4/",
    "chatangg": "https://vt.tiktok.com/ZS4yjnsWB/",
}
```

| key | ชิ้นงาน |
|---|---|
| `vdo_teaser` / `vdo_launching` / `vdo_intro` / `vdo_review` | คลิปแบรนด์ 4 ตัว |
| `chatangg` / `100lowteens` / `sristories.official` / `foodballstylee` | KOL 4 ราย |

## กรอกผลฝั่ง Facebook — ใช้ฟอร์มบนหน้าเว็บ (แนะนำ)

เปิดแดชบอร์ด → กดปุ่ม **＋ กรอกยอด Facebook** (อยู่ข้างหัวข้อ "KPI แยกตามกลุ่มงาน")
→ กรอก Views / Reach / Engagement ฝั่ง Facebook (ช่องที่มีเลขอยู่แล้วคือค่าปัจจุบัน แก้ทับได้)
→ กด **Copy JSON** → กด **เปิดไฟล์บน GitHub** → วางทับทั้งไฟล์ `manual_stats.json` → Commit

หน้าเว็บจะอัปเดตทันทีที่ commit เสร็จ ไม่ต้องแก้โค้ด ไม่ต้อง push จากเครื่อง

| ช่องในฟอร์ม | ไปอยู่ที่ |
|---|---|
| FB Views | View Actual (บวกกับยอด TikTok ถ้าชิ้นนั้นมีคลิป) |
| FB Reach | Reach Actual (TikTok ไม่เปิดให้ดึง reach จึงมาจาก FB ล้วน) |
| FB Eng. | Engagement Actual (บวกกับ TikTok เช่นกัน) |

> `manual_stats.json` มีค่าเมื่อไหร่ จะ**ทับ**ค่า `ar/av/ae` ที่ hardcode ไว้ใน `index.html`
> เว้นช่องว่าง = ใช้ค่าเดิม ไม่ได้แปลว่าศูนย์

## แก้ผลฝั่ง Facebook ในโค้ดโดยตรง (ทางสำรอง)

แก้ในบล็อก `GROUPS` ของ `index.html` โดยตรง แต่ละแถวมี 3 ช่อง

| ช่อง | ความหมาย |
|---|---|
| `ar` | Reach จาก Facebook |
| `av` | View จาก Facebook |
| `ae` | Engagement จาก Facebook |

ใส่ตัวเลขทับ `null` ได้เลย **แถวไหนมี `key` ระบบจะเอายอด TikTok บวกทับให้อีกที**
เช่น VDO Teaser กรอก `av:` เป็นยอดวิวฝั่ง FB อย่างเดียว แล้วยอด TikTok จะบวกเพิ่มเองทุกรอบ
ยอดรวมรายกลุ่ม การ์ดบนสุด และ % ความสำเร็จคำนวณต่อให้เอง — งบที่ใช้จริงแก้ที่ `ACTUAL_SPEND`

> TikTok ไม่เปิดตัวเลข reach ให้ดึง ช่อง Reach Actual จึงต้องกรอกมือทั้งหมด

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
```

> เปิด `index.html` จาก `file://` ตรง ๆ จะไม่เห็นยอดสด (เบราว์เซอร์บล็อก fetch)
> ให้ดูที่ GitHub Pages หรือรัน `python3 -m http.server` ในโฟลเดอร์นี้

## ที่มาข้อมูล

`Client_Sheet_JELE CHEWY X KAMU KAMU — June2026.xlsx` (ชีต KPI · Working · KOL List · Timeline)
