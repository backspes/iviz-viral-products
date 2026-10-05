# iviz Picks — Malaysia Viral & Evergreen Product Review Portal

Portal ulasan editorial bebas untuk produk fizikal trending di Malaysia (Shopee/TikTok viral). Dibina menggunakan Programmatic SEO (p-SEO) dengan fokus kepada kredibiliti E-E-A-T dan pematuhan PDPA.

**Hosting**: Cloudflare Pages
**Domain**: [https://link.iviztrading.com/](https://link.iviztrading.com/)
**Status**: Aktif (100/100 Produk Selesai)

## Struktur Projek
```
iviz-viral-products/
├── generator/
│   ├── build_microsites.py       # Generator HTML Statik (Dinamik: Skor, Tarikh, Lencana)
│   └── ingest_datafeed.py        # Pemadanan automatik dengan Shopee Product Feed
├── data/
│   ├── trending_products.json    # Pangkalan data 100 produk (Single Source of Truth)
│   └── shopee_feed.csv           # Shopee Extra Commission Feed (Source Data)
├── dist/                         # Fail HTML Statik yang dideploy (100 produk + Trust Pages)
├── GUIDELINES.md                 # Piawaian Editorial & Tatabahasa Bahasa Melayu DBP
├── PRD.md                        # Product Requirements Document
└── PSEO-AEO-GEO-STANDARDS.md     # Strategi Optimasi Carian & AI (SEO/AEO/GEO)
```

## Milestone Terkini (Oktober 2026)
- **100/100 Produk**: Katalog penuh produk viral (Gadgets, Skincare, Home Appliances).
- **Skor Dinamik**: Sistem pemarkahan editorial berasaskan algoritma unik (tiada hardcode).
- **Trust Badges**: Lencana pengesahan automatik (Shopee Mall vs Preferred vs Global).
- **Audit Playwright**: Semua 100 halaman melepasi ujian status 200, imej CDN, dan link affiliate.
- **E-E-A-T Compliance**: Halaman About, Editorial Policy, Privacy Policy (PDPA), dan Contact sedia ada.

## Pembangunan
1. Tambah produk baru dalam `data/trending_products.json`.
2. Jalankan `python3 generator/build_microsites.py` untuk jana HTML baru.
3. Deploy menggunakan Wrangler: `wrangler pages deploy dist`.

---
© 2026 iviz Picks Malaysia | hello@iviztrading.com

### Kemaskini Terkini (Oktober 2026 - V1.3 UI & Mobile UX)
- **Tahun Dinamik**: Memperbaiki isu `{current_year}` pada badge laman utama kepada tahun semasa automatik (`2026`).
- **Navigasi Responsif Penuh (Mobile Burger Menu)**: Menambah butang menu burger dan dropdown navigasi pada paparan peranti mudah alih (mobile view) merentasi laman utama, ulasan produk, dan halaman polisi E-E-A-T.
- **Bar Perkongsian Sosial (Social Share Bar)**: Dilengkapi butang 1-klik WhatsApp, Telegram, Facebook, Salin Pautan, dan Web Share API native mudah alih pada semua 100 produk.
- **Fail SEO & AEO Indeks**: Penjanaan automatik `sitemap.xml` (105 URLs) dan `robots.txt` dengan kebenaran bot enjin carian dan AI moden (Googlebot, Bingbot, GPTBot, PerplexityBot, ClaudeBot).
