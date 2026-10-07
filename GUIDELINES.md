# Garis Panduan Rasmi & Piawaian Kualiti: iviz Picks Microsites

Dokumen ini adalah **rujukan mandatori** untuk membina, menyunting, dan menyebarkan (*deploy*) sebarang microsite ulasan produk di bawah domain `link.iviztrading.com`. Sebarang penambahan produk baharu WAJIB mematuhi piawaian di bawah bagi mengelakkan penurunan ranking SEO, penalti Google, dan kekeliruan pembaca.

---

## 1. Piawaian Bahasa & Penulisan (Linguistic Standards)

### A. Standard Bahasa Melayu Malaysia (DBP Journalism Style)
- **Gaya Penulisan**: Mesti menggunakan **Bahasa Melayu Malaysia Standard** dengan gaya kewartawanan media digital (contoh penanda aras: *ProductNation Malaysia, SoyaCincau BM, Amanz*).
- **Elakkan Dua Ekstrem**:
  1. *Jangan terlalu kaku / terjemahan literal mesin*: Jangan terjemah terus daripada teks bahasa Inggeris/Indonesia yang menghasilkan ayat pelik (*cth: "peroksida kakis", "latihan berat badan", "formulasinya nipis", "pencahayaan optik"*).
  2. *Jangan terlalu pasar / bahasa WhatsApp*: Jangan guna perkataan slang mesej (*cth: "nak", "bila", "senang dicuci", "bawah RM80"*). Gantikan dengan ayat editorial yang kemas (*cth: "mudah dibersihkan", "pada harga di bawah RM80", "untuk memudahkan", "apabila"*).

### B. Senarai Hitam Perkataan (Banned Words)
Dilarang sama sekali menggunakan perkataan bahasa Indonesia / slang berikut:
- ❌ **Perkataan Indonesia**: `bisa`, `cuma`, `gampang`, `bikin`, `pake`, `kalo`, `udah`, `banget`, `perawatan`, `pelembab`, `steker`, `menetralkan`, `ngilu`, `nggak`, `gimana`.
- ✅ **Padanan BM Standard**:
  - `bisa` → `boleh` / `dapat`
  - `cuma` → `hanya` / `sekadar`
  - `gampang` → `mudah` / `ringkas`
  - `bikin` → `membuat` / `menghasilkan`
  - `pake` → `pakai` / `guna`
  - `perawatan` → `penjagaan`
  - `pelembab` → `pelembap`
  - `steker` → `soket dinding` / `plag`
  - `menetralkan` → `meneutralkan` / `peneutralan`
  - `ngilu` → `sengal` / `pedih`
  - `isipadu` → `isi padu` (dua perkataan mengikut DBP)

---

## 2. Struktur Editorial & Elemen Konversi (CRO Architecture)

Setiap halaman ulasan microsite produk mesti mengandungi elemen berikut:
1. **Breadcrumbs Penuh**: Navigasi hierarki (`Utama / Kategori Induk / Sub-Kategori / Nama Produk`).
2. **Tajuk & Meta Pengarang**: Dipaparkan sebagai organisasi bebas (**`Pasukan Editorial iviz Picks`**) dengan pautan terus ke `/editorial-policy.html` dan tarikh kemas kini bulanan (*Oktober 2026*).
3. **Kotak Rumusan Editorial (*Quick Verdict*)**:
   - 1 atau 2 perenggan ringkas menerangkan fungsi sebenar, tekstur/reka bentuk, dan had produk secara jujur.
   - **Sesuai Untuk Anda Jika** (*Emerald Checkmark*): Menyasarkan masalah pengguna yang tepat.
   - **Pertimbangkan Semula Jika** (*Amber Warning*): Menjelaskan siapa yang patut elak atau had produk.
4. **Kad Perbandingan Harga & CTA Utama**:
   - Anggaran harga pasaran terkini vs harga asal.
   - Lencana kepercayaan: `🚚 Penghantaran Pantas`, `🛡️ Jaminan 100% Original`, `Disahkan Rasmi`.
   - Butang CTA menonjol (*Sunset Orange Gradient*): *"Semak Harga Terkini di Stor Rasmi"*.
5. **Kelebihan (Pros) vs Kekurangan (Cons)**:
   - 3-4 poin kelebihan nyata berasaskan pengalaman pengguna terverifikasi.
   - 2-3 poin kekurangan jujur bagi membina kepercayaan pembaca (*Zero bias*).
6. **Spesifikasi & Semakan Pihak Ketiga (3rd Party Audit)**:
   - Skincare/Kosmetik: Semakan senarai NOT / amaran racun berjadual NPRA KKM.
   - Elektrik/Rumah: Piawaian Suruhanjaya Tenaga (ST) & SIRIM Malaysia.
   - Gajet: Piawaian CE / FCC / MCMC.
7. **Soalan Lazim (FAQ)**: 2-3 soalan lazim pembeli bersama Schema JSON-LD `FAQPage`.
8. **Sticky Mobile Bar**: Butang CTA kekal di bahagian bawah skrin telefon.

---

## 3. Integriti E-E-A-T & Larangan Data Palsu (Strict Ethics)

1. **Larangan Rating & Ulasan Palsu**:
   - Dilarang mereka-reka penarafan bintang palsu atau kuantiti ulasan buatan (*cth: "68,400 ulasan pembeli"*).
   - Schema JSON-LD `Review` mesti dikaitkan kepada entiti penerbitan (**`iviz Picks Editorial Team`**).
2. **Kerahsiaan Identiti Pengasas**:
   - Jangan masukkan nama individu. Portal mesti dipersembahkan 100% sebagai organisasi media ulasan bebas.
3. **Pendedahan Afiliasi (*Affiliate Disclosure*)**:
   - Footer dan halaman About wajib memaparkan penafian afiliasi yang telus (komisen kecil tanpa kos tambahan kepada pembaca).

---

## 4. Pengurusan Gambar Produk (Zero VM Storage Rule)

1. **Tiada Gambar Disimpan Dalam VM**:
   - Dilarang memuat turun atau menyimpan fail gambar produk dalam cakera keras VM / git repository bagi mengekalkan saiz repositori yang ringan dan mengelakkan isu hak cipta setempat.
2. **Guna URL CDN Pihak Ketiga Sahaja**:
   - Tag `<img>` dalam HTML mesti memaut terus kepada URL luaran CDN rasmi jenama atau URL daripada Datafeed Involve Asia.

---

## 4b. Involve Asia API Reference (WAJIB rujuk untuk apa-apa kerja affiliate)

Fail rujukan rasmi disimpan dalam repo ini — rujuk SEBELUM jana/kemas kini pautan affiliate:

- `docs/involve-asia/skill.md` — panduan penuh: auth, 9 endpoint, parameter, gotchas, error model.
- `docs/involve-asia/llms.txt` — ringkasan operasi: base URL, rate limit (60 req/min), had 1,000 deeplink/30 hari, sub-ID.
- `docs/involve-asia/openapi.yaml` — spesifikasi OpenAPI 3.1 (untuk codegen/Postman).

Fakta kritikal akaun ini:
- Kunci API: `INVOLVE_ASIA_KEY` + `INVOLVE_ASIA_SECRET` dalam `/root/.env` (jangan dedah dalam output).
- Publisher aff_id: `122839`, Property ID: `39493`, Shopee MY Offer ID (tracking): `103878`.
- Pautan WAJIB guna shortlink rasmi `invl.me/clo...` (auto-atribut ke akaun). Format `aff_m` manual DIBLOK Shopee → redirect ke homepage (komisen hilang).
- `/deeplink/generate` untuk Shopee pulang HTTP 500 (ralat kekal, jangan retry) — guna shortlink sedia ada atau dapatkan dari dashboard Involve Asia.

---

## 5. Taksonomi 2 Peringkat (2-Tier Taxonomy)

Semua produk baharu mesti dipetakan mengikut hierarki:
- **Kesihatan & Penjagaan Diri** (`health-care`):
  - *Skincare & Wajah*
  - *Penjagaan Kulit Badan*
  - *Penjagaan Mulut & Gigi*
  - *Wellness & Kualiti Tidur*
- **Gajet & Elektronik** (`gadget`):
  - *Audio & Fon Telinga*
  - *Aksesori Telefon*
- **Rumah & Dapur** (`home-kitchen`):
  - *Perkakas Dapur & Elektrik*
  - *Pembersihan & Kediaman*
- **Sukan & Kecergasan** (`sports-fitness`):
  - *Alatan Senaman Rumah*

---

## 6. Aliran Kerja Pelaksanaan (Build & Deploy Workflow)

Bila menambah produk baharu:
1. Masukkan entri ke dalam `data/trending_products.json` mengikut skema di atas (atau guna enjin automatik `generator/auto_expand.py`).
2. Jalankan penjana: `python3 generator/build_microsites.py`.
3. Jalankan ujian semakan perkataan dilarang bagi memastikan tiada unsur Indonesia / typo.
4. Deploy ke Cloudflare Pages: `wrangler pages deploy dist --project-name=picks-iviztrading`.
5. Bersihkan cache CDN Cloudflare (*purge_everything*).

---

## 7. Standard Penambahan & Hub Ekspansi Automatik (Auto-Expand Pipeline)

Bagi memastikan laman tidak tunggang-langgang apabila diskalakan secara automatik:
1. **Enjin Pipeline**: `generator/auto_expand.py` bertindak sebagai pintu masuk automatik bagi datafeed Shopee/Involve Asia.
2. **Pemisahan Data & Logik**:
   - Senarai produk hab disimpan secara berasingan dalam `data/hub_assignments.json`.
   - Peraturan penapisan negatif & kata kunci wajib disimpan dalam `data/hub_guardrail_rules.json`.
3. **Penguatkuasaan Sempadan Perkataan (Word-Boundary Matching)**:
   - Padanan kata kunci wajib menggunakan sempadan perkataan (`\b` / regex boundary) bagi menghalang padanan ralat substring (contoh: perkataan 'aha' dilarang memadankan 'tahan').
4. **Pengesahan Imej Mandatori (HTTP 200)**:
   - Setiap imej produk disahkan aktif (HTTP 200 OK) melalui permintaan `HEAD` sebelum disimpan ke dalam pangkalan data.
5. **Sekatan Automatik (*Hard Abort*)**:
   - Jika mana-mana produk melanggar peraturan hab masalah/persona, fungsi `validate_problem_hub_guardrails()` akan membatalkan binaan secara automatik (*raise ValueError*) bagi memelihara integriti portal.

