# SOP & Dasar Pengurusan Hayat Produk (Product Lifecycle Policy)

Dokumen ini menetapkan garis panduan editorial, teknikal, dan pengurusan hayat produk bagi **iviz Picks Malaysia** untuk memastikan ketahanan SEO, AEO (Search Generative Experience / Perplexity / ChatGPT), dan GEO (Generative Engine Optimization) tanpa menjejaskan integriti atau kredibiliti jenama.

---

## 1. Prinsip Asas (Core Principles)

1. **LARANGAN KERAS memadamkan (Delete / 404) mana-mana URL produk**:
   - Setiap halaman produk yang pernah diterbitkan mempunyai nilai autoriti domain (*link equity*) dan sejarah carian.
   - Memadam halaman menyebabkan *404 Not Found* yang menurunkan skor kredibiliti domain di Google dan enjin AI.

2. **Pengurusan Status Produk (Product Status States)**:
   Setiap produk dalam pangkalan data `data/trending_products.json` dikelaskan kepada salah satu status berikut:

   - **`active` (Aktif)**:
     - Produk sedia ada di pasaran rasmi (Shopee Mall / Official / Preferred Store).
     - Schema JSON-LD: `https://schema.org/InStock`.
     - Butang CTA: "Semak Harga Terkini di Stor Rasmi" (Aktif & Berwarna Penuh).

   - **`out_of_stock` (Stok Habis / Sementara Tiada)**:
     - Produk sementara tidak dapat dibeli di stor rasmi.
     - Schema JSON-LD: `https://schema.org/OutOfStock`.
     - Lencana Paparan: `STOK HABIS` dipaparkan pada kad produk.
     - Halaman Kekal Live (HTTP 200) dengan amaran makluman mesra pengguna.

   - **`discontinued` (Batal / Obsolete / Model Diganti)**:
     - Produk tidak lagi dikeluarkan oleh pengilang atau digantikan oleh model baharu (cth: Mi Band 8 -> Mi Band 9).
     - Schema JSON-LD: `https://schema.org/Discontinued`.
     - **Tindakan**: Halaman kekal live. Menyediakan pautan *Internal Link* secara automatik ke model pengganti (`replacement_id`).

---

## 2. Automasi & Jadual Kemaskini (Sync & Maintenance)

- **Kekerapan Kemaskini**: Mingguan (Setiap Isnin, 09:00 MYT).
- **Hasil Automasi**:
  1. Memeriksa kesihatan pautan CDN Shopee & status HTTP pautan afiliasi.
  2. Mengemas kini nilai `last_checked` bagi setiap produk.
  3. Menjana semula `sitemap.xml` (105+ URLs) dan `robots.txt`.
  4. Menyuntik *Global Chrome* (Header/Footer/Burger Nav) secara konsisten merentasi 100% halaman.

---

## 3. Garis Panduan Kemas Kini Task di Workspace

Segala perubahan pada kod, skrip generator, atau pangkalan data **MUST** didokumentasikan serta-merta di dalam:
- `README.md` (Gambaran keseluruhan projek & ciri teknikal)
- `PRD.md` (Product Requirements Document)
- `LIFECYCLE-POLICY.md` (Dokumen ini)
