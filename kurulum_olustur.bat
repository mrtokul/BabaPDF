@echo off
chcp 65001 > nul
cd /d "%~dp0"

echo ==========================================
echo Baba PDF KURULUM (setup) DOSYASI OLUSTURUCU
echo ==========================================
echo Sirasi: 1) EXE derlenir  2) EXE imzalanir  3) Kurulum paketi (Inno Setup) olusur ve imzalanir.
echo Onkosul: Python, Inno Setup 6 ve Windows SDK (signtool). Kurulu degilse asagida hata verir.
echo.

if not exist pdf_gui.py goto missing_py
if not exist kurulum\BabaPDF.iss goto missing_iss

set "ISCC="
if exist "%ProgramFiles(x86)%\Inno Setup 6\ISCC.exe" set "ISCC=1"
if exist "%ProgramFiles%\Inno Setup 6\ISCC.exe" set "ISCC=1"
if exist "%LOCALAPPDATA%\Programs\Inno Setup 6\ISCC.exe" set "ISCC=1"
if not defined ISCC goto missing_inno

echo [1/2] EXE derleniyor, birkac dakika surebilir...
python -m pip install -r requirements-build.txt
if errorlevel 1 goto pip_failed
rem Eski dist ciktisi acik bir Baba_PDF.exe ya da klasor penceresi yuzunden kilitli kalabilir: once kapat ve temizle.
taskkill /f /im Baba_PDF.exe >nul 2>&1
if exist "dist\Baba_PDF" rmdir /s /q "dist\Baba_PDF" >nul 2>&1
if exist "dist\Baba_PDF" goto dist_locked
set PDF_GUI_DEBUG=0
set PDF_GUI_ONEFILE=
set "BABA_WORK=%LOCALAPPDATA%\BabaPDF_build"
if exist "%BABA_WORK%" rmdir /s /q "%BABA_WORK%"
python -m PyInstaller --clean --noconfirm --workpath "%BABA_WORK%" pdf_gui.spec
if errorlevel 1 goto build_failed

echo.
echo [2/2] Kurulum paketi hazirlaniyor ve imzalaniyor...
powershell -NoProfile -ExecutionPolicy Bypass -File "kurulum\imzala_ve_paketle.ps1" -SertifikaOlustur
if errorlevel 1 goto pack_failed

echo.
echo ==========================================
echo Tamamlandi! Kurulum dosyasi: dist\BabaPDF-Kurulum-SURUM.exe
echo (SURUM, pdf_gui.py icindeki APP_VERSION degeridir.)
echo ==========================================
pause
exit /b 0

:dist_locked
echo HATA: dist\Baba_PDF klasoru silinemedi (Erisim engellendi).
echo Acik Baba PDF programini ve dist klasorunu gosteren Gezgin pencerelerini kapatin,
echo gerekirse klasoru elle silin ve tekrar calistirin.
pause
exit /b 1

:missing_py
echo HATA: pdf_gui.py bu klasorde bulunamadi.
pause
exit /b 1

:missing_iss
echo HATA: kurulum\BabaPDF.iss bulunamadi.
pause
exit /b 1

:missing_inno
echo HATA: Inno Setup 6 kurulu degil. https://jrsoftware.org/isdl.php adresinden kurup tekrar calistirin.
pause
exit /b 1

:pip_failed
echo HATA: Paketler yuklenemedi. Internet baglantisini ve Python kurulumunu kontrol edin.
pause
exit /b 1

:build_failed
echo HATA: EXE olusturulamadi. Yukaridaki mesajlara bakin.
pause
exit /b 1

:pack_failed
echo HATA: Kurulum paketi olusturulamadi. Windows SDK (signtool) ve Inno Setup kurulu mu kontrol edin.
pause
exit /b 1
