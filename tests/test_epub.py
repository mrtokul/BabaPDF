"""EPUB desteği testleri (arayüz açılmaz)."""
import os
import sys
import zipfile

import pytest

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

pymupdf = pytest.importorskip("pymupdf")
import pdf_gui as g  # noqa: E402


@pytest.fixture
def epub(tmp_path, monkeypatch):
    monkeypatch.setattr(g, "settings_path", lambda: str(tmp_path / "settings.json"))
    monkeypatch.setattr(g, "app_data_dir", lambda: str(tmp_path))
    path = tmp_path / "kitap.epub"
    with zipfile.ZipFile(path, "w") as z:
        z.writestr("mimetype", "application/epub+zip", compress_type=zipfile.ZIP_STORED)
        z.writestr("META-INF/container.xml", '<?xml version="1.0"?><container version="1.0" xmlns="urn:oasis:names:tc:opendocument:xmlns:container"><rootfiles><rootfile full-path="c.opf" media-type="application/oebps-package+xml"/></rootfiles></container>')
        z.writestr("c.opf", '<?xml version="1.0"?><package xmlns="http://www.idpf.org/2007/opf" version="2.0" unique-identifier="i"><metadata xmlns:dc="http://purl.org/dc/elements/1.1/"><dc:title>Deneme</dc:title><dc:creator>Yazar</dc:creator><dc:identifier id="i">x</dc:identifier><dc:language>tr</dc:language></metadata><manifest><item id="a" href="a.xhtml" media-type="application/xhtml+xml"/></manifest><spine><itemref idref="a"/></spine></package>')
        z.writestr("a.xhtml", '<html xmlns="http://www.w3.org/1999/xhtml"><body><h1>Başlık</h1>' + "<p>Merhaba dünya ğüşiöç. </p>" * 300 + "</body></html>")
    return str(path)


def test_epub_pdf_donusur_ve_meta_tasinir(epub):
    out = g.resolve_document_path(epub)
    assert out.endswith(".pdf") and g.epub_source_of(out) == epub
    with pymupdf.open(out) as doc:
        assert len(doc) > 1 and doc.metadata["title"] == "Deneme" and doc.metadata["author"] == "Yazar"


def test_ayar_degisince_yeniden_duzenlenir(epub):
    n1 = len(pymupdf.open(g.resolve_document_path(epub)))
    g.save_setting("epub_font", "Çok büyük")
    assert g.epub_cached_pdf(epub) is None
    assert len(pymupdf.open(g.resolve_document_path(epub))) > n1


def test_yabanci_pdf_ezilmez(epub, tmp_path):
    foreign = tmp_path / "kitap.pdf"
    foreign.write_bytes(b"baska")
    out = g.resolve_document_path(epub)
    assert out != str(foreign) and foreign.read_bytes() == b"baska"


def test_bozuk_epub_anlasilir_hata(tmp_path):
    bad = tmp_path / "bozuk.epub"
    bad.write_bytes(b"junk")
    with pytest.raises(ValueError):
        g.resolve_document_path(str(bad))


def test_okuma_konumu(epub):
    g.remember_position(epub, 5, 20)
    assert g.recall_position(epub) == (5, 20)


def test_sayfa_rengi_yalniz_goruntuyu_boyar():
    doc = pymupdf.open()
    page = doc.new_page()
    pix = g.tint_pixmap(page.get_pixmap(alpha=False), "koyu")
    assert pix.pixel(0, 0) == (28, 28, 34)
    assert g.tint_pixmap(page.get_pixmap(alpha=False), "normal").pixel(0, 0) == (255, 255, 255)


def test_kitaplik_bilgisi_ve_ilerleme(epub):
    info = g.library_info(epub)
    assert info["title"] == "Deneme" and info["author"] == "Yazar" and os.path.exists(info["cover"])
    assert g.reading_progress(epub) is None
    g.remember_position(epub, 4, 20)
    assert g.reading_progress(epub) == (25, 5, 20)


def test_son_acilanlar_temizlenir(epub):
    g.add_recent_file(epub)
    assert g.load_recent_files() == [epub]
    assert g.clear_recent_files() and g.load_recent_files() == []
