"""Shared navigation — single source of truth for the site menu.

Menu (all pages, desktop + mobile):
  Forecasters | Predictions | Methodology

Only Methodology uses external-tab icon and target=_blank.
Forecasters and Predictions are normal same-tab site links.
"""


def render_nav(active: str = "", relative_prefix: str = "") -> str:
    def link_cls(key: str) -> str:
        if key == active:
            return "font-normal text-slate-900"
        return "font-normal text-slate-600 hover:text-slate-900 transition-colors"

    p = relative_prefix
    icon = '<i class="fa-solid fa-arrow-up-right-from-square text-xs opacity-70"></i>'

    desktop_links = f"""
          <a href="{p}forecasters.html" class="{link_cls('forecasters')}">Forecasters</a>
          <a href="{p}predictions.html" class="{link_cls('predictions')}">Predictions</a>
          <a href="https://github.com/TittaDiGirolamo/trackrecord.info/blob/main/METHODOLOGY.md" target="_blank" rel="noopener noreferrer" class="{link_cls('methodology')} inline-flex items-center gap-1">Methodology {icon}</a>"""

    mobile_links = f"""
          <a href="{p}forecasters.html" class="{link_cls('forecasters')} px-2 py-1">Forecasters</a>
          <a href="{p}predictions.html" class="{link_cls('predictions')} px-2 py-1">Predictions</a>
          <a href="https://github.com/TittaDiGirolamo/trackrecord.info/blob/main/METHODOLOGY.md" target="_blank" rel="noopener noreferrer" class="{link_cls('methodology')} px-2 py-1 inline-flex items-center gap-1">Methodology {icon}</a>"""

    return f"""
  <nav id="main-nav" class="bg-white sticky top-0 z-50">
    <div class="max-w-7xl mx-auto px-6">
      <div class="flex items-center justify-between h-16 md:h-20">
        <div class="flex items-center gap-x-2.5">
          <div class="w-7 h-7 bg-slate-900 rounded-lg flex items-center justify-center flex-shrink-0">
            <span class="text-white text-sm font-normal tracking-tight">T</span>
          </div>
          <a href="{p}index.html" class="font-normal text-slate-900">Trackrecord.info</a>
        </div>
        <div class="hidden md:flex items-center gap-x-8">{desktop_links}
        </div>
        <div class="flex items-center gap-x-3">
          <a href="https://x.com/titta_girolamo" class="hidden sm:flex items-center gap-x-2 font-normal text-slate-600 hover:text-slate-900 transition-colors">
            <i class="fa-brands fa-x-twitter"></i>
            <span>Follow</span>
          </a>
          <button id="mobile-menu-btn" class="md:hidden p-2 text-slate-700 hover:text-slate-900 focus:outline-none" aria-label="Toggle menu" aria-expanded="false">
            <i class="fa-solid fa-bars text-2xl"></i>
          </button>
        </div>
      </div>
      <div id="mobile-menu" class="hidden md:hidden py-4">
        <div class="flex flex-col gap-y-4">{mobile_links}
          <div class="pt-4 flex flex-col gap-y-3">
            <a href="https://x.com/titta_girolamo" class="flex items-center gap-x-2 px-2 py-1 text-slate-700 hover:text-slate-900">
              <i class="fa-brands fa-x-twitter"></i> Follow on X
            </a>
          </div>
        </div>
      </div>
    </div>
  </nav>
"""


def nav_script() -> str:
    return """
  <script>
    document.getElementById('mobile-menu-btn')?.addEventListener('click', function () {
      const m = document.getElementById('mobile-menu');
      const open = !m.classList.contains('hidden');
      m.classList.toggle('hidden', open);
      this.setAttribute('aria-expanded', String(!open));
      this.querySelector('i').className = open
        ? 'fa-solid fa-bars text-2xl'
        : 'fa-solid fa-xmark text-2xl';
    });
  </script>
"""
