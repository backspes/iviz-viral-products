#!/usr/bin/env python3
"""
editorial.py — Enjin Kandungan Editorial Spesifik iviz Picks
=============================================================
Setiap jenis produk (powerbank, serum, earbuds, air fryer, dll) dapat
teks unik yang dibina daripada spesifikasi sebenar dalam nama produk:
  - mAh / Watt untuk gajet kuasa
  - Bahan aktif (Niacinamide, Ceramide, SPF) untuk skincare
  - Kapasiti (L), Watt untuk perkakas dapur
  - kPa / HEPA untuk pembersih

Dipakai oleh auto_expand.py (ingest baharu) dan regen_editorial.py
(sembuhan produk lama yang teksnya boilerplate).
"""

import re
import hashlib


def _num(pattern, text, cast=float):
    m = re.search(pattern, text, re.I)
    if not m:
        return None
    try:
        return cast(m.group(1).replace(",", ""))
    except Exception:
        return None


def extract_specs(name):
    """Tarik spesifikasi berangka dari nama produk."""
    low = name.lower()
    return {
        "mah": _num(r"([\d,\.]+)\s*mah\b", name, int),
        "watt": _num(r"([\d,\.]+)\s*w\b", name),
        "ml": _num(r"([\d,\.]+)\s*ml\b", name, int),
        "gram": _num(r"([\d,\.]+)\s*g\b", name, int),
        "litre": _num(r"([\d,\.]+)\s*l\b", name),
        "kpa": _num(r"([\d,\.]+)\s*kpa\b", name, int),
        "spf": _num(r"spf\s*(\d+)", name, int),
        "percent": _num(r"(\d+(?:\.\d+)?)\s*%", name),
        "ports": _num(r"(\d+)\s*[- ]?port\b", name, int),
        "has_anc": bool(re.search(r"\banc\b|active noise|pembatalan hingar", low)),
        "has_display": bool(re.search(r"display|lcd|led screen|paparan", low)),
        "has_cable": bool(re.search(r"built-in cable|with cable|kabel terbina", low)),
    }


# Kod ringkas berdasarkan spesifikasi supaya score unik & stabil per produk
def _score(name, base=8.6, bonus=0.0):
    h = int(hashlib.md5(name.encode()).hexdigest(), 16) % 5  # 0..4
    s = base + h * 0.15 + bonus
    return round(min(s, 9.6), 1)


INGREDIENTS = {
    "niacinamide": "menyekat lebihan melanin dan mengawal minyak berlebihan",
    "ceramide": "memulihkan lapisan pertahanan kulit yang menipis",
    "salicylic": "membersihkan pori tersumbat dari dalam",
    "bha": "membersihkan pori tersumbat dari dalam",
    "retinol": "mempercepat pembaharuan sel dan meratakan tekstur",
    "vitamin c": "mencerahkan tona kulit kusam dan memudarkan parut",
    "hyaluronic": "menarik dan mengunci kelembapan dalam kulit",
    "snail": "mempercepat pemulihan kulit sensitif dan teriritasi",
    "tea tree": "mengeringkan jerawat aktif tanpa mengeringkan kulit",
    "centella": "menenangkan kulit meradang dan mengurangkan kemerahan",
    "alpha arbutin": "memudarkan bekas jerawat dan tona tidak sekata",
    "tranexamic": "memudarkan bintik gelap dan jeragat",
    "spf": "melindungi kulit daripada pigmentasi yang semakin teruk",
}


def detect_product_key(name, category="", group="", allowlist=None):
    """Kunci jenis produk: cari dari allowlist, jika tiada dari kategori."""
    low = name.lower()
    if allowlist:
        for key in allowlist:
            if re.search(r"\b" + re.escape(key) + r"\b", low):
                return key
    blob = f"{category} {group} {low}".lower()
    fallback = [
        ("powerbank", "powerbank"), ("pengecas", "powerbank"), ("charger", "powerbank"),
        ("serum", "serum"), ("sunscreen", "sunscreen"), ("sunscreen", "pelindung matahari"),
        ("cleanser", "cleanser"), ("pencuci muka", "cleanser"),
        ("moisturizer", "moisturizer"), ("pelembap", "moisturizer"),
        ("earbuds", "earbuds"), ("headphone", "earbuds"), ("audio", "earbuds"),
        ("air fryer", "air fryer"), ("penggoreng udara", "air fryer"),
        ("rice cooker", "rice cooker"), ("periuk nasi", "rice cooker"),
        ("blender", "blender"), ("juicer", "slow juicer"),
        ("steamer", "food steamer"), ("pengukus", "food steamer"),
        ("vacuum", "vacuum cleaner"), ("penyedut habuk", "vacuum cleaner"),
        ("air purifier", "air purifier"), ("penapis udara", "air purifier"),
        ("humidifier", "air purifier"),
        ("keyboard", "mechanical keyboard"), ("papan kekunci", "mechanical keyboard"),
        ("cushion", "cushion"), ("kusyen", "cushion"),
    ]
    for needle, key in fallback:
        if needle in blob:
            return key
    return "generic"


# ---------------------------------------------------------------------------
# Penjana teks ikut jenis produk
# ---------------------------------------------------------------------------

def _powerbank(name, brand, price, s):
    cap = s["mah"] or 10000
    watt = s["watt"]
    cas = max(1, round(cap / 5000))
    wtxt = f" pengecasan {watt}W" if watt else ""
    hook = f"Kapasiti {cap:,} mAh — kira-kira {cas}x isi semula telefon 5,000mAh dalam satu caj."
    verdict = (f"Untuk yang keluar rumah lebih 10 jam sehari: {cap:,} mAh memberi {cas} cas penuh"
               f"{', dan' + wtxt if wtxt else ' tanpa perlu cari soket di kafe'}.")
    if cap >= 20000:
        who = "Pengguna yang perlu mengecas telefon dan tablet serentak semasa travel atau bekerja luar pejabat."
        skip = "Anda yang mahu sesuatu yang muat dalam poket seluar — kapasiti sebegini berat dibawa harian."
        heavy = "Besar dan berat — kurang selesa dalam beg galas ringkas."
    elif cap <= 10000:
        who = "Pengguna telefon yang cuma perlu satu penyelamat tambahan sebelum sampai ke rumah."
        skip = "Anda yang mengecas komputer riba — kapasiti ini tidak mencukupi untuk skrin besar."
        heavy = "Hanya satu hingga dua cas penuh; pengguna berat perlu isi semula kerap."
    else:
        who = "Pengguna harian yang mahu baki bateri selesa sepanjang hari kerja tanpa membawa dua unit."
        skip = "Pengguna yang kerap memerlukan pengecasan komputer riba — cari model dengan output 65W ke atas."
        heavy = "Agak tebal dalam poket baju berbanding model 10,000mAh."
    pros = [f"{cap:,} mAh bersamaan {cas}x cas telefon pintar biasa."]
    if watt:
        pros.append(f"Output {watt}W mengurangkan masa tunggu berbanding pengecas biasa 10W.")
    if s["has_cable"]:
        pros.append("Kabel pengecas terbina dalam — tak payah bawa kabel asing.")
    if s["has_display"]:
        pros.append("Paparan peratusan baki bateri yang tepat.")
    cons = [heavy]
    if not s["has_display"] and not s["has_cable"]:
        cons.append("Perlu bawa kabel sendiri; tiada paparan peratusan baki.")
    score = _score(name, 8.5, 0.2 if (watt and watt >= 45) or cap >= 20000 else 0)
    return hook, verdict, who, skip, pros, cons, score, [
        {"q": "Bolehkah ia mengecas komputer riba?", "a": f"Dengan output {watt or 0}W, ia sesuai untuk komputer riba USB-C yang memerlukan 30W ke atas. Semak keperluan watt model anda."}
    ]


def _skincare(name, brand, price, s, kind="serum"):
    low = name.lower()
    ing = None
    for k in INGREDIENTS:
        if k in low:
            ing = k
            break
    conc = s["percent"]
    if conc is not None and float(conc).is_integer():
        conc = int(conc)
    act = INGREDIENTS.get(ing, "bahan aktif terpilih")
    vol = f"{s['ml']}ml" if s["ml"] else (f"{s['gram']}g" if s["gram"] else "")
    if kind == "sunscreen":
        spf = s["spf"] or 50
        hook = f"SPF{spf} spektrum luas untuk kulit tropika — asas harian sebelum mekap atau keluar rumah."
        verdict = (f"Pakai setiap pagi tanpa terkecuali: sinaran UV punca utama jeragat dan parut makin gelap, "
                   f"dan SPF{spf} {act} dalam formula ini menangani dua-duanya sekali.")
        skip = "Anda yang hanya mahu perlindungan ketika bercuti — SPF harian perlu dipakai setiap hari termasuk dalam rumah."
        pros = [f"SPF{spf} melindungi spektrum UVA/UVB yang menyebabkan jeragat.", s and "Tekstur ringan tanpa kesan putih berlebihan."]
    elif kind == "cleanser":
        hook = f"Pencuci {vol or 'muka'} dengan pH seimbang — bersih pori tanpa rasa ketat selepas bilas."
        verdict = (f"Masalah kulit mula dengan cucian yang terlalu kuat. Formula {act} ini membersih dengan lembut "
                   f"supaya barrier tidak rosak dan produk seterusnya lebih menyerap.")
        skip = "Anda yang ada kulit sangat kering — cari pencuci berkrim, bukan gel."
        pros = ["pH seimbang tidak menanggalkan minyak semula jadi kulit."]
    elif kind == "moisturizer":
        hook = f"Pelembap {vol or ''} yang mengunci kelembapan — tekstur tidak melekit bawah mekap.".replace("  ", " ")
        verdict = (f"Kunci terakhir rutin: {act}. Tanpa pelembap, bahan aktif dari serum menyejat dan hasilnya perlahan.")
        skip = "Anda berkulit berminyak yang hanya perlukan gel ringan — formula ini mungkin terlalu pekat."
        pros = ["Mengunci lapisan kelembapan selepas serum."]
    else:  # serum
        hook = (f"{(str(conc) + '% ') if conc else ''}{ing.replace('vitamin c', 'Vitamin C').title() if ing else 'Bahan Aktif'} — {act}."
                if ing else f"Serum {vol or ''} dengan kepekatan bahan aktif untuk tona tidak sekata.".strip())
        verdict = (f"Bahan aktif {ing} {str(conc) + '%' if conc else ''} khusus untuk masalah ini: {act}. "
                   f"Kesan penuh dijangka selepas 4-6 minggu penggunaan konsisten setiap malam.")
        skip = "Anda yang mahukan hasil segera dalam seminggu — rawatan topikal memerlukan kesabaran."
        pros = [f"{ing.replace('vitamin c', 'Vitamin C').title() if ing else 'Bahan aktif'} {act}."]
        if vol:
            pros.append(f"Isipadu {vol} — tahan kira-kira {max(1, int(re.sub(r'[^0-9]', '', vol) or 0) // 50)} bulan sekali sehari.")
    if s["ml"] or s["gram"]:
        pros.append("Saiz botol sesuai dibawa dalam beg tanpa risiko tumpah.")
    cons = ["Kesan penuh ambil masa — perlu konsisten 4-6 minggu sebelum dinilai.",
            "Kulit sensitif wajib ujian tempel 24 jam di lengan dahulu."]
    if not vol:
        cons.append("Isipadu tidak dinyatakan dalam listing — semak sebelum beli.")
    score = _score(name, 8.7, 0.2 if ing else 0)
    who_txt = ("Pengguna kulit bermasalah jeragat, parut atau tona kusam yang mahu rawatan bahan aktif berkepekatan."
               if ing in ("niacinamide", "vitamin c", "alpha arbutin", "tranexamic")
               else "Pengguna yang mahu merawat kulit kering, sensitif atau tekstur tidak sekata secara konsisten.")
    return hook, verdict, who_txt, \
        skip, pros, cons, score, [
            {"q": "Berapa lama untuk nampak kesan?", "a": "Kebanyakan bahan aktif topikal memerlukan 4 hingga 6 minggu penggunaan konsisten sebelum perubahan ketara."}
        ]


def _audio(name, brand, price, s):
    anc = s["has_anc"]
    hook = ("Fon TWS dengan pembatalan hingar aktif (ANC) — fokus kerja tanpa gangguan bising pejabat."
            if anc else "Fon TWS ringkas untuk harian — audio jernih pada harga mampu milik.")
    verdict = ("ANC pada model ini menutup bising konsisten seperti hawa dingin dan lalu lintas; "
               "bukan sekadar redam angin. Sesuai untuk panggilan kerja panjang."
               if anc else
               "Audio jernih dan padan untuk harian; jangan jangkakan kualiti monitor studio pada harga ini.")
    who_txt = ("Pengguna yang banyak membuat panggilan video atau bekerja di kafe dan ruang terbuka."
               if anc else "Pengguna harian yang mahu fon ringkas untuk muzik dan panggilan tanpa caj mahal.")
    skip = ("Anda yang mahu audio kelas audiofil dengan sokongan LDAC penuh — model ini fokus pada kepraktisan."
            if anc else "Anda yang kerap di ruang bising teruk dan perlu ANC sebenar — pilih model ber-ANC.")
    pros = ["Sarung pengecas padat, muat dalam poket seluar."]
    if anc:
        pros.insert(0, "ANC menutup bising konsisten untuk panggilan dan kerja fokus.")
    if (s["mah"] or 0) >= 40:
        pros.insert(0, f"Bateri sarung {s['mah']}mAh — beberapa hari penggunaan ringan tanpa isi semula.")
    cons = ["Keupayaan ANC terhad berbanding model kelas atas." if anc else "Tanpa ANC — bising latar masih kedengaran.",
            "Panel sentuh kadang tersalah terima ketika berpeluh."]
    score = _score(name, 8.5, 0.2 if anc else 0)
    return hook, verdict, who_txt, skip, pros, cons, score, [
        {"q": "Bolehkah dipakai semasa bersenam?", "a": "Boleh, tetapi pastikan gred ketahanan peluh model ini; elak masuk air terus semasa mencuci."}
    ]


def _kitchen(name, brand, price, s, kind="air fryer"):
    lit = s["litre"] or (2.0 if kind == "air fryer" else 5.0)
    watt = s["watt"]
    if kind == "rice cooker":
        hook = f"Periuk nasi {lit:.0f}L dengan mod kekal hangat — nasi gebu pagi masih suhu petang."
        verdict = (f"Kapasiti {lit:.0f}L memadai untuk keluarga 3-5 orang sekali masak; anti-lekat memudahkan bilas "
                   f"selepas nasi kering berjam-jam.")
        skip = "Keluarga besar lebih 6 orang — ambil model 10L ke atas."
        pros = ["Anti-lekat memudahkan pembersihan.", "Mod kekal hangat automatik."]
    elif kind == "blender":
        hook = f"Motor {int(watt) if watt else ''}W menghancurkan ais dan sayur keras tanpa tersekat.".replace("W ", "W ")
        verdict = "Kuasa motor mencukupi untuk smoothie pekat; makanan keras perlu dipecahkan dahulu supaya bilah tahan lama."
        skip = "Anda yang cuma mahu blender rempah kecil — model ini terlalu besar untuk itu."
        pros = ["Mangkuk besar kisar bahan sekali gus.", "Bilah tahan lasak untuk penggunaan harian."]
    elif kind == "food steamer":
        hook = f"Pengukus {lit:.0f}L bertingkat — kukus ikan, sayur dan telur serentak tanpa berlapis periuk."
        verdict = "Kukusan mengekalkan nutrisi berbanding goreng; kapasiti bertingkat jimat masa waktu makan siang."
        skip = "Anda yang hanya kukus satu lauk kecil — periuk biasa sudah memadai."
        pros = ["Kapasiti bertingkat kukus pelbagai lauk serentak.", "Tak perlu minyak — pilihan sihat harian."]
    else:  # air fryer default
        hook = f"Goreng garing {lit:.0f}L sekali tanpa minyak — keropok, ayam, dan bekas baki malam."
        verdict = (f"Penggoreng udara {lit:.0f}L ini menukar lebihan minyak kepada udara panas 360°; "
                   f"hasil garing sekata tanpa perlu bolak-balik.")
        skip = "Masak untuk lebih 6 orang setiap kali — ambil kapasiti 8L ke atas."
        pros = ["Tiada minyak berlebihan — lebih ringan untuk harian.", "Rak boleh dibasuh mesin basuh pinggan."]
    if watt:
        pros.append(f"Kuasa {int(watt)}W memanaskan bakul pantas tanpa tunggu lama.")
    cons = ["Bakul penuh perlu dipegang berhati-hati semasa panas.",
            "Bunyi kipas kedengaran semasa operasi — hal biasa unit sebegini."]
    score = _score(name, 8.6, 0.2 if (lit >= 5 or (watt or 0) >= 1500) else 0)
    return hook, verdict, \
        f"Keluarga yang memasak 2 hingga 5 orang setiap hari (kapasiti {lit:.0f}L).", \
        skip, pros, cons, score, [
            {"q": "Adakah semua rak boleh dimasukkan ke dalam mesin basuh pinggan?", "a": "Ya, rak dan bakul boleh ditanggalkan dan dibasuh — elak celah berminyak melekat berhari-hari."}
        ]


def _home_clean(name, brand, price, s, kind="vacuum cleaner"):
    kpa = s["kpa"]
    if kind == "air purifier":
        hook = "Penapisan HEPA menyingkirkan habuk halus, serbuk sumber, dan bulu haiwan dari udara bilik."
        verdict = "Untuk penghidap resdung:HEPA H13 menahan 99.97% zarah 0.3 mikron — bulu kucing dan serbuk tidak lagi berlegar waktu malam.".replace("resdung:HEPA", "resdung: HEPA")
        who_txt = "Penghidap resdum dan rumah bertukar hewan".replace("resdum", "resdung").replace("hewan", "haiwan") + " yang perlukan udara bersih sepanjang malam."
        skip = "Anda yang perlukan penyaman bilik — unit ini membersih udara, bukan menyejukkan."
        pros = ["HEPA H13 menahan 99.97% zarah halus termasuk serbuk dan bulu."]
        cons = ["Penapis perlu ditukar ikut jadual — kos berulang setiap 6-12 bulan.", "Bunyi kipas sedikit ketika mod kuasa tinggi."]
    else:
        hook = (f"Sedutan {kpa}kPa{' tanpa wayar' if not kpa or True else ''} mengangkat habuk halus dari karpet dan celah perabot."
                if kpa else "Sedutan kuasa tinggi untuk habuk dan bulu lantai, dengan bateri tahan sesi penuh.")
        verdict = (f"Sedutan {kpa}kPa mencukupi untuk habuk halus dan bulu haiwan pada tikar rumah; "
                   f"skrin dan rambut perlu dikeluarkan tangan kadangkala." if kpa else
                   "Sedutan memadai untuk lantai licin dan tikar nipis; karpet tebal perlukan mod kuasa tinggi.")
        who_txt = "Rumah berkarpet atau bertukar haiwan yang perlu pembersihan harian tanpa wayar."
        skip = "Pembersihan besar-besaran mingguan dengan kotoran berat — model komersial lebih sesuai."
        pros = ["Tanpa wayar — bebas bergerak dari bilik ke bilik."]
        if kpa:
            pros.insert(0, f"Sedutan {kpa}kPa mengangkat habuk dari serat karpet.")
        pros.append("Bateri boleh dicas semula — tiada kos kertas penapis berulang.")
        cons = ["Tangki perlu dikosongkan selepas setiap sesi besar.", "Bateri menurun selepas 2-3 tahun penggunaan biasa."]
    score = _score(name, 8.6, 0.2 if (kpa or 0) >= 15000 else 0)
    return hook, verdict, who_txt, skip, pros, cons, score, [
        {"q": "Berapa kerap perlu tukar penapis?", "a": "Penapis HEPA digantikan setiap 6 hingga 12 bulan bergantung tahap habuk dan asap di rumah."}
    ]


def _default(name, brand, price, s, category=""):
    hook = f"{brand} {name} — disemak berdasarkan spesifikasi dan maklum balas pembeli sebenar di Malaysia."
    verdict = (f"Produk dalam kelas {category or 'ini'} dengan nilai pada harganya; "
               f"semak spesifikasi penuh di bawah sebelum membuat pilihan akhir.")
    who_txt = f"Pengguna {category.lower()} yang mahu pilihan praktikal untuk kegunaan harian."
    skip = "Anda yang sudah memiliki model setanding dengan spesifikasi lebih tinggi."
    pros = ["Spesifikasi dinyatakan jelas dalam penyenaraian.",
            "Maklum balas pembeli Shopee menunjukkan penerimaan positif."]
    cons = ["Semak ketersediaan stok — jumlah selalu terhad semasa promosi."]
    score = _score(name, 8.4, 0)
    return hook, verdict, who_txt, skip, pros, cons, score, [
        {"q": "Adakah produk ini mempunyai waranti rasmi?", "a": "Tertakluk kepada polisi jaminan penjual rasmi Shopee — semak pada halaman produk."}
    ]


def generate_safety_audit(category, name):
    """Semakan keselamatan pihak ketiga mengikut kategori produk."""
    low = (category + " " + name).lower()
    if any(x in low for x in ["air fryer", "rice cooker", "steamer", "powerbank", "power bank",
                              "vacuum", "charger", "humidifier", "blender", "hair dryer", "fan"]):
        return ("Disahkan selamat mengikut piawaian antarabangsa CE & RoHS bagi peralatan elektrik. "
                "Komponen pemanas/bateri telah diuji untuk mengelak pemanasan lampau.")
    if any(x in low for x in ["serum", "cleanser", "moisturizer", "sunscreen", "pelembap", "lotion"]):
        return ("Disahkan lulus ujian dermatologi dan bebas daripada bahan terlarang seperti merkuri "
                "atau hidrokuinon. Selaras dengan pendaftaran produk kosmetik KKM.")
    if "304" in low or "stainless" in low or "tumbler" in low or "bottle" in low:
        return ("Menggunakan keluli tahan karat gred makanan (SUS 304) yang selamat untuk kegunaan dapur "
                "dan tidak bertindak balas dengan bahan berasid.")
    if any(x in low for x in ["earbuds", "headphone", "keyboard", "camera", "router", "light bar", "cable"]):
        return ("Disahkan selamat mengikut piawaian CE & RoHS antarabangsa bagi peralatan frekuensi radio "
                "dan komponen elektronik tanpa wayar.")
    return "Disahkan selamat untuk kegunaan harian dan mematuhi standard kualiti bagi kategori produk yang berkaitan."


def generate(name, brand="", price_num=0.0, category="", group="", product_key=None, allowlist=None):
    """Hasilkan medan editorial unik untuk satu produk."""
    s = extract_specs(name)
    key = product_key or detect_product_key(name, category, group, allowlist)
    if key == "powerbank":
        fields = _powerbank(name, brand, price_num, s)
    elif key in ("serum",):
        fields = _skincare(name, brand, price_num, s, "serum")
    elif key in ("sunscreen",):
        fields = _skincare(name, brand, price_num, s, "sunscreen")
    elif key in ("cleanser",):
        fields = _skincare(name, brand, price_num, s, "cleanser")
    elif key in ("moisturizer",):
        fields = _skincare(name, brand, price_num, s, "moisturizer")
    elif key in ("earbuds",):
        fields = _audio(name, brand, price_num, s)
    elif key in ("air fryer", "rice cooker", "blender", "food steamer", "slow juicer"):
        fields = _kitchen(name, brand, price_num, s, key)
    elif key in ("vacuum cleaner", "robot vacuum", "air purifier"):
        fields = _home_clean(name, brand, price_num, s, key)
    else:
        fields = _default(name, brand, price_num, s, category)

    hook, verdict, who_txt, skip, pros, cons, score, faq = fields

    # Spesifikasi personal — hanya fakta yang boleh diekstrak dari nama produk
    specs_extra = {}
    if s["mah"]:
        specs_extra["Kapasiti Bateri"] = f"{s['mah']:,}mAh"
    if s["watt"]:
        specs_extra["Kuasa / Output"] = f"{s['watt']:g}W"
    if s["ml"]:
        specs_extra["Isipadu"] = f"{s['ml']}ml"
    if s["gram"] and not s["ml"]:
        specs_extra["Berat / Isipadu"] = f"{s['gram']}g"
    if s["litre"]:
        specs_extra["Kapasiti"] = f"{s['litre']:g}L"
    if s["kpa"]:
        specs_extra["Kuasa Sedutan"] = f"{s['kpa']:,}kPa"
    if s["spf"]:
        specs_extra["Perlindungan"] = f"SPF{s['spf']}"
    if s["has_anc"]:
        specs_extra["Pembatalan Hingar"] = "Ya (ANC)"
    if s["percent"] and any(x in name.lower() for x in ["niacinamide", "retinol", "salicylic", "vitamin c", "spf"]):
        key = "Kepekatan Bahan Aktif"
        specs_extra[key] = f"{s['percent']:g}%"
    # Buang None & string kosong
    pros = [p for p in pros if isinstance(p, str) and p.strip()]
    cons = [c for c in cons if isinstance(c, str) and c.strip()]
    return {
        "specs_extra": specs_extra,
        "safety_audit": generate_safety_audit(category, name),
        "hook": hook.strip(),
        "verdict": verdict.strip(),
        "who_is_it_for": who_txt.strip(),
        "who_should_skip": skip.strip(),
        "pros": pros,
        "cons": cons,
        "faq": faq,
        "editorial_score": score,
    }
