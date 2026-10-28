@echo off
chcp 65001 > nul
cd /d "%~dp0"

echo ==========================================
echo PDF Isleyici TEK DOSYA (bagimsiz) EXE Donusturucu
echo ==========================================

if not exist pdf_gui.py goto missing_py
if not exist app_icon.ico goto missing_ico
if not exist app_icon.png goto missing_png

echo.
echo Gerekli paketler kontrol ediliyor...
if not exist requirements-build.txt goto missing_req
python -m pip install -r requirements-build.txt
if errorlevel 1 goto pip_failed

set PDF_GUI_ONEFILE=1
rem Acik Baba_PDF.exe dosyasi derlemeyi engeller: once kapat.
taskkill /f /im Baba_PDF.exe >nul 2>&1
if exist "dist\Baba_PDF.exe" del /f /q "dist\Baba_PDF.exe" >nul 2>&1
if exist "dist\Baba_PDF.exe" goto dist_locked
set PDF_GUI_DEBUG=0
if /i "%~1"=="debug" set PDF_GUI_DEBUG=1
if "%PDF_GUI_DEBUG%"=="1" echo Hata ayiklama modu: konsol penceresi acik olacak.

echo.
echo EXE olusturuluyor, birkac dakika surebilir...
rem Gecici dosyalar Masaustu disinda tutulur (OneDrive/Defender kilitleri "Erisim engellendi" hatasi verebilir).
set "BABA_WORK=%LOCALAPPDATA%\BabaPDF_build"
if exist "%BABA_WORK%" rmdir /s /q "%BABA_WORK%"
python -m PyInstaller --clean --noconfirm --workpath "%BABA_WORK%" pdf_gui.spec
if errorlevel 1 goto build_failed

echo.
echo ==========================================
echo Islem Tamamlandi!
echo dist\Baba_PDF.exe  ->  tek basina calisir, istediginiz yere kopyalayabilirsiniz.
echo Ikon eski gorunurse exe dosyasini baska bir klasore kopyalayin.
echo Program acilmazsa:  build_exe.bat debug  ile derleyip hatayi gorun.
echo ==========================================
pause
exit /b 0

:dist_locked
echo HATA: dist\Baba_PDF.exe dosyasi silinemedi (Erisim engellendi).
echo Acik Baba PDF programini ve dist klasorunu gosteren pencereleri kapatin,
echo gerekirse dosyayi elle silin ve tekrar calistirin.
pause
exit /b 1

:missing_py
echo HATA: pdf_gui.py bu klasorde bulunamadi.
pause
exit /b 1

:missing_ico
echo HATA: app_icon.ico bu klasorde bulunamadi.
pause
exit /b 1

:missing_png
echo HATA: app_icon.png bu klasorde bulunamadi.
pause
exit /b 1

:missing_req
echo HATA: requirements-build.txt bu klasorde bulunamadi.
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




