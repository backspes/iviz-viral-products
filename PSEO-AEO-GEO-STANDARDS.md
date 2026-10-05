# Standard Operasi & Garis Panduan P-SEO, AEO & GEO Arbitrage
**Status**: Wajib Patuh (Production-Ready / Monetizable)  
**Tujuan**: Menjana komisen affiliate melalui carian Google, enjin carian AI (Perplexity/ChatGPT), dan audiens tempatan Malaysia tanpa dibuang (de-index) oleh Google.

---

## 1. Teras Seni Bina Halaman (Zero Half-Baked Policy)
Setiap halaman yang dijana secara automatik (Programmatic SEO) **MESTI** memenuhi 4 tiang utama sebelum di-publish:

### Tiang 1: SEO Tradisional (Google Rank & Rich Snippets)
- **Schema.org Structured Data (JSON-LD)**:
  - `@type: "Product"` — Nama rasmi, jenama, SKU/ID unik, imej tulen.
  - `@type: "AggregateRating"` — `ratingValue` (contoh: 4.9), `reviewCount` / `ratingCount`.
  - `@type: "Offer"` — `price`, `priceCurrency: "MYR"`, `availability: "https://schema.org/InStock"`, `seller: "Shopee Mall / Preferred"`.
  - `@type: "BreadcrumbList"` — Struktur hierarki kategori yang jelas.
- **Meta Tag Lengkap**:
  - `title`: Mengandungi Kata Kunci Utama + Format ("Harga Promosi Shopee Malaysia").
  - `description`: Menyelesaikan search intent pembeli dalam 155 aksara.
  - `canonical`: URL kanonikal mutlak bagi mengelak isu penduaan (duplicate content).
  - OpenGraph (`og:title`, `og:image`, `og:description`) & Twitter Card untuk paparan kemas bila link dikongsi ke WhatsApp/Telegram/Facebook.

### Tiang 2: AEO (AI Engine Optimization untuk ChatGPT / Perplexity / Claude)
Enjin AI memetik jawapan dari laman yang menstrukturkan maklumat secara terus, padat, dan berfakta:
- **Jadual Spesifikasi & Rumusan Cepat (Quick Answer Box)**: Jadual perbandingan ringkas di bahagian atas.
- **Bahagian FAQ Berstruktur + Schema `FAQPage`**:
  - Format soalan yang orang selalu tanya (Contoh: *"Adakah produk ini ada kelulusan KKM?"*, *"Berapa lama nampak kesan?"*, *"Original ke beli di Shopee?"*).
  - Jawapan terus pada ayat pertama (Direct-to-the-point) tanpa ayat berbunga.

### Tiang 3: GEO Optimization (Pasaran Khusus Malaysia)
- **Mata Wang & Harga**: Wajib format `RM` (Ringgit Malaysia) dan kod `MYR`.
- **Logistik & Kurier Tempatan**:
  - Menyebut penghantaran melalui J&T Express, Shopee Express (SPX), Ninja Van, Pos Laju.
  - Tempoh anggaran sampai: Semenanjung (1-3 hari), Sabah & Sarawak (3-5 hari).
- **Kaedah Pembayaran Tempatan**:
  - Sokongan FPX (Maybank2u, CIMB Clicks), SPayLater (ansuran 0%), ShopeePay, Touch 'n Go eWallet, dan COD (Cash on Delivery).
- **Status Stok Tempatan**: Penegasan "Ready Stock dari Gudang Malaysia (Selangor / KL)".

### Tiang 4: CRO & Monetization (Conversion Rate Optimization)
- **Gambar Produk Sebenar**: Menggunakan visual pembungkusan atau botol sebenar, bukan gambar model gaya hidup semata-mata.
- **Sticky CTA Mobile (Wajib)**: Butang terapung di bahagian bawah skrin telefon pintar *"Beli di Shopee (RM XX.XX)"* supaya pembeli boleh tekan bila-bila masa tanpa perlu scroll ke atas/bawah.
- **Perbandingan Nilai (Urgency & Diskaun)**: Memaparkan harga asal vs harga diskaun promosi.
- **Pautan Tracking Affiliate**: Pautan Involve Asia / Shopee Affiliate dengan `rel="nofollow sponsored noopener"` yang sah.

---

## 2. Struktur Data Produk (`trending_products.json`)
Setiap rekod produk mesti mempunyai skema lengkap berikut:

```json
{
  "id": "prod_xxx",
  "name": "Nama Penuh Produk",
  "brand": "Jenama Rasmi",
  "keyword": "kata kunci carian viral tiktok shopee",
  "category": "Kategori Produk",
  "tiktok_trending_score": 9.5,
  "shopee_price": "RM 19.90",
  "original_price": "RM 49.00",
  "discount": "59% OFF",
  "currency": "MYR",
  "image_url": "URL imej produk sebenar beresolusi tinggi",
  "rating": "4.9",
  "review_count": "12,450",
  "hook": "Sebab utama produk ini viral",
  "highlights": ["Ciri 1", "Ciri 2", "Ciri 3", "Ciri 4"],
  "specs": {
    "Isipadu / Berat": "50g",
    "Status Halal / KKM": "Ya / Notifikasi KKM",
    "Lokasi Penghantaran": "Selangor / Semenanjung Malaysia",
    "Jaminan": "100% Original Shopee Mall"
  },
  "faq": [
    {
      "q": "Adakah produk ini original?",
      "a": "Ya, pautan kami membawa anda terus ke Shopee Mall / Preferred Seller rasmi di Malaysia."
    },
    {
      "q": "Berapa lama penghantaran ke Semenanjung dan Sabah/Sarawak?",
      "a": "Penghantaran ke Semenanjung mengambil masa 1-3 hari bekerja, manakala Sabah dan Sarawak sekitar 3-5 hari melalui kurier pilihan (SPX / J&T)."
    }
  ],
  "affiliate_url": "https://invl.io/xxx"
}
```

---

## 3. Checklist Sebelum Publish (Kualiti Kawalan)
- [ ] Schema `Product` disahkan sah (valid) pada Google Rich Results Test.
- [ ] Schema `FAQPage` disertakan dan sepadan dengan teks FAQ pada halaman.
- [ ] Imej produk asli terpapar dengan betul (aspek nisbah 1:1 atau 16:9).
- [ ] Butang CTA Sticky di mobile berfungsi dan membawa parameter tracking affiliate.
- [ ] Elemen GEO (RM, Sabah/Sarawak, FPX, Kurier tempatan) jelas kelihatan untuk membina kepercayaan (*trust factor*) pengguna tempatan.
