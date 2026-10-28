"""Kaynak ağacının derlenebilir ve dağıtılabilir kaldığını denetler (arayüz açmaz, derleme yapmaz)."""
import os
import re

KOK = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


def _oku(*parcalar):
    with open(os.path.join(KOK, *parcalar), encoding="utf-8-sig") as dosya:
        return dosya.read()


def test_kurulum_betigindeki_kaynak_dosyalari_var():
    iss = _oku("kurulum", "BabaPDF.iss")
    eksik = []
    for yol in re.findall(r'^Source:\s*"([^"*]+)"', iss, flags=re.MULTILINE):
        if yol.startswith("..\\dist\\"):
            continue  # derleme çıktısı; build_exe.bat üretir
        if not os.path.exists(os.path.normpath(os.path.join(KOK, "kurulum", yol))):
            eksik.append(yol)
    assert not eksik, f"Kurulum betiğinin istediği dosyalar yok: {eksik}"


def test_spec_dosyasindaki_veri_dosyalari_var():
    spec = _oku("pdf_gui.spec")
    for ad in re.findall(r'\("([\w.\-]+\.(?:png|ico|txt))", "\."\)', spec):
        assert os.path.exists(os.path.join(KOK, ad)), ad


def test_paket_surumleri_sabit():
    for ad in ("requirements-build.txt",):
        for satir in _oku(ad).splitlines():
            satir = satir.strip()
            if satir and not satir.startswith("#"):
                assert "==" in satir, f"{ad}: sürüm sabitlenmemiş: {satir}"


def test_lisans_dosyalari_agpl():
    assert "GNU AFFERO GENERAL PUBLIC LICENSE" in _oku("LICENSE.txt")
    assert "AGPL-3.0" in _oku("NOTICE.txt")


def test_depoda_ozel_anahtar_yok():
    yasak = (".pfx", ".p12", ".key", ".pem")
    bulunan = []
    for klasor, alt, dosyalar in os.walk(KOK):
        alt[:] = [a for a in alt if a not in ("build", "dist", "__pycache__", ".pytest_cache")]
        bulunan += [os.path.join(klasor, d) for d in dosyalar if d.lower().endswith(yasak)]
    assert not bulunan, f"Özel anahtar/sertifika dosyası bulundu: {bulunan}"


def test_kurulum_sureci_surumu_koddan_okur():
    kod = _oku("pdf_gui.py")
    assert re.search(r'^APP_VERSION = "\d+\.\d+\.\d+"', kod, flags=re.MULTILINE)
    assert "APP_VERSION" in _oku("kurulum", "imzala_ve_paketle.ps1")


def test_arama_takimi_menude_ve_arac_cubugunda_birlikte():
    """Ara + Sonraki + Önceki tek takımdır; biri kaldırılırsa diğerleri anlamsız kalır."""
    kod = _oku("pdf_gui.py")
    for parca in ('label="PDF İçinde Ara…"', 'label="Sonraki Eşleşme"', 'label="Önceki Eşleşme"',
                  'add_button("🔍"', "self.search_prev_button", "self.search_next_button"):
        assert parca in kod, f"Arama takımından eksik: {parca}"


def test_menu_yinelenen_oge_ve_olu_eylem_yok():
    kod = _oku("pdf_gui.py")
    govde = kod[kod.index("def _build_menus"):kod.index("def _build_toolbars")]
    eylemler = re.findall(r"self\.(action_\w+)", govde)
    tanimlar = set(re.findall(r"def (action_\w+)\(", kod))
    assert not [e for e in eylemler if e not in tanimlar], "menüde tanımsız eylem var"
    # aynı eylem iki menü öğesine bağlanmaz (arama takımı ve toolbar hariç yalnızca menü gövdesi sayılır)
    tekrar = {e for e in eylemler if eylemler.count(e) > 1 and e not in ("action_annotation", "action_save_office")}  # parametreli (tür bağımsız değişkeni)
    assert not tekrar, f"menüde yinelenen eylem: {tekrar}"
    for silinen in ("Belge Bilgilerini (Metadata) Temizle", "Yer İmlerini Göster\"", "Son Yer İmini Sil"):
        assert silinen not in kod


def test_acilis_sayfasinda_menu_durumu_yonetilir():
    kod = _oku("pdf_gui.py")
    assert "def _refresh_menu_state" in kod
    assert kod.count("_refresh_menu_state()") >= 2  # açılışta ve belge açılınca


def test_kindle_destegi_paketlenir():
    """MOBI/AZW3 açmak için gereken paketler hem sabitlenmiş hem de PyInstaller betiğinde toplanır."""
    gereksinim = _oku("requirements-build.txt")
    spec = _oku("pdf_gui.spec")
    for paket in ("mobi==", "loguru=="):
        assert paket in gereksinim, paket
    for ad in ('"mobi"', '"loguru"'):
        assert ad in spec, ad
