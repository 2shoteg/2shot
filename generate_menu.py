import requests
import csv
import io
import hashlib
import json

# =============================================
# 🔗 رابط Google Sheets (CSV)
# =============================================
SHEET_URL = "https://docs.google.com/spreadsheets/d/e/2PACX-1vSNymcwLC-PZdkS07k46Yg3dIYhtUoWIsXypczOI0UcV3woXR7xXZkKFh60jJMn0-xH-q6j60P0aXWt/pub?gid=0&single=true&output=csv"

# =============================================
# 📋 الأعمدة المتوقعة في الشيت:
# category_id | category_ar | category_en | category_icon | type | name_ar | name_en | price | seasonal
#
# category_id: مثال hot, ice, frapp, milkshake ...
# type: item أو addon
# seasonal: 1 لو موسمي، فاضي لو لا
# =============================================

WA = "201111385543"

LOGO_SVG = '''<svg id="Layer_1" style="filter: drop-shadow(0 0 6px rgba(255,255,255,0.5)) drop-shadow(0 0 14px rgba(255,255,255,0.3))" data-name="Layer 1" xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1684.54 1577.16">
  <path fill="#FFFFFF" d="M387.47,1470.14c-.55,1.33-2.56,1.56-5.32,2.24-3.59.71-7.67,1.19-11.38,1.6-78.92,9.81-134.84,14.55-209.49,32.39-10.21,2.81-18.64,5.82-23.9,8.98-6.71,4.03-8.27,8.33-1.81,12.79,107.12,36.75,274.95,33.2,375.81,42.69,202.74,10.95,356.58,8,527.35-11.79,44.63-7.03,163.77-10.58,189.37-41.65-29.54-34.68-177.77-35.22-243.1-48.92-7.73-4.06,12.3-12.69,15.18-15.45,48.95-31.77,92.67-72.38,127.99-118.74,5.11-6.3,9.17-13.62,15.69-18.52,187.73-21.93,393.12-95.29,510.04-255.88,45.29-78.31,42.69-194.23-23.28-261.76-28.88-30.94-76.83-48.87-120.24-51.91-27.19-1.57-76.07-1.86-78.69,10.54-7.61,26.42-14.06,53.31-20.31,80.09-4.27,14.99,8.36,13.4,18.34,10.82,40.06-8.93,88.28-3.66,116.84,28.45,88.78,123.64-100.77,238.11-206.19,280.68-26.07,9.76-79.27,30.35-96.65,27.96-4.73-1.4-1.21-9.26.04-12.77,45.1-107.65,72.97-268.85,64.21-389.75-.3-5.61-1.39-14.13,2.54-18.54,5.11-6.04,14.7-5.19,21.96-5.55,11.46-.35,22.9-.69,34.36-1.04,7.94-.18,18.2,0,21.85-8.53,2.07-4.82,1.36-11.49.95-16.73-1.42-20.31-2.9-40.64-4.35-60.98-.33-4.93-.85-10.24-3.23-14.56-2.81-5.5-9.45-7.16-15.29-6.71-88.12,3.12-176.77,6.32-264.72,11.91-11.65,2.49-15.26,14.28-15.09,24.86-2.77,50.6,42.22,90.83,91.51,84.69,16.17-3.1,12.06,13.88,12.75,24.2.25,34.66-1.18,68.24-4.44,103.24-17.42,143.88-37.26,306.1-136.18,414.69-134.11,136.18-348.85,157.18-526.14,95.32-183.06-60.31-346.23-233.04-388.59-440.17-50.79-192.93,34.25-254.77,220.34-221.93,5.93.09,10.78-.34,15.83-1.88,30.38-9.05,51.63-61.63,21.9-81.3-30.03-18.97-73.67-16.3-107.97-19.12-85.09-1.88-158.66-1.68-260.06,8.97-9.4,1.44-14.81,7.9-15.82,16.6-59.16,333.75,152.62,633.4,377.43,800.37l-.02.07Z"></path>
  <path fill="#FFFFFF" d="M670.96,683.6c1.08-.53,1.9-1.88,2.67-3.87.97-2.53,1.84-6.25,2.52-9.28,7.7-36.95,27.65-72.96,61.82-90.67,6.94-3.85,15.14-7.68,23.39-11.33,30.37-13.01,62.56-27.56,92.02-42.96,85.94-41.79,137.22-95.73,141.12-192.58.14-4.88-.6-13.38-6.7-6.17-8.32,10.57-15.63,21.33-24.82,31.52-45.13,54.68-106.15,81.64-171.16,111.7-19.06,8.97-37.98,17.44-57.05,26.38-18.77,8.91-38.19,17.67-52.89,32.65-35.7,35.14-51.11,88.17-27.82,134.73,2.66,4.61,10.79,21.88,16.82,19.92l.1-.05Z"></path>
  <path fill="#FFFFFF" d="M600.9,659.42c2.35-4.49-1.07-11.61-2.04-16.4-11.29-39.4-8.31-85.88,18.95-117.89,17.4-21.25,40.8-36.31,63.75-51.06,42.91-27.35,85.55-51.51,130.43-74.46,67.89-34.55,90.32-39.78,129.22-84.43,21.01-23.56,37.74-51.22,48.85-80.91,10.15-28.87,14.97-49.79,13.17-70.42-7.42-65.91-64.9-113.46-101.48-134.71-99.76-60.47-228.79-13.18-276.95,19.71-44.79,36.36-70.88,99.77-58.08,153.73,3.87,17.91,12.35,35.69,23.54,50.95,14.75,21.25,29.73,29.3,58.27,36.53,5.54,1.35,11.66,3.72,17.08,3.44,4.72-.68-1.47-7.06-2.89-9.34-18.43-23.49-26.79-56.55-19.87-86.11,4.08-19.57,12.53-36.8,27.57-49.72,32.68-29.06,83.81-30.78,121-9.44,19.87,11.02,37.71,28.67,43.25,50.86,8.08,31.02-11.48,59.14-31.64,80.9-23.31,25.12-53.36,51.42-82.88,66.82-35.3,19.23-71.48,29.2-105.39,52.16-45.44,32.82-97.24,84.6-101.62,146.41-1.46,31.02,11.01,62.84,29.86,86.52,10.29,12.32,23.35,22.37,37.22,30.77,4.36,2.39,16.61,10.53,20.59,6.2l.07-.1Z"></path>
  <path fill="#FFFFFF" d="M234.95,1126.52c-9.72,1.62,29.19,56.43,35,63.66,26.8,35.19,74.62,89.34,120.23,51.73,20.04-18.98,23.99-48.77,26.71-74.95,7.14-78.46-26.26-135.73-87.43-182.03-23.21-18.92-46.8-34.23-45.04-67.67,1.17-19.37,16.71-29.88,35.13-30.69,22.32-1.93,49.12,9.82,67.38-3.51,15.85-12.2,16.12-35.79,17.83-54.48,5.48-48.16-46.47-41.06-78.97-42.45-43.57-.73-75.24-6.45-113.74,20.07-82.73,57.08-35.59,176.31,43.88,239.22,21.86,17.69,43.46,38.52,47.75,67.47,1.34,10.29.53,22.63-6.75,30.65-7.78,8.7-20.94,7.96-30.64,2.99-7.83-3.71-14.68-9.06-20.77-13.66-2.89-2.04-7.63-6.05-10.46-6.35h-.11Z"></path>
  <path fill="#FFFFFF" d="M628.22,947.31c-8.62,8.05-21.56,6.93-32.63,7.53-19.9.91-35.82-.96-39.77-17.69-5.8-82.91-1.94-166.79-6.32-249.9.53-26.99-25.48-27.67-46.13-27.25-39.6-2.03-59.38-3.36-56.29,39.47,1.21,200.71-5.81,401.96-.07,602.44,1.87,9.55,5.91,17.97,12.99,24.22,12.88,11.26,30.52,14.02,46.63,18.73,13.58,4.02,32.54,9.61,38.52-.55,3.16-4.13,4.29-12.25,4.42-17.9,2.33-77.12,1.78-154.57,5.42-231.62.4-23.63,20.83-26.26,40.85-25.82,13.24-.59,30.96-.5,35.43,15.02,7.64,88.88,2.93,179.14,7.43,268.37-.52,18.29,9.62,33.83,28.71,36.1,9.69,1.66,19.9,1,29.71.1,14.21-1.15,29.32-.91,37.06-13.41,14.51-199.8,5.1-403.95,11.55-605.11.91-11.06-1.95-26.57-12.11-30.59-12.36-5.95-32.61-3.27-47.5-4.01-17.48-.23-39.37-2.47-44.85,16.06-6.09,58.12-2.41,117.21-5.65,175.6-.5,7-2.19,15.18-7.27,20.08l-.13.13Z"></path>
  <path fill="#FFFFFF" d="M1079.41,790.31c-24.54-61.76-82.22-129.48-155.76-117.38-73.11,14.86-105.73,90.46-127.24,156.42-34.6,115.26-35.7,266.81,2.91,378.47,12.6,35.32,31.16,72.93,58.72,97.48,48.21,45.32,118.94,31.77,161.89-13.22,41.69-42.17,66.23-103.62,79.49-161.55,23.72-110.21,21.9-235.61-19.93-340.05l-.07-.18ZM996.13,1104.01c-3.23,35.63-12.97,130.72-60.98,119.29-20.69-9-30.4-31.98-36.59-53.73-17.7-76.61-12.59-154.43-9.76-232.09,2.52-31.64,5.06-64.72,16.38-94.69,7.37-21.23,28.95-55.26,53.79-41.97,36.35,22.3,38.17,88.21,40.75,127.88,2.38,58.37,1.17,116.95-3.58,175.14v.17Z"></path>
</svg>'''

def fetch_sheet():
    print("📥 جاري تحميل البيانات من Google Sheets...")
    r = requests.get(SHEET_URL)
    r.encoding = 'utf-8'
    reader = csv.DictReader(io.StringIO(r.text))
    return list(reader)

def parse_data(rows):
    cats = {}
    cat_order = []
    for row in rows:
        cid = row.get('category_id','').strip()
        if not cid:
            continue
        if cid not in cats:
            cats[cid] = {
                'icon': row.get('category_icon','').strip(),
                'ar': row.get('category_ar','').strip(),
                'en': row.get('category_en','').strip(),
                'items': [],
                'addons': []
            }
            cat_order.append(cid)
        rtype = row.get('type','').strip().lower()
        name_ar = row.get('name_ar','').strip()
        name_en = row.get('name_en','').strip()
        price = row.get('price','').strip()
        seasonal = row.get('seasonal','').strip()
        if not name_ar or not price:
            continue
        entry = {'ar': name_ar, 'en': name_en, 'p': int(price)}
        if seasonal == '1':
            entry['b'] = 1
        if rtype == 'addon':
            cats[cid]['addons'].append(entry)
        else:
            cats[cid]['items'].append(entry)
    return cats, cat_order

def mk_id(cat_id, typ, idx):
    raw = f"{cat_id}_{typ}_{idx}"
    return hashlib.md5(raw.encode()).hexdigest()[:6]

def build_cats_js(cats, cat_order):
    lines = []
    for cid in cat_order:
        c = cats[cid]
        items_js = json.dumps(c['items'], ensure_ascii=False)
        addons_js = json.dumps(c['addons'], ensure_ascii=False)
        # convert {"ar":...,"en":...,"p":...} to {ar:...,en:...,p:...}
        def to_js_obj(s):
            import re
            s = re.sub(r'"ar":', 'ar:', s)
            s = re.sub(r'"en":', 'en:', s)
            s = re.sub(r'"p":', 'p:', s)
            s = re.sub(r'"b":', 'b:', s)
            return s
        lines.append(
            f'  {cid}:{{icon:"{c["icon"]}",ar:"{c["ar"]}",en:"{c["en"]}",\n'
            f'    items:{to_js_obj(items_js)},\n'
            f'    addons:{to_js_obj(addons_js)}}}')
    return 'const cats = {\n' + ',\n'.join(lines) + '\n};'

def build_grid_html(cats, cat_order):
    html = ''
    for cid in cat_order:
        c = cats[cid]
        html += f'      <div class="cat-card" onclick="showCat(\'{cid}\')"><span class="ci">{c["icon"]}</span><span class="ca">{c["ar"]}</span><span class="ce">{c["en"]}</span></div>\n'
    return html

def generate_html(cats, cat_order):
    cats_js = build_cats_js(cats, cat_order)
    grid_html = build_grid_html(cats, cat_order)

    html = f'''<!DOCTYPE html>
<html lang="ar" dir="rtl">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>2Shot - Menu</title>
<style>
@font-face{{font-family:"Tajawal";font-weight:400;src:url(https://fonts.gstatic.com/s/tajawal/v12/Iura6YBj_oCad4k1nzSBC45I.woff2) format("woff2");unicode-range:U+0600-06FF}}
@font-face{{font-family:"Tajawal";font-weight:400;src:url(https://fonts.gstatic.com/s/tajawal/v12/Iura6YBj_oCad4k1nzGBCw.woff2) format("woff2");unicode-range:U+0000-00FF}}
@font-face{{font-family:"Tajawal";font-weight:700;src:url(https://fonts.gstatic.com/s/tajawal/v12/Iurf6YBj_oCad4k1l4qkHrRpiYlJ.woff2) format("woff2");unicode-range:U+0600-06FF}}
@font-face{{font-family:"Tajawal";font-weight:700;src:url(https://fonts.gstatic.com/s/tajawal/v12/Iurf6YBj_oCad4k1l4qkHrFpiQ.woff2) format("woff2");unicode-range:U+0000-00FF}}
@font-face{{font-family:"Tajawal";font-weight:900;src:url(https://fonts.gstatic.com/s/tajawal/v12/Iurf6YBj_oCad4k1l7KmHrRpiYlJ.woff2) format("woff2");unicode-range:U+0600-06FF}}
@font-face{{font-family:"Tajawal";font-weight:900;src:url(https://fonts.gstatic.com/s/tajawal/v12/Iurf6YBj_oCad4k1l7KmHrFpiQ.woff2) format("woff2");unicode-range:U+0000-00FF}}

:root{{--bg:#0E0E0E;--accent:#2ECC71;--dg:#1A4D35;--cream:#F5F5F5;--muted:#999}}
*{{margin:0;padding:0;box-sizing:border-box}}
body{{background:var(--bg);font-family:"Tajawal",sans-serif;color:var(--cream);min-height:100vh;overflow-x:hidden}}
body::before{{content:"";position:fixed;inset:0;background:radial-gradient(ellipse at 20% 20%,rgba(46,204,113,.06) 0%,transparent 50%),radial-gradient(ellipse at 80% 80%,rgba(46,204,113,.04) 0%,transparent 50%);pointer-events:none;z-index:0}}
.page{{display:none;position:relative;z-index:1}}
.page.active{{display:block}}
#home{{max-width:640px;margin:0 auto;padding:40px 20px 80px;text-align:center}}
.logo-wrap{{display:flex;justify-content:center;padding:20px 0 10px;margin-right:-26px}}
.logo-wrap svg{{width:min(200px,50vw);height:auto}}
.cb-sub{{font-size:clamp(11px,2.5vw,15px);letter-spacing:6px;text-transform:uppercase;color:var(--accent);opacity:.9;margin-top:10px}}
.ornament{{display:flex;align-items:center;justify-content:center;gap:16px;margin:20px 0}}
.orn-line{{flex:1;height:1px;background:linear-gradient(90deg,transparent,var(--accent),transparent);max-width:120px}}
.orn-diamond{{width:8px;height:8px;background:var(--accent);transform:rotate(45deg);box-shadow:0 0 8px rgba(46,204,113,.6)}}
.page-title{{font-size:clamp(20px,4vw,28px);font-weight:400;color:#fff;letter-spacing:2px;text-shadow:0 0 12px rgba(255,255,255,.15)}}
.offers-btn{{display:block;width:100%;background:linear-gradient(135deg,#1a3a20,#0d2d15);border:1px solid rgba(46,204,113,.4);border-radius:16px;padding:18px 20px;margin:0 0 24px;cursor:pointer;transition:all .3s;text-align:center}}
.offers-btn:hover{{border-color:var(--accent);box-shadow:0 0 24px rgba(46,204,113,.3);transform:translateY(-2px)}}
.offers-btn .ob-icon{{font-size:26px}}
.offers-btn .ob-ar{{font-size:17px;font-weight:900;color:var(--accent);display:block;margin-top:4px}}
.offers-btn .ob-en{{font-size:11px;color:var(--muted);letter-spacing:1px}}
.offers-btn .ob-badge{{display:inline-block;background:rgba(46,204,113,.15);color:var(--accent);border:1px solid rgba(46,204,113,.35);border-radius:20px;font-size:10px;font-weight:700;padding:2px 10px;margin-top:6px}}
.grid{{display:grid;grid-template-columns:repeat(2,1fr);gap:14px}}
.cat-card{{background:linear-gradient(135deg,#111,#1a2e1f);border:1px solid rgba(46,204,113,.15);border-radius:16px;padding:22px 16px;cursor:pointer;transition:all .3s;position:relative;overflow:hidden;text-align:center}}
.cat-card::before{{content:"";position:absolute;inset:0;background:linear-gradient(135deg,var(--dg),var(--accent));opacity:0;transition:opacity .3s}}
.cat-card:hover,.cat-card:active{{border-color:var(--accent);box-shadow:0 0 24px rgba(46,204,113,.35);transform:translateY(-2px)}}
.cat-card:hover::before{{opacity:1}}
.cat-card:hover .ci,.cat-card:hover .ca,.cat-card:hover .ce{{color:#000!important}}
.ci{{font-size:28px;display:block;margin-bottom:10px;position:relative;z-index:1}}
.ca{{font-size:16px;font-weight:700;color:var(--cream);display:block;position:relative;z-index:1;transition:color .3s}}
.ce{{font-size:11px;color:var(--muted);display:block;letter-spacing:1px;text-transform:uppercase;position:relative;z-index:1;margin-top:3px;transition:color .3s}}
#cat-page{{max-width:900px;margin:0 auto;padding:0 20px 100px}}
.back-btn{{display:inline-flex;align-items:center;gap:8px;background:rgba(46,204,113,.1);border:1px solid rgba(46,204,113,.3);color:var(--accent);padding:10px 20px;border-radius:30px;cursor:pointer;font-family:"Tajawal",sans-serif;font-size:14px;font-weight:700;margin:24px 0 24px;transition:all .25s}}
.back-btn:hover{{background:rgba(46,204,113,.2)}}
.back-btn svg{{width:18px;height:18px;fill:currentColor}}
.cat-hdr{{display:flex;align-items:center;gap:16px;margin-bottom:24px;padding-bottom:14px;border-bottom:1px solid rgba(46,204,113,.2)}}
.cat-hdr-icon{{font-size:28px;width:54px;height:54px;background:rgba(26,77,53,.3);border:1px solid rgba(46,204,113,.5);border-radius:50%;display:flex;align-items:center;justify-content:center;flex-shrink:0}}
.cat-hdr-ar{{font-size:26px;font-weight:700;color:var(--accent)}}
.cat-hdr-en{{font-size:13px;color:var(--muted);letter-spacing:2px;text-transform:uppercase;text-align:left}}
.items-grid{{display:grid;grid-template-columns:repeat(auto-fill,minmax(260px,1fr));gap:10px}}
.menu-item{{display:flex;justify-content:space-between;align-items:center;padding:14px 16px;background:rgba(255,255,255,.02);border:1px solid rgba(255,255,255,.07);border-radius:10px;transition:border .2s;gap:10px}}
.menu-item.has-qty{{border-color:rgba(46,204,113,.5);background:rgba(26,77,53,.15)}}
.item-left{{flex:1}}
.item-name-ar{{font-size:14px;font-weight:500;color:var(--cream)}}
.item-name-en{{font-size:11px;color:var(--muted);font-style:italic}}
.item-right{{display:flex;flex-direction:column;align-items:flex-end;gap:8px;flex-shrink:0}}
.item-price{{font-size:15px;font-weight:700;color:var(--accent);text-shadow:0 0 8px rgba(46,204,113,.4);white-space:nowrap}}
.item-price span{{font-size:10px;font-weight:400;color:var(--muted)}}
.qty-row{{display:flex;align-items:center;gap:8px}}
.qty-btn{{width:28px;height:28px;border-radius:50%;border:1px solid rgba(46,204,113,.5);background:rgba(26,77,53,.3);color:var(--accent);font-size:18px;font-weight:700;cursor:pointer;display:flex;align-items:center;justify-content:center;transition:all .2s;line-height:1;flex-shrink:0}}
.qty-btn:hover{{background:var(--accent);color:#000}}
.qty-num{{font-size:15px;font-weight:700;color:var(--accent);min-width:18px;text-align:center}}
.addons-section{{margin-top:28px;padding-top:20px;border-top:1px dashed rgba(46,204,113,.2)}}
.addons-label{{font-size:13px;font-weight:700;color:var(--accent);letter-spacing:2px;margin-bottom:12px;opacity:.8}}
.addons-grid{{display:grid;grid-template-columns:repeat(auto-fill,minmax(180px,1fr));gap:8px}}
.addon-item{{display:flex;justify-content:space-between;align-items:center;padding:10px 14px;background:rgba(26,77,53,.1);border:1px dashed rgba(255,255,255,.12);border-radius:8px;transition:border .2s;gap:8px}}
.addon-item.has-qty{{border-color:rgba(46,204,113,.5);background:rgba(26,77,53,.2)}}
.badge{{font-size:9px;background:rgba(46,204,113,.15);color:var(--accent);border:1px solid rgba(46,204,113,.35);border-radius:20px;padding:2px 7px;margin-right:5px;vertical-align:middle}}
.cart-fab{{position:fixed;bottom:24px;left:50%;transform:translateX(-50%);z-index:200;background:linear-gradient(135deg,var(--dg),var(--accent));border:none;border-radius:40px;padding:14px 28px;color:#000;font-family:"Tajawal",sans-serif;font-size:15px;font-weight:900;cursor:pointer;box-shadow:0 4px 24px rgba(46,204,113,.5);display:none;align-items:center;gap:10px;white-space:nowrap;transition:all .3s}}
.cart-fab.show{{display:flex}}
.cart-fab:hover{{transform:translateX(-50%) translateY(-2px)}}
.cart-count{{background:#000;color:var(--accent);border-radius:50%;width:22px;height:22px;font-size:12px;display:flex;align-items:center;justify-content:center;font-weight:900;line-height:1}}
.overlay{{position:fixed;inset:0;background:rgba(0,0,0,.85);z-index:300;display:none;align-items:flex-end;justify-content:center}}
.overlay.open{{display:flex}}
.sheet{{background:#141414;border:1px solid rgba(46,204,113,.3);border-radius:24px 24px 0 0;padding:28px 24px 44px;width:100%;max-width:500px;max-height:90vh;overflow-y:auto;animation:slideUp .3s ease;position:relative}}
@keyframes slideUp{{from{{transform:translateY(100%)}}to{{transform:translateY(0)}}}}
.sheet-title{{font-size:20px;font-weight:900;color:var(--accent);margin-bottom:20px;text-align:center;letter-spacing:2px}}
.close-btn{{position:absolute;top:16px;left:16px;background:rgba(255,255,255,.08);border:none;border-radius:50%;width:32px;height:32px;color:var(--muted);font-size:18px;cursor:pointer}}
.order-row{{display:flex;justify-content:space-between;align-items:center;padding:10px 0;border-bottom:1px solid rgba(255,255,255,.06);font-size:14px;gap:8px}}
.order-row .qty-row{{gap:6px}}
.order-row .qty-btn{{width:24px;height:24px;font-size:14px}}
.order-row .qty-num{{font-size:13px;min-width:16px}}
.order-total{{display:flex;justify-content:space-between;font-size:17px;font-weight:900;padding:16px 0 20px;border-top:1px solid rgba(46,204,113,.3);margin-top:4px}}
.order-total span:last-child{{color:var(--accent);font-size:20px}}
.field{{margin-bottom:14px}}
.field label{{font-size:12px;color:var(--muted);letter-spacing:1px;margin-bottom:6px;display:block}}
.field input{{width:100%;background:rgba(255,255,255,.05);border:1px solid rgba(46,204,113,.25);border-radius:10px;padding:12px 16px;color:var(--cream);font-family:"Tajawal",sans-serif;font-size:15px;outline:none;transition:border .2s}}
.field input:focus{{border-color:var(--accent)}}
.send-btn{{width:100%;background:linear-gradient(135deg,var(--dg),var(--accent));border:none;border-radius:14px;padding:16px;color:#000;font-family:"Tajawal",sans-serif;font-size:16px;font-weight:900;cursor:pointer;margin-top:8px;display:flex;align-items:center;justify-content:center;gap:10px;transition:all .3s}}
.send-btn:hover{{box-shadow:0 0 24px rgba(46,204,113,.5)}}
.dev-credit{{text-align:center;margin-top:6px}}
.dev-btn{{display:inline-flex;align-items:center;gap:6px;background:rgba(255,255,255,.04);border:1px solid rgba(255,255,255,.1);border-radius:20px;padding:5px 14px;color:var(--muted);font-family:"Tajawal",sans-serif;font-size:11px;cursor:pointer;transition:all .25s;text-decoration:none}}
.dev-btn:hover{{border-color:rgba(46,204,113,.4);color:var(--accent)}}
.dev-btn svg{{width:13px;height:13px;fill:currentColor;opacity:.7}}
footer{{text-align:center;padding:40px 20px;border-top:1px solid rgba(255,255,255,.08);margin-top:20px}}
.footer-note{{font-size:12px;color:var(--muted);margin-top:8px;letter-spacing:1px}}
@keyframes fadeUp{{from{{opacity:0;transform:translateY(20px)}}to{{opacity:1;transform:translateY(0)}}}}
</style>
</head>
<body>

<!-- HOME -->
<div id="home" class="page active">
  <div style="max-width:640px;margin:0 auto;padding:40px 20px 80px;text-align:center">
    <div class="logo-wrap">{LOGO_SVG}</div>
    <div class="cb-sub">Coffee &amp; Bar</div>
    <div class="ornament"><div class="orn-line"></div><div class="orn-diamond"></div><div class="orn-line"></div></div>
    <div class="page-title">قائمة المشروبات والحلويات</div>
    <div class="ornament"><div class="orn-line"></div><div class="orn-diamond"></div><div class="orn-line"></div></div>
    <div class="grid">
{grid_html}    </div>
    <footer>
      <div style="text-align:center;margin-bottom:10px;margin-right:-10px">{LOGO_SVG}</div>
      <div class="footer-note">2Shot Coffee &amp; Bar</div>
      <div class="dev-credit" style="margin-top:12px">
        <a class="dev-btn" href="https://wa.me/201211255580" target="_blank">
          <svg viewBox="0 0 24 24"><path d="M12 2C6.48 2 2 6.48 2 12s4.48 10 10 10 10-4.48 10-10S17.52 2 12 2zm-2 14.5v-9l6 4.5-6 4.5z"/></svg>
          هل تريد موقع مثل هذا؟
        </a>
      </div>
    </footer>
  </div>
</div>

<!-- CATEGORY PAGE -->
<div id="cat-page" class="page">
  <div id="cat-page-inner"></div>
</div>

<!-- CART FAB -->
<button class="cart-fab" id="cartFab" onclick="openCheckout()">
  🛒 <span>عرض الطلب</span>
  <span class="cart-count" id="cartCount">0</span>
</button>

<!-- CHECKOUT -->
<div class="overlay" id="overlay">
  <div class="sheet">
    <button class="close-btn" onclick="closeCheckout()">✕</button>
    <div class="sheet-title">🛒 طلبك</div>
    <div id="orderList"></div>
    <div class="order-total"><span>الإجمالي</span><span id="orderTotal">0 ج</span></div>
    <div class="field"><label>الاسم</label><input id="custName" placeholder="اكتب اسمك" /></div>
    <div class="field"><label>رقم التليفون</label><input id="custPhone" type="tel" placeholder="رقمك" /></div>
    <button class="send-btn" onclick="sendOrder()">
      <svg width="20" height="20" viewBox="0 0 24 24" fill="currentColor"><path d="M17.472 14.382c-.297-.149-1.758-.867-2.03-.967-.273-.099-.471-.148-.67.15-.197.297-.767.966-.94 1.164-.173.199-.347.223-.644.075-.297-.15-1.255-.463-2.39-1.475-.883-.788-1.48-1.761-1.653-2.059-.173-.297-.018-.458.13-.606.134-.133.298-.347.446-.52.149-.174.198-.298.298-.497.099-.198.05-.371-.025-.52-.075-.149-.669-1.612-.916-2.207-.242-.579-.487-.5-.669-.51-.173-.008-.371-.01-.57-.01-.198 0-.52.074-.792.372-.272.297-1.04 1.016-1.04 2.479 0 1.462 1.065 2.875 1.213 3.074.149.198 2.096 3.2 5.077 4.487.709.306 1.262.489 1.694.625.712.227 1.36.195 1.871.118.571-.085 1.758-.719 2.006-1.413.248-.694.248-1.289.173-1.413-.074-.124-.272-.198-.57-.347z"/><path d="M12 0C5.373 0 0 5.373 0 12c0 2.127.558 4.126 1.528 5.857L.057 23.882l6.184-1.622A11.954 11.954 0 0012 24c6.627 0 12-5.373 12-12S18.627 0 12 0zm0 22c-1.854 0-3.6-.5-5.1-1.373l-.366-.217-3.671.963.98-3.582-.239-.381A9.938 9.938 0 012 12C2 6.477 6.477 2 12 2s10 4.477 10 10-4.477 10-10 10z"/></svg>
      ارسل الطلب على واتساب
    </button>
  </div>
</div>

<script>
const WA = "{WA}";
{cats_js}

let cart = {{}};

function mkId(catId, type, idx){{ return catId+"_"+type+"_"+idx; }}

function showPage(id){{
  document.querySelectorAll(".page").forEach(p=>p.classList.remove("active"));
  document.getElementById(id).classList.add("active");
  window.scrollTo(0,0);
}}

function showCat(catId){{
  const cat = cats[catId];
  let html = `<button class="back-btn" onclick="showPage('home')">
    <svg viewBox="0 0 24 24"><path d="M20 11H7.83l5.59-5.59L12 4l-8 8 8 8 1.41-1.41L7.83 13H20v-2z"/></svg>
    رجوع للقائمة
  </button>
  <div class="cat-hdr">
    <div class="cat-hdr-icon">${{cat.icon}}</div>
    <div><div class="cat-hdr-ar">${{cat.ar}}</div><div class="cat-hdr-en">${{cat.en}}</div></div>
  </div>
  <div class="items-grid">`;

  cat.items.forEach((item, idx)=>{{
    const id = mkId(catId,"i",idx);
    const qty = cart[id] ? cart[id].qty : 0;
    const badge = item.b ? '<span class="badge">موسمي</span>' : "";
    html += `<div class="menu-item ${{qty>0?"has-qty":""}}" id="el_${{id}}">
      <div class="item-left">
        <div class="item-name-ar">${{item.ar}}${{badge}}</div>
        <div class="item-name-en">${{item.en}}</div>
      </div>
      <div class="item-right">
        <div class="item-price">${{item.p}} <span>ج</span></div>
        <div class="qty-row">
          <button class="qty-btn" onclick="chg('${{id}}','${{item.ar}}',${{item.p}},-1,'${{cat.ar}}')">−</button>
          <span class="qty-num" id="q_${{id}}">${{qty}}</span>
          <button class="qty-btn" onclick="chg('${{id}}','${{item.ar}}',${{item.p}},1,'${{cat.ar}}')">+</button>
        </div>
      </div>
    </div>`;
  }});

  html += `</div>`;

  if(cat.addons && cat.addons.length){{
    html += `<div class="addons-section">
      <div class="addons-label">➕ الإضافات المتاحة</div>
      <div class="addons-grid">`;
    cat.addons.forEach((addon, idx)=>{{
      const id = mkId(catId,"a",idx);
      const qty = cart[id] ? cart[id].qty : 0;
      html += `<div class="addon-item ${{qty>0?"has-qty":""}}" id="el_${{id}}">
        <div class="item-left">
          <div class="item-name-ar">${{addon.ar}}</div>
          <div class="item-name-en">${{addon.en}}</div>
        </div>
        <div class="item-right">
          <div class="item-price">${{addon.p}} <span>ج</span></div>
          <div class="qty-row">
            <button class="qty-btn" onclick="chg('${{id}}','${{addon.ar}}',${{addon.p}},-1,'${{cat.ar}} - إضافات')">−</button>
            <span class="qty-num" id="q_${{id}}">${{qty}}</span>
            <button class="qty-btn" onclick="chg('${{id}}','${{addon.ar}}',${{addon.p}},1,'${{cat.ar}} - إضافات')">+</button>
          </div>
        </div>
      </div>`;
    }});
    html += `</div></div>`;
  }}

  html += `<footer>
    <div style="text-align:center;margin-bottom:10px;margin-right:-10px">{LOGO_SVG}</div>
    <div class="footer-note">2Shot Coffee &amp; Bar</div>
    <div class="dev-credit" style="margin-top:12px">
      <a class="dev-btn" href="https://wa.me/201211255580" target="_blank">
        <svg viewBox="0 0 24 24"><path d="M12 2C6.48 2 2 6.48 2 12s4.48 10 10 10 10-4.48 10-10S17.52 2 12 2zm-2 14.5v-9l6 4.5-6 4.5z"/></svg>
        هل تريد موقع مثل هذا؟
      </a>
    </div>
  </footer>`;

  document.getElementById("cat-page-inner").innerHTML = html;
  showPage("cat-page");
}}

function chg(id, name, price, delta, catName){{
  if(!cart[id]) cart[id]={{name, fullName: catName ? catName+" | "+name : name, price, qty:0}};
  cart[id].qty = Math.max(0, cart[id].qty + delta);
  if(cart[id].qty === 0) delete cart[id];
  const qEl = document.getElementById("q_"+id);
  if(qEl) qEl.textContent = cart[id] ? cart[id].qty : 0;
  const el = document.getElementById("el_"+id);
  if(el){{
    if(cart[id] && cart[id].qty > 0) el.classList.add("has-qty");
    else el.classList.remove("has-qty");
  }}
  updateFab();
}}

function updateFab(){{
  const total = Object.values(cart).reduce((s,i)=>s+i.qty,0);
  const fab = document.getElementById("cartFab");
  document.getElementById("cartCount").textContent = total;
  if(total > 0) fab.classList.add("show");
  else fab.classList.remove("show");
}}

function openCheckout(){{
  const items = Object.values(cart).filter(i=>i.qty>0);
  if(!items.length) return;
  renderOrderList();
  document.getElementById("overlay").classList.add("open");
}}

function renderOrderList(){{
  const entries = Object.entries(cart).filter(([,v])=>v.qty>0);
  let html = "";
  let total = 0;
  const groups = {{}};
  entries.forEach(([id, i])=>{{
    const parts = (i.fullName || i.name).split(" | ");
    const cat = parts.length > 1 ? parts[0] : "—";
    const itemName = parts.length > 1 ? parts[1] : parts[0];
    if(!groups[cat]) groups[cat] = [];
    groups[cat].push({{id, i, itemName}});
  }});
  Object.entries(groups).forEach(([cat, items])=>{{
    html += `<div style="font-size:11px;font-weight:700;color:var(--accent);letter-spacing:1px;padding:10px 0 4px;opacity:.7;border-bottom:1px solid rgba(46,204,113,.15)">${{cat}}</div>`;
    items.forEach(({{id, i, itemName}})=>{{
      const sub = i.price * i.qty;
      total += sub;
      html += `<div class="order-row">
        <span style="flex:1;color:var(--cream)">${{itemName}}</span>
        <div class="qty-row">
          <button class="qty-btn" onclick="chgInCart('${{id}}',-1)">−</button>
          <span class="qty-num" style="color:var(--accent)">${{i.qty}}</span>
          <button class="qty-btn" onclick="chgInCart('${{id}}',1)">+</button>
        </div>
        <span style="color:var(--accent);font-weight:700;min-width:50px;text-align:left">${{sub}} ج</span>
      </div>`;
    }});
  }});
  document.getElementById("orderList").innerHTML = html || '<div style="color:var(--muted);text-align:center;padding:20px">الطلب فاضي</div>';
  document.getElementById("orderTotal").textContent = total + " ج";
  if(total === 0) closeCheckout();
}}

function chgInCart(id, delta){{
  if(!cart[id]) return;
  cart[id].qty = Math.max(0, cart[id].qty + delta);
  if(cart[id].qty === 0) delete cart[id];
  const qEl = document.getElementById("q_"+id);
  if(qEl) qEl.textContent = cart[id] ? cart[id].qty : 0;
  const el = document.getElementById("el_"+id);
  if(el){{
    if(cart[id] && cart[id].qty > 0) el.classList.add("has-qty");
    else el.classList.remove("has-qty");
  }}
  updateFab();
  renderOrderList();
}}

function closeCheckout(){{ document.getElementById("overlay").classList.remove("open"); }}

document.getElementById("overlay").addEventListener("click", function(e){{
  if(e.target === this) closeCheckout();
}});

function sendOrder(){{
  const name = document.getElementById("custName").value.trim();
  const phone = document.getElementById("custPhone").value.trim();
  if(!name || !phone){{ alert("من فضلك اكتب اسمك ورقمك"); return; }}
  const items = Object.values(cart).filter(i=>i.qty>0);
  const total = items.reduce((s,i)=>s+i.price*i.qty,0);
  let msg = "🛒 *طلب جديد - 2Shot*\\n\\n";
  msg += "👤 *الاسم:* " + name + "\\n";
  msg += "📞 *التليفون:* " + phone + "\\n\\n";
  msg += "📋 *الطلبات:*\\n";
  const groups = {{}};
  items.forEach(i=>{{
    const parts = (i.fullName || i.name).split(" | ");
    const cat = parts.length > 1 ? parts[0] : "عام";
    const itemName = parts.length > 1 ? parts[1] : parts[0];
    if(!groups[cat]) groups[cat] = [];
    groups[cat].push({{...i, itemName}});
  }});
  Object.entries(groups).forEach(([cat, gitems])=>{{
    msg += `\\n📌 ${{cat}}\\n`;
    gitems.forEach(i=>{{ msg += "• " + i.itemName + " × " + i.qty + " = " + (i.price*i.qty) + " ج\\n"; }});
  }});
  msg += "\\n💰 *الإجمالي: " + total + " جنيه*";
  window.open("https://wa.me/" + WA + "?text=" + encodeURIComponent(msg.replace(/\\\\n/g,"\\n")), "_blank");
}}
</script>
</body>
</html>'''
    return html

def main():
    rows = fetch_sheet()
    print(f"✅ تم تحميل {len(rows)} صف")
    cats, cat_order = parse_data(rows)
    print(f"✅ تم تحليل {len(cats)} كاتيجوري: {', '.join(cat_order)}")
    html = generate_html(cats, cat_order)
    with open("menu.html", "w", encoding="utf-8") as f:
        f.write(html)
    print("✅ تم حفظ menu.html بنجاح!")

if __name__ == "__main__":
    main()
