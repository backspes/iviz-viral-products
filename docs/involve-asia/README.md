# Dokumentasi Involve Asia (Rujukan Rasmi)

Folder ini menyimpan rujukan rasmi **Involve Asia Publisher API**. Rujuk di sini
setiap kali nak update atau tambah projek baharu yang menggunakan affiliate Involve Asia.

## Fail

| Fail | Kegunaan |
|------|----------|
| `skill.md` | Panduan penuh: auth JWT, 9 endpoint, parameter, gotchas, error model. |
| `llms.txt` | Ringkasan operasi pantas: base URL, rate limit, had kuota, sub-ID. |
| `openapi.yaml` | Spesifikasi OpenAPI 3.1 — untuk codegen / import Postman / Insomnia. |
| `collection.json` | Postman Collection v2.1 — request Authenticate auto-isi `{{token}}`. |
| `generate_deeplink.py` | Skrip helper: auth + jana deeplink + semak quota. |

## Fakta Kritikal Akaun iviz Picks

- **Base URL**: `https://api.involve.asia/api`
- **Kredensial**: `INVOLVE_ASIA_KEY` + `INVOLVE_ASIA_SECRET` dalam `/root/.env` (JANGAN dedah).
- **Publisher aff_id**: `122839`
- **Property ID**: `39493`
- **Shopee MY Offer ID (tracking)**: `103878`
- **Rate limit**: 60 request / minit / akaun.
- **Had deeplink**: 1,000 unique tracking link / 30 hari bergolek / akaun.
- **Data lag**: data conversion lambat ~24 jam — jangan kira hari ini dalam rollup.

## Amaran Pautan (PENTING — komisen)

- ✅ **GUNA**: shortlink rasmi `https://invl.me/clo...` — auto-atribut ke akaun.
- ❌ **JANGAN GUNA**: format `aff_m` manual yang dibina sendiri. Shopee MY menyekatnya
  → redirect ke homepage (`verify/traffic/error`), komisen HILANG.
- `/deeplink/generate` untuk offer Shopee memulangkan **HTTP 500** (ralat kekal,
  jangan retry). Jana shortlink melalui dashboard Involve Asia atau guna yang sedia ada.

## Cara Jana Deeplink

```bash
python3 docs/involve-asia/generate_deeplink.py \
  --offer-id 103878 \
  --url "https://shopee.com.my/product/SHOPID/ITEMID" \
  --aff-sub ivizpicks \
  --aff-sub2 <product_id>
```

Semak quota / status akaun:

```bash
python3 docs/involve-asia/generate_deeplink.py --check
```
