"""Bağlantı, katman ve içindekiler yardımcıları için testler (arayüz açılmaz)."""
import os
import sys

import pytest

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

pymupdf = pytest.importorskip("pymupdf")
import pdf_gui as g  # noqa: E402


@pytest.fixture
def linked_pdf(tmp_path):
    doc = pymupdf.open()
    for _ in range(3):
        doc.new_page()
    first = doc[0]
    first.insert_link({"kind": pymupdf.LINK_GOTO, "from": pymupdf.Rect(50, 50, 150, 80), "page": 2,
                       "to": pymupdf.Point(0, 300)})
    first.insert_link({"kind": pymupdf.LINK_URI, "from": pymupdf.Rect(50, 100, 150, 130), "uri": "https://example.org"})
    doc.set_toc([[1, "Bir", 1], [2, "Alt", 2], [1, "İki", 3]])
    path = tmp_path / "b.pdf"
    doc.save(path)
    doc.close()
    return str(path)


def test_baglanti_bulunur_ve_tanimlanir(linked_pdf):
    with pymupdf.open(linked_pdf) as doc:
        page = doc[0]
        goto = g.find_link_at(page, pymupdf.Point(100, 60))
        assert goto["kind"] == pymupdf.LINK_GOTO and goto["page"] == 2
        assert g.describe_link(goto) == "Sayfa 3"
        uri = g.find_link_at(page, pymupdf.Point(100, 110))
        assert g.describe_link(uri) == "https://example.org"
        assert g.find_link_at(page, pymupdf.Point(400, 400)) is None


def test_donuk_sayfada_baglanti_dogru_yerde_bulunur(linked_pdf):
    with pymupdf.open(linked_pdf) as doc:
        page = doc[0]
        page.set_rotation(90)
        visible = pymupdf.Point(100, 60) * page.rotation_matrix  # ekranda görünen konum
        link = g.find_link_at(page, visible)
        assert link is not None and link["kind"] == pymupdf.LINK_GOTO
        assert g.find_link_at(page, pymupdf.Point(100, 60)) is None  # döndürülmemiş konum artık boş


def test_guvenli_semalar():
    assert "https://a".startswith(g.SAFE_LINK_SCHEMES)
    assert "mailto:x@y".startswith(g.SAFE_LINK_SCHEMES)
    assert not "file:///c:/x".startswith(g.SAFE_LINK_SCHEMES)
    assert not "javascript:alert(1)".startswith(g.SAFE_LINK_SCHEMES)


def test_icindekiler_ve_katman_arayuzu_verisi(linked_pdf):
    with pymupdf.open(linked_pdf) as doc:
        toc = doc.get_toc(simple=False)
        assert [(e[0], e[1], e[2]) for e in toc] == [(1, "Bir", 1), (2, "Alt", 2), (1, "İki", 3)]
        assert isinstance(toc[0][3], dict)
        assert doc.layer_ui_configs() == []
    doc = pymupdf.open()
    page = doc.new_page()
    oc = doc.add_ocg("Katman A", on=True)
    page.insert_text((50, 100), "MERHABA", fontsize=40, oc=oc)
    açık = page.get_pixmap(dpi=40).samples
    doc.set_layer_ui_config(0, 1)
    assert page.get_pixmap(dpi=40).samples != açık
    doc.set_layer_ui_config(0, 0)
    assert page.get_pixmap(dpi=40).samples == açık
