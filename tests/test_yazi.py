"""Yazı ekleme (draw_text_block) için testler: Türkçe karakter, biçim, döndürülmüş sayfa (arayüz açılmaz)."""
import os
import sys

import pytest

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

pymupdf = pytest.importorskip("pymupdf")
import pdf_gui as g  # noqa: E402


@pytest.mark.parametrize("rotation", [0, 90, 180, 270])
def test_yazi_okunur_ve_bicimli(rotation):
    doc = pymupdf.open()
    page = doc.new_page(width=400, height=300)
    page.set_rotation(rotation)
    style = g.default_text_style()
    style.update(size=18, bold=True, underline=True, strike=True, angle=0, align="center")
    g.draw_text_block(page, (40, 40), "Merhaba şğıİ\nikinci satır", style)
    text = page.get_text()
    assert "Merhaba" in text
    if g.text_font_file("Arial")[0]:  # Windows yazı tipi varsa Türkçe karakterler korunmalı
        assert "ikinci satır" in text and "şğıİ" in text
    assert len(page.get_drawings()) >= 4  # iki satır x (altı + üstü çizgi)


def test_aci_ve_sinir_kutusu():
    style = g.default_text_style()
    flat = g.text_block_bbox("Deneme", style, (10, 10))
    style["angle"] = 90
    turned = g.text_block_bbox("Deneme", style, (10, 10))
    assert turned.height > flat.height and turned.width < flat.width


def test_stil_alanlari():
    style = g.default_text_style()
    for key in ("family", "size", "bold", "italic", "underline", "strike", "color", "opacity", "align", "spacing", "angle"):
        assert key in style
