"""
Komponen Global (Header / Footer / Navigation Script)
=====================================================
Satu sumber tunggal (Single Source of Truth) untuk navbar & footer
yang digunakan pada SEMUA halaman iviz Picks:
  - index.html (homepage)
  - <product>.html (100 halaman ulasan)
  - about.html, editorial-policy.html, privacy-policy.html, contact.html

Dijaga oleh: apply_global_chrome() dalam build_microsites.py
"""

# ---------------------------------------------------------------
# NAVIGATION LINKS (satu tempat sahaja untuk kemas kini)
# ---------------------------------------------------------------
NAV_LINKS = [
    ("index.html", "Pilihan Utama"),
    ("kategori.html", "Kategori"),
    ("segmen-pembeli.html", "Segmen Pembeli"),
    ("panduan-keperluan.html", "Panduan Keperluan"),
    ("about.html", "Mengenai Kami"),
]

MOBILE_NAV_LINKS = [
    ("index.html", "🏠 Pilihan Utama"),
    ("kategori.html", "📁 Semua Kategori Produk"),
    ("segmen-pembeli.html", "👥 Segmen Pembeli & Gaya Hidup"),
    ("panduan-keperluan.html", "🎯 Panduan Mengikut Keperluan"),
    ("about.html", "📖 Mengenai Kami"),
    ("editorial-policy.html", "🛡️ Polisi Semakan"),
    ("privacy-policy.html", "🔒 Polisi Privasi"),
    ("contact.html", "✉️ Hubungi Kami"),
]


def _desktop_links():
    return "\n".join(
        f'                <a href="{href}" class="hover:text-slate-900 transition-colors">{label}</a>'
        for href, label in NAV_LINKS
    )


def _mobile_links():
    parts = []
    for i, (href, label) in enumerate(MOBILE_NAV_LINKS):
        is_last = i == len(MOBILE_NAV_LINKS) - 1
        border = "" if is_last else " border-b border-slate-100"
        parts.append(
            f'                <a href="{href}" class="flex items-center gap-2 py-3 px-2{border} hover:text-orange-600 hover:bg-slate-50/80 rounded-lg transition-all min-h-[44px]">{label}</a>'
        )
    return "\n".join(parts)


# ---------------------------------------------------------------
# GLOBAL HEADER (termasuk burger button + dropdown mobile)
# ---------------------------------------------------------------
GLOBAL_HEADER = f'''    <!-- GLOBAL HEADER (komponen dikongsi — jangan edit manual per halaman) -->
    <header class="bg-white/90 backdrop-blur-md border-b border-slate-200 sticky top-0 z-50 shadow-sm">
        <div class="max-w-4xl mx-auto px-4 py-3.5 flex items-center justify-between">
            <a href="index.html" class="flex items-center gap-2.5 font-extrabold text-lg text-slate-900 tracking-tight hover:opacity-80 transition-opacity">
                <span class="bg-gradient-to-tr from-orange-500 to-amber-400 text-white w-7 h-7 rounded-lg flex items-center justify-center font-black text-sm shadow-md shadow-orange-500/20">i</span>
                <span>iviz <span class="text-orange-500 font-bold">Picks</span></span>
            </a>
            <div class="hidden md:flex items-center gap-5 text-xs font-bold text-slate-600">
{_desktop_links()}
            </div>
            <!-- Mobile Burger Button -->
            <button id="nav-burger" aria-label="Buka menu navigasi" aria-expanded="false" aria-controls="nav-mobile-menu" onclick="toggleNav()"
                    class="md:hidden w-9 h-9 flex items-center justify-center rounded-lg border border-slate-200 bg-white text-slate-700 hover:bg-slate-50 transition-colors">
                <svg id="nav-burger-icon" class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2.5" d="M4 6h16M4 12h16M4 18h16"></path></svg>
            </button>
        </div>
        <!-- Mobile Dropdown Menu -->
        <div id="nav-mobile-menu" class="md:hidden hidden border-t border-slate-100 bg-white/98 backdrop-blur-md">
            <nav class="max-w-4xl mx-auto px-4 py-2 flex flex-col text-sm font-bold text-slate-700">
{_mobile_links()}
            </nav>
        </div>
    </header>'''


# ---------------------------------------------------------------
# GLOBAL FOOTER (E-E-A-T trust links + penafian)
# ---------------------------------------------------------------
GLOBAL_FOOTER = '''    <!-- GLOBAL FOOTER (komponen dikongsi — jangan edit manual per halaman) -->
    <footer class="bg-white border-t border-slate-200 py-10 px-4 text-xs text-slate-500 mt-12 mb-20 md:mb-0">
        <div class="max-w-4xl mx-auto flex flex-col md:flex-row items-center justify-between gap-4">
            <div class="flex items-center gap-2.5 font-bold text-slate-900">
                <span class="bg-gradient-to-tr from-orange-500 to-amber-400 text-white w-5 h-5 rounded flex items-center justify-center text-[11px] font-black shadow-sm">i</span>
                <span>iviz Picks Malaysia</span>
            </div>
            <div class="flex flex-wrap items-center justify-center gap-5 text-slate-600 font-semibold">
                <a href="about.html" class="hover:text-slate-900 transition-colors">Mengenai Kami</a>
                <a href="editorial-policy.html" class="hover:text-slate-900 transition-colors">Polisi Semakan</a>
                <a href="privacy-policy.html" class="hover:text-slate-900 transition-colors">Polisi Privasi</a>
                <a href="contact.html" class="hover:text-slate-900 transition-colors">Hubungi Kami</a>
            </div>
        </div>
        <div class="max-w-4xl mx-auto text-[11px] text-slate-400 mt-6 pt-6 border-t border-slate-100 text-center leading-relaxed">
            Penafian: iviz Picks ialah saluran media ulasan bebas. Pautan luar mungkin mengandungi rujukan perkongsian komisen afiliasi. Sebarang ulasan diterbitkan secara objektif tanpa tajaan penjual. Hubungi kami: <a href="mailto:hello@iviztrading.com" class="text-slate-600 underline font-medium">hello@iviztrading.com</a>.
        </div>
    </footer>'''


# ---------------------------------------------------------------
# GLOBAL NAV SCRIPT (fungsi toggleNav untuk burger menu)
# ---------------------------------------------------------------
GLOBAL_NAV_SCRIPT = '''    <!-- GLOBAL NAV SCRIPT (komponen dikongsi) -->
    <script>
    function toggleNav() {
        var menu = document.getElementById('nav-mobile-menu');
        var btn = document.getElementById('nav-burger');
        if (!menu) return;
        var isOpen = !menu.classList.contains('hidden');
        menu.classList.toggle('hidden');
        if (btn) btn.setAttribute('aria-expanded', String(!isOpen));
    }
    // Tutup menu apabila pautan diklik (UX mudah alih)
    document.addEventListener('click', function (e) {
        var menu = document.getElementById('nav-mobile-menu');
        var btn = document.getElementById('nav-burger');
        if (!menu || menu.classList.contains('hidden')) return;
        if (btn && btn.contains(e.target)) return;
        if (menu.contains(e.target)) { menu.classList.add('hidden'); if (btn) btn.setAttribute('aria-expanded', 'false'); return; }
        menu.classList.add('hidden');
        if (btn) btn.setAttribute('aria-expanded', 'false');
    });
    </script>'''
