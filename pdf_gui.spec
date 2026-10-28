# -*- mode: python ; coding: utf-8 -*-
# build_exe.bat tarafindan calistirilir. Ikon ve gerekli paketler burada tanimlidir.
import os
from PyInstaller.utils.hooks import collect_all

# build_exe.bat debug  ->  konsol penceresi acik exe uretir (hatalari gormek icin)
debug_console = os.environ.get("PDF_GUI_DEBUG") == "1"
# Varsayilan: klasor (onedir) modu, acilista dosya cikarmaz, daha hizli acilir.
# PDF_GUI_ONEFILE=1  ->  eski tek dosya EXE.
onefile = os.environ.get("PDF_GUI_ONEFILE") == "1"

# app_icon.png programin icinde pencere ikonu olarak kullanilir (resource_path ile bulunur)
datas = [("app_icon.png", "."), ("app_icon.ico", "."), ("LICENSE.txt", "."), ("NOTICE.txt", ".")]
binaries = []
hiddenimports = ["fitz", "pymupdf", "imghdr"]
# Tesseract OCR motoru ve İngilizce/Türkçe dil verileri EXE içine alınır.
tesseract_root = os.environ.get("TESSERACT_ROOT", r"C:\Program Files\Tesseract-OCR")
if os.path.isdir(tesseract_root):
    for root, _, files in os.walk(tesseract_root):
        for filename in files:
            source = os.path.join(root, filename)
            relative = os.path.relpath(source, tesseract_root)
            datas.append((source, os.path.join("tesseract", os.path.dirname(relative))))
for pkg in ("pdfplumber", "pdfminer", "pypdfium2", "pymupdf", "PIL", "pytesseract", "tkinterdnd2", "pyhanko", "asn1crypto", "cryptography", "xsdata", "toposort", "mobi", "loguru", "docx", "pptx", "openpyxl", "et_xmlfile", "xlsxwriter"):
    try:
        d, b, h = collect_all(pkg)
        datas += d
        binaries += b
        hiddenimports += h
    except Exception as exc:
        print(f"UYARI: {pkg} toplanamadi: {exc}")

a = Analysis(
    ["pdf_gui.py"],
    pathex=[],
    binaries=binaries,
    datas=datas,
    hiddenimports=hiddenimports,
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[],
    noarchive=False,
    optimize=0,
)
pyz = PYZ(a.pure)

exe = EXE(
    pyz,
    a.scripts,
    *([a.binaries, a.datas] if onefile else []),
    [],
    exclude_binaries=not onefile,
    name="Baba_PDF",
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=False,  # UPX bazen exe'yi bozar ve antivirus yanlis alarmini artirir
    upx_exclude=[],
    runtime_tmpdir=None,
    console=debug_console,
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
    icon="app_icon.ico",  # exe dosyasinin Explorer'daki ikonu
)

if not onefile:
    coll = COLLECT(
        exe,
        a.binaries,
        a.datas,
        strip=False,
        upx=False,
        upx_exclude=[],
        name="Baba_PDF",
    )
