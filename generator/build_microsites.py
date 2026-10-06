import json
import os
import re

from components import GLOBAL_HEADER, GLOBAL_FOOTER, GLOBAL_NAV_SCRIPT

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
                <a href="index.html" class="hover:text-slate-900 transition-colors">Katalog</a>
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
                <a href="index.html" class="py-3 border-b border-slate-100 hover:text-orange-600 transition-colors">Katalog</a>
                <a href="about.html" class="py-3 border-b border-slate-100 hover:text-orange-600 transition-colors">Mengenai Kami</a>
                <a href="editorial-policy.html" class="py-3 border-b border-slate-100 hover:text-orange-600 transition-colors">Polisi Semakan</a>
                <a href="privacy-policy.html" class="py-3 border-b border-slate-100 hover:text-orange-600 transition-colors">Polisi Privasi</a>
                <a href="contact.html" class="py-3 hover:text-orange-600 transition-colors">Hubungi Kami</a>
            </nav>
        </div>
        </div>
    </header>

    <main class="max-w-3xl mx-auto px-4 py-6 md:py-10 w-full">
        
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
                            *Harga disemak secara berkala daripada stor pengedar rasmi di platform e-dagang.
                        </p>
                    </div>

                    <!-- CTA Button -->
                    <a href="{{affiliate_url}}" target="_blank" rel="nofollow noopener" 
                       class="w-full bg-gradient-to-r from-orange-500 via-orange-600 to-amber-500 hover:from-orange-600 hover:to-amber-600 text-white font-extrabold py-4 px-6 rounded-xl text-center transition-all flex items-center justify-center gap-2 text-sm md:text-base shadow-lg shadow-orange-500/25 hover:shadow-orange-500/35 hover:-translate-y-0.5 active:translate-y-0">
                        <span>Semak Harga Terkini di Stor Rasmi</span>
                        <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2.5" d="M14 5l7 7m0 0l-7 7m7-7H3"></path></svg>
                    </a>
                    
                    <p class="text-[11px] text-slate-500 text-center mt-2.5">
                        Pautan dihalakan terus ke halaman produk di {{merchant_platform}}.
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
        <div class="fixed bottom-0 left-0 right-0 p-3 bg-white/95 backdrop-blur-md border-t border-slate-200 z-40 md:hidden flex items-center justify-between gap-3 shadow-2xl">
            <div>
                <span class="text-[10px] text-slate-500 block uppercase font-extrabold">Harga Promosi:</span>
                <span class="text-base font-black text-slate-900">{{shopee_price}}</span>
            </div>
            <a href="{{affiliate_url}}" target="_blank" rel="nofollow noopener" 
               class="bg-gradient-to-r from-orange-500 to-amber-500 text-white font-extrabold py-2.5 px-4 rounded-xl text-xs flex items-center gap-1.5 shadow-md shadow-orange-500/20">
                <span>Semak di Stor Rasmi</span>
                <svg class="w-3.5 h-3.5" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2.5" d="M14 5l7 7m0 0l-7 7m7-7H3"></path></svg>
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
        "title_short": "Diet Sihat & Low Sugar",
        "emoji": "🥗",
        "meta_title": "{n} Periuk Nasi Rendah Gula & Air Fryer untuk Diet Sihat ({year})",
        "meta_desc": "Ulasan {n} periuk nasi low-sugar dan penggoreng udara tanpa minyak terbaik untuk gaya hidup sihat & kurangkan kolesterol ({year}).",
        "h1": "{n} Periuk Nasi Rendah Gula & Air Fryer Terbaik untuk Diet Sihat ({year})",
        "intro": "Perkakas dapur moden yang membantu mengurangkan kanji nasi dan minyak masakan tanpa menjejaskan rasa makanan harian keluarga.",
        "match": lambda p: match_problem_category(p, "diet_sihat"),
        "is_problem": True
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
    }
]

def match_problem_category(p, problem_type):
    """
    GUARDRAIL: Padanan produk ke hab masalah HANYA melalui whitelist ID eksplisit.
    JANGAN guna padanan keyword/regex lagi — ia menyebabkan produk tak berkaitan
    tersalah masuk (cth: 'cushion' padan 'backrest cushion', 'vacuum' padan 'vacuum sealer').
    Setiap ID di bawah telah disemak manual supaya 100% relevan dengan masalah tersebut.
    """
    return p.get("id") in PROBLEM_HUB_PRODUCT_IDS.get(problem_type, set())


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
    # Masalah jeragat, parut hitam & tona kulit tak sekata
    "jeragat_parut": {
        "anua-niacinamide-10-txa-4-dark-spot-serum",
        "the-ordinary-niacinamide-10-zinc-1",
        "glad2glow-10-niacinamide-pomegranate-serum-17ml",
        "glad2glow-body-serum-set",
        "aiken-5x-ceramide-bright-vitamin-c-serum-15ml",
        "nivea-extra-bright-c-and-e-vitamin-body-lotion-320ml",
        "hada-labo-softening-whitening-face-wash-100g",
        "nivea-men-bright-c-hya-wash-foam-100g",
    },
    # Masalah kulit kering, mengelupas & skin barrier rosak
    "kulit_kering": {
        "skintific-5x-ceramide-moisture-gel",
        "the-originote-hyalucera-moisturizer-gel",
        "torriden-dive-in-low-molecule-hyaluronic-acid-serum",
        "hada-labo-hydrating-lotion-light-170ml",
        "laneige-water-bank-blue-hyaluronic-serum",
        "cosrx-advanced-snail-96-mucin-power-essence",
        "glad2glow-pomegranate-niacinamide-moisturizer",
    },
    # Masalah diet sihat: kurangkan minyak & gula (air fryer + periuk low-sugar SAHAJA)
    "diet_sihat": {
        "tefal-5l-low-sugar-rice-cooker",
        "gaabor-air-fryer-3-5l-smokeless-oil-free",
        "gaabor-smokeless-air-fryer-4l",
    },
    # Masalah sakit pinggang & postur duduk lama (kerusi + kusyen lumbar SAHAJA)
    "sakit_pinggang": {
        "boldlux-memory-foam-backrest-cushion",
        "ttracing-swift-x-2020-gaming-chair",
    },
    # Masalah bulu kucing, habuk & kualiti udara rumah (vakum rumah + penapis udara SAHAJA)
    "bulu_habuk": {
        "xiaomi-smart-air-purifier-4-compact",
        "xiaomi-mijia-smart-air-purifier-6",
        "deerma-dx300-vacuum-cleaner",
        "deerma-ultrasonic-air-humidifier-f628",
    },
    # Masalah kereta kotor & keselesaan pemanduan (aksesori kereta SAHAJA)
    "kereta_bersih": {
        "wireless-car-vacuum-cleaner-handheld",
        "70mai-dash-cam-a500s-pro-plus-gps",
        "dashcam-a22-3-camera-dvr-recorder",
        "baseus-360-rotation-magnetic-car-holder",
        "baseus-primetrip-vp2-car-charger-60w",
        "ugreen-bluetooth-5-4-car-receiver-70601",
    },
    # Masalah pakaian berkedut & berbulu (steamer + lint remover SAHAJA)
    "pakaian_kemas": {
        "panasonic-ni-ghd021-handheld-garment-steamer",
        "xiaomi-showsee-electric-lint-remover",
    },
}

def classify_category(p):
    text = (p.get("name","") + " " + p.get("category","") + " " + p.get("group","") + " " + " ".join(p.get("tags",[]))).lower()
    if any(k in text for k in ["serum","sunscreen","sunblock","cleanser","toner","moisturizer","skincare","ceramide","retinol","kkm","npra","jerawat","jeragat","kulit","collagen","vitamin c","brightening","whitening","spf"]): return "skincare"
    if any(k in text for k in ["kerusi","keyboard","papan kekunci","desk","standing desk","light bar","ergonom","gaming chair"]): return "setup_wfh"
    if any(k in text for k in ["air fryer","rice cooker","periuk","pressure cooker","blender","chopper","cooker","dapur","masak","pan","kuali","steamer"]): return "dapur"
    if any(k in text for k in ["earbuds","earphone","tws","fon telinga","powerbank","charger","pengecas","kabel","cable","dashcam","ugreen","baseus","smartwatch","jam tangan","bluetooth"]): return "gajet"
    # Rumah Pintar & Gaya Hidup
    return "rumah_pintar"

def generate_category_listicles(dist_dir, products):
    import datetime as _dt
    _now = _dt.datetime.now()
    year = _now.year
    generated_slugs = []

    # GUARDRAIL: sahkan setiap ID dalam whitelist wujud dalam katalog sebenar
    all_ids = {p["id"] for p in products}
    for ptype, ids in PROBLEM_HUB_PRODUCT_IDS.items():
        for pid in ids:
            if pid not in all_ids:
                print(f"  ⚠️  AMARAN: ID '{pid}' dalam whitelist hab '{ptype}' TIDAK wujud dalam katalog!")

    for spec in CATEGORY_LISTICLE_SPECS:
        matched = [p for p in products if spec["match"](p)]
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
                        <div class="flex flex-wrap items-center justify-between gap-3 mt-4 pt-3 border-t border-slate-100">
                            <div>
                                <span class="text-xs text-slate-400 block">Harga Pasaran:</span>
                                <span class="text-lg md:text-xl font-black text-slate-900">{p['shopee_price']}</span>
                                <span class="text-xs text-slate-400 line-through ml-1">{p.get('original_price', '')}</span>
                            </div>
                            <div class="flex items-center gap-2">
                                <a href="{p['id']}.html" class="inline-flex items-center gap-1 text-xs font-bold text-slate-700 hover:text-slate-900 bg-slate-100 hover:bg-slate-200 px-3 py-2 rounded-lg transition-colors">
                                    Baca Ulasan
                                </a>
                                <a href="{p['affiliate_url']}" target="_blank" rel="nofollow noopener sponsored" class="inline-flex items-center gap-1 text-xs font-extrabold text-white bg-gradient-to-r from-orange-500 to-amber-500 hover:from-orange-600 hover:to-amber-600 px-3.5 py-2 rounded-lg shadow-sm transition-all">
                                    Beli di Shopee →
                                </a>
                            </div>
                        </div>
                    </div>
                </div>
            </article>
            """

        # Other category quick links
        other_cats = ""
        for ospec in CATEGORY_LISTICLE_SPECS:
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
    <meta property="og:site_name" content="iviz Picks Malaysia">
    <meta name="twitter:card" content="summary">

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

    with open(data_path, "r", encoding="utf-8") as f:
        products = json.load(f)

    print(f"Loaded {len(products)} production products.")

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
        page = page.replace("{{group}}", prod.get("group", "Kesihatan & Penjagaan Diri"))
        page = page.replace("{{category}}", prod["category"])
        page = page.replace("{{verdict}}", prod.get("verdict", prod["hook"]))
        page = page.replace("{{hook}}", prod["hook"])
        page = page.replace("{{who_is_it_for}}", prod.get("who_is_it_for", "Semua pembeli."))
        page = page.replace("{{who_should_skip}}", prod.get("who_should_skip", "Tiada."))
        page = page.replace("{{shopee_price}}", prod["shopee_price"])
        page = page.replace("{{price_num}}", prod.get("price_num", "0.00"))
        page = page.replace("{{original_price}}", prod["original_price"])
        page = page.replace("{{discount}}", prod["discount"])
        page = page.replace("{{affiliate_url}}", prod["affiliate_url"])
        page = page.replace("{{merchant_platform}}", prod.get("merchant_platform", "Shopee Mall"))
        page = page.replace("{{image_url}}", prod.get("image_url", ""))
        page = page.replace("{{editorial_score}}", prod["editorial_score"])
        page = page.replace("{{rating_val}}", prod["schema"]["rating"])
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
        group_names[slug] = p.get("group", slug.title())

    tab_buttons_html = f'''<button onclick="filterGroup('all', this)" class="tab-btn active px-4 py-2 rounded-xl text-xs font-bold transition-all shrink-0">Semua ({len(products)})</button>'''
    for slug, count in group_counts.items():
        tab_buttons_html += f'''\n            <button onclick="filterGroup('{slug}', this)" class="tab-btn px-4 py-2 rounded-xl text-xs font-bold transition-all shrink-0">{group_names[slug]} ({count})</button>'''

    # Build Listicle Hub banner dynamically (split into Main Categories and Problem Solutions)
    cat_banner_html = ""
    prob_banner_html = ""
    for spec in CATEGORY_LISTICLE_SPECS:
        hcount = sum(1 for p in products if spec["match"](p))
        if hcount == 0:
            continue
        card_html = f'''\n            <a href="{spec['slug']}" class="p-3.5 bg-white border border-slate-200 hover:border-orange-400 rounded-xl flex items-center gap-3 transition-all group shadow-xs">
                <span class="text-2xl p-2 bg-orange-50 rounded-lg shrink-0">{spec['emoji']}</span>
                <div class="min-w-0">
                    <span class="text-xs font-extrabold text-slate-900 group-hover:text-orange-600 block truncate">{spec['title_short']}</span>
                    <span class="text-[11px] text-slate-500">{hcount} produk ulasan →</span>
                </div>
            </a>'''
        if spec.get("is_problem"):
            prob_banner_html += card_html
        else:
            cat_banner_html += card_html

    # Rebuild Index Hub
    index_html = f"""<!DOCTYPE html>
<html lang="ms">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>iviz Picks — Direktori Ulasan Produk & Panduan Belian Malaysia</title>
    <meta name="description" content="Direktori ulasan editorial bebas produk trending di pasaran Malaysia. Dilengkapi semakan pendaftaran NPRA KKM, SIRIM, dan pensijilan keselamatan.">
    <!-- OpenGraph / Social Meta -->
    <meta property="og:type" content="website">
    <meta property="og:title" content="iviz Picks — Direktori Ulasan Produk & Panduan Belian Malaysia">
    <meta property="og:description" content="Direktori ulasan editorial bebas produk trending di pasaran Malaysia. Dilengkapi semakan pendaftaran NPRA KKM, SIRIM, dan pensijilan keselamatan.">
    <meta property="og:url" content="https://link.iviztrading.com/">
    <meta property="og:site_name" content="iviz Picks Malaysia">
    <meta name="twitter:card" content="summary_large_image">
    <meta name="twitter:title" content="iviz Picks — Direktori Ulasan Produk & Panduan Belian Malaysia">
    <meta name="twitter:description" content="Direktori ulasan editorial bebas produk trending di pasaran Malaysia. Dilengkapi semakan keselamatan NPRA & SIRIM.">
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
                <a href="index.html" class="hover:text-slate-900 transition-colors">Katalog</a>
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
                <a href="index.html" class="py-3 border-b border-slate-100 hover:text-orange-600 transition-colors">Katalog</a>
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
                Katalog Ulasan & Panduan Belian Malaysia
            </h1>
            <p class="text-slate-600 text-sm md:text-base mt-3 max-w-xl mx-auto leading-relaxed">
                Analisis ulasan objektif berasaskan data pembeli terverifikasi dan semakan piawaian rasmi (NPRA KKM, SIRIM, MCMC).
            </p>
        </div>

        <!-- 3rd Party Verification Callout -->
        <div class="bg-white border border-slate-200 rounded-2xl p-4 md:p-5 mb-8 shadow-sm flex flex-col sm:flex-row items-start sm:items-center justify-between gap-4 text-xs">
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

        <!-- Category Hubs Banner -->
        <div class="mb-6">
            <h2 class="text-xs font-black text-slate-400 uppercase tracking-widest mb-3 flex items-center gap-1.5">
                <span>📁 Hab Kategori Produk</span>
            </h2>
            <div class="grid sm:grid-cols-2 lg:grid-cols-3 gap-3">
                {cat_banner_html}
            </div>
        </div>

        <!-- Problem-Focused Listicle Hubs Banner -->
        <div class="mb-8 bg-gradient-to-br from-orange-50/60 to-amber-50/60 border border-orange-200/80 rounded-2xl p-4 sm:p-5 shadow-xs">
            <div class="flex items-center justify-between mb-3">
                <h2 class="text-xs font-black text-orange-900 uppercase tracking-widest flex items-center gap-1.5">
                    <span>🎯 Pilihan Mengikut Masalah & Solusi</span>
                </h2>
                <span class="text-[10px] bg-orange-500 text-white font-black px-2 py-0.5 rounded-md">Popular</span>
            </div>
            <div class="grid sm:grid-cols-2 lg:grid-cols-3 gap-3">
                {prob_banner_html}
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
                            <span class="text-xs font-extrabold text-slate-900 bg-slate-100 border border-slate-200 px-2.5 py-0.5 rounded-md">{prod['group']}</span>
                            <span class="text-xs font-bold text-orange-700 bg-orange-50 border border-orange-200/80 px-2.5 py-0.5 rounded-md">{prod['category']}</span>
                            <span class="text-xs text-slate-500 font-semibold">{prod['brand']}</span>
                        </div>
                        <h2 class="text-base md:text-lg font-extrabold text-slate-900 group-hover:text-orange-600 transition-colors leading-snug">{prod['name']}</h2>
                        <p class="text-xs text-slate-600 mt-1.5 line-clamp-2 leading-relaxed">{prod['hook']}</p>
                    </div>
                </div>
                <div class="flex items-center justify-between mt-4 pt-3 border-t border-slate-100">
                    <div class="flex items-baseline gap-2.5">
                        <span class="text-lg md:text-xl font-black text-slate-900">{prod['shopee_price']}</span>
                        <span class="text-xs text-slate-400 line-through font-semibold">{prod['original_price']}</span>
                        <span class="text-[11px] text-amber-700 font-extrabold bg-amber-50 border border-amber-200 px-2 py-0.5 rounded">{prod['discount']}</span>
                    </div>
                    <span class="text-xs font-extrabold text-orange-600 group-hover:translate-x-1 transition-transform flex items-center gap-1.5">
                        <span>Baca Ulasan Penuh</span>
                        <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2.5" d="M14 5l7 7m0 0l-7 7m7-7H3"></path></svg>
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

    for trust_page in ["about.html", "editorial-policy.html", "privacy-policy.html", "contact.html"]:
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

if __name__ == "__main__":
    generate_production_microsites()
