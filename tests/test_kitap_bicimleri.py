"""MOBI, AZW3, IBA ve RTF desteği testleri (arayüz açılmaz)."""
import gzip
import os
import shutil
import struct
import sys
import tempfile
import zipfile
import zlib

import pytest

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

pymupdf = pytest.importorskip("pymupdf")
import pdf_gui as g  # noqa: E402

VERI = os.path.join(os.path.dirname(os.path.abspath(__file__)), "veri")
def _png(genislik=40, yukseklik=30):
    """Küçük, geçerli bir PNG üretir (kırmızı dolgu)."""
    def parca(ad, veri):
        govde = ad + veri
        return struct.pack(">I", len(veri)) + govde + struct.pack(">I", zlib.crc32(govde))
    satir = b"\x00" + b"\xc8\x1e\x1e" * genislik
    return (b"\x89PNG\r\n\x1a\n" + parca(b"IHDR", struct.pack(">IIBBBBB", genislik, yukseklik, 8, 2, 0, 0, 0))
            + parca(b"IDAT", zlib.compress(satir * yukseklik)) + parca(b"IEND", b""))


PNG = _png()


@pytest.fixture(autouse=True)
def ayarlar(tmp_path, monkeypatch):
    monkeypatch.setattr(g, "settings_path", lambda: str(tmp_path / "settings.json"))
    monkeypatch.setattr(g, "app_data_dir", lambda: str(tmp_path))


def _metin(pdf_yolu):
    with pymupdf.open(pdf_yolu) as doc:
        return "\n".join(page.get_text() for page in doc)


def test_desteklenen_uzantilar():
    for ad in ("a.pdf", "a.EPUB", "a.mobi", "a.azw3", "a.IBA", "a.rtf"):
        assert g.is_openable_document(ad), ad
    assert not g.is_openable_document("a.docx")
    assert g.is_book_file("a.rtf") and not g.is_book_file("a.pdf")
    assert g.book_format_name("x/Kitap.AZW3") == "AZW3"


# --- RTF ------------------------------------------------------------------------------------------
RTF = (rb"{\rtf1\ansi\ansicpg1254\deff0{\fonttbl{\f0\fnil\fcharset162 Arial;}}{\colortbl;\red0\green0\blue0;}"
       rb"{\info{\title Deneme Belgesi}{\author Yazar Ad\'fd}}"
       rb"\pard\qc\b Ba\'fel\'fdk\b0\par"
       rb"\pard Merhaba d\'fcnya \'fd\'f0\'fe \i e\u287?\i0 \u"
       rb"8364?\par"
       rb"{\*\generator Gizli;}{\footnote Dipnot}"
       rb"\trowd\intbl A\cell B\cell\row"
       rb"\pard Son \{satir\}\par}")


def test_rtf_turkce_bicim_ve_tablo():
    govde, resimler, meta = g.rtf_to_html(RTF)
    assert "<b>Başlık</b>" in govde and 'text-align:center' in govde
    assert "Merhaba dünya ığş" in govde and "<i>eğ</i>" in govde and "€" in govde
    assert "Gizli" not in govde and "Dipnot" not in govde
    assert "<table" in govde and "<td>A</td>" in govde and "<td>B</td>" in govde
    assert "Son {satir}" in govde
    assert meta["title"] == "Deneme Belgesi" and meta["author"] == "Yazar Adı"
    assert not resimler


def test_rtf_resim_ve_pdf_donusumu(tmp_path):
    hexa = PNG.hex().encode()
    rtf = b"{\\rtf1\\ansi Merhaba{\\pict\\pngblip\\picwgoal600 " + hexa + b"}\\par Bitti\\par}"
    govde, resimler, _ = g.rtf_to_html(rtf)
    assert resimler == [("resim1.png", PNG)] and '<img src="resim1.png"' in govde
    yol = tmp_path / "resimli.rtf"
    yol.write_bytes(rtf)
    with pymupdf.open(g.resolve_document_path(str(yol))) as doc:
        assert len(doc[0].get_images()) == 1  # resim gerçekten sayfaya yerleşti
    yol = tmp_path / "belge.rtf"
    yol.write_bytes(RTF)
    cikti = g.resolve_document_path(str(yol))
    assert cikti.endswith("belge_rtf.pdf") and g.epub_source_of(cikti) == str(yol)
    assert "Merhaba dünya" in _metin(cikti)
    with pymupdf.open(cikti) as doc:
        assert doc.metadata["title"] == "Deneme Belgesi"


def test_rtf_gecersiz_dosya(tmp_path):
    yol = tmp_path / "bozuk.rtf"
    yol.write_bytes(b"bu rtf degil")
    with pytest.raises(ValueError):
        g.resolve_document_path(str(yol))


def test_rtf_ve_epub_ayni_adda_cakismaz(tmp_path):
    (tmp_path / "kitap.rtf").write_bytes(RTF)
    cikti = g.resolve_document_path(str(tmp_path / "kitap.rtf"))
    assert os.path.basename(cikti) == "kitap_rtf.pdf"


# --- IBA ------------------------------------------------------------------------------------------
INDEX = """<?xml version="1.0" encoding="UTF-8"?>
<sl:document xmlns:sl="http://developer.apple.com/namespaces/sl" xmlns:sf="http://developer.apple.com/namespaces/sf"
             xmlns:sfa="http://developer.apple.com/namespaces/sfa">
  <sf:text-body>
    <sf:p sf:style="title"><sf:span>Kitabın Adı</sf:span></sf:p>
    <sf:p sf:style="heading-1"><sf:span>Birinci Bölüm</sf:span></sf:p>
    <sf:p sf:style="body"><sf:span>Merhaba </sf:span><sf:span>dünya ığşçöü.</sf:span><sf:br/><sf:span>İkinci satır</sf:span></sf:p>
    <sf:p sf:style="body"><sf:ghost-text>Yer tutucu</sf:ghost-text></sf:p>
  </sf:text-body>
  <sf:image-media><sf:data sf:path="Data/resim.png" sf:size="68"/></sf:image-media>
</sl:document>"""


@pytest.fixture
def iba(tmp_path):
    yol = tmp_path / "kitap.iba"
    with zipfile.ZipFile(yol, "w") as z:
        z.writestr("Kitap.iba/index.xml.gz", gzip.compress(INDEX.encode("utf-8")))
        z.writestr("Kitap.iba/Data/resim.png", PNG)
    return str(yol)


def test_iba_metin_baslik_ve_resim(iba):
    govde, resimler, _ = g.iba_to_html(iba)
    assert "<h1>Kitabın Adı</h1>" in govde and "<h2>Birinci Bölüm</h2>" in govde
    assert "Merhaba dünya ığşçöü.<br/>İkinci satır" in govde
    assert "Yer tutucu" not in govde
    assert resimler == [("resim1.png", PNG)]


def test_iba_pdfe_donusur(iba):
    cikti = g.resolve_document_path(iba)
    assert cikti.endswith("kitap_iba.pdf")
    metin = _metin(cikti)
    assert "Birinci Bölüm" in metin and "dünya" in metin
    with pymupdf.open(cikti) as doc:
        assert any(page.get_images() for page in doc)


def test_iba_gecersiz(tmp_path):
    bos = tmp_path / "bos.iba"
    with zipfile.ZipFile(bos, "w") as z:
        z.writestr("alakasiz.txt", "x")
    with pytest.raises(ValueError):
        g.resolve_document_path(str(bos))
    duz = tmp_path / "duz.iba"
    duz.write_bytes(b"zip degil")
    with pytest.raises(ValueError):
        g.resolve_document_path(str(duz))


# --- MOBI / AZW3 ----------------------------------------------------------------------------------
pytest.importorskip("mobi")


@pytest.mark.parametrize("uzanti", [".mobi", ".azw3"])
def test_kindle_kitabi_pdfe_donusur(tmp_path, uzanti):
    kaynak = tmp_path / ("kitap" + uzanti)
    shutil.copyfile(os.path.join(VERI, "demo.mobi"), kaynak)
    cikti = g.resolve_document_path(str(kaynak))
    assert os.path.basename(cikti) == f"kitap_{uzanti[1:]}.pdf"
    with pymupdf.open(cikti) as doc:
        assert len(doc) > 20
        assert "Children" in doc.metadata["title"] or len(_metin(cikti)) > 1000
    assert g.epub_cached_pdf(str(kaynak)) == cikti
    assert not [n for n in os.listdir(tempfile.gettempdir()) if n.startswith("babapdf_kitap_")]  # geçici klasör kalmaz


def test_bozuk_kindle_anlasilir_hata(tmp_path):
    yol = tmp_path / "bozuk.azw3"
    yol.write_bytes(b"\x00" * 200)
    with pytest.raises(ValueError):
        g.resolve_document_path(str(yol))


def test_kitaplik_bilgisi_donusturulmus_pdften(tmp_path):
    yol = tmp_path / "belge.rtf"
    yol.write_bytes(RTF)
    assert g.library_info(str(yol))["cover"] is None  # henüz dönüştürülmedi
    g.resolve_document_path(str(yol))
    bilgi = g.library_info(str(yol))
    assert bilgi["title"] == "Deneme Belgesi" and os.path.exists(bilgi["cover"])
