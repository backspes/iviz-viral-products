import json, re

def strict_clean(title):
    # Buang emoji, simbol, tag promosi [..], [..], New, dsb.
    title = re.sub(r'[\U00010000-\U0010ffff]', '', title)
    title = re.sub(r'[\u2600-\u27bf\u2300-\u23ff☃◎🕯️©✨🔥★☆⚡]+', '', title)
    title = re.sub(r'^(?:\[[^\]]+\]|【[^】]+】)\s*', '', title)
    title = re.sub(r'^(?:New|Ready Stock|In Stock|Hot)\s+', '', title, flags=re.IGNORECASE)
    title = re.sub(r'^[\u4e00-\u9fff\s]+', '', title)
    title = re.sub(r'^[^\w\s]+', '', title)
    title = re.sub(r'[^\w\s\)]+$', '', title)
    return title.strip()
import os
import re

from components import GLOBAL_HEADER, GLOBAL_FOOTER, GLOBAL_NAV_SCRIPT

# ==============================================================================
# DATA: Import dynamic hub assignments & guardrail rules from /data directory
# This allows auto-expansion without editing this source file directly.
# ==============================================================================
_DATA_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "data")
_ASSIGNMENTS_FILE = os.path.join(_DATA_DIR, "hub_assignments.json")
_RULES_FILE = os.path.join(_DATA_DIR, "hub_guardrail_rules.json")

TEMPLATE_HTML = """<!DOCTYPE html>
<html lang="ms" class="scroll-smooth">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{{name}} - Ulasan Penuh & Harga Pasaran Malaysia</title>
    <meta name="description" content="Ulasan bebas {{name}}. Analisis ramuan, kelebihan, kekurangan, spesifikasi teknikal dan perbandingan harga di pasaran Malaysia.">
    <link rel="canonical" href="https://link.iviztrading.com/{{id}}.html">
    
    <!-- OpenGraph / Social Meta -->
    <meta property="og:type" content="article">
    <meta property="og:title" content="{{name}} - Ulasan Editorial iviz Picks">
    <meta property="og:description" content="{{hook}}">
    <meta property="og:url" content="https://link.iviztrading.com/{{id}}.html">
    <meta property="og:image" content="{{image_url}}">
    <meta property="og:site_name" content="iviz Picks Malaysia">
    <meta name="twitter:card" content="summary_large_image">
    <meta name="twitter:title" content="{{name}} - Ulasan Editorial iviz Picks">
    <meta name="twitter:description" content="{{hook}}">
    <meta name="twitter:image" content="{{image_url}}">

    <script src="https://cdn.tailwindcss.com"></script>
    <link href="https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@400;500;600;700;800&display=swap" rel="stylesheet">
    <style>
        body { font-family: 'Plus Jakarta Sans', sans-serif; }
    </style>

    <!-- Schema.org Product & Organization Review -->
    <script type="application/ld+json">
    {
      "@context": "https://schema.org/",
      "@type": "Product",
      "name": "{{name}}",
      "image": "{{image_url}}",
      "description": "{{hook}}",
      "brand": {
        "@type": "Brand",
        "name": "{{brand}}"
      },
      "review": {
        "@type": "Review",
        "reviewRating": {
          "@type": "Rating",
          "ratingValue": "{{rating_val}}",
          "bestRating": "5"
        },
        "author": {
          "@type": "Organization",
          "name": "iviz Picks Editorial Team",
          "url": "https://link.iviztrading.com/about.html"
        },
        "publisher": {
          "@type": "Organization",
          "name": "iviz Picks Malaysia",
          "url": "https://link.iviztrading.com/"
        }
      },
      "offers": {
        "@type": "Offer",
        "url": "{{affiliate_url}}",
        "priceCurrency": "MYR",
        "price": "{{price_num}}",
        "priceValidUntil": "{{price_valid_until}}",
        "itemCondition": "https://schema.org/NewCondition",
        "availability": "{{schema_availability}}",
        "seller": {
          "@type": "Organization",
          "name": "{{merchant_platform}}"
        }
      }
    }
    </script>

    <!-- Schema.org FAQPage -->
    <script type="application/ld+json">
    {
      "@context": "https://schema.org",
      "@type": "FAQPage",
      "mainEntity": [
        {{faq_schema_items}}
      ]
    }
    </script>
</head>
<body class="bg-slate-50 text-slate-900 antialiased min-h-screen flex flex-col justify-between selection:bg-orange-500 selection:text-white">

            <!-- Top Navigation Header -->
    <header class="bg-white/90 backdrop-blur-md border-b border-slate-200 sticky top-0 z-50 shadow-sm">
        <div class="max-w-4xl mx-auto px-4 py-3.5 flex items-center justify-between">
            <a href="index.html" class="flex items-center gap-2.5 font-extrabold text-lg text-slate-900 tracking-tight hover:opacity-80 transition-opacity">
                <span class="bg-gradient-to-tr from-orange-500 to-amber-400 text-white w-7 h-7 rounded-lg flex items-center justify-center font-black text-sm shadow-md shadow-orange-500/20">i</span>
                <span>iviz <span class="text-orange-500 font-bold">Picks</span></span>
            </a>
            <div class="hidden md:flex items-center gap-5 text-xs font-bold text-slate-600">
                <a href="index.html" class="hover:text-slate-900 transition-colors">Pilihan Utama</a>
                <a href="about.html" class="hover:text-slate-900 transition-colors">Mengenai Kami</a>
                <a href="editorial-policy.html" class="hover:text-slate-900 transition-colors">Polisi Semakan</a>
                <a href="privacy-policy.html" class="hover:text-slate-900 transition-colors">Privasi</a>
                <a href="contact.html" class="hover:text-slate-900 transition-colors">Hubungi</a>
            </div>
            <!-- Mobile Burger Button -->
            <button id="nav-burger" aria-label="Buka menu navigasi" aria-expanded="false" onclick="toggleNav()"
                    class="md:hidden w-9 h-9 flex items-center justify-center rounded-lg border border-slate-200 bg-white text-slate-700 hover:bg-slate-50 transition-colors">
                <svg id="nav-burger-icon" class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2.5" d="M4 6h16M4 12h16M4 18h16"></path></svg>
            </button>
        </div>
        <!-- Mobile Dropdown Menu -->
        <div id="nav-mobile-menu" class="md:hidden hidden border-t border-slate-100 bg-white/98 backdrop-blur-md">
            <nav class="max-w-4xl mx-auto px-4 py-2 flex flex-col text-sm font-bold text-slate-700">
                <a href="index.html" class="py-3 border-b border-slate-100 hover:text-orange-600 transition-colors">Pilihan Utama</a>
                <a href="about.html" class="py-3 border-b border-slate-100 hover:text-orange-600 transition-colors">Mengenai Kami</a>
                <a href="editorial-policy.html" class="py-3 border-b border-slate-100 hover:text-orange-600 transition-colors">Polisi Semakan</a>
                <a href="privacy-policy.html" class="py-3 border-b border-slate-100 hover:text-orange-600 transition-colors">Polisi Privasi</a>
                <a href="contact.html" class="py-3 hover:text-orange-600 transition-colors">Hubungi Kami</a>
            </nav>
        </div>
        </div>
    </header>

    <main class="max-w-3xl mx-auto px-4 pt-6 pb-32 md:py-10 w-full">

        <!-- Breadcrumb -->
        <nav class="flex items-center gap-2 text-xs text-slate-500 mb-6" aria-label="Breadcrumb">
            <a href="index.html" class="hover:text-orange-600 font-medium transition-colors">Utama</a>
            <span>/</span>
            <span class="text-slate-500 font-medium">{{group}}</span>
            <span>/</span>
            <span class="text-slate-500 font-medium">{{category}}</span>
            <span>/</span>
            <span class="text-slate-900 font-semibold truncate max-w-[180px]">{{name}}</span>
        </nav>

        <!-- Product Header Title Block -->
        <div class="mb-8">
            <div class="flex flex-wrap items-center gap-2 mb-3">
                <span class="bg-slate-900 text-white text-xs font-extrabold px-2.5 py-1 rounded-md shadow-sm">
                    {{group}}
                </span>
                <span class="bg-orange-50 text-orange-700 border border-orange-200 text-xs font-bold px-2.5 py-1 rounded-md">
                    {{category}}
                </span>
                {{verification_badge}}
            </div>
            
            <h1 class="text-2xl md:text-3xl lg:text-4xl font-extrabold text-slate-900 tracking-tight leading-tight">
                {{name}}
            </h1>
            
            <div class="flex flex-wrap items-center gap-2 text-xs text-slate-500 mt-3.5 pt-3 border-t border-slate-200">
                <span>Penyunting: <strong class="text-slate-800">Pasukan Editorial iviz Picks</strong></span>
                <span>•</span>
                <span>Kemaskini: <strong class="text-slate-800">{{last_updated}}</strong></span>
                <span>•</span>
                <a href="editorial-policy.html" class="text-orange-600 hover:underline font-bold">Metodologi Semakan</a>
            </div>
        </div>

        <!-- Quick Verdict Block -->
        <div class="bg-white border border-slate-200 rounded-2xl p-5 md:p-6 mb-8 shadow-sm">
            <div class="flex items-center justify-between gap-2 mb-3">
                <span class="text-xs font-extrabold text-orange-600 uppercase tracking-wider flex items-center gap-1.5">
                    <svg class="w-4 h-4 text-orange-500" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2.5" d="M9 12l2 2 4-4m6 2a9 9 0 11-18 0 9 9 0 0118 0z"></path></svg>
                    Rumusan Editorial iviz
                </span>
                <span class="bg-amber-50 text-amber-800 text-[11px] font-extrabold px-2.5 py-0.5 rounded-full border border-amber-200">
                    ⭐ Skor Nilai: {{editorial_score}} / 10
                </span>
            </div>
            <p class="text-slate-800 text-base md:text-lg font-bold leading-relaxed mb-5">
                "{{verdict}}"
            </p>
            <div class="grid grid-cols-1 md:grid-cols-2 gap-4 pt-4 border-t border-slate-100 text-xs">
                <div class="bg-emerald-50/70 border border-emerald-200/80 rounded-xl p-3.5">
                    <span class="font-extrabold text-emerald-900 flex items-center gap-1.5 mb-1.5 text-sm">
                        <svg class="w-4 h-4 text-emerald-600" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2.5" d="M5 13l4 4L19 7"></path></svg>
                        Sesuai Untuk Anda Jika:
                    </span>
                    <span class="text-slate-700 font-medium leading-relaxed block">{{who_is_it_for}}</span>
                </div>
                <div class="bg-amber-50/70 border border-amber-200/80 rounded-xl p-3.5">
                    <span class="font-extrabold text-amber-900 flex items-center gap-1.5 mb-1.5 text-sm">
                        <svg class="w-4 h-4 text-amber-600" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2.5" d="M12 9v2m0 4h.01m-6.938 4h13.856c1.54 0 2.502-1.667 1.732-3L13.732 4c-.77-1.333-2.694-1.333-3.464 0L3.34 16c-.77 1.333.192 3 1.732 3z"></path></svg>
                        Pertimbangkan Semula Jika:
                    </span>
                    <span class="text-slate-700 font-medium leading-relaxed block">{{who_should_skip}}</span>
                </div>
            </div>
        </div>

        <!-- Pricing & Store Link Box with Direct CDN Image -->
        <div class="bg-white rounded-2xl border border-slate-200 p-6 shadow-md mb-8 relative overflow-hidden">
            <div class="grid grid-cols-1 md:grid-cols-12 gap-6 items-center">
                
                <!-- Product External CDN Image Container -->
                <div class="md:col-span-5 bg-slate-100 border border-slate-200 rounded-xl overflow-hidden aspect-square relative shadow-inner flex items-center justify-center p-3">
                    <img src="{{image_url}}" alt="{{name}}" class="w-full h-full object-contain rounded-lg transition-transform hover:scale-105 duration-300" loading="lazy" />
                    <div class="absolute top-2 right-2 bg-gradient-to-r from-orange-500 to-amber-500 text-white font-black text-xs px-2.5 py-1 rounded-lg shadow-sm">
                        {{discount}}
                    </div>
                </div>

                <!-- Price & CTA Column -->
                <div class="md:col-span-7 flex flex-col justify-center">
                    <!-- Localized Trust Badges -->
                    <div class="flex flex-wrap items-center gap-2 mb-3.5 text-[11px] font-bold text-slate-600">
                        {{trust_badges}}
                    </div>

                    <div class="bg-slate-50 border border-slate-200 rounded-xl p-4 mb-4">
                        <span class="text-[11px] font-bold text-slate-500 uppercase tracking-wider block mb-1">Anggaran Harga Pasaran Terkini:</span>
                        <div class="flex items-baseline gap-3">
                            <span class="text-3xl md:text-4xl font-black text-slate-900 tracking-tight">{{shopee_price}}</span>
                            <span class="text-sm text-slate-400 line-through font-semibold">{{original_price}}</span>
                        </div>
                        <p class="text-[11px] text-slate-500 mt-2">
                            *Harga dan ketersediaan disemak secara berkala mengikut pengedar rasmi berdaftar.
                        </p>
                    </div>

                    <!-- CTA Button -->
                    <a href="{{affiliate_url}}" target="_blank" rel="nofollow noopener" 
                       class="w-full bg-gradient-to-r from-orange-500 via-orange-600 to-amber-500 hover:from-orange-600 hover:to-amber-600 text-white font-extrabold py-4 px-6 rounded-xl text-center transition-all flex items-center justify-center gap-2 text-sm md:text-base shadow-lg shadow-orange-500/25 hover:shadow-orange-500/35 hover:-translate-y-0.5 active:translate-y-0">
                        <span>Semak Tawaran di {{merchant_platform}}</span>
                        <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2.5" d="M14 5l7 7m0 0l-7 7m7-7H3"></path></svg>
                    </a>
                    
                    <p class="text-[11px] text-slate-500 text-center mt-2.5">
                        Pautan dihalakan terus ke halaman produk rasmi di {{merchant_platform}}.
                    </p>

                    <!-- Social Share Action Bar -->
                    <div class="mt-4 pt-3.5 border-t border-slate-100 flex items-center justify-between gap-2">
                        <span class="text-[11px] font-bold text-slate-500 uppercase tracking-wider flex items-center gap-1">
                            <svg class="w-3.5 h-3.5 text-slate-400" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M8.684 13.342C8.886 12.938 9 12.482 9 12c0-.482-.114-.938-.316-1.342m0 2.684a3 3 0 110-2.684m0 2.684l6.632 3.316m-6.632-6l6.632-3.316m0 0a3 3 0 105.367-2.684 3 3 0 00-5.367 2.684zm0 9.316a3 3 0 105.368 2.684 3 3 0 00-5.368-2.684z"></path></svg>
                            Kongsi:
                        </span>
                        <div class="flex items-center gap-1.5">
                            <!-- WhatsApp -->
                            <a href="https://api.whatsapp.com/send?text={{share_title_encoded}}%20https%3A%2F%2Flink.iviztrading.com%2F{{id}}.html" target="_blank" rel="noopener" title="Kongsi di WhatsApp"
                               class="w-7 h-7 rounded-lg bg-emerald-50 hover:bg-emerald-100 text-emerald-600 flex items-center justify-center transition-all hover:scale-105 border border-emerald-200/60 shadow-xs">
                                <svg class="w-3.5 h-3.5 fill-current" viewBox="0 0 24 24"><path d="M.057 24l1.687-6.163c-1.041-1.804-1.588-3.849-1.587-5.946.003-6.556 5.338-11.891 11.893-11.891 3.181.001 6.167 1.24 8.413 3.488 2.245 2.248 3.481 5.236 3.48 8.414-.003 6.557-5.338 11.892-11.893 11.892-1.99-.001-3.951-.5-5.688-1.448l-6.305 1.654zm6.597-3.807c1.676.995 3.276 1.591 5.392 1.592 5.448 0 9.886-4.434 9.889-9.885.002-5.462-4.415-9.89-9.881-9.892-5.452 0-9.887 4.434-9.889 9.884-.001 2.225.651 3.891 1.746 5.634l-.999 3.648 3.742-.981z"/></svg>
                            </a>
                            <!-- Telegram -->
                            <a href="https://t.me/share/url?url=https%3A%2F%2Flink.iviztrading.com%2F{{id}}.html&text={{share_title_encoded}}" target="_blank" rel="noopener" title="Kongsi di Telegram"
                               class="w-7 h-7 rounded-lg bg-sky-50 hover:bg-sky-100 text-sky-500 flex items-center justify-center transition-all hover:scale-105 border border-sky-200/60 shadow-xs">
                                <svg class="w-3.5 h-3.5 fill-current" viewBox="0 0 24 24"><path d="M12 0c-6.627 0-12 5.373-12 12s5.373 12 12 12 12-5.373 12-12-5.373-12-12-12zm5.894 8.221l-1.97 9.28c-.145.658-.537.818-1.084.508l-3-2.21-1.446 1.394c-.14.18-.357.34-.697.34l.2-3.05 5.56-5.022c.24-.213-.054-.334-.373-.121l-6.869 4.326-2.96-.924c-.643-.204-.657-.643.136-.953l11.57-4.461c.537-.194 1.006.131.833.863z"/></svg>
                            </a>
                            <!-- Facebook -->
                            <a href="https://www.facebook.com/sharer/sharer.php?u=https%3A%2F%2Flink.iviztrading.com%2F{{id}}.html" target="_blank" rel="noopener" title="Kongsi di Facebook"
                               class="w-7 h-7 rounded-lg bg-blue-50 hover:bg-blue-100 text-blue-600 flex items-center justify-center transition-all hover:scale-105 border border-blue-200/60 shadow-xs">
                                <svg class="w-3.5 h-3.5 fill-current" viewBox="0 0 24 24"><path d="M9 8h-3v4h3v12h5v-12h3.642l.358-4h-4v-1.667c0-.955.192-1.333 1.115-1.333h2.885v-5h-3.808c-3.596 0-5.192 1.583-5.192 4.615v3.385z"/></svg>
                            </a>
                            <!-- Salin Pautan / Copy -->
                            <button onclick="copyShareUrl(this, 'https://link.iviztrading.com/{{id}}.html')" title="Salin Pautan Ulasan"
                                    class="h-7 px-2 rounded-lg bg-slate-100 hover:bg-slate-200 text-slate-700 text-[11px] font-bold flex items-center gap-1 transition-all border border-slate-200 shadow-xs cursor-pointer">
                                <svg class="w-3 h-3" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M8 5H6a2 2 0 00-2 2v12a2 2 0 002 2h10a2 2 0 002-2v-1M8 5a2 2 0 002 2h2a2 2 0 002-2M8 5a2 2 0 012-2h2a2 2 0 012 2m0 0h2a2 2 0 012 2v3m2 4H10m0 0l3-3m-3 3l3 3"></path></svg>
                                <span>Salin</span>
                            </button>
                            <!-- Web Share API (if supported) -->
                            <button onclick="nativeShare('{{name}}', 'https://link.iviztrading.com/{{id}}.html')" title="Menu Kongsi" id="btn-native-share"
                                    class="w-7 h-7 rounded-lg bg-orange-50 hover:bg-orange-100 text-orange-600 flex items-center justify-center transition-all border border-orange-200/60 shadow-xs cursor-pointer">
                                <svg class="w-3.5 h-3.5" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4 16v1a3 3 0 003 3h10a3 3 0 003-3v-1m-4-8l-4-4m0 0L8 8m4-4v12"></path></svg>
                            </button>
                        </div>
                    </div>
                </div>
            </div>
        </div>

        <!-- Pros & Cons Grid -->
        <div class="grid grid-cols-1 md:grid-cols-2 gap-5 mb-8">
            <!-- Pros -->
            <div class="bg-emerald-50/40 border border-emerald-200 rounded-2xl p-5 md:p-6 shadow-sm">
                <h2 class="text-sm font-extrabold text-emerald-900 mb-4 uppercase tracking-wider flex items-center gap-2">
                    <svg class="w-4 h-4 text-emerald-600" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2.5" d="M5 13l4 4L19 7"></path></svg>
                    Kelebihan Utama:
                </h2>
                <ul class="space-y-3 text-sm text-slate-800">
                    {{pros_html}}
                </ul>
            </div>

            <!-- Cons -->
            <div class="bg-amber-50/40 border border-amber-200 rounded-2xl p-5 md:p-6 shadow-sm">
                <h2 class="text-sm font-extrabold text-amber-900 mb-4 uppercase tracking-wider flex items-center gap-2">
                    <svg class="w-4 h-4 text-amber-600" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2.5" d="M12 9v2m0 4h.01m-6.938 4h13.856c1.54 0 2.502-1.667 1.732-3L13.732 4c-.77-1.333.192 3 1.732 3z"></path></svg>
                    Kekurangan & Had:
                </h2>
                <ul class="space-y-3 text-sm text-slate-800">
                    {{cons_html}}
                </ul>
            </div>
        </div>

        <!-- Specs Table -->
        <div class="bg-white rounded-2xl border border-slate-200 p-5 md:p-6 shadow-sm mb-8">
            <h2 class="text-base font-extrabold text-slate-900 mb-4 border-b border-slate-100 pb-3 flex items-center gap-2">
                <svg class="w-5 h-5 text-orange-500" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 5H7a2 2 0 00-2 2v12a2 2 0 002 2h10a2 2 0 002-2V7a2 2 0 00-2-2h-2M9 5a2 2 0 002 2h2a2 2 0 002-2M9 5a2 2 0 012-2h2a2 2 0 012 2"></path></svg>
                Spesifikasi & Semakan Pihak Ketiga
            </h2>
            <div class="divide-y divide-slate-100 text-sm">
                {{specs_html}}
            </div>
        </div>

        <!-- FAQ Section -->
        <div class="bg-white rounded-2xl border border-slate-200 p-5 md:p-6 shadow-sm mb-8">
            <h2 class="text-base font-extrabold text-slate-900 mb-4 border-b border-slate-100 pb-3 flex items-center gap-2">
                <svg class="w-5 h-5 text-orange-500" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M8.228 9c.549-1.165 2.03-2 3.772-2 2.21 0 4 1.343 4 3 0 1.4-1.278 2.575-3.006 2.907-.542.104-.994.54-.994 1.093m0 3h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z"></path></svg>
                Soalan Lazim Pembeli (FAQ)
            </h2>
            <div class="space-y-3">
                {{faq_html}}
            </div>
        </div>

        <!-- Sticky Mobile Bottom Bar -->
        <div class="fixed bottom-0 left-0 right-0 p-3.5 pb-[max(0.875rem,env(safe-area-inset-bottom))] bg-white/95 backdrop-blur-md border-t border-slate-200/90 z-40 md:hidden flex items-center justify-between gap-3 shadow-2xl">
            <div class="shrink-0">
                <span class="text-[10px] text-slate-500 block uppercase font-extrabold leading-tight">Harga Promosi:</span>
                <span class="text-base font-black text-slate-900 leading-tight">{{shopee_price}}</span>
            </div>
            <a href="{{affiliate_url}}" target="_blank" rel="nofollow noopener" 
               class="bg-gradient-to-r from-orange-500 to-amber-500 text-white font-extrabold py-3 px-4 rounded-xl text-xs flex items-center justify-center gap-1.5 shadow-md shadow-orange-500/20 min-h-[44px] flex-grow text-center">
                <span>Semak di Stor Rasmi</span>
                <svg class="w-3.5 h-3.5 shrink-0" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2.5" d="M14 5l7 7m0 0l-7 7m7-7H3"></path></svg>
            </a>
        </div>

    </main>

        <!-- Footer -->
    <footer class="bg-white border-t border-slate-200 py-10 px-4 text-xs text-slate-500 mt-12 mb-16 md:mb-0">
        <div class="max-w-4xl mx-auto flex flex-col md:flex-row items-center justify-between gap-4">
            <div class="flex items-center gap-2.5 font-bold text-slate-900">
                <span class="bg-gradient-to-tr from-orange-500 to-amber-400 text-white w-5 h-5 rounded flex items-center justify-center text-[11px] font-black shadow-sm">i</span>
                <span>iviz Picks Malaysia</span>
            </div>
            <div class="flex items-center gap-5 text-slate-600 font-semibold">
                <a href="about.html" class="hover:text-slate-900 transition-colors">Mengenai Kami</a>
                <a href="editorial-policy.html" class="hover:text-slate-900 transition-colors">Polisi Semakan</a>
                <a href="privacy-policy.html" class="hover:text-slate-900 transition-colors">Polisi Privasi</a>
                <a href="contact.html" class="hover:text-slate-900 transition-colors">Hubungi Kami</a>
            </div>
        </div>
        <div class="max-w-4xl mx-auto text-[11px] text-slate-400 mt-6 pt-6 border-t border-slate-100 text-center leading-relaxed">
            Penafian: iviz Picks ialah saluran media ulasan bebas. Pautan luar mungkin mengandungi rujukan perkongsian komisen afiliasi. Sebarang ulasan diterbitkan secara objektif tanpa tajaan penjual. Hubungi kami: <a href="mailto:hello@iviztrading.com" class="text-slate-600 underline font-medium">hello@iviztrading.com</a>.
        </div>
    </footer>

    <script>
    function copyShareUrl(btn, url) {
        if (navigator.clipboard) {
            navigator.clipboard.writeText(url).then(() => {
                const orig = btn.innerHTML;
                btn.innerHTML = '<span>✅ Disalin!</span>';
                btn.classList.add('bg-emerald-100', 'text-emerald-700', 'border-emerald-300');
                setTimeout(() => {
                    btn.innerHTML = orig;
                    btn.classList.remove('bg-emerald-100', 'text-emerald-700', 'border-emerald-300');
                }, 2000);
            });
        }
    }
    function nativeShare(title, url) {
        if (navigator.share) {
            navigator.share({
                title: title + ' - iviz Picks',
                text: 'Semak ulasan penuh ' + title + ' di iviz Picks:',
                url: url
            }).catch(() => {});
        } else {
            const tempBtn = document.createElement('button');
            copyShareUrl(tempBtn, url);
        }
    }
    // Hide native share button if not supported
    if (!navigator.share) {
        document.querySelectorAll('#btn-native-share').forEach(b => b.style.display = 'none');
    }
    // Mobile navigation toggle
    function toggleNav() {
        const menu = document.getElementById('nav-mobile-menu');
        const btn = document.getElementById('nav-burger');
        if (!menu) return;
        const isOpen = !menu.classList.contains('hidden');
        menu.classList.toggle('hidden');
        if (btn) btn.setAttribute('aria-expanded', String(!isOpen));
    }
    </script>
</body>
</html>
"""

# ==============================================================================
# CATEGORY LISTICLE HUBS GENERATOR (Hub-and-Spoke, AEO/GEO/SEO)
# ==============================================================================
CATEGORY_LISTICLE_SPECS = [
    # --------------------------------------------------------------------------
    # HAB KATEGORI UTAMA (CATEGORY HUBS)
    # --------------------------------------------------------------------------
    {
        "slug": "skincare-kesihatan-viral.html",
        "title_short": "Skincare & Kesihatan",
        "emoji": "✨",
        "meta_title": "{n} Produk Skincare & Kesihatan Viral Malaysia ({year}) — Pilihan Terbaik",
        "meta_desc": "Bandingkan {n} produk skincare dan kesihatan viral paling berbaloi di Shopee & Lazada Malaysia ({year}). Semakan ramuan bebas, status NPRA KKM, dan harga terkini.",
        "h1": "{n} Produk Skincare & Kesihatan Viral Terbaik di Malaysia ({year})",
        "intro": "Senarai semakan bebas produk penjagaan kulit dan kesihatan paling laris di Malaysia. Setiap ulasan menilai keberkesanan bahan aktif, maklum balas pengguna sebenar, serta status keselamatan berdaftar rasmi.",
        "match": lambda p: classify_category(p) == "skincare"
    },
    {
        "slug": "gajet-elektronik-terbaik.html",
        "title_short": "Gajet & Elektronik",
        "emoji": "⚡",
        "meta_title": "{n} Gajet & Aksesori Elektronik Terbaik Malaysia ({year}) — Berbaloi Beli",
        "meta_desc": "Bandingkan {n} gajet viral dan aksesori telefon paling berbaloi di pasaran Malaysia ({year}). Ulasan fon telinga, powerbank, kabel pantas, dan pengecas.",
        "h1": "{n} Gajet & Aksesori Elektronik Paling Berbaloi di Malaysia ({year})",
        "intro": "Panduan ulasan bebas gajet pintar, fon telinga tanpa wayar, powerbank tahan lasak, dan aksesori komputer berkualiti tinggi yang menawarkan nilai terbaik untuk wang anda.",
        "match": lambda p: classify_category(p) == "gajet"
    },
    {
        "slug": "perkakas-dapur-viral.html",
        "title_short": "Perkakas Dapur & Rumah",
        "emoji": "🍳",
        "meta_title": "{n} Perkakas Dapur & Rumah Viral Malaysia ({year}) — Jimat Masa Masak",
        "meta_desc": "Bandingkan {n} perkakas dapur dan rumah viral paling popular di Malaysia ({year}). Semakan air fryer, periuk nasi rendah gula, induction cooker, dan alatan pembersih.",
        "h1": "{n} Perkakas Dapur & Rumah Paling Viral di Malaysia ({year})",
        "intro": "Ulasan objektif alatan dapur moden dan perkakas rumah pintar yang terbukti memudahkan rutin harian keluarga Malaysia. Jimat masa memasak dan mengemas kediaman.",
        "match": lambda p: classify_category(p) == "dapur"
    },
    {
        "slug": "rumah-pintar-pembersihan.html",
        "title_short": "Rumah Pintar & Pembersihan",
        "emoji": "🏠",
        "meta_title": "{n} Produk Rumah Pintar & Pembersihan Viral Malaysia ({year})",
        "meta_desc": "Bandingkan {n} produk rumah pintar, pembersih udara, dan vakum viral terbaik di Malaysia ({year}). Semakan prestasi dan nilai harga.",
        "h1": "{n} Produk Rumah Pintar & Pembersihan Paling Viral di Malaysia ({year})",
        "intro": "Pilihan penapis udara, robot vakum, dan alatan kebersihan kediaman yang memudahkan tugas harian dengan teknologi terkini.",
        "match": lambda p: classify_category(p) == "rumah_pintar",
        "is_problem": False
    },
    {
        "slug": "setup-meja-wfh-terbaik.html",
        "title_short": "Setup Meja WFH",
        "emoji": "🖥️",
        "meta_title": "{n} Kelengkapan Setup Meja WFH Terbaik Malaysia ({year})",
        "meta_desc": "Bandingkan {n} kerusi ergonomik, meja boleh laras, dan aksesori meja yang selesa untuk produktiviti kerja dari rumah ({year}).",
        "h1": "{n} Kelengkapan Setup Meja WFH Paling Selesa di Malaysia ({year})",
        "intro": "Optimalkan ruang kerja anda dengan pilihan kerusi ergonomik, meja berdiri (standing desk), dan aksesori meja yang membantu kesihatan postur.",
        "match": lambda p: classify_category(p) == "setup_wfh",
        "is_problem": False
    },

    # --------------------------------------------------------------------------
    # HAB LISTICLE BERFOKUSKAN MASALAH (PROBLEM-FOCUSED HUBS)
    # --------------------------------------------------------------------------
    {
        "slug": "skincare-kulit-berminyak.html",
        "title_short": "Kulit Berminyak & Pori",
        "emoji": "🧼",
        "meta_title": "{n} Skincare Terbaik untuk Kulit Berminyak & Jerawat Malaysia ({year})",
        "meta_desc": "Panduan {n} pencuci muka, sunscreen, dan pelembap paling berkesan kawal minyak dan pori tersumbat tanpa melekit ({year}).",
        "h1": "{n} Skincare Terbaik untuk Kulit Berminyak & Mudah Berjerawat ({year})",
        "intro": "Ulasan bebas produk skincare ringan berasaskan gel dan buih lembut yang terbukti mengawal lebihan sebum serta mencerahkan pori tersumbat.",
        "match": lambda p: match_problem_category(p, "kulit_berminyak"),
        "is_problem": True
    },
    {
        "slug": "serum-jeragat-parut-hitam.html",
        "title_short": "Jeragat & Parut Hitam",
        "emoji": "🎯",
        "meta_title": "{n} Serum Paling Berkesan Hilangkan Jeragat & Parut Hitam ({year})",
        "meta_desc": "Semakan {n} serum Niacinamide, Vitamin C, dan Alpha Arbutin terbaik untuk pudar jeragat dan parut jerawat kusam ({year}).",
        "h1": "{n} Serum Paling Berkesan Hilangkan Jeragat & Parut Hitam di Malaysia ({year})",
        "intro": "Pilihan serum bahan aktif terbukti (Niacinamide, TXA, Vitamin C) yang diformulasi khas untuk memudarkan hiperpigmentasi dan meratakan tona kulit.",
        "match": lambda p: match_problem_category(p, "jeragat_parut"),
        "is_problem": True
    },
    {
        "slug": "pelembap-kulit-kering-barrier.html",
        "title_short": "Kulit Kering & Barrier",
        "emoji": "💧",
        "meta_title": "{n} Pelembap Terbaik Pulihkan Skin Barrier & Kulit Kering ({year})",
        "meta_desc": "Senarai {n} moisturizer Ceramide dan Hyaluronic Acid terbaik untuk atasi kulit kering mengelupas dan pedih ({year}).",
        "h1": "{n} Pelembap Terbaik Pulihkan Skin Barrier & Kulit Kering ({year})",
        "intro": "Koleksi pelembap berformula Ceramide 5X dan Asid Hialuronik yang berkesan mengunci kelembapan 24 jam serta merawat skin barrier terjejas.",
        "match": lambda p: match_problem_category(p, "kulit_kering"),
        "is_problem": True
    },
    {
        "slug": "perkakas-dapur-diet-sihat.html",
        "title_short": "Diet Sihat & Rendah Gula",
        "emoji": "🥗",
        "meta_title": "{n} Periuk Nasi Low Sugar & Pengisar Sihat Terbaik ({year})",
        "meta_desc": "Ulasan {n} periuk nasi rendah gula, pengisar smoothie dan penimbang digital terbaik untuk gaya hidup sihat & pesakit diabetes ({year}).",
        "h1": "{n} Alatan Dapur Rendah Gula & Pengisar Sihat untuk Diet ({year})",
        "intro": "Perkakas dapur yang membantu menguruskan pengambilan gula dan kalori harian — daripada periuk nasi teknologi 'low sugar' hingga pengisar nutrisi untuk smoothie segar.",
        "match": lambda p: match_problem_category(p, "diet_sihat"),
        "is_problem": True,
        "added_at": "2026-10-08"
    },
    {
        "slug": "gajet-dapur-masak-pantas.html",
        "title_short": "Dapur Masak Pantas",
        "emoji": "⚡",
        "meta_title": "{n} Air Fryer & Steamer Terbaik untuk Masakan Pantas ({year})",
        "meta_desc": "Senarai {n} air fryer smokeless dan pengukus elektrik terbaik di Malaysia untuk yang sibuk — masak cepat tanpa berlama-lama di dapur ({year}).",
        "h1": "{n} Gajet Dapur Masak Pantas: Air Fryer & Steamer Terbaik ({year})",
        "intro": "Selesai masalah tiada masa memasak dengan gajet dapur yang mempercepatkan penyediaan makanan harian tanpa pengawet dan tanpa minyak berlebihan.",
        "match": lambda p: match_problem_category(p, "masak_pantas"),
        "is_problem": True,
        "added_at": "2026-10-08"
    },
    {
        "slug": "kerusi-ergonomik-sakit-pinggang.html",
        "title_short": "Sakit Pinggang & Postur",
        "emoji": "🪑",
        "meta_title": "{n} Kerusi Ergonomik & Kusyen Tulang Belakang Terbaik ({year})",
        "meta_desc": "Bandingkan {n} kerusi pejabat ergonomik dan kusyen sokongan lumbar untuk elak sakit pinggang bekerja seharian ({year}).",
        "h1": "{n} Kerusi Ergonomik & Kusyen Sokongan Pinggang Terbaik ({year})",
        "intro": "Solusi keselesaan duduk berjam-jam di meja kerja dengan sokongan lumbar dan fabrik bernafas untuk mengelakkan lenguh tulang belakang.",
        "match": lambda p: match_problem_category(p, "sakit_pinggang"),
        "is_problem": True
    },
    {
        "slug": "penapis-udara-vakum-bulu-habuk.html",
        "title_short": "Bulu Kucing & Habuk",
        "emoji": "🧹",
        "meta_title": "{n} Penapis Udara & Vakum Terbaik Atasi Bulu Kucing & Habuk ({year})",
        "meta_desc": "Panduan {n} penapis udara HEPA dan vakum mudah alih terbaik untuk bersihkan bulu haiwan, habuk halus, dan atasi alahan rumah ({year}).",
        "h1": "{n} Penapis Udara & Vakum Terbaik untuk Bulu Kucing & Habuk ({year})",
        "intro": "Kombinasi penapis udara berteknologi HEPA dan vakum berkuasa tinggi yang berkesan menangkap bulu haiwan peliharaan serta habuk halus di udara dan permukaan.",
        "match": lambda p: match_problem_category(p, "bulu_habuk"),
        "is_problem": True
    },
    {
        "slug": "aksesori-pembersih-kereta.html",
        "title_short": "Kereta Bersih & Selesa",
        "emoji": "🚗",
        "meta_title": "{n} Aksesori & Pembersih Kereta Terbaik untuk Pemandu ({year})",
        "meta_desc": "Senarai {n} vakum kereta, pemegang telefon magnetik, pengecas pantas, dan dashcam terbaik untuk keselesaan & keselamatan pemanduan ({year}).",
        "h1": "{n} Aksesori & Pembersih Kereta Terbaik untuk Keselesaan Pemandu ({year})",
        "intro": "Lengkapkan pengalaman memandu anda dengan vakum kereta mudah alih, pemegang telefon stabil, dan pengecas pantas yang menjadikan setiap perjalanan lebih selesa.",
        "match": lambda p: match_problem_category(p, "kereta_bersih"),
        "is_problem": True
    },
    {
        "slug": "steamer-lint-remover-pakaian.html",
        "title_short": "Pakaian Kemas & Licin",
        "emoji": "👔",
        "meta_title": "{n} Garment Steamer & Lint Remover Terbaik Malaysia ({year})",
        "meta_desc": "Bandingkan {n} steamer pakaian mudah alih dan penggilap bulu fabrik terbaik untuk pakaian kemas tanpa seterika ({year}).",
        "h1": "{n} Garment Steamer & Lint Remover Terbaik untuk Pakaian Kemas ({year})",
        "intro": "Alatan penjagaan pakaian moden yang melicinkan kedutan dan membuang bulu fabrik dengan pantas, tanpa perlu mengeluarkan papan seterika.",
        "match": lambda p: match_problem_category(p, "pakaian_kemas"),
        "is_problem": True
    },
    {
        "slug": "penjagaan-diri-lelaki-grooming.html",
        "title_short": "Penjagaan Diri Lelaki",
        "emoji": "🧔",
        "meta_title": "{n} Produk Penjagaan Diri Lelaki & Grooming Terbaik ({year})",
        "meta_desc": "Bandingkan {n} produk grooming lelaki terbaik di Malaysia — pencukur elektrik, deodorant tahan 48 jam, pencuci muka, dan pengering rambut untuk rutin harian ({year}).",
        "h1": "{n} Produk Penjagaan Diri Lelaki Wajib Untuk Rutin Harian ({year})",
        "intro": "Rutin grooming lelaki yang ringkas tetapi lengkap: cukur janggut tanpa iritasi, bau badan kekal segar sepanjang hari, dan rambut sentiasa kemas — semua dengan produk berpatutan di Malaysia.",
        "match": lambda p: match_problem_category(p, "grooming_lelaki"),
        "is_problem": True,
        "added_at": "2026-10-08"
    },

    # --------------------------------------------------------------------------
    # HAB LISTICLE PSIKOLOGI, GAYA HIDUP & HADIAH (INTENT & LIFE-STAGE HUBS)
    # --------------------------------------------------------------------------
    {
        "slug": "idea-hadiah-housewarming-birthday.html",
        "title_short": "Idea Hadiah & Housewarming",
        "emoji": "🎁",
        "meta_title": "{n} Idea Hadiah Housewarming & Hari Jadi Bawah RM100 Malaysia ({year})",
        "meta_desc": "Panduan {n} idea hadiah housewarming dan hari jadi berguna bawah RM100 yang gerenti dipakai tuan rumah ({year}).",
        "h1": "{n} Idea Hadiah Housewarming & Hari Jadi Bawah RM100 Paling Berguna ({year})",
        "intro": "Senarai idea hadiah praktikal, estetik, dan bernilai tinggi bawah RM100 yang sesuai untuk kenduri masuk rumah baharu, hari jadi kawan, atau majlis pertukaran hadiah.",
        "match": lambda p: match_problem_category(p, "hadiah_housewarming"),
        "is_problem": False,
        "is_intent": True
    },
    {
        "slug": "starter-pack-rumah-sewa-asrama.html",
        "title_short": "Starter Pack Rumah Sewa",
        "emoji": "📦",
        "meta_title": "{n} Starter Pack Barang Wajib Masuk Rumah Sewa & Asrama ({year})",
        "meta_desc": "Senarai semak {n} barang elektrik dan alatan asas jimat ruang wajib ada untuk penyewa rumah pertama atau pelajar asrama ({year}).",
        "h1": "{n} Starter Pack Barang Wajib Ada untuk Masuk Rumah Sewa & Asrama ({year})",
        "intro": "Panduan permulaan hidup berdikari: peralatan elektrik kompak, alatan memasak jimat tenaga, dan perkakas pembersihan penting yang tahan lasak dan mudah dibawa pindah.",
        "match": lambda p: match_problem_category(p, "starter_pack_rumah_sewa"),
        "is_problem": False,
        "is_intent": True
    },
    {
        "slug": "gajet-penampilan-kemas-glow-up.html",
        "title_short": "Gajet Penampilan Kemas",
        "emoji": "✨",
        "meta_title": "{n} Gajet & Produk Penampilan Kemas Profesional Malaysia ({year})",
        "meta_desc": "Bandingkan {n} alatan penjagaan pakaian, dandanan, dan skincare ringkas untuk penampilan segak dan profesional setiap hari ({year}).",
        "h1": "{n} Gajet & Produk Penjagaan Diri untuk Penampilan Sentiasa Kemas ({year})",
        "intro": "Rutin ringkas dan alatan pintar yang memastikan pakaian bebas kedutan, fabrik bebas bulu, serta wajah segar bertenaga untuk keyakinan harian.",
        "match": lambda p: match_problem_category(p, "rutin_penampilan_kemas"),
        "is_problem": False,
        "is_intent": True
    },
    {
        "slug": "kelengkapan-pelajar-asrama-universiti.html",
        "title_short": "Kelengkapan Pelajar Asrama",
        "emoji": "🎓",
        "meta_title": "{n} Kelengkapan Wajib Pelajar Asrama & Universiti Malaysia ({year})",
        "meta_desc": "Senarai semak {n} barang elektrik dan kelengkapan asas wajib ada untuk bilik asrama dan universiti — jimat ruang & tenaga ({year}).",
        "h1": "{n} Kelengkapan Wajib Pelajar Asrama & Universiti Paling Praktikal ({year})",
        "intro": "Peralatan serbaguna berkuasa rendah yang menjimatkan ruang dan bil elektrik, direka khas untuk memudahkan kehidupan harian pelajar di kampus.",
        "match": lambda p: match_problem_category(p, "pelajar_asrama"),
        "is_problem": False,
        "is_intent": True
    },
    {
        "slug": "peralatan-rumah-mesra-keluarga-bayi.html",
        "title_short": "Rumah Mesra Keluarga & Bayi",
        "emoji": "👶",
        "meta_title": "{n} Peralatan Rumah Mesra Keluarga & Anak Kecil Malaysia ({year})",
        "meta_desc": "Bandingkan {n} alatan kebersihan, pensterilan, dan keselamatan rumah terbaik untuk keluarga dengan bayi dan anak kecil ({year}).",
        "h1": "{n} Peralatan Rumah Mesra Keluarga & Anak Kecil Paling Dipercayai ({year})",
        "intro": "Panduan alatan penjagaan kesihatan kediaman, penapis udara bebas alergen, dan perkakas pensterilan selamat untuk kesejahteraan si manja.",
        "match": lambda p: match_problem_category(p, "keluarga_bayi"),
        "is_problem": False,
        "is_intent": True
    },
    {
        "slug": "peralatan-dapur-jimat-masa-bujang.html",
        "title_short": "Dapur Bujang Jimat Masa",
        "emoji": "🍳",
        "meta_title": "{n} Peralatan Dapur & Rumah Jimat Masa untuk Bujang ({year})",
        "meta_desc": "Pilihan {n} gajet dapur ringkas dan perkakas rumah pantas untuk bujang sibuk yang ingin jimat masa memasak dan mengemas ({year}).",
        "h1": "{n} Peralatan Dapur & Rumah Jimat Masa untuk Kehidupan Bujang ({year})",
        "intro": "Perkakas kompak satu hidangan yang pantas dipanaskan dan mudah dibersihkan, sesuai untuk individu berkerjaya yang mahukan keselesaan maksimum.",
        "match": lambda p: match_problem_category(p, "bujang_sibuk"),
        "is_problem": False,
        "is_intent": True
    },
    {
        "slug": "gajet-aksesori-travel-outstation.html",
        "title_short": "Gajet Kaki Travel & Outstation",
        "emoji": "✈️",
        "meta_title": "{n} Gajet & Aksesori Wajib Ada untuk Kaki Travel ({year})",
        "meta_desc": "Bandingkan {n} powerbank, pengecas pantas GaN, dan perkakas mudah lipat terbaik untuk penerbangan dan urusan luar kawasan ({year}).",
        "h1": "{n} Gajet & Aksesori Travel Terbaik untuk Perjalanan Lancar ({year})",
        "intro": "Kelengkapan kompak dan tahan lasak yang memastikan semua peranti anda kekal bertenaga serta pakaian kekal rapi semasa mengembara.",
        "match": lambda p: match_problem_category(p, "kaki_travel"),
        "is_problem": False,
        "is_intent": True
    },
    {
        "slug": "kelengkapan-gaya-hidup-cergas-fitness.html",
        "title_short": "Gaya Hidup Cergas & Fitness",
        "emoji": "🏃‍♂️",
        "meta_title": "{n} Kelengkapan Gaya Hidup Cergas & Fitness di Rumah ({year})",
        "meta_desc": "Senarai {n} pengisar protein, penimbang diet tepat, dan penjejak aktiviti terbaik untuk sokong matlamat kesihatan harian ({year}).",
        "h1": "{n} Kelengkapan Gaya Hidup Cergas & Penjagaan Kesihatan ({year})",
        "intro": "Alatan praktikal yang membantu pemantauan pemakanan seimbang, pengambilan hidrasi optimum, serta pemulihan otot selepas bersenam.",
        "match": lambda p: match_problem_category(p, "fitness_kesihatan"),
        "is_problem": False,
        "is_intent": True
    },
    {
        "slug": "setup-meja-kerja-minimalis-estetik.html",
        "title_short": "Setup Meja Kerja Minimalis",
        "emoji": "🖥️",
        "meta_title": "{n} Aksesori Setup Meja Kerja Minimalis & Produktif ({year})",
        "meta_desc": "Panduan {n} aksesori meja kerja estetik, lampu monitor, dan papan kekunci ergonomik untuk ruang kerja kemas dan selesa ({year}).",
        "h1": "{n} Aksesori Setup Meja Kerja Minimalis untuk Produktiviti ({year})",
        "intro": "Inspirasi susun atur meja bebas serabut dengan alatan berprestasi tinggi yang menyokong ergonomik postur dan fokus berpanjangan.",
        "match": lambda p: match_problem_category(p, "setup_minimalis"),
        "is_problem": False,
        "is_intent": True
    },
    {
        "slug": "barang-viral-berbaloi-bawah-rm50.html",
        "title_short": "Pilihan Berbaloi Bawah RM50",
        "emoji": "💰",
        "meta_title": "{n} Barang Viral Shopee Bawah RM50 yang Paling Berbaloi ({year})",
        "meta_desc": "Senarai {n} produk trending dan berkualiti tinggi bawah RM50 daripada stor rasmi yang terbukti bernilai setiap ringgit ({year}).",
        "h1": "{n} Barang Viral Bawah RM50 Paling Berbaloi & Tahan Lasak ({year})",
        "intro": "Pilihan bijak bajet rendah: produk kegunaan harian tulen dengan skor ulasan tinggi yang membuktikan kualiti premium tidak semestinya mahal.",
        "match": lambda p: match_problem_category(p, "bajet_bawah_rm50"),
        "is_problem": False,
        "is_intent": True
    }
]


def sorted_specs(specs=None):
    """Susun listicle spec: terbaru (ada added_at) di ATAS, lama (tanpa added_at)
    kekal ikut susunan asal di bawah. Standard enterprise: kad latest di atas."""
    specs = specs if specs is not None else CATEGORY_LISTICLE_SPECS
    dated = sorted([s for s in specs if s.get("added_at")],
                   key=lambda s: s["added_at"], reverse=True)
    undated = [s for s in specs if not s.get("added_at")]
    return dated + undated

def parse_numeric_price(p):
    raw = str(p.get("shopee_price") or p.get("price") or "0")
    c = re.sub(r"[^\d.]", "", raw)
    try:
        return float(c)
    except Exception:
        return 9999.0


def match_problem_category(p, problem_type):
    """
    GUARDRAIL: Padanan produk ke hab masalah HANYA melalui whitelist ID eksplisit
    serta tapisan hard-cap harga numerik automatik untuk segmen bajet.
    """
    if p.get("id") not in PROBLEM_HUB_PRODUCT_IDS.get(problem_type, set()):
        return False
    
    # HARD CAP HARGA: Tolak jika melebihi had bajet
    price = parse_numeric_price(p)
    if problem_type in ("hadiah_housewarming",) and price > 100.0:
        return False
    if problem_type in ("bajet_bawah_rm50",) and price > 50.0:
        return False
        
    return True


# ==============================================================================
# WHITELIST EKSPLISIT: ID produk yang SAH untuk setiap hab masalah.
# Semak manual setiap kali tambah produk baharu. JANGAN tambah secara rambang.
# ==============================================================================
# WHITELIST EKSPLISIT: ID produk yang SAH untuk setiap hab masalah.
# Semak manual setiap kali tambah produk baharu. JANGAN tambah secara rambang.
# ==============================================================================
PROBLEM_HUB_PRODUCT_IDS = {
    # Masalah jerawat, kulit berminyak & pori tersumbat
    "kulit_berminyak": {
        "cosrx-acne-pimple-master-patch-24pcs",
        "some-by-mi-aha-bha-pha-miracle-toner-150ml",
        "skintific-5-panthenol-acne-calming-water-gel-45g",
        "aiken-tea-tree-oil-facial-cleanser-100g",
        "cosmoderm-tea-tree-oil-calming-cleanser",
        "cosrx-low-ph-good-morning-gel-cleanser-150ml",
        "cetaphil-gentle-exfoliating-salicylic-cleanser",
        "cerave-foaming-cleanser-473ml",
    },
    # Masalah jeragat, parut hitam & tona kulit tak sekata (Serum pencerah & rawatan jeragat SAHAJA)
    "jeragat_parut": {
        "skintific-symwhite-377-dark-spot-serum-20ml",
        "anua-niacinamide-10-txa-4-dark-spot-serum",
        "the-ordinary-niacinamide-10-zinc-1",
        "glad2glow-10-niacinamide-pomegranate-serum-17ml",
        "aiken-5x-ceramide-bright-vitamin-c-serum-15ml",
        "hada-labo-softening-whitening-face-wash-100g",
        "nivea-men-bright-c-hya-wash-foam-100g",
    },
    # Masalah kulit kering, mengelupas & skin barrier rosak (Ceramides, Hyaluronic, Snail Mucin)
    "kulit_kering": {
        "skintific-5x-ceramide-moisture-gel",
        "the-originote-hyalucera-moisturizer-gel",
        "torriden-dive-in-low-molecule-hyaluronic-acid-serum",
        "hada-labo-hydrating-lotion-light-170ml",
        "laneige-water-bank-blue-hyaluronic-serum",
        "cosrx-advanced-snail-96-mucin-power-essence",
    },
    # Masalah diet sihat: kurangkan minyak & gula (Air Fryer, Periuk Low-Sugar, Penimbang Gram, Blender Fruit)
    "diet_sihat": {
        "tefal-5l-low-sugar-rice-cooker",
        "gaabor-air-fryer-3-5l-smokeless-oil-free",
        "gaabor-smokeless-air-fryer-4l",
        "admore-digital-kitchen-scale-5kg",
        "maxeko-portable-smoothie-blender-cup",
    },
    # Masalah sakit pinggang & postur duduk lama (Kerusi Ergonomik, Kusyen Lumbar, Laptop Stand)
    "sakit_pinggang": {
        "boldlux-memory-foam-backrest-cushion",
        "ttracing-swift-x-2020-gaming-chair",
        "ergonomic-foldable-aluminum-laptop-stand",
    },
    # Masalah bulu kucing, habuk & kualiti udara rumah (Penapis HEPA, Vakum Lantai, Vakum Hama Tilam, Lint Shaver)
    "bulu_habuk": {
        "xiaomi-smart-air-purifier-4-compact",
        "deerma-dx300-vacuum-cleaner",
        "deerma-cordless-dust-mite-vacuum-cleaner",
        "xiaomi-showsee-electric-lint-remover",
    },
    # Masalah ruang kereta kotor & bersepah (Vakum Kereta, Tong Sampah Kabin, Box But Lipat, Phone Holder)
    "kereta_bersih": {
        "wireless-car-vacuum-cleaner-handheld",
        "foldable-car-trunk-organizer-waterproof",
        "foldable-hanging-car-trash-can-waterproof",
        "baseus-360-rotation-magnetic-car-holder",
    },
    # Masalah pakaian berkedut & berbulu (Steamer Lipat Travel, Garment Steamer, Lint Remover)
    "pakaian_kemas": {
        "panasonic-ni-ghd021-handheld-garment-steamer",
        "tobi-portable-travel-garment-steamer-handheld",
        "xiaomi-showsee-electric-lint-remover",
    },
    # Niat Hadiah Housewarming & Birthday Bawah RM100
    "hadiah_housewarming": {
        "gaabor-air-fryer-3-5l-smokeless-oil-free",
        "tyeso-vacuum-insulated-tumbler-750ml",
        "baseus-bowie-wm02-earbuds",
        "admore-digital-kitchen-scale-5kg",
        "maxeko-portable-smoothie-blender-cup",
        "montigo-ace-bottle-950ml",
        "portable-electric-usb-juicer-blender-580ml",
    },
    # Niat Starter Pack Rumah Sewa & Asrama
    "starter_pack_rumah_sewa": {
        "tefal-5l-low-sugar-rice-cooker",
        "panasonic-ni-ghd021-handheld-garment-steamer",
        "deerma-dx300-vacuum-cleaner",
        "boldlux-memory-foam-backrest-cushion",
        "tobi-portable-travel-garment-steamer-handheld",
        "gaabor-smokeless-air-fryer-4l",
    },
    # Niat Rutin & Gajet Penampilan Kemas
    "rutin_penampilan_kemas": {
        "xiaomi-showsee-electric-lint-remover",
        "panasonic-ni-ghd021-handheld-garment-steamer",
        "tobi-portable-travel-garment-steamer-handheld",
        "skintific-5x-ceramide-moisture-gel",
        "skintific-symwhite-377-dark-spot-serum-20ml",
    },
    # Persona: Pelajar Asrama & Universiti
    "pelajar_asrama": {
        "khind-rc360-big-rice-cooker-keep-warm",
        "xiaomi-youlg-electric-gooseneck-kettle",
        "pineng-pn951-20000mah-powerbank-built-in-cable",
        "anker-soundcore-r50i-nc-wireless-earbuds",
        "tobi-portable-travel-garment-steamer-handheld",
        "xiaomi-showsee-electric-lint-remover",
        "jisulife-handheld-fan-ultra-2-9000mah",
    },
    # Persona: Keluarga & Anak Kecil
    "keluarga_bayi": {
        "samu-giken-baby-booster-dining-chair-bbc7003",
        "samu-giken-mini-portable-uv-sterilizer-box",
        "xiaomi-smart-air-purifier-4-compact",
        "deerma-cordless-dust-mite-vacuum-cleaner",
        "stainless-steel-304-thermal-insulated-food-jar",
        "omron-blood-pressure-monitor-hem-7120",
        "tp-link-tapo-c120-outdoor-security-camera",
    },
    # Persona: Bujang Sibuk
    "bujang_sibuk": {
        "gaabor-air-fryer-3-5l-smokeless-oil-free",
        "tefal-5l-low-sugar-rice-cooker",
        "maxeko-portable-smoothie-blender-cup",
        "deerma-dx300-vacuum-cleaner",
        "panasonic-ni-ghd021-handheld-garment-steamer",
    },
    # Persona: Kaki Travel & Outstation
    "kaki_travel": {
        "pineng-pn951-20000mah-powerbank-built-in-cable",
        "ugreen-nexode-65w-gan-charger-3port",
        "anker-soundcore-r50i-nc-wireless-earbuds",
        "tyeso-vacuum-insulated-tumbler-750ml",
        "tobi-portable-travel-garment-steamer-handheld",
        "jisulife-handheld-fan-ultra-2-9000mah",
    },
    # Persona: Fitness & Kesihatan
    "fitness_kesihatan": {
        "admore-digital-kitchen-scale-5kg",
        "maxeko-portable-smoothie-blender-cup",
        "xiaomi-smart-band-9-pro-amoled",
        "tyeso-vacuum-insulated-tumbler-750ml",
        "boldlux-memory-foam-backrest-cushion",
    },
    # Persona: Setup Meja Minimalis
    "setup_minimalis": {
        "baseus-i-wok-series-monitor-light-bar",
        "ergonomic-foldable-aluminum-laptop-stand",
        "keychron-q5-max-wireless-mechanical-keyboard",
        "ugreen-10in1-usb-c-transfer-hub-80133",
        "ugreen-wired-keyboard-mouse-combo-mk003",
    },
    # Persona: Bajet Bawah RM50
    "bajet_bawah_rm50": {
        "baseus-bowie-wm02-earbuds",
        "baseus-crystal-shine-100w-fast-charging-cable",
        "tyeso-vacuum-insulated-tumbler-750ml",
        "xiaomi-showsee-electric-lint-remover",
        "cosrx-acne-pimple-master-patch-24pcs",
        "aiken-tea-tree-oil-facial-cleanser-100g",
    },
    # Masalah penampilan lelaki: cukur, bau badan, rambut & kemasan diri
    "grooming_lelaki": {
        "philips-electric-shaver-pro-pq217",
        "dashing-anti-perspirant-roll-on-deodorant-50ml",
        "nivea-men-bright-c-hya-wash-foam-100g",
        "simplus-high-speed-hair-dryer-ionic",
        "dettol-antibacterial-body-wash-berry-cool-950g",
    },
}

# ==============================================================================
# GUARDRAIL AUTOMATIK: Peraturan larangan & kelayakan untuk setiap hab masalah
# ==============================================================================
PROBLEM_GUARDRAIL_RULES = {
    "jeragat_parut": {
        "negative": ["body lotion", "losyen badan", "body serum", "body wash", "sabun mandi", "syampu"],
        "required": ["serum", "niacinamide", "txa", "vitamin c", "symwhite", "arbutin", "brightening", "whitening", "dark spot", "parut", "jeragat", "cleanser", "face wash"]
    },
    "kulit_berminyak": {
        "negative": ["body lotion", "losyen badan", "rambut", "shampoo"],
        "required": ["tea tree", "salicylic", "bha", "aha", "acne", "pimple", "foaming", "low ph", "panthenol", "cleanser", "toner", "patch"]
    },
    "kulit_kering": {
        "negative": ["body lotion", "losyen badan", "rambut", "shampoo"],
        "required": ["ceramide", "hyaluronic", "hyalucera", "snail", "mucin", "lotion", "moisturizer", "moisture", "essence"]
    },
    "diet_sihat": {
        "negative": ["cerek", "kettle", "pencuci", "fan", "kipas"],
        "required": ["rice cooker", "air fryer", "scale", "timbang", "blender", "smoothie", "low sugar"]
    },
    "sakit_pinggang": {
        "negative": ["fan", "kipas", "keyboard", "mouse", "tetikus"],
        "required": ["lumbar", "backrest", "chair", "kerusi", "laptop stand", "footrest", "ergonomic"]
    },
    "bulu_habuk": {
        "negative": ["humidifier", "pelembap udara", "fan", "kipas", "kettle"],
        "required": ["vacuum", "purifier", "lint", "mite", "hama", "hepa", "remover"]
    },
    "kereta_bersih": {
        "negative": ["dashcam", "camera", "recorder", "charger", "pengecas", "bluetooth", "receiver", "kabel"],
        "required": ["vacuum", "organizer", "trash", "holder", "but", "kabin", "kebersihan"]
    },
    "pakaian_kemas": {
        "negative": ["shaver muka", "pencukur janggut", "hair dryer"],
        "required": ["steamer", "lint", "remover", "seterika", "iron"]
    },
    "hadiah_housewarming": {
        "negative": ["serum", "cleanser", "shampoo", "deodorant", "sunscreen", "toner", "pelembap", "cushion", "vacuum", "steamer", "rice cooker", "purifier", "keyboard"],
        "required": ["air fryer", "tumbler", "earbuds", "kitchen scale", "blender", "bottle", "juicer"]
    },
    "starter_pack_rumah_sewa": {
        "negative": ["earbuds", "tws", "dashcam", "holder"],
        "required": ["rice cooker", "steamer", "vacuum", "cushion", "air fryer"]
    },
    "rutin_penampilan_kemas": {
        "negative": ["air fryer", "rice cooker", "vacuum", "purifier", "dashcam"],
        "required": ["steamer", "lint", "remover", "ceramide", "serum", "skincare"]
    },
    "pelajar_asrama": {
        "negative": ["air purifier", "vacuum cleaner", "monitor light", "dashcam"],
        "required": ["rice cooker", "kettle", "powerbank", "earbuds", "steamer", "lint", "fan"]
    },
    "keluarga_bayi": {
        "negative": ["gaming chair", "keyboard", "laptop stand", "dashcam"],
        "required": ["bottle", "sterilizer", "purifier", "vacuum", "food jar", "pressure monitor", "camera", "chair", "booster"]
    },
    "bujang_sibuk": {
        "negative": ["powerbank", "earbuds", "keyboard", "baby"],
        "required": ["air fryer", "rice cooker", "blender", "vacuum", "steamer"]
    },
    "kaki_travel": {
        "negative": ["air purifier", "rice cooker", "monitor light", "keyboard"],
        "required": ["powerbank", "charger", "earbuds", "tumbler", "steamer", "fan"]
    },
    "fitness_kesihatan": {
        "negative": ["charger", "earbuds", "keyboard", "dashcam", "bra", "waistband", "strap", "pants"],
        "required": ["scale", "blender", "smart band", "fitness band", "smartwatch", "tumbler", "cushion", "timbang"]
    },
    "setup_minimalis": {
        "negative": ["air fryer", "rice cooker", "steamer", "serum"],
        "required": ["light bar", "laptop stand", "keyboard", "hub", "mouse"]
    },
    "bajet_bawah_rm50": {
        "negative": ["air fryer", "vacuum cleaner", "monitor light", "mechanical keyboard"],
        "required": ["earbuds", "cable", "tumbler", "lint", "patch", "cleanser"]
    },
    "grooming_lelaki": {
        "negative": ["lip tint", "lipstik", "false nail", "toenail", "kuku", "mascara",
                     "solekan", "tudung", "hijab", "shayla", "body lotion", "losyen badan"],
        "required": ["shaver", "cukur", "deodorant", "roll-on", "bau badan", "face wash",
                     "body wash", "mandian", "hair dryer", "pengering rambut", "grooming"]
    },
}

# Override with dynamic JSON files if present in /data
if os.path.exists(_ASSIGNMENTS_FILE):
    try:
        with open(_ASSIGNMENTS_FILE, "r", encoding="utf-8") as _f:
            PROBLEM_HUB_PRODUCT_IDS = {k: set(v) for k, v in json.load(_f).items()}
    except Exception as _e:
        print(f"⚠️ Warning loading {_ASSIGNMENTS_FILE}: {_e}")

if os.path.exists(_RULES_FILE):
    try:
        with open(_RULES_FILE, "r", encoding="utf-8") as _f:
            PROBLEM_GUARDRAIL_RULES = json.load(_f)
    except Exception as _e:
        print(f"⚠️ Warning loading {_RULES_FILE}: {_e}")

def _kw_match(keyword, text):
    """
    Padanan kata kunci SELAMAT dengan sempadan perkataan (word boundary).
    Menghalang pepijat kritikal seperti 'aha' memadankan 'tahan', atau 'bha' memadankan 'bahan'.
    Kata kunci berbilang perkataan (cth: 'tea tree') dipadankan sebagai frasa penuh.
    """
    kw = keyword.lower().strip()
    if not kw:
        return False
    if " " in kw:
        return kw in text
    # Gunakan sempadan perkataan untuk kata kunci tunggal
    return re.search(r"(?<![a-z0-9])" + re.escape(kw) + r"(?![a-z0-9])", text) is not None


def generate_segment_directory(dist_dir, products, _now):
    """
    ARKITEKTUR ENTERPRISE: Jana 3 Laman Direktori Rasmi
    1. dist/kategori.html - Semua 5 Kategori Pasaran Utama
    2. dist/segmen-pembeli.html - Semua 10 Segmen Pembeli & Gaya Hidup
    3. dist/panduan-keperluan.html - Semua 8 Panduan Keperluan & Solusi
    """
    year = _now.year
    pids_by_spec = {}
    for spec in CATEGORY_LISTICLE_SPECS:
        matched = [p for p in products if spec["match"](p)]
        matched.sort(key=lambda p: (p.get("added_at", ""), p.get("editorial_score", 0)), reverse=True)
        pids_by_spec[spec["slug"]] = (spec, matched)

    def _build_page(filename, title, subtitle, specs_list):
        grid_cards = ""
        for spec in sorted_specs(specs_list):
            spec_obj, matched = pids_by_spec.get(spec["slug"], (spec, []))
            n = len(matched)
            if n == 0:
                continue
            card_h1 = spec["h1"].replace("{n}", str(n)).replace("{year}", str(year))
            blurb = spec["intro"]
            
            # Show top 3 sample product titles inside card with clean truncated bullets
            samples_html = ""
            for sp in matched[:3]:
                clean_name = strict_clean(sp["name"])
                samples_html += f'<li class="truncate text-[11px] text-slate-600 font-medium flex items-center gap-1.5"><span class="w-1.5 h-1.5 rounded-full bg-orange-400 shrink-0"></span><span class="truncate">{clean_name}</span></li>\n'
                
            grid_cards += f'''
            <div class="bg-white rounded-2xl border border-slate-200 p-4 sm:p-5 hover:border-orange-400 hover:shadow-lg transition-all flex flex-col justify-between group">
                <div>
                    <div class="flex items-center gap-3 mb-3">
                        <span class="text-2xl p-2.5 bg-slate-100 rounded-xl shrink-0 group-hover:scale-105 transition-transform">{spec["emoji"]}</span>
                        <div class="min-w-0">
                            <span class="text-xs font-black text-slate-900 block truncate">{spec["title_short"]}</span>
                            <span class="inline-flex items-center text-[10px] font-bold text-orange-700 bg-orange-50 border border-orange-200/60 px-1.5 py-0.5 rounded-md mt-0.5">{n} Pilihan Terpilih</span>
                        </div>
                    </div>
                    <h2 class="text-sm font-extrabold text-slate-900 leading-snug mb-1.5 group-hover:text-orange-600 transition-colors">{card_h1}</h2>
                    <p class="text-xs text-slate-600 mb-3 leading-relaxed line-clamp-2">{blurb}</p>
                    <ul class="space-y-1.5 mb-4 bg-slate-50 p-3 rounded-xl border border-slate-100">
                        {samples_html}
                    </ul>
                </div>
                <a href="{spec['slug']}" class="inline-flex items-center justify-center gap-2 w-full min-h-[44px] py-3 px-4 rounded-xl text-xs font-extrabold text-white bg-slate-900 hover:bg-orange-600 active:scale-[0.98] transition-all text-center shadow-sm">
                    <span>Buka Panduan Penuh ({n})</span>
                    <svg class="w-4 h-4 shrink-0" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2.5" d="M14 5l7 7m0 0l-7 7m7-7H3"></path></svg>
                </a>
            </div>
            '''

        page_html = f'''<!DOCTYPE html>
<html lang="ms">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{title} — iviz Picks Malaysia</title>
    <meta name="description" content="{subtitle}">
    <link rel="canonical" href="https://link.iviztrading.com/{filename}">
    <script src="https://cdn.tailwindcss.com"></script>
    <link href="https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@400;500;600;700;800&display=swap" rel="stylesheet">
    <style>body {{ font-family: 'Plus Jakarta Sans', sans-serif; }}</style>
</head>
<body class="bg-slate-50 text-slate-900 min-h-screen flex flex-col justify-between antialiased">
    <main class="max-w-4xl mx-auto px-4 pt-6 pb-20 md:py-10 w-full">
        <!-- Breadcrumbs -->
        <nav class="flex items-center gap-2 text-xs font-bold text-slate-400 mb-4" aria-label="Breadcrumb">
            <a href="index.html" class="hover:text-slate-900 transition-colors">Utama</a>
            <span>/</span>
            <span class="text-slate-900">{title}</span>
        </nav>
        
        <!-- Header Hero -->
        <div class="mb-6 sm:mb-8 bg-white p-5 sm:p-6 rounded-2xl border border-slate-200 shadow-sm">
            <h1 class="text-xl sm:text-2xl md:text-3xl font-black text-slate-900 tracking-tight">{title}</h1>
            <p class="text-slate-600 text-xs sm:text-sm mt-2 font-medium max-w-2xl leading-relaxed">{subtitle}</p>
        </div>

        <!-- Cards Grid -->
        <div class="grid gap-4 grid-cols-1 sm:grid-cols-2 lg:grid-cols-3">
            {grid_cards}
        </div>
    </main>
</body>
</html>
'''
        with open(os.path.join(dist_dir, filename), "w", encoding="utf-8") as f:
            f.write(page_html)

    # 1. Categories
    cats = [s for s in CATEGORY_LISTICLE_SPECS if not s.get("is_problem") and not s.get("is_intent")]
    _build_page("kategori.html", "Semua Kategori Produk", "Direktori lengkap 5 segmen pasaran teras iviz Picks — Skincare, Gajet, Perkakas Dapur, Rumah Pintar, dan Setup WFH.", cats)

    # 2. Buyer Segments
    intents = [s for s in CATEGORY_LISTICLE_SPECS if s.get("is_intent")]
    _build_page("segmen-pembeli.html", "Segmen Pembeli & Gaya Hidup", "Koleksi panduan mengikut situasi hidup — Pelajar, Keluarga, Kaki Travel, Bujang, Fitness, Hadiah, dan Bajet.", intents)

    # 3. Need Guides
    problems = [s for s in CATEGORY_LISTICLE_SPECS if s.get("is_problem")]
    _build_page("panduan-keperluan.html", "Panduan Mengikut Keperluan", "Senarai ulasan berfokuskan solusi masalah — Jeragat, Kulit Berminyak, Sakit Pinggang, Bulu Kucing, dan Kereta.", problems)

    print(" Generated Enterprise Architecture Directories: dist/kategori.html, dist/segmen-pembeli.html, dist/panduan-keperluan.html")


def validate_problem_hub_guardrails(products):
    """
    Sahkan kesahihan dan integriti produk untuk setiap hab masalah:
    1. Pastikan setiap ID wujud dalam pangkalan data.
    2. Pastikan tiada kata kunci terlarang (Negative Keywords).
    3. Pastikan mengandungi sekurang-kurangnya satu kata kunci penyelesaian (Required Keywords).
    Jika gagal, jana ralat kritikal dan henti proses build!
    """
    pbid = {p["id"]: p for p in products}
    guardrail_errors = []

    for ptype, pids in PROBLEM_HUB_PRODUCT_IDS.items():
        rules = PROBLEM_GUARDRAIL_RULES.get(ptype, {})
        negs = rules.get("negative", [])
        reqs = rules.get("required", [])

        for pid in pids:
            p = pbid.get(pid)
            if not p:
                guardrail_errors.append(f"❌ ID '{pid}' dalam hab '{ptype}' tidak wujud dalam database!")
                continue

            full_text = (p.get("name","") + " " + p.get("category","") + " " + p.get("verdict","") + " " + " ".join(p.get("tags",[]))).lower()

            # Semak negative keywords (word-boundary safe)
            for neg in negs:
                if _kw_match(neg, full_text):
                    guardrail_errors.append(f"❌ Produk '{pid}' dalam hab '{ptype}' dilarang kerana mengandungi kata kunci '{neg}'!")

            # Semak required keywords (word-boundary safe)
            if reqs and not any(_kw_match(req, full_text) for req in reqs):
                guardrail_errors.append(f"❌ Produk '{pid}' dalam hab '{ptype}' tidak mengandungi kata kunci solusi yang sah {reqs}!")

    if guardrail_errors:
        print("\n" + "="*80)
        print("🚨 CRITICAL GUARDRAIL ERROR: KESILAPAN PADANAN PRODUK MASALAH DIKESAN!")
        print("="*80)
        for err in guardrail_errors:
            print("  " + err)
        print("="*80 + "\n")
        raise ValueError("Build dibatalkan automatik kerana terdapat produk yang tidak menyelesaikan masalah sebenar.")

    print(f"  🛡️  Guardrail Integriti Masalah: LULUS 100% (Semua produk disahkan relevan).")

def validate_product_page_fields(products):
    """
    Guardrail kualiti page produk: setiap produk AKTIF mesti ada
    - 'specs'         : dict label->nilai (Spesifikasi & Semakan Pihak Ketiga)
    - 'who_should_skip': ayat spesifik (Pertimbangkan Semula Jika)
    Tanpa kedua-dua field ini, page produk hanya menunjukkan ringkasan generik.
    """
    missing = []
    for p in products:
        if p.get("status") != "active":
            continue
        if not isinstance(p.get("specs"), dict) or not p.get("specs"):
            missing.append((p["id"], "specs"))
        elif not str(p.get("who_should_skip", "")).strip() or str(p.get("who_should_skip", "")).strip() == "Tiada.":
            missing.append((p["id"], "who_should_skip"))
    if missing:
        for pid, field in missing:
            print(f"  ❌ Produk '{pid}' tiada field '{field}' — page produk akan generik!")
        raise ValueError(
            f"Build dibatalkan: {len(missing)} produk aktif tanpa field kualiti "
            f"(specs / who_should_skip). Sila isi sebelum deploy."
        )
    print(f"  🛡️  Guardrail Kualiti Page Produk: LULUS (semua ada specs + who_should_skip).")

def get_outbound_url(p):
    """
    Dapatkan URL destinasi keluar untuk butang CTA:
    1. Utamakan affiliate_url (deeplink Involve Asia) jika ada.
    2. Fallback WAJIB ke matched_real_link / shopee_url (link produk Shopee sebenar).
    DILARANG pulangkan string kosong atau '#' — itu punca butang 'flickering'
    dan tidak menghala ke mana-mana.
    """
    url = (p.get("affiliate_url") or "").strip()
    if url and url != "#":
        return url
    fallback = (p.get("matched_real_link") or p.get("shopee_url") or "").strip()
    if fallback and fallback != "#":
        return fallback
    return "https://shopee.com.my/"

def classify_category(p):
    # NOTA: guna name + category + group_slug SAHAJA (bukan label group — label
    # "Rumah & Dapur" pernah mengkontaminasi keyword dapur, menarik vacuum masuk)
    text = (p.get("name","") + " " + p.get("category","") + " " + (p.get("group_slug") or "")).lower()
    if any(k in text for k in ["grooming","shaver","cukur","deodorant","roll-on","pomade","hair gel","styling spray","body cologne","dashing","gatsby","gillette"]) and not any(x in text for x in ["garment steamer","food steamer"]):
        return "grooming"

    # 2. Setup WFH
    if any(k in text for k in ["kerusi","keyboard","papan kekunci","light bar","ergonom","gaming chair","laptop stand","lumbar","backrest","mouse pad","tetikus","kvm"]):
        return "setup_wfh"

    # 3. Perkakas Dapur (alat memasak/penyediaan makanan)
    dapur_kw = ["air fryer","rice cooker","periuk","pressure cooker","blender","chopper","pengisar","food processor","dapur","kuali","pengukus makanan","food steamer","kettle","cerek","hotpot","oven thermometer","timbangan dapur","penimbang","coffee grinder","lunch box","pemanas makanan","vacuum sealer","perkakas dapur"]
    if any(k in text for k in dapur_kw) and not any(x in text for x in ["garment steamer","steamer pakaian"]):
        return "dapur"

    # 4. Gajet & Elektronik
    gajet_kw = ["earbuds","earphone","tws","fon telinga","powerbank","charger","pengecas","kabel","cable","dashcam","dash cam","smartwatch","smart band","jam tangan","bluetooth","usb-c","audio receiver","otg","san disk","flash drive","router","penghala","wifi","hdmi","jisulife","fan ultra"]
    if any(k in text for k in gajet_kw):
        return "gajet"

    # 5. Rumah Pintar & Pembersihan (kebersihan/udara/keselamatan rumah + alatan pakaian)
    rumah_kw = ["vacuum","vakum","purifier","penapis udara","humidifier","smart led","lampu pintar","motion sensor","night light","uv sterilizer","disinfectant","stand fan","kipas industri","kamera keselamatan","tapo","garment steamer","lint remover","seterika","pembersih","kediaman"]
    if any(k in text for k in rumah_kw):
        return "rumah_pintar"

    # 6. Skincare & Kesihatan Diri (kulit muka/badan sahaja — bukan solekan/rambut)
    skin_kw = ["serum","sunscreen","sunblock","cleanser","toner","moisturizer","skincare","ceramide","retinol","pelembap","face wash","facial","pimple","dark spot","parut","whitening","brightening","teeth gel","pemutih gigi","lotion","losyen","body wash","mandian","eye mask","stretch marks","bio-oil","snail mucin","micellar","jerawat","jeragat","kulit"]
    if any(k in text for k in skin_kw):
        return "skincare"

    # 7. Khas: solekan & rambut (tiada hub kategori sendiri — biar di situ sahaja)
    if any(k in text for k in ["solekan","bibir","lip tint","water tint","rambut","shampoo","syampu"]):
        return "kecantikan"

    cat_orig = p.get("category","").lower()
    if "dapur" in cat_orig: return "dapur"
    if "gajet" in cat_orig or "audio" in cat_orig: return "gajet"
    if "skincare" in cat_orig or "kulit" in cat_orig: return "skincare"
    if "wfh" in cat_orig or "meja" in cat_orig: return "setup_wfh"
    return "lain_lain"

def generate_category_listicles(dist_dir, products):
    import datetime as _dt
    _now = _dt.datetime.now()
    year = _now.year
    generated_slugs = []

    # ENFORCE CRITICAL GUARDRAIL: Sahkan integriti produk masalah secara automatik
    validate_problem_hub_guardrails(products)
    # ENFORCE QUALITY GUARDRAIL: setiap produk aktif mesti ada specs + who_should_skip
    validate_product_page_fields(products)

    for spec in CATEGORY_LISTICLE_SPECS:
        matched = [p for p in products if spec["match"](p)]
        # SORT: Produk terbaru di atas dalam setiap listicle
        matched.sort(key=lambda p: (p.get("added_at", ""), p.get("editorial_score", 0)), reverse=True)
        n = len(matched)
        if n == 0:
            continue

        slug = spec["slug"]
        generated_slugs.append(slug)
        title = spec["meta_title"].format(n=n, year=year)
        desc = spec["meta_desc"].format(n=n, year=year)
        h1 = spec["h1"].format(n=n, year=year)

        # Build items schema
        item_schema_list = []
        for idx, p in enumerate(matched, start=1):
            item_schema_list.append({
                "@type": "ListItem",
                "position": idx,
                "name": p["name"],
                "url": f"https://link.iviztrading.com/{p['id']}.html"
            })

        list_json_ld = {
            "@context": "https://schema.org",
            "@type": "ItemList",
            "name": h1,
            "description": desc,
            "numberOfItems": n,
            "itemListElement": item_schema_list
        }

        # Build cards HTML
        items_html = ""
        for idx, p in enumerate(matched, start=1):
            status_badge = '<span class="bg-slate-200 text-slate-600 px-2 py-0.5 rounded text-[10px] font-bold">STOK HABIS</span>' if p.get('status') == 'out_of_stock' else ''
            items_html += f"""
            <article class="bg-white rounded-2xl border border-slate-200 p-5 md:p-6 shadow-sm hover:shadow-md transition-all group">
                <div class="flex items-start gap-4 md:gap-6">
                    <div class="flex flex-col items-center justify-center shrink-0">
                        <span class="w-8 h-8 rounded-full bg-slate-900 text-white font-extrabold text-xs flex items-center justify-center shadow-sm">#{idx}</span>
                    </div>
                    <div class="w-20 h-20 md:w-24 md:h-24 bg-slate-100 border border-slate-200 rounded-xl shrink-0 overflow-hidden p-1 flex items-center justify-center relative">
                        <img src="{p.get('image_url', '')}" alt="{p['name']}" class="w-full h-full object-contain rounded-lg group-hover:scale-105 transition-transform duration-300" loading="lazy" />
                        <div class="absolute inset-0 flex items-center justify-center">{status_badge}</div>
                    </div>
                    <div class="flex-grow min-w-0">
                        <div class="flex flex-wrap items-center gap-2 mb-2">
                            <span class="text-xs font-bold text-orange-700 bg-orange-50 border border-orange-200/80 px-2.5 py-0.5 rounded-md">{p['category']}</span>
                            <span class="text-xs text-slate-500 font-semibold">{p['brand']}</span>
                            <span class="text-xs font-bold text-amber-600 ml-auto">⭐ {p.get('editorial_score', '9.0')}/10</span>
                        </div>
                        <h2 class="text-base md:text-lg font-extrabold text-slate-900 group-hover:text-orange-600 transition-colors leading-snug">
                            <a href="{p['id']}.html">{p['name']}</a>
                        </h2>
                        <p class="text-xs md:text-sm text-slate-600 mt-2 line-clamp-2 leading-relaxed">
                            "{p.get('verdict', p.get('hook', ''))}"
                        </p>
                        <div class="mt-4 pt-3.5 border-t border-slate-100 flex flex-col sm:flex-row sm:items-center sm:justify-between gap-3">
                            <div class="flex items-baseline gap-2">
                                <span class="text-xs text-slate-400">Harga:</span>
                                <span class="text-lg md:text-xl font-black text-slate-900">{p['shopee_price']}</span>
                                <span class="text-xs text-slate-400 line-through">{p.get('original_price', '')}</span>
                            </div>
                            <div class="grid grid-cols-2 sm:flex sm:items-center gap-2 w-full sm:w-auto">
                                <a href="{p['id']}.html" class="inline-flex items-center justify-center gap-1 text-xs font-bold text-slate-700 hover:text-slate-900 bg-slate-100 hover:bg-slate-200 py-2.5 px-3 rounded-xl transition-colors min-h-[42px] text-center">
                                    <span>Baca Ulasan</span>
                                </a>
                                <a href="{get_outbound_url(p)}" target="_blank" rel="nofollow noopener sponsored" class="inline-flex items-center justify-center gap-2 text-sm font-bold text-white bg-orange-600 hover:bg-orange-700 py-3 px-6 rounded-lg shadow-md hover:shadow-lg transition-all duration-200 min-h-[48px] w-full sm:w-auto text-center">
                                    <span>Lihat Tawaran di Shopee</span>
                                    <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M10 6H6a2 2 0 00-2 2v10a2 2 0 002 2h10a2 2 0 002-2v-4M14 4h6m0 0v6m0-6L10 14"></path></svg>
                                </a>
                            </div>
                        </div>
                    </div>
                </div>
            </article>
            """

        # Other category quick links
        other_cats = ""
        for ospec in sorted_specs():
            is_cur = ospec["slug"] == slug
            cur_cls = "bg-orange-500 text-white font-extrabold shadow-sm" if is_cur else "bg-white hover:bg-slate-50 text-slate-700 border border-slate-200 font-bold"
            other_cats += f'<a href="{ospec["slug"]}" class="px-4 py-2 rounded-xl text-xs whitespace-nowrap transition-colors {cur_cls}">{ospec["emoji"]} {ospec["title_short"]}</a>\n'

        cat_page_html = f"""<!DOCTYPE html>
<html lang="ms" class="scroll-smooth">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{title}</title>
    <meta name="description" content="{desc}">
    <link rel="canonical" href="https://link.iviztrading.com/{slug}">
    
    <!-- OpenGraph / Social Meta -->
    <meta property="og:type" content="website">
    <meta property="og:title" content="{title}">
    <meta property="og:description" content="{desc}">
    <meta property="og:url" content="https://link.iviztrading.com/{slug}">
    <meta property="og:site_name" content="iviz Picks">
    <meta property="og:image" content="https://link.iviztrading.com/og-preview.png">
    <meta property="og:image:width" content="1200">
    <meta property="og:image:height" content="630">
    <meta name="twitter:card" content="summary_large_image">
    <meta name="twitter:title" content="{title}">
    <meta name="twitter:description" content="{desc}">
    <meta name="twitter:image" content="https://link.iviztrading.com/og-preview.png">

    <script src="https://cdn.tailwindcss.com"></script>
    <link href="https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@400;500;600;700;800&display=swap" rel="stylesheet">
    <style>body {{ font-family: 'Plus Jakarta Sans', sans-serif; }}</style>

    <!-- Schema.org ItemList (AEO / Search Citation) -->
    <script type="application/ld+json">
    {json.dumps(list_json_ld, ensure_ascii=False, indent=2)}
    </script>
</head>
<body class="bg-slate-50 text-slate-900 antialiased min-h-screen flex flex-col justify-between selection:bg-orange-500 selection:text-white">

    <main class="max-w-3xl mx-auto px-4 py-6 md:py-10 w-full flex-1">
        <!-- Breadcrumb -->
        <nav class="flex items-center gap-2 text-xs text-slate-500 mb-6" aria-label="Breadcrumb">
            <a href="index.html" class="hover:text-orange-600 font-medium transition-colors">Utama</a>
            <span>/</span>
            <span class="text-slate-900 font-semibold">{spec['title_short']}</span>
        </nav>

        <!-- Header -->
        <div class="mb-8">
            <div class="inline-flex items-center gap-2 bg-orange-50 border border-orange-200 text-orange-700 text-xs font-extrabold px-3 py-1 rounded-full uppercase tracking-wider mb-3">
                <span>{spec['emoji']} Panduan Listicle {year}</span>
            </div>
            <h1 class="text-2xl md:text-3xl lg:text-4xl font-extrabold text-slate-900 tracking-tight leading-tight">
                {h1}
            </h1>
            <p class="text-slate-600 text-sm md:text-base mt-3 leading-relaxed">
                {spec['intro']}
            </p>
        </div>

        <!-- Category Pills Filter Bar -->
        <div class="flex items-center gap-2 overflow-x-auto pb-3 mb-8 no-scrollbar">
            <a href="index.html" class="px-4 py-2 rounded-xl text-xs whitespace-nowrap bg-white hover:bg-slate-50 text-slate-700 border border-slate-200 font-bold transition-colors">🏷️ Semua Produk</a>
            {other_cats}
        </div>

        <!-- Products Listicle Grid -->
        <div class="space-y-4 mb-10">
            {items_html}
        </div>

        <!-- Transparency & Affiliate Disclaimer -->
        <div class="bg-white border border-slate-200 rounded-2xl p-5 text-xs text-slate-500 leading-relaxed shadow-sm">
            <strong class="text-slate-800 block mb-1">Ketelusan Editorial & Pematuhan Afiliasi:</strong>
            iviz Picks adalah saluran ulasan bebas. Pautan luar di atas menghala terus ke stor rasmi jenama di platform e-dagang (Shopee/Lazada). Kami mungkin menerima komisen kecil tanpa sebarang kos tambahan kepada anda sekiranya anda membuat pembelian melalui pautan ini. Kedudukan produk dinilai berdasarkan kepuasan pembeli, spesifikasi rasmi dan harga pasaran sebenar.
        </div>
    </main>

</body>
</html>"""

        with open(os.path.join(dist_dir, slug), "w", encoding="utf-8") as f:
            f.write(cat_page_html)
        print(f" Generated Listicle Hub: dist/{slug} ({n} produk)")

    return generated_slugs

def generate_production_microsites():
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    data_path = os.path.join(base_dir, "data", "trending_products.json")
    dist_dir = os.path.join(base_dir, "dist")
    os.makedirs(dist_dir, exist_ok=True)

    # Salin halaman statik trust (about, editorial-policy, privacy-policy, contact)
    # daripada /static ke /dist supaya tidak hilang semasa rebuild.
    static_dir = os.path.join(base_dir, "static")
    if os.path.isdir(static_dir):
        import shutil
        copied = 0
        for fn in os.listdir(static_dir):
            if fn.endswith(".html"):
                shutil.copy2(os.path.join(static_dir, fn), os.path.join(dist_dir, fn))
                copied += 1
        if copied:
            print(f" Copied {copied} static trust pages from /static to /dist.")

    with open(data_path, "r", encoding="utf-8") as f:
        products = json.load(f)

    # SORT: Produk terbaru (added_at) di atas terlebih dahulu
    products.sort(key=lambda p: (p.get("added_at", ""), p.get("editorial_score", 0)), reverse=True)

    print(f"Loaded {len(products)} production products.")

    # GUARDRAIL: Buang fail HTML orphan (microsite produk yang telah dipadam dari
    # katalog) supaya tiada halaman basi (harga/tajuk lama) kekal dalam dist/.
    # Halaman bukan-produk (index, direktori, listicle hub, trust) dijana semula
    # setiap build, jadi kita senaraikan nama sahnya dan hanya buang selebihnya.
    _valid_html = {p["id"] + ".html" for p in products}
    _non_product_html = {
        "index.html", "kategori.html", "segmen-pembeli.html", "panduan-keperluan.html",
        "about.html", "editorial-policy.html", "privacy-policy.html", "contact.html",
        "404.html", "offline.html", "sitemap.html",
    }
    try:
        for _spec in CATEGORY_LISTICLE_SPECS:
            _slug = _spec.get("slug", "")
            if _slug:
                _non_product_html.add(_slug if _slug.endswith(".html") else _slug + ".html")
    except NameError:
        pass
    for _prob in ("PROBLEM_HUB_PRODUCT_IDS",):
        pass
    _orphans = 0
    for _fn in os.listdir(dist_dir):
        if not _fn.endswith(".html"):
            continue
        if _fn in _valid_html or _fn in _non_product_html:
            continue
        try:
            os.remove(os.path.join(dist_dir, _fn))
            _orphans += 1
        except Exception:
            pass
    if _orphans:
        print(f" Removed {_orphans} orphan product pages.")

    # Dynamic date (Bahasa Melayu) & schema validity
    import datetime as _dt
    _month_ms = {
        1: "Januari", 2: "Februari", 3: "Mac", 4: "April", 5: "Mei", 6: "Jun",
        7: "Julai", 8: "Ogos", 9: "September", 10: "Oktober", 11: "November", 12: "Disember",
    }
    _now = _dt.datetime.now()
    last_updated = f"{_month_ms[_now.month]} {_now.year}"
    price_valid_until = f"{_now.year + 1}-12-31"

    for prod in products:
        # Pros
        pros_html = ""
        for p in prod.get("pros", []):
            pros_html += f"""
                <li class="flex items-start gap-2.5 text-slate-800">
                    <span class="text-emerald-600 font-bold mt-0.5 shrink-0">✓</span>
                    <span class="leading-relaxed font-medium">{p}</span>
                </li>
            """

        # Cons
        cons_html = ""
        for c in prod.get("cons", []):
            cons_html += f"""
                <li class="flex items-start gap-2.5 text-slate-800">
                    <span class="text-amber-600 font-bold mt-0.5 shrink-0">!</span>
                    <span class="leading-relaxed font-medium">{c}</span>
                </li>
            """

        # Specs
        specs_html = ""
        for label, val in prod.get("specs", {}).items():
            specs_html += f"""
                <div class="py-3 flex flex-col sm:flex-row sm:justify-between gap-1 sm:gap-4">
                    <span class="font-medium text-slate-500 text-xs sm:text-sm">{label}</span>
                    <span class="text-slate-900 font-semibold text-xs sm:text-sm sm:text-right">{val}</span>
                </div>
            """
        # Baris Semakan Pihak Ketiga — automatik jika specs belum ada
        _AUDIT_KEYS = ("semakan", "kkm", "sirim", "npra", "keselamatan",
                       "pensijilan", "persijilan", "piawaian")
        _has_audit = any(any(w in lbl.lower() for w in _AUDIT_KEYS)
                         for lbl in prod.get("specs", {}))
        if not _has_audit and prod.get("safety_audit"):
            specs_html += f"""
                <div class="py-3 flex flex-col sm:flex-row sm:justify-between gap-1 sm:gap-4">
                    <span class="font-medium text-slate-500 text-xs sm:text-sm">Semakan Keselamatan</span>
                    <span class="text-slate-900 font-semibold text-xs sm:text-sm sm:text-right">{prod['safety_audit']}</span>
                </div>
            """

        # FAQ & FAQ Schema
        faq_html = ""
        faq_schema_list = []
        for item in prod.get("faq", []):
            faq_html += f"""
                <div class="border border-slate-200/80 rounded-xl p-4 bg-slate-50/70">
                    <h3 class="font-bold text-slate-900 text-sm mb-1.5 flex items-center gap-2">
                        <span class="text-orange-500">Q:</span> {item['q']}
                    </h3>
                    <p class="text-slate-600 text-xs leading-relaxed pl-5 font-medium">{item['a']}</p>
                </div>
            """
            faq_schema_list.append(json.dumps({
                "@type": "Question",
                "name": item["q"],
                "acceptedAnswer": {
                    "@type": "Answer",
                    "text": item["a"]
                }
            }, ensure_ascii=False))

        faq_schema_items = ",\n        ".join(faq_schema_list)


        # Dynamic verification badge
        platform = prod.get("merchant_platform", "").lower()
        if "mall" in platform or "official" in platform:
            badge_text = "Disahkan Rasmi"
            badge_color = "bg-emerald-50 text-emerald-700 border-emerald-200"
            dot_color = "bg-emerald-500"
        else:
            badge_text = "Penjual Pilihan"
            badge_color = "bg-blue-50 text-blue-700 border-blue-200"
            dot_color = "bg-blue-500"
            
        badge_html = f'''<span class="{badge_color} text-xs px-2.5 py-1 rounded-md border font-bold flex items-center gap-1">
                    <span class="w-1.5 h-1.5 rounded-full {dot_color} animate-pulse"></span> {badge_text}
                </span>'''
                
        # Dynamic trust badges (based on merchant platform / seller type)
        platform_raw = prod.get("merchant_platform", "")
        platform_lc = platform_raw.lower()
        if "mall" in platform_lc or "official" in platform_lc or "flagship" in platform_lc or "watsons" in platform_lc:
            trust_badges_html = (
                '<span class="bg-emerald-50 border border-emerald-200 px-2 py-0.5 rounded text-emerald-800">🛡️ Jaminan 100% Original</span>'
                '<span class="bg-slate-100 border border-slate-200 px-2 py-0.5 rounded text-slate-700">🚚 Penghantaran Pantas</span>'
                '<span class="bg-orange-50 border border-orange-200 px-2 py-0.5 rounded text-orange-800">✅ Shopee Mall</span>'
            )
        elif "global" in platform_lc:
            trust_badges_html = (
                '<span class="bg-blue-50 border border-blue-200 px-2 py-0.5 rounded text-blue-800">🌏 Penghantaran Antarabangsa</span>'
                '<span class="bg-slate-100 border border-slate-200 px-2 py-0.5 rounded text-slate-700">🛡️ Jaminan Ketulenan Global</span>'
            )
        else:
            trust_badges_html = (
                '<span class="bg-slate-100 border border-slate-200 px-2 py-0.5 rounded text-slate-700">🚚 Penghantaran Pantas</span>'
                '<span class="bg-slate-100 border border-slate-200 px-2 py-0.5 rounded text-slate-700">🏪 Penjual Pilihan</span>'
            )

        # Replace placeholders
        page = TEMPLATE_HTML
        page = page.replace("{{verification_badge}}", badge_html)
        page = page.replace("{{trust_badges}}", trust_badges_html)
        page = page.replace("{{id}}", prod["id"])
        page = page.replace("{{name}}", prod["name"])
        page = page.replace("{{brand}}", prod.get("brand", "Jenama Sah"))
        _grp = prod.get("group", "Kesihatan & Penjagaan Diri")
        if "_" in _grp:  # guard: slug tak sepatutnya terpapar
            _grp = _grp.replace("_", " ").title()
        page = page.replace("{{group}}", _grp)
        page = page.replace("{{category}}", prod["category"])
        page = page.replace("{{verdict}}", prod.get("verdict", prod["hook"]))
        page = page.replace("{{hook}}", prod.get("hook", prod.get("verdict", "")))
        page = page.replace("{{who_is_it_for}}", prod.get("who_is_it_for", "Semua pembeli."))
        page = page.replace("{{who_should_skip}}", prod.get("who_should_skip", "Tiada."))
        page = page.replace("{{shopee_price}}", str(prod.get("shopee_price", "RM 0.00")))
        page = page.replace("{{price_num}}", str(prod.get("price_num", "0.00")))
        page = page.replace("{{original_price}}", str(prod.get("original_price", "")))
        page = page.replace("{{discount}}", str(prod.get("discount", "")))
        page = page.replace("{{affiliate_url}}", get_outbound_url(prod))
        page = page.replace("{{merchant_platform}}", prod.get("merchant_platform", "Shopee Mall"))
        page = page.replace("{{image_url}}", prod.get("image_url", ""))
        page = page.replace("{{editorial_score}}", str(prod.get("editorial_score", "9.0")))
        page = page.replace("{{rating_val}}", str(prod.get("schema", {}).get("rating", "4.8")))
        availability_schema = "https://schema.org/OutOfStock" if prod.get("status") == "out_of_stock" else "https://schema.org/InStock"
        page = page.replace("{{schema_availability}}", availability_schema)
        page = page.replace("{{price_valid_until}}", price_valid_until)
        page = page.replace("{{last_updated}}", last_updated)
        page = page.replace("{{pros_html}}", pros_html)
        page = page.replace("{{cons_html}}", cons_html)
        page = page.replace("{{specs_html}}", specs_html)
        page = page.replace("{{faq_html}}", faq_html)
        page = page.replace("{{faq_schema_items}}", faq_schema_items)
        import urllib.parse
        share_title_enc = urllib.parse.quote(f"{prod['name']} - Ulasan iviz Picks")
        page = page.replace("{{share_title_encoded}}", share_title_enc)

        filename = f"{prod['id']}.html"
        file_path = os.path.join(dist_dir, filename)

        with open(file_path, "w", encoding="utf-8") as f:
            f.write(page)

        print(f" Generated: {file_path}")

    # Build unique groups dynamically for tabs
    group_counts = {}
    group_names = {}
    for p in products:
        slug = p.get("group_slug", "health-care")
        group_counts[slug] = group_counts.get(slug, 0) + 1
        _gn = p.get("group", slug.title())
        if "_" in _gn:
            _gn = _gn.replace("_", " ").title()
        group_names[slug] = _gn

    tab_buttons_html = f'''<button onclick="filterGroup('all', this)" class="tab-btn active px-4 py-2 rounded-xl text-xs font-bold transition-all shrink-0">Semua ({len(products)})</button>'''
    for slug, count in group_counts.items():
        tab_buttons_html += f'''\n            <button onclick="filterGroup('{slug}', this)" class="tab-btn px-4 py-2 rounded-xl text-xs font-bold transition-all shrink-0">{group_names[slug]} ({count})</button>'''

    # ==========================================================================
    # HYBRID LAYOUT:
    # 1. Categories as Icon Pills
    # 2. Buying Psychology & Life-Stage Hubs (Intent Guides)
    # 3. Problem & Solution Hubs (Technical Fixes)
    # ==========================================================================
    cat_pills_html = ""
    intent_cards_html = ""
    problem_cards_html = ""

    for spec in sorted_specs():
        hcount = sum(1 for p in products if spec["match"](p))
        if hcount == 0:
            continue

        if not spec.get("is_problem") and not spec.get("is_intent"):
            # Vertical Icon Card for Horizontal Scroll (2-line label, no truncation)
            cat_pills_html += f'''\n                <a href="{spec['slug']}" class="flex flex-col items-center justify-start gap-2 p-3 pt-3.5 bg-white hover:bg-orange-50/50 border border-slate-200 hover:border-orange-400 rounded-2xl w-[6.5rem] h-[7.25rem] shrink-0 transition-all shadow-xs group text-center">
                    <span class="text-2xl leading-none p-1.5 bg-slate-50 group-hover:bg-orange-100/60 rounded-xl transition-colors">{spec['emoji']}</span>
                    <span class="text-[11px] font-extrabold text-slate-800 group-hover:text-orange-600 leading-[1.15] line-clamp-2 break-words w-full">{spec['title_short']}</span>
                </a>'''
        elif spec.get("is_intent"):
            # Buying Psychology / Life Stage Guide Cards (Human-friendly labels)
            blurb = spec["intro"]
            if len(blurb) > 135:
                blurb = blurb[:132].rsplit(" ", 1)[0] + "..."
            card_h1 = spec["h1"].replace("{n}", str(hcount)).replace("{year}", str(_now.year))
            intent_cards_html += f'''\n            <a href="{spec['slug']}" class="group bg-gradient-to-br from-white to-amber-50/30 p-5 rounded-2xl border border-amber-200/70 hover:border-amber-400 hover:shadow-lg transition-all flex flex-col justify-between">
                <div>
                    <div class="flex items-center gap-2 mb-2.5">
                        <span class="text-xl p-1.5 bg-amber-100/70 rounded-lg shrink-0">{spec['emoji']}</span>
                        <span class="text-[10px] font-black text-amber-800 bg-amber-100/80 border border-amber-300/70 px-2 py-0.5 rounded uppercase tracking-wide">Idea & Keperluan</span>
                    </div>
                    <h3 class="font-extrabold text-slate-900 text-sm group-hover:text-amber-600 transition-colors leading-snug">{card_h1}</h3>
                    <p class="text-xs text-slate-500 mt-2 leading-relaxed">{blurb}</p>
                </div>
                <div class="mt-4 pt-3 border-t border-amber-100 flex items-center justify-between text-xs font-bold text-slate-400 group-hover:text-amber-600 transition-colors">
                    <span>{hcount} Koleksi Idea</span>
                    <span class="flex items-center gap-1">Lihat Pilihan
                        <svg class="w-3.5 h-3.5 group-hover:translate-x-0.5 transition-transform" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2.5" d="M14 5l7 7m0 0l-7 7m7-7H3"></path></svg>
                    </span>
                </div>
            </a>'''
        else:
            # Option A: Editorial Guide Cards (ALL problems)
            blurb = spec["intro"]
            if len(blurb) > 135:
                blurb = blurb[:132].rsplit(" ", 1)[0] + "..."
            card_h1 = spec["h1"].replace("{n}", str(hcount)).replace("{year}", str(_now.year))
            problem_cards_html += f'''\n            <a href="{spec['slug']}" class="group bg-white p-5 rounded-2xl border border-slate-200 hover:border-orange-400 hover:shadow-lg transition-all flex flex-col justify-between">
                <div>
                    <div class="flex items-center gap-2 mb-2.5">
                        <span class="text-xl p-1.5 bg-orange-50 rounded-lg shrink-0">{spec['emoji']}</span>
                        <span class="text-[10px] font-black text-orange-700 bg-orange-50 border border-orange-200/70 px-2 py-0.5 rounded uppercase tracking-wide">Panduan Beli</span>
                    </div>
                    <h3 class="font-extrabold text-slate-900 text-sm group-hover:text-orange-600 transition-colors leading-snug">{card_h1}</h3>
                    <p class="text-xs text-slate-500 mt-2 leading-relaxed">{blurb}</p>
                </div>
                <div class="mt-4 pt-3 border-t border-slate-100 flex items-center justify-between text-xs font-bold text-slate-400 group-hover:text-orange-600 transition-colors">
                    <span>{hcount} Produk Ulasan</span>
                    <span class="flex items-center gap-1">Baca Panduan
                        <svg class="w-3.5 h-3.5 group-hover:translate-x-0.5 transition-transform" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2.5" d="M14 5l7 7m0 0l-7 7m7-7H3"></path></svg>
                    </span>
                </div>
            </a>'''

    # ------------------------------------------------------------------
    # ENTERPRISE IA: Featured (terhad) di homepage + direktori penuh
    # ------------------------------------------------------------------
    def _featured(cards_html, limit):
        # Bahagikan dengan tag pembuka <a href, tapi simpan tag tersebut
        parts = re.split(r'(?=<a href)', cards_html)
        # Ambil bahagian yang bermula dengan <a href
        cards = [p for p in parts if p.strip().startswith("<a href")]
        trimmed = cards[:limit]
        return "".join(trimmed)

    intent_cards_html_featured = _featured(intent_cards_html, 3)
    problem_cards_html_featured = _featured(problem_cards_html, 3)

    # Direktori segmen (arketktur hub-and-spoke standard enterprise)
    generate_segment_directory(dist_dir, products, _now)

    # Rebuild Index Hub
    index_html = f"""<!DOCTYPE html>
<html lang="ms">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>iviz Picks — Panduan Ulasan & Pilihan Produk Terbaik Malaysia</title>
    <meta name="description" content="Panduan ulasan editorial bebas produk trending di pasaran Malaysia. Dilengkapi semakan pendaftaran NPRA KKM, SIRIM, dan pensijilan keselamatan.">
    <!-- OpenGraph / Social Meta -->
    <meta property="og:type" content="website">
    <meta property="og:title" content="iviz Picks — Panduan Ulasan & Pilihan Produk Terbaik Malaysia">
    <meta property="og:description" content="Panduan ulasan editorial bebas produk trending di pasaran Malaysia. Dilengkapi semakan pendaftaran NPRA KKM, SIRIM, dan pensijilan keselamatan.">
    <meta property="og:url" content="https://link.iviztrading.com/">
    <meta property="og:site_name" content="iviz Picks">
    <meta property="og:image" content="https://link.iviztrading.com/og-preview.png">
    <meta property="og:image:width" content="1200">
    <meta property="og:image:height" content="630">
    <meta name="twitter:card" content="summary_large_image">
    <meta name="twitter:title" content="iviz Picks — Panduan Ulasan & Pilihan Produk Terbaik Malaysia">
    <meta name="twitter:description" content="Panduan ulasan editorial bebas produk trending di pasaran Malaysia. Dilengkapi semakan keselamatan NPRA & SIRIM.">
    <meta name="twitter:image" content="https://link.iviztrading.com/og-preview.png">
    <script src="https://cdn.tailwindcss.com"></script>
    <link href="https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@400;500;600;700;800&display=swap" rel="stylesheet">
    <style>
        body {{ font-family: 'Plus Jakarta Sans', sans-serif; }}
        .tab-btn.active {{ background: linear-gradient(135deg, #f97316 0%, #f59e0b 100%); color: #ffffff; font-weight: 800; box-shadow: 0 4px 14px rgba(249, 115, 22, 0.3); }}
        .tab-btn {{ background-color: #ffffff; color: #475569; border: 1px solid #e2e8f0; }}
        .tab-btn:hover:not(.active) {{ color: #0f172a; border-color: #cbd5e1; background-color: #f8fafc; }}
        .product-card.hidden {{ display: none !important; }}
    </style>
</head>
<body class="bg-slate-50 text-slate-900 min-h-screen flex flex-col justify-between antialiased selection:bg-orange-500 selection:text-white">
        <!-- Top Navigation Header -->
    <header class="bg-white/90 backdrop-blur-md border-b border-slate-200 sticky top-0 z-50 shadow-sm">
        <div class="max-w-4xl mx-auto px-4 py-3.5 flex items-center justify-between">
            <a href="index.html" class="flex items-center gap-2.5 font-extrabold text-lg text-slate-900 tracking-tight hover:opacity-80 transition-opacity">
                <span class="bg-gradient-to-tr from-orange-500 to-amber-400 text-white w-7 h-7 rounded-lg flex items-center justify-center font-black text-sm shadow-md shadow-orange-500/20">i</span>
                <span>iviz <span class="text-orange-500 font-bold">Picks</span></span>
            </a>
            <div class="hidden md:flex items-center gap-5 text-xs font-bold text-slate-600">
                <a href="index.html" class="hover:text-slate-900 transition-colors">Pilihan Utama</a>
                <a href="about.html" class="hover:text-slate-900 transition-colors">Mengenai Kami</a>
                <a href="editorial-policy.html" class="hover:text-slate-900 transition-colors">Polisi Semakan</a>
                <a href="privacy-policy.html" class="hover:text-slate-900 transition-colors">Privasi</a>
                <a href="contact.html" class="hover:text-slate-900 transition-colors">Hubungi</a>
            </div>
            <!-- Mobile Burger Button -->
            <button id="nav-burger" aria-label="Buka menu navigasi" aria-expanded="false" onclick="toggleNav()"
                    class="md:hidden w-9 h-9 flex items-center justify-center rounded-lg border border-slate-200 bg-white text-slate-700 hover:bg-slate-50 transition-colors">
                <svg id="nav-burger-icon" class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2.5" d="M4 6h16M4 12h16M4 18h16"></path></svg>
            </button>
        </div>
        <!-- Mobile Dropdown Menu -->
        <div id="nav-mobile-menu" class="md:hidden hidden border-t border-slate-100 bg-white/98 backdrop-blur-md">
            <nav class="max-w-4xl mx-auto px-4 py-2 flex flex-col text-sm font-bold text-slate-700">
                <a href="index.html" class="py-3 border-b border-slate-100 hover:text-orange-600 transition-colors">Pilihan Utama</a>
                <a href="about.html" class="py-3 border-b border-slate-100 hover:text-orange-600 transition-colors">Mengenai Kami</a>
                <a href="editorial-policy.html" class="py-3 border-b border-slate-100 hover:text-orange-600 transition-colors">Polisi Semakan</a>
                <a href="privacy-policy.html" class="py-3 border-b border-slate-100 hover:text-orange-600 transition-colors">Polisi Privasi</a>
                <a href="contact.html" class="py-3 hover:text-orange-600 transition-colors">Hubungi Kami</a>
            </nav>
        </div>
        </div>
    </header>

    <main class="max-w-3xl mx-auto px-4 w-full">
        
        <!-- Header -->
        <div class="text-center mb-10">
            <div class="inline-flex items-center gap-2 bg-orange-50 border border-orange-200 text-orange-700 text-xs font-extrabold px-3.5 py-1.5 rounded-full uppercase tracking-wider mb-4 shadow-sm">
                <span class="w-2 h-2 bg-emerald-500 rounded-full animate-pulse"></span>
                <span>iviz Picks • Semakan Editorial Bebas {{current_year}}</span>
            </div>
            <h1 class="text-3xl md:text-5xl font-extrabold text-slate-900 tracking-tight leading-tight">
                Pilihan Produk Terbaik & Panduan Belian Malaysia
            </h1>
            <p class="text-slate-600 text-sm md:text-base mt-3 max-w-xl mx-auto leading-relaxed">
                Analisis ulasan objektif berasaskan data pembeli yang disahkan dan semakan piawaian rasmi (NPRA KKM, SIRIM, MCMC).
            </p>
        </div>

        <!-- 3rd Party Verification Callout -->
        <div class="bg-white border border-slate-200 rounded-2xl p-4 md:p-5 mb-6 shadow-sm flex flex-col sm:flex-row items-start sm:items-center justify-between gap-4 text-xs">
            <div class="flex items-center gap-3.5">
                <div class="w-10 h-10 rounded-xl bg-gradient-to-tr from-emerald-500 to-teal-500 text-white flex items-center justify-center font-black shrink-0 text-base shadow-md shadow-emerald-500/20">
                    ✓
                </div>
                <div>
                    <span class="font-extrabold text-slate-900 text-sm block">Standard Semakan Bebas & Telus</span>
                    <span class="text-slate-600">Setiap produk disaring mengikut status keselamatan NPRA KKM, SIRIM, dan pengedar rasmi.</span>
                </div>
            </div>
            <a href="editorial-policy.html" class="text-orange-600 font-bold hover:underline shrink-0 flex items-center gap-1">
                Polisi Semakan →
            </a>
        </div>

        <!-- ELEMENT 1: Category Hubs -->
        <div class="mb-8">
            <div class="flex items-center justify-between mb-4">
                <span class="text-[11px] font-black text-slate-400 uppercase tracking-widest">📁 Kategori Produk Utama</span>
                <a href="kategori.html" class="text-orange-600 font-bold text-xs hover:underline">Lihat Semua →</a>
            </div>
            <div class="flex overflow-x-auto gap-4 pb-4 no-scrollbar -mx-4 px-4 mask-fade-right">
                {cat_pills_html}
            </div>
        </div>

        <!-- ELEMENT 2: Featured Collections -->
        <div class="mb-8">
            <div class="flex items-center justify-between mb-4">
                <h2 class="text-xs font-black text-amber-900 uppercase tracking-widest flex items-center gap-1.5">
                    <span>💡 Koleksi & Idea Pilihan</span>
                </h2>
                <a href="segmen-pembeli.html" class="text-amber-600 font-bold text-xs hover:underline">Lihat Semua Segmen →</a>
            </div>
            <div class="grid gap-4 sm:grid-cols-2 lg:grid-cols-3">
                {intent_cards_html_featured}
            </div>
        </div>

        <!-- ELEMENT 3: Featured Guides -->
        <div class="mb-8">
            <div class="flex items-center justify-between mb-4">
                <h2 class="text-xs font-black text-slate-900 uppercase tracking-widest flex items-center gap-1.5">
                    <span>🎯 Panduan Keperluan Editor</span>
                </h2>
                <a href="panduan-keperluan.html" class="text-orange-600 font-bold text-xs hover:underline">Lihat Semua Panduan →</a>
            </div>
            <div class="grid gap-4 sm:grid-cols-2 lg:grid-cols-3">
                {problem_cards_html_featured}
            </div>
        </div>

        <!-- Dynamic Group Filter Tabs -->
        <div class="flex items-center gap-2.5 overflow-x-auto pb-3 mb-6 no-scrollbar">
            {tab_buttons_html}
        </div>

        <!-- Product Cards Container -->
        <div id="productsGrid" class="space-y-4">
    """
    for prod in products:
        status_badge = '<span class="bg-slate-200 text-slate-600 px-2 py-0.5 rounded text-[10px] font-bold">STOK HABIS</span>' if prod.get('status') == 'out_of_stock' else ''
        
        index_html += f"""
            <a href="{prod['id']}.html" data-group="{prod.get('group_slug', 'health-care')}" class="product-card block bg-white hover:bg-slate-50 p-5 md:p-6 rounded-2xl border border-slate-200 hover:border-orange-400 shadow-sm hover:shadow-md transition-all group">
                <div class="flex items-start justify-between gap-4 md:gap-6">
                    <div class="w-20 h-20 md:w-24 md:h-24 bg-slate-100 border border-slate-200 rounded-xl shrink-0 overflow-hidden p-1 flex items-center justify-center relative">
                        <img src="{prod.get('image_url', '')}" alt="{prod['name']}" class="w-full h-full object-contain rounded-lg group-hover:scale-105 transition-transform duration-300" loading="lazy" />
                        <div class="absolute inset-0 flex items-center justify-center">{status_badge}</div>
                    </div>
                    <div class="flex-grow">
                        <div class="flex flex-wrap items-center gap-2 mb-2">
                            <span class="text-xs font-extrabold text-slate-900 bg-slate-100 border border-slate-200 px-2.5 py-0.5 rounded-md">{prod.get('group', 'Pilihan')}</span>
                            <span class="text-xs font-bold text-orange-700 bg-orange-50 border border-orange-200/80 px-2.5 py-0.5 rounded-md">{prod.get('category', 'Am')}</span>
                            <span class="text-xs text-slate-500 font-semibold">{prod.get('brand', 'Pilihan Terpilih')}</span>
                        </div>
                        <h2 class="text-base md:text-lg font-extrabold text-slate-900 group-hover:text-orange-600 transition-colors leading-snug">{prod['name']}</h2>
                        <p class="text-xs text-slate-600 mt-1.5 line-clamp-2 leading-relaxed">{prod.get('hook', '')}</p>
                    </div>
                </div>
                <div class="flex flex-col sm:flex-row sm:items-center sm:justify-between gap-3 mt-4 pt-3 border-t border-slate-100">
                    <div class="flex flex-wrap items-baseline gap-2">
                        <span class="text-lg md:text-xl font-black text-slate-900">{prod.get('shopee_price', prod.get('price', 'RM --'))}</span>
                        <span class="text-xs text-slate-400 line-through font-semibold">{prod.get('original_price', '')}</span>
                        <span class="text-[11px] text-amber-700 font-extrabold bg-amber-50 border border-amber-200 px-2 py-0.5 rounded">{prod.get('discount', 'Terkini')}</span>
                    </div>
                    <span class="text-xs font-extrabold text-orange-600 flex items-center gap-1.5 sm:group-hover:translate-x-1 transition-transform shrink-0">
                        <span>Baca Ulasan</span>
                        <svg class="w-4 h-4 shrink-0" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2.5" d="M14 5l7 7m0 0l-7 7m7-7H3"></path></svg>
                    </span>
                </div>
            </a>
        """
    index_html += f"""
        </div>
    </div>
    
    <script>
        function filterGroup(slug, btn) {{
            document.querySelectorAll('.tab-btn').forEach(b => b.classList.remove('active'));
            btn.classList.add('active');

            const cards = document.querySelectorAll('.product-card');
            cards.forEach(card => {{
                if (slug === 'all' || card.getAttribute('data-group') === slug) {{
                    card.classList.remove('hidden');
                }} else {{
                    card.classList.add('hidden');
                }}
            }});
        }}
        function toggleNav() {{
            const menu = document.getElementById('nav-mobile-menu');
            const btn = document.getElementById('nav-burger');
            if (!menu) return;
            const isOpen = !menu.classList.contains('hidden');
            menu.classList.toggle('hidden');
            if (btn) btn.setAttribute('aria-expanded', String(!isOpen));
        }}
    </script>

        <!-- Footer -->
    <footer class="bg-white border-t border-slate-200 py-10 px-4 text-xs text-slate-500 mt-12 mb-16 md:mb-0">
        <div class="max-w-4xl mx-auto flex flex-col md:flex-row items-center justify-between gap-4">
            <div class="flex items-center gap-2.5 font-bold text-slate-900">
                <span class="bg-gradient-to-tr from-orange-500 to-amber-400 text-white w-5 h-5 rounded flex items-center justify-center text-[11px] font-black shadow-sm">i</span>
                <span>iviz Picks Malaysia</span>
            </div>
            <div class="flex items-center gap-5 text-slate-600 font-semibold">
                <a href="about.html" class="hover:text-slate-900 transition-colors">Mengenai Kami</a>
                <a href="editorial-policy.html" class="hover:text-slate-900 transition-colors">Polisi Semakan</a>
                <a href="privacy-policy.html" class="hover:text-slate-900 transition-colors">Polisi Privasi</a>
                <a href="contact.html" class="hover:text-slate-900 transition-colors">Hubungi Kami</a>
            </div>
        </div>
        <div class="max-w-4xl mx-auto text-[11px] text-slate-400 mt-6 pt-6 border-t border-slate-100 text-center leading-relaxed">
            Penafian: iviz Picks ialah saluran media ulasan bebas. Pautan luar mungkin mengandungi rujukan perkongsian komisen afiliasi. Sebarang ulasan diterbitkan secara objektif tanpa tajaan penjual. Hubungi kami: <a href="mailto:hello@iviztrading.com" class="text-slate-600 underline font-medium">hello@iviztrading.com</a>.
        </div>
    </footer>
</body>
</html>
    """
    index_html = index_html.replace("{current_year}", str(_now.year)).replace("{{current_year}}", str(_now.year))
    with open(os.path.join(dist_dir, "index.html"), "w", encoding="utf-8") as f:
        f.write(index_html)
    print(" Generated External-CDN Image Hub: dist/index.html")

    # 3b. Generate Category Listicle Hubs (Hub-and-Spoke, format dinamik)
    category_slugs = generate_category_listicles(dist_dir, products)

    # 4. Generate sitemap.xml & robots.txt (AEO/GEO/SEO for Google, Bing, GPTBot, Perplexity)
    today_iso = _now.strftime("%Y-%m-%d")
    sitemap_entries = [
        f"""  <url>
    <loc>https://link.iviztrading.com/</loc>
    <lastmod>{today_iso}</lastmod>
    <changefreq>daily</changefreq>
    <priority>1.0</priority>
  </url>"""
    ]

    for cslug in category_slugs:
        sitemap_entries.append(f"""  <url>
    <loc>https://link.iviztrading.com/{cslug}</loc>
    <lastmod>{today_iso}</lastmod>
    <changefreq>daily</changefreq>
    <priority>0.9</priority>
  </url>""")

    for p in products:
        sitemap_entries.append(f"""  <url>
    <loc>https://link.iviztrading.com/{p['id']}.html</loc>
    <lastmod>{today_iso}</lastmod>
    <changefreq>weekly</changefreq>
    <priority>0.8</priority>
  </url>""")

    for trust_page in ["kategori.html", "segmen-pembeli.html", "panduan-keperluan.html", "about.html", "editorial-policy.html", "privacy-policy.html", "contact.html"]:
        sitemap_entries.append(f"""  <url>
    <loc>https://link.iviztrading.com/{trust_page}</loc>
    <lastmod>{today_iso}</lastmod>
    <changefreq>monthly</changefreq>
    <priority>0.5</priority>
  </url>""")

    sitemap_xml = f"""<?xml version="1.0" encoding="UTF-8"?>
<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">
{chr(10).join(sitemap_entries)}
</urlset>
"""
    with open(os.path.join(dist_dir, "sitemap.xml"), "w", encoding="utf-8") as f:
        f.write(sitemap_xml.strip() + "\n")
    print(f" Generated: dist/sitemap.xml ({len(sitemap_entries)} URLs)")

    robots_txt = """# robots.txt for https://link.iviztrading.com
User-agent: *
Allow: /

# Dedicated AI & Search Crawlers (AEO / GEO)
User-agent: Googlebot
Allow: /

User-agent: Bingbot
Allow: /

User-agent: GPTBot
Allow: /

User-agent: ChatGPT-User
Allow: /

User-agent: PerplexityBot
Allow: /

User-agent: ClaudeBot
Allow: /

User-agent: Applebot
Allow: /

Sitemap: https://link.iviztrading.com/sitemap.xml
"""
    with open(os.path.join(dist_dir, "robots.txt"), "w", encoding="utf-8") as f:
        f.write(robots_txt.strip() + "\n")
    print(" Generated: dist/robots.txt")

    # 5. Apply Global Chrome (Unified Header, Footer, Mobile Burger Script across ALL pages)
    apply_global_chrome(dist_dir)


def apply_global_chrome(dist_dir):
    header_regex = re.compile(r'(?:<!-- (?:GLOBAL HEADER|Top Navigation Header) -->\s*)?<header[\s\S]*?</header>', re.MULTILINE)
    footer_regex = re.compile(r'(?:<!-- (?:GLOBAL FOOTER|Footer) -->\s*)?<footer[\s\S]*?</footer>', re.MULTILINE)

    count = 0
    for fname in os.listdir(dist_dir):
        if not fname.endswith(".html"):
            continue

        fpath = os.path.join(dist_dir, fname)
        html = open(fpath, encoding="utf-8").read()

        # Replace Header if exists, else INSERT after <body...>
        if header_regex.search(html):
            html = header_regex.sub(GLOBAL_HEADER, html, count=1)
        elif "<header" not in html:
            html = re.sub(r'(<body[^>]*>)', r'\1\n' + GLOBAL_HEADER, html, count=1)

        # Replace Footer if exists, else INSERT before </body>
        if footer_regex.search(html):
            html = footer_regex.sub(GLOBAL_FOOTER, html, count=1)
        elif "<footer" not in html:
            html = html.replace("</body>", GLOBAL_FOOTER + "\n</body>")

        # Ensure GLOBAL_NAV_SCRIPT is present before </body>
        if "function toggleNav" not in html:
            html = html.replace("</body>", f"{GLOBAL_NAV_SCRIPT}\n</body>")

        open(fpath, "w", encoding="utf-8").write(html)
        count += 1

    print(f" Applied Global Chrome (Header/Footer/Burger Nav) to ALL {count} HTML pages in dist/.")

    # 6. Stealth Post-Processing (Static CSS, Strip Comments, Minify HTML)
    optimize_and_stealth_dist(dist_dir)


def optimize_and_stealth_dist(dist_dir):
    """
    STEALTH POST-PROCESSOR:
    1. Compiles Tailwind CSS to a single static `styles.css` file via Tailwind CLI (no CDN script).
    2. Replaces Tailwind CDN script and inline styles with <link rel="stylesheet" href="styles.css">.
    3. Strips all HTML comments (e.g., <!-- GLOBAL HEADER ... -->).
    4. Minifies HTML to look like a clean production developer build.
    """
    import subprocess, htmlmin

    tw_bin = "/root/tools/tw/node_modules/.bin/tailwindcss"
    tw_config = "/root/tools/tw/tailwind.config.js"
    tw_input = "/root/tools/tw/input.css"
    tw_output = os.path.join(dist_dir, "styles.css")

    try:
        subprocess.run([tw_bin, "-c", tw_config, "-i", tw_input, "-o", tw_output, "--minify"], check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    except Exception as e:
        print(f"  ⚠️ Warning: Tailwind CLI compile failed ({e}), keeping existing styles.css if present.")

    comment_regex = re.compile(r'<!--(?!\[if).*?-->', re.DOTALL)
    tw_script_regex = re.compile(r'<script\s+src=["\']https://cdn\.tailwindcss\.com["\']><\s*/script\s*>', re.IGNORECASE)
    inline_style_regex = re.compile(r'<style>[\s\S]*?</style>', re.IGNORECASE)

    count = 0
    for fname in os.listdir(dist_dir):
        if not fname.endswith(".html"):
            continue

        fpath = os.path.join(dist_dir, fname)
        html = open(fpath, encoding="utf-8").read()

        # Replace Tailwind CDN with static stylesheet link
        html = tw_script_regex.sub('<link rel="stylesheet" href="styles.css">', html)
        
        # Remove inline <style> tags (compiled into styles.css)
        html = inline_style_regex.sub('', html)

        # Strip HTML comments
        html = comment_regex.sub('', html)

        # Minify HTML
        try:
            html = htmlmin.minify(html, remove_comments=True, remove_empty_space=True)
        except Exception:
            pass

        open(fpath, "w", encoding="utf-8").write(html)
        count += 1

    print(f" Stealth & Minify complete: Compiled static styles.css & cleaned {count} HTML pages.")

if __name__ == "__main__":
    generate_production_microsites()
