"""Baba PDF çekirdek işlevleri için testler (arayüz açılmaz). Çalıştırma: python -m pytest tests -q"""
import os
import sys
import time

import pytest

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

pymupdf = pytest.importorskip("pymupdf")
import pdf_gui as g  # noqa: E402

TURKCE = "Çalışma ğüşöıİĞŞÖÜÇ"


@pytest.fixture
def sample_pdf(tmp_path):
    doc = pymupdf.open()
    for i in range(4):
        page = doc.new_page()
        g.insert_text_tr(page, (72, 100), f"Sayfa {i + 1} {TURKCE}", fontsize=14)
    path = tmp_path / "ornek.pdf"
    doc.save(path)
    doc.close()
    return str(path)


def test_turkce_karakterler_pdf_icinde_korunur(sample_pdf):
    with pymupdf.open(sample_pdf) as doc:
        text = doc[0].get_text().replace("\xa0", " ")
    assert TURKCE in text


@pytest.mark.parametrize("value,total,expected", [
    ("1-3", 10, [1, 2, 3]),
    ("1, 3; 5-6", 10, [1, 3, 5, 6]),
    ("8-20", 10, [8, 9, 10]),
    ("0, 11", 10, []),
    ("", 10, []),
])
def test_sayfa_araligi(value, total, expected):
    assert g.PDFProcessor.parse_page_range(value, total) == expected


def test_sayfa_cikar_birlestir_sikistir(sample_pdf, tmp_path):
    out = str(tmp_path / "cikti.pdf")
    g.PDFProcessor.extract_pages(sample_pdf, [2, 4], out)
    with pymupdf.open(out) as doc:
        assert len(doc) == 2 and "Sayfa 4" in doc[1].get_text().replace(" ", " ")
    merged = str(tmp_path / "birlesik.pdf")
    g.PDFProcessor.merge_pdfs([sample_pdf, out], merged)
    with pymupdf.open(merged) as doc:
        assert len(doc) == 6
    small = str(tmp_path / "kucuk.pdf")
    g.PDFProcessor.compress(merged, small)
    assert os.path.getsize(small) > 0


def test_sifreli_pdf_birlestirilmez(sample_pdf, tmp_path):
    enc = str(tmp_path / "sifreli.pdf")
    with pymupdf.open(sample_pdf) as doc:
        doc.save(enc, encryption=pymupdf.PDF_ENCRYPT_AES_256, user_pw="a", owner_pw="b")
    with pytest.raises(ValueError):
        g.PDFProcessor.merge_pdfs([sample_pdf, enc], str(tmp_path / "x.pdf"))


def test_duzenlenmis_dosya_adi_numaralanir(tmp_path):
    original = tmp_path / "belge.pdf"
    original.write_bytes(b"x")
    first = g.generate_edited_filepath(str(original))
    assert first.endswith("belge_D1.pdf")
    open(first, "wb").close()
    assert g.generate_edited_filepath(str(original)).endswith("belge_D2.pdf")


def test_kurtarma_yolu_kalici():
    assert g.recovery_path(r"C:\A\b.pdf") == g.recovery_path(r"c:\a\B.PDF")


def test_doner_sayfada_arama_vurgusu_metnin_ustune_oturur():
    """PyMuPDF arama koordinatları döndürülmemiş uzaydadır; görünüme çevirirken sayfa dönüşü uygulanmalı."""
    doc = pymupdf.open()
    page = doc.new_page()
    g.insert_text_tr(page, (72, 100), "Merhaba dünya", fontsize=20)
    page.set_rotation(90)
    matrix = pymupdf.Matrix(1.5, 1.5)
    pix = page.get_pixmap(matrix=matrix)
    rect = page.search_for("Merhaba")[0] * page.rotation_matrix * matrix
    clip = pymupdf.IRect(int(rect.x0), int(rect.y0), int(rect.x1), int(rect.y1)) & pix.irect
    dark = sum(1 for y in range(clip.y0, clip.y1) for x in range(clip.x0, clip.x1) if sum(pix.pixel(x, y)[:3]) < 300)
    assert dark > 20


def test_eski_gecici_kopyalar_supurulur(tmp_path, monkeypatch):
    monkeypatch.setattr(g.tempfile, "gettempdir", lambda: str(tmp_path))
    eski = tmp_path / ("baba_pdf_" + "a" * 32 + ".pdf")
    yeni = tmp_path / ("baba_pdf_" + "b" * 32 + ".pdf")
    korunan = tmp_path / "baba_pdf_empty_workspace_v2.pdf"
    for p in (eski, yeni, korunan):
        p.write_bytes(b"x")
    os.utime(eski, (1, 1))
    g.sweep_old_temp_files(max_age_seconds=600)
    assert not eski.exists() and yeni.exists() and korunan.exists()


def test_surum_bicimi():
    parts = g.APP_VERSION.split(".")
    assert len(parts) == 3 and all(p.isdigit() for p in parts)
    assert time.strptime(g.APP_DATE, "%d.%m.%Y")


def test_surum_karsilastirma():
    assert g.parse_version("1.10.0") > g.parse_version("1.9.9")
    assert g.parse_version("v2.0") > g.parse_version(g.APP_VERSION)
    assert not g.parse_version("1.0.0") > g.parse_version("1.0.0")


def test_guncelleme_yalniz_https():
    with pytest.raises(ValueError):
        g.check_for_update("http://ornek.invalid/surum.json")


def test_pdf_isleyici_kaydi_hkcu(monkeypatch):
    """Kayıt yalnızca HKCU altına yazılır; gerçek kayıt defterine dokunmamak için winreg taklit edilir."""
    yazilan = []

    class Anahtar:
        def __enter__(self):
            return self

        def __exit__(self, *a):
            return False

    class Taklit:
        HKEY_CURRENT_USER = "HKCU"
        REG_SZ, REG_NONE = 1, 0

        @staticmethod
        def CreateKey(kok, yol):
            yazilan.append((kok, yol))
            return Anahtar()

        @staticmethod
        def SetValueEx(*a):
            pass

    import sys
    monkeypatch.setitem(sys.modules, "winreg", Taklit)
    g.register_pdf_handler(r"C:\Uygulama\Baba_PDF.exe")
    assert yazilan and all(kok == "HKCU" for kok, _ in yazilan)
    assert any(yol == r"Software\RegisteredApplications" for _, yol in yazilan)


@pytest.fixture
def baslatma_kaydi(tmp_path, monkeypatch):
    """Kayıt dosyasını geçici klasöre yönlendirir; çalışan 'diğer' süreç olarak bu testin kendi PID'i kullanılır."""
    monkeypatch.setattr(g, "_startup_record_path", lambda: str(tmp_path / "baslatma.json"))
    return tmp_path


def test_acilis_surerken_ikinci_baslatma_yok_sayilir(baslatma_kaydi, monkeypatch):
    import os as _os
    monkeypatch.setattr(g, "_process_start_epoch", lambda pid: 1.0)  # diğer süreç canlı
    assert g.claim_startup("", click=1000.0, pid=111)          # ilk tıklama kopya açar
    assert not g.claim_startup("", click=1001.5, pid=222)      # açılış sürerken ikinci tıklama
    assert not g.claim_startup("", click=1000.0, pid=333)      # aynı anda gelen çift tıklama


def test_acilis_bittikten_sonra_yeni_kopyaya_izin_verilir(baslatma_kaydi, monkeypatch):
    monkeypatch.setattr(g, "_process_start_epoch", lambda pid: 1.0)
    assert g.claim_startup("", click=1000.0, pid=111)
    monkeypatch.setattr(g.os, "getpid", lambda: 111)
    süre = g.mark_startup_ready(now=1010.0)
    assert süre == pytest.approx(10.0)
    assert g.claim_startup("", click=1010.5, pid=222)          # hazır olduktan sonra yeni kopya
    assert g._read_startup_record()["pid"] == 222


def test_cokmus_ilk_kopya_ikinci_baslatmayi_engellemez(baslatma_kaydi, monkeypatch):
    monkeypatch.setattr(g, "_process_start_epoch", lambda pid: 1.0)
    assert g.claim_startup("", click=1000.0, pid=111)
    monkeypatch.setattr(g, "_process_start_epoch", lambda pid: None)  # ilk süreç öldü
    assert g.claim_startup("", click=1002.0, pid=222)


def test_farkli_dosya_acma_istegi_engellenmez(baslatma_kaydi, monkeypatch):
    monkeypatch.setattr(g, "_process_start_epoch", lambda pid: 1.0)
    assert g.claim_startup("a.pdf", click=1000.0, pid=111)
    assert not g.claim_startup("a.pdf", click=1001.0, pid=222)
    assert g.claim_startup("b.pdf", click=1001.0, pid=333)


def test_koruma_suresi_olculen_acilistan_hesaplanir():
    assert g.startup_guard_seconds([]) == g.STARTUP_GUARD_DEFAULT
    assert g.startup_guard_seconds([10.0]) == pytest.approx(17.0)
    assert g.startup_guard_seconds([4, 10, 12]) == pytest.approx(17.0)


def test_ust_surec_ayni_exe_degilse_tiklama_anina_sayilmaz(monkeypatch):
    import os
    assert g._same_image(os.getpid(), os.getpid())
    assert not g._same_image(os.getpid(), 4)  # Windows "System" süreci: farklı/okunamaz
    monkeypatch.setattr(g.sys, "frozen", True, raising=False)
    monkeypatch.setattr(g, "_same_image", lambda a, b: False)
    own = g._process_start_epoch(os.getpid())
    assert g.launch_click_epoch() == pytest.approx(own, abs=1.0)


def test_kenar_kirpma_sayfayi_kucultur_ve_dondurulmusta_calisir(sample_pdf):
    with pymupdf.open(sample_pdf) as doc:
        doc[1].set_rotation(90)
        before = [(p.rect.width, p.rect.height) for p in doc]
        g.PDFProcessor.crop_margins(doc, 20, [0, 1])
        for i in (0, 1):
            assert doc[i].rect.width == pytest.approx(before[i][0] - 40)
            assert doc[i].rect.height == pytest.approx(before[i][1] - 40)
        assert doc[2].rect.width == pytest.approx(before[2][0])  # seçilmeyen sayfa değişmez
        with pytest.raises(ValueError):
            g.PDFProcessor.crop_margins(doc, 400, [0])


def test_kitapcik_sayfa_sirasi_ve_bos_tamamlama(tmp_path):
    src = tmp_path / "alti.pdf"
    doc = pymupdf.open()
    for i in range(6):
        doc.new_page(width=200, height=300).insert_text((20, 50), f"S{i + 1}X")
    doc.save(src)
    doc.close()
    out = tmp_path / "kitapcik.pdf"
    g.PDFProcessor.make_booklet(str(src), str(out))
    with pymupdf.open(out) as book:
        assert len(book) == 4  # 6 sayfa -> 8'e tamamlanır -> 4 yaprak yüzü
        assert book[0].rect.width == pytest.approx(400)

        def yarilar(page):
            left = page.get_text(clip=pymupdf.Rect(0, 0, 200, 300)).strip()
            right = page.get_text(clip=pymupdf.Rect(200, 0, 400, 300)).strip()
            return left, right

        assert yarilar(book[0]) == ("", "S1X")           # 8 boş | 1
        assert yarilar(book[1]) == ("S2X", "")           # 2 | 7 boş
        assert yarilar(book[2]) == ("S6X", "S3X")        # 6 | 3
        assert yarilar(book[3]) == ("S4X", "S5X")        # 4 | 5


def test_onarim_bozuk_dosyadan_temiz_kopya_uretir(sample_pdf, tmp_path):
    data = open(sample_pdf, "rb").read()
    bozuk = tmp_path / "bozuk.pdf"
    bozuk.write_bytes(data[:-80])  # xref/trailer kuyruğunu kes
    with pymupdf.open(bozuk) as doc:
        lines, problem = g.PDFProcessor.check_document(doc)
    assert problem
    assert any("BOZUKTU" in line or "Sorunlu" in line for line in lines)
    onarilmis = tmp_path / "onarilmis.pdf"
    g.PDFProcessor.repair_pdf(str(bozuk), str(onarilmis))
    with pymupdf.open(onarilmis) as fixed:
        assert len(fixed) == 4
        lines, problem = g.PDFProcessor.check_document(fixed)
    assert not problem


def test_saglam_dosya_dogrulamada_sorunsuz(sample_pdf):
    with pymupdf.open(sample_pdf) as doc:
        lines, problem = g.PDFProcessor.check_document(doc)
    assert not problem
    assert "Sayfa sayısı: 4" in lines


# --- Stirling PDF incelemesinden eklenen araçlar ---
def _resimli_pdf(tmp_path, adet=2):
    """Her sayfasında aynı düz renk görsel, metin ve (isteğe bağlı) boş sayfa içeren örnek."""
    pix = pymupdf.Pixmap(pymupdf.csRGB, pymupdf.IRect(0, 0, 20, 20), False)
    pix.clear_with(200)
    doc = pymupdf.open()
    for i in range(adet):
        page = doc.new_page()
        page.insert_text((72, 100), f"Sayfa {i + 1} gizli123")
        page.insert_image(pymupdf.Rect(72, 150, 172, 250), pixmap=pix)
    doc.new_page()  # tamamen boş
    path = tmp_path / "resimli.pdf"
    doc.save(path)
    doc.close()
    return str(path)


def test_bos_sayfa_bulunur_ve_silinir_ama_hepsi_silinmez(tmp_path):
    with pymupdf.open(_resimli_pdf(tmp_path)) as doc:
        assert g.PDFProcessor.find_blank_pages(doc) == [2]
        assert g.PDFProcessor.remove_blank_pages(doc) == 1
        assert len(doc) == 2
    tamamen_bos = pymupdf.open()
    tamamen_bos.new_page()
    with pytest.raises(ValueError):
        g.PDFProcessor.remove_blank_pages(tamamen_bos)


def test_gorsel_cikarma_ve_silme(tmp_path):
    with pymupdf.open(_resimli_pdf(tmp_path)) as doc:
        assert g.PDFProcessor.count_images(doc) == 1  # iki sayfada aynı görsel = 1 tekil görsel
        klasor = tmp_path / "gorseller"
        assert g.PDFProcessor.extract_images(doc, str(klasor)) == 1  # aynı görsel bir kez
        assert len(list(klasor.iterdir())) == 1
        assert g.PDFProcessor.remove_images(doc) == 1
        assert g.PDFProcessor.count_images(doc) == 0
        assert "gizli123" in doc[0].get_text()  # metin korunur


def test_kalici_karartma_metni_icerikten_siler(tmp_path):
    with pymupdf.open(_resimli_pdf(tmp_path)) as doc:
        assert g.PDFProcessor.count_matches(doc, "gizli123") == 2
        assert g.PDFProcessor.redact_text(doc, "gizli123") == 2
        assert "gizli123" not in doc[0].get_text()
        kopya = doc.tobytes()
    with pymupdf.open(stream=kopya, filetype="pdf") as yeniden:
        assert "gizli123" not in yeniden[0].get_text()
        assert g.PDFProcessor.count_matches(yeniden, "gizli123") == 0
    with pytest.raises(ValueError):
        g.PDFProcessor.redact_text(pymupdf.open(), "")


def test_temizle_javascript_gomulu_dosya_ve_bilgileri_siler(tmp_path):
    doc = pymupdf.open()
    doc.new_page().insert_text((72, 100), "icerik")
    doc.embfile_add("ek.txt", b"gizli ek")
    doc.set_metadata({"author": "Ben", "title": "Baslik"})
    assert doc.embfile_count() == 1
    g.PDFProcessor.sanitize(doc)
    assert doc.embfile_count() == 0
    assert not doc.metadata.get("author")
    assert "icerik" in doc[0].get_text()


def test_duzlestirme_form_alanini_sayfaya_gomer():
    doc = pymupdf.open()
    page = doc.new_page()
    widget = pymupdf.Widget()
    widget.field_type = pymupdf.PDF_WIDGET_TYPE_TEXT
    widget.field_name = "ad"
    widget.field_value = "Ahmet"
    widget.rect = pymupdf.Rect(72, 72, 250, 100)
    page.add_widget(widget)
    assert any(True for _ in page.widgets())
    g.PDFProcessor.flatten(doc)
    assert not any(True for _ in doc[0].widgets())


def test_izin_degistirme_parolasiz_acilir_ve_izinler_kisitli(tmp_path, sample_pdf):
    out = tmp_path / "izinli.pdf"
    with pymupdf.open(sample_pdf) as doc:
        g.PDFProcessor.save_with_permissions(doc, str(out), allow_print=True, allow_copy=False, allow_edit=False)
    with pymupdf.open(out) as sonuc:
        assert not sonuc.needs_pass
        assert sonuc.permissions & pymupdf.PDF_PERM_PRINT
        assert not sonuc.permissions & pymupdf.PDF_PERM_COPY
        assert not sonuc.permissions & pymupdf.PDF_PERM_MODIFY


def test_damga_metni_istenen_sayfalara_eklenir(sample_pdf):
    with pymupdf.open(sample_pdf) as doc:
        doc[1].set_rotation(90)
        g.PDFProcessor.stamp_pages(doc, "ONAYLANDI", 20, 9, [0, 1])
        assert "ONAYLANDI" in doc[0].get_text()
        assert "ONAYLANDI" in doc[1].get_text()
        assert "ONAYLANDI" not in doc[2].get_text()
        with pytest.raises(ValueError):
            g.PDFProcessor.stamp_pages(doc, "X", 20, 10, [0])


@pytest.mark.parametrize("adet,sayfa", [(2, 2), (4, 1), (9, 1)])
def test_n_up_yaprak_sayisi(tmp_path, sample_pdf, adet, sayfa):
    out = tmp_path / "nup.pdf"
    g.PDFProcessor.n_up(sample_pdf, str(out), adet)
    with pymupdf.open(out) as doc:
        assert len(doc) == sayfa  # 4 sayfa: 2'li -> 2, 4'lü -> 1, 9'lu -> 1
    with pytest.raises(ValueError):
        g.PDFProcessor.n_up(sample_pdf, str(out), 3)


def test_tek_uzun_sayfa_ve_sinir(tmp_path, sample_pdf):
    out = tmp_path / "uzun.pdf"
    g.PDFProcessor.single_long_page(sample_pdf, str(out))
    with pymupdf.open(out) as doc:
        assert len(doc) == 1
        assert doc[0].rect.height == pytest.approx(4 * 842, abs=1)
        assert "Sayfa 4" in doc[0].get_text().replace(" ", " ")
    cok = pymupdf.open()
    for _ in range(20):
        cok.new_page()
    uzun = tmp_path / "cok.pdf"
    cok.save(uzun)
    with pytest.raises(ValueError):
        g.PDFProcessor.single_long_page(str(uzun), str(tmp_path / "x.pdf"))


def test_yer_imi_metni_gidis_donus_ve_dogrulama():
    toc = [[1, "Giriş", 1], [2, "Alt | başlık", 2], [1, "Son", 3]]
    metin = g.PDFProcessor.toc_to_text(toc)
    assert g.PDFProcessor.parse_toc_text(metin, 3) == [[1, "Giriş", 1], [2, "Alt / başlık", 2], [1, "Son", 3]]
    for bozuk in ("2 | A | 1", "1 | A | 1\n3 | B | 1", "1 | A | 9", "1 | | 1", "bir | A | 1", "1 | A"):
        with pytest.raises(ValueError):
            g.PDFProcessor.parse_toc_text(bozuk, 3)


def test_belge_karsilastirma_farki_bulur(tmp_path):
    def yap(metinler):
        doc = pymupdf.open()
        for m in metinler:
            doc.new_page().insert_text((72, 100), m)
        return doc
    a, b = yap(["ayni", "eski satir"]), yap(["ayni", "yeni satir", "ek sayfa"])
    satirlar, farkli = g.PDFProcessor.compare_documents(a, b, "a.pdf", "b.pdf")
    assert farkli == 2
    assert any("Sayfa 2" in s for s in satirlar) and any("Sayfa 3" in s for s in satirlar)
    _, ayni = g.PDFProcessor.compare_documents(a, a, "a.pdf", "a.pdf")
    assert ayni == 0


def test_bindirme_ust_pdf_metnini_tabana_ekler(tmp_path, sample_pdf):
    ust = pymupdf.open()
    ust.new_page().insert_text((72, 300), "DAMGA-USTTE")
    ust_yolu = tmp_path / "ust.pdf"
    ust.save(ust_yolu)
    ust.close()
    out = tmp_path / "bindirilmis.pdf"
    g.PDFProcessor.overlay_pdf(sample_pdf, str(ust_yolu), str(out))
    with pymupdf.open(out) as doc:
        assert len(doc) == 4
        for page in doc:  # tek sayfalık üst PDF her sayfaya tekrarlanır
            assert "DAMGA-USTTE" in page.get_text()
        assert "Sayfa" in doc[3].get_text()  # taban metin korunur


def test_ekler_ekle_listele_cikar_sil(tmp_path):
    kaynak = tmp_path / "not.txt"
    kaynak.write_bytes(b"merhaba")
    doc = pymupdf.open()
    doc.new_page()
    assert g.PDFProcessor.add_attachment(doc, str(kaynak)) == "not.txt"
    assert g.PDFProcessor.add_attachment(doc, str(kaynak)) == "not_2.txt"  # ad çakışması
    assert g.PDFProcessor.list_attachments(doc) == [("not.txt", 7), ("not_2.txt", 7)]
    cikti = tmp_path / "geri.txt"
    g.PDFProcessor.extract_attachment(doc, "not.txt", str(cikti))
    assert cikti.read_bytes() == b"merhaba"
    g.PDFProcessor.remove_attachment(doc, "not.txt")
    assert [n for n, _ in g.PDFProcessor.list_attachments(doc)] == ["not_2.txt"]


@pytest.mark.parametrize("yazi_donusu,sayfa_donusu", [(0, 0), (90, 0), (270, 0), (180, 0), (0, 90)])
def test_otomatik_dondurme_metni_okunur_yapar(yazi_donusu, sayfa_donusu):
    doc = pymupdf.open()
    page = doc.new_page()
    page.insert_text((200, 400), "Bu uzun bir deneme cümlesidir okunur olmalı", fontsize=14, rotate=yazi_donusu)
    page.set_rotation(sayfa_donusu)
    düzeltilecek = g.PDFProcessor.auto_rotate(doc, dry_run=True)
    beklenen_duzeltme = (yazi_donusu - sayfa_donusu) % 360  # metin dönüşü ile sayfa dönüşü farkı
    if beklenen_duzeltme == 0:
        assert düzeltilecek == {}
    else:
        assert len(düzeltilecek) == 1
        g.PDFProcessor.auto_rotate(doc)
        assert g.PDFProcessor.detect_page_fix(doc[0]) == 0  # düzeltmeden sonra tekrar düzeltme gerekmez


def test_turkce_katlama_i_harfleri():
    assert g.turkish_fold("İMZALA") in g.turkish_fold("PDF'yi Dijital Olarak imzala…")
    assert g.turkish_fold("ISIK") == g.turkish_fold("ısık") == g.turkish_fold("isik")
