"""Açıklama türleri (üstü çizili, dalgalı, kalem) ve yeni açılan biçimler: FB2, CBZ, SVG (arayüz açılmaz)."""
import os
import sys
import zipfile

import pytest

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

pymupdf = pytest.importorskip("pymupdf")
import pdf_gui as g  # noqa: E402
from test_kitap_bicimleri import PNG  # noqa: E402


@pytest.fixture(autouse=True)
def ayarlar(tmp_path, monkeypatch):
    monkeypatch.setattr(g, "settings_path", lambda: str(tmp_path / "settings.json"))
    monkeypatch.setattr(g, "app_data_dir", lambda: str(tmp_path))


def _pdf(yol):
    doc = pymupdf.open()
    sayfa = doc.new_page()
    g.insert_text_tr(sayfa, pymupdf.Point(72, 100), "Merhaba dünya ışığı", fontsize=14)
    doc.save(yol)
    doc.close()
    return yol


@pytest.mark.parametrize("tur,ad", [("highlight", "Highlight"), ("underline", "Underline"),
                                    ("strikeout", "StrikeOut"), ("squiggly", "Squiggly")])
def test_isaretleme_turleri_kaydedilir(tmp_path, tur, ad):
    yol = _pdf(str(tmp_path / "a.pdf"))
    with pymupdf.open(yol) as doc:
        sayfa = doc[0]
        kutular = sayfa.search_for("dünya")
        assert kutular
        assert g.add_markup(sayfa, kutular, tur) == len(kutular)
        doc.saveIncr()
    with pymupdf.open(yol) as doc:
        turler = [a.type[1] for a in doc[0].annots()]
    assert turler == [ad] * len(kutular)


def test_action_annotation_eski_hatali_cagri_yok():
    kaynak = open(os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "pdf_gui.py"),
                  encoding="utf-8-sig").read()
    assert 'getattr(page, f"add_{kind}")' not in kaynak  # PyMuPDF'de add_highlight yoktur, add_highlight_annot vardır
    for kind, yontem in g.MARKUP_KINDS.items():
        assert hasattr(pymupdf.Page, yontem), kind


def test_kalem_cizgisi(tmp_path):
    yol = _pdf(str(tmp_path / "b.pdf"))
    with pymupdf.open(yol) as doc:
        annot = g.add_ink(doc[0], [[(10, 10), (50, 40), (90, 20)]])
        assert annot is not None
        assert g.add_ink(doc[0], [[(1, 1)]]) is None  # tek nokta çizgi değildir
        doc.saveIncr()
    with pymupdf.open(yol) as doc:
        [a] = list(doc[0].annots())
    assert a.type[1] == "Ink"
    assert a.border["width"] == pytest.approx(2.0)


def test_yeni_uzantilar_tanimli():
    for ad in ("a.fb2", "a.xps", "a.OXPS", "a.cbz", "a.svg"):
        assert g.is_openable_document(ad) and g.is_book_file(ad), ad
    assert g.book_format_name("x/Roman.CBZ") == "CBZ"
    assert set(g.BOOK_FORMATS.values()) >= {"FB2", "XPS", "CBZ", "SVG"}
    for tur in ("FB2", "XPS", "CBZ", "SVG"):
        assert tur in g.BOOK_PATTERNS


def test_cbz_pdfe_cevrilir(tmp_path):
    yol = tmp_path / "roman.cbz"
    with zipfile.ZipFile(yol, "w") as z:
        z.writestr("01.png", PNG)
        z.writestr("02.png", PNG)
    cikti = g.epub_to_pdf(str(yol))
    with pymupdf.open(cikti) as doc:
        assert doc.is_pdf and doc.page_count == 2


def test_svg_pdfe_cevrilir(tmp_path):
    yol = tmp_path / "ciz.svg"
    yol.write_text('<svg xmlns="http://www.w3.org/2000/svg" width="200" height="100">'
                   '<rect width="200" height="100" fill="red"/></svg>', encoding="utf-8")
    cikti = g.epub_to_pdf(str(yol))
    with pymupdf.open(cikti) as doc:
        assert doc.is_pdf and doc.page_count == 1


def test_fb2_pdfe_cevrilir(tmp_path):
    yol = tmp_path / "kitap.fb2"
    yol.write_text('<?xml version="1.0" encoding="utf-8"?><FictionBook xmlns="http://www.gribuser.ru/xml/fictionbook/2.0">'
                   '<description><title-info><book-title>Deneme Kitabı</book-title><author><first-name>Ali</first-name>'
                   '<last-name>Veli</last-name></author></title-info></description>'
                   '<body><section><title><p>Bölüm Bir</p></title><p>Merhaba dünya, ışığın ağzı.</p></section></body>'
                   '</FictionBook>', encoding="utf-8")
    cikti = g.epub_to_pdf(str(yol))
    with pymupdf.open(cikti) as doc:
        assert "Merhaba" in doc[0].get_text()


def test_silgi_secilen_yaziyi_siler(tmp_path):
    yol = str(tmp_path / "s.pdf")
    with pymupdf.open() as doc:
        sayfa = doc.new_page()
        sayfa.insert_text((72, 100), "ilk satir kalsin")
        sayfa.insert_text((72, 200), "silinecek satir")
        doc.save(yol)
    with pymupdf.open(yol) as doc:
        n = g.PDFProcessor.erase_area(doc[0], pymupdf.Rect(60, 185, 300, 210))
        assert n == 2
        metin = doc[0].get_text()
        assert "silinecek" not in metin and "ilk satir kalsin" in metin
        assert g.PDFProcessor.erase_area(doc[0], pymupdf.Rect(60, 300, 300, 320)) == 0


def test_silgi_resim_piksellerini_siler(tmp_path):
    yol = str(tmp_path / "r.pdf")
    with pymupdf.open() as doc:
        sayfa = doc.new_page(width=200, height=200)
        pix = pymupdf.Pixmap(pymupdf.csRGB, pymupdf.IRect(0, 0, 100, 100), False)
        pix.set_rect(pix.irect, (0, 0, 0))
        sayfa.insert_image(pymupdf.Rect(50, 50, 150, 150), pixmap=pix)
        doc.save(yol)
    with pymupdf.open(yol) as doc:
        assert g.PDFProcessor.erase_area(doc[0], pymupdf.Rect(50, 50, 100, 150)) >= 1
        sol = doc[0].get_pixmap(clip=pymupdf.Rect(55, 60, 95, 140)).pixel(10, 10)
        sag = doc[0].get_pixmap(clip=pymupdf.Rect(110, 60, 145, 140)).pixel(10, 10)
        assert sol == (255, 255, 255) and sag == (0, 0, 0)


def test_silgi_zemin_rengine_uyar_ve_cizimi_korur(tmp_path):
    with pymupdf.open() as doc:
        sayfa = doc.new_page(width=300, height=300)
        sayfa.draw_rect(pymupdf.Rect(0, 0, 300, 300), color=None, fill=(0.9, 0.85, 0.7))  # krem arka plan (çizim)
        sayfa.insert_text((72, 150), "silinecek yazi")
        sayfa.insert_text((72, 250), "kalacak")
        assert g.PDFProcessor.erase_area(sayfa, pymupdf.Rect(60, 120, 290, 290)) >= 1
        assert "silinecek" not in sayfa.get_text()
        piksel = sayfa.get_pixmap(clip=pymupdf.Rect(200, 130, 220, 150)).pixel(5, 5)
        assert abs(piksel[0] - 230) < 12 and abs(piksel[2] - 178) < 12  # beyaz değil, krem
        dis = sayfa.get_pixmap(clip=pymupdf.Rect(10, 10, 30, 30)).pixel(5, 5)
        assert abs(dis[0] - 230) < 12  # arka plan çizimi silinmedi
