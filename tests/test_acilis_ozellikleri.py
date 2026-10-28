"""Açılış sayfası: menülerdeki her özelliğin bir kartı ya da düğmesi olmalı (yeni özellik eklenince unutulmasın)."""
import os
import re

KOK = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# Menüde olup açılış sayfasında bilerek düğmesi olmayanlar (nedeni ile):
BILEREK_YOK = {
    "_on_close",         # Çıkış: pencere kapatma düğmesi
    "show_welcome",      # Ana Sayfa: zaten buradasınız
    "save_pdf",          # Kaydet: yalnızca düzenleme varken anlamlı (Ctrl+S); "Farklı Kaydet" düğmesi var
    "search_step",       # Sonraki/Önceki eşleşme: aramaya bağlı
    "set_page_mode",     # Sayfa Rengi: "Sayfa Rengi…" düğmesi _popup_page_mode ile açar
    "set_orientation",   # Dikey/Yatay: düğmeler _toggle_check ile çağırır
    "toggle_dark_mode",  # Koyu tema: sağ üstteki tema düğmesi
}


def _kaynak():
    with open(os.path.join(KOK, "pdf_gui.py"), encoding="utf-8-sig") as dosya:
        return dosya.read()


def _govde(kod, baslangic, bitis):
    a = kod.index(baslangic)
    return kod[a:kod.index(bitis, a)]


def test_menudeki_her_eylemin_acilis_sayfasinda_dugmesi_var():
    kod = _kaynak()
    menu = _govde(kod, "def _build_menus", "self.config(menu=menubar)")
    acilis = _govde(kod, "def _welcome_feature_groups", "def _make_library_card")
    gerekli = set(re.findall(r"self\.((?:action|toggle|nav|rotate|delete|save|undo|redo|show|set|search|_on)\w*)", menu))
    eksik = sorted(ad for ad in gerekli - BILEREK_YOK if f"self.{ad}" not in acilis)
    assert not eksik, f"Açılış sayfasında kartı/düğmesi olmayan özellikler: {eksik}"


def test_ust_serit_banner_yok():
    assert "_banner_closed" not in _kaynak()
