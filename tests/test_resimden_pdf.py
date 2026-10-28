"""Resimden PDF çekirdek işlevi için testler (arayüz açılmaz)."""
import os
import sys

import pytest

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

pymupdf = pytest.importorskip("pymupdf")
Image = pytest.importorskip("PIL.Image")
import pdf_gui as g  # noqa: E402


def _make(tmp_path, name, size, mode="RGB", color="red", **save):
    path = tmp_path / name
    Image.new(mode, size, color).save(path, **save)
    return str(path)


def test_sirayla_sayfa_uretir_ve_yon_secer(tmp_path):
    a = _make(tmp_path, "a.png", (400, 200))   # yatay
    b = _make(tmp_path, "b.jpg", (200, 400))   # dikey
    out = str(tmp_path / "o.pdf")
    assert g.PDFProcessor.images_to_pdf([a, b], out) == 2
    with pymupdf.open(out) as doc:
        assert doc[0].rect.width > doc[0].rect.height
        assert doc[1].rect.width < doc[1].rect.height
        assert len(doc[0].get_images()) == 1


def test_resim_boyutunda_ve_saydam_png(tmp_path):
    p = _make(tmp_path, "s.png", (300, 100), mode="RGBA", color=(0, 0, 0, 0))
    out = str(tmp_path / "o.pdf")
    g.PDFProcessor.images_to_pdf([p], out, page_size="Resim boyutunda")
    with pymupdf.open(out) as doc:
        assert round(doc[0].rect.width) == 225 and round(doc[0].rect.height) == 75  # 96 dpi
        pix = doc[0].get_pixmap()
        assert pix.pixel(10, 10)[:3] == (255, 255, 255)  # saydamlık beyaza basılır


def test_cok_kareli_tiff_her_kare_bir_sayfa(tmp_path):
    path = str(tmp_path / "m.tif")
    frames = [Image.new("RGB", (50, 50), c) for c in ("red", "blue", "green")]
    frames[0].save(path, save_all=True, append_images=frames[1:])
    out = str(tmp_path / "o.pdf")
    assert g.PDFProcessor.images_to_pdf([path], out) == 3


def test_hatalar(tmp_path):
    with pytest.raises(ValueError):
        g.PDFProcessor.images_to_pdf([], str(tmp_path / "o.pdf"))
    bad = tmp_path / "bozuk.png"
    bad.write_bytes(b"degil")
    with pytest.raises(ValueError, match="bozuk.png"):
        g.PDFProcessor.images_to_pdf([str(bad)], str(tmp_path / "o.pdf"))
    with pytest.raises(ValueError):
        g.PDFProcessor.images_to_pdf([_make(tmp_path, "x.png", (9, 9))], str(tmp_path / "o.pdf"), page_size="A0")
