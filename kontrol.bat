@echo off
rem Tek komutlu kalite kapisi: derleme denetimi + eksik/tanimsiz ad denetimi + testler.
rem Her adim basarili degilse cikis kodu 1 doner. Surumden once calistirin.
cd /d "%~dp0"

echo [1/3] Soz dizimi denetimi...
python -X utf8 -m py_compile pdf_gui.py
if errorlevel 1 goto basarisiz

echo [2/3] Eksik ad denetimi (pyflakes)...
python -m pyflakes pdf_gui.py
if errorlevel 1 goto basarisiz

echo [3/3] Testler...
python -X utf8 -m pytest tests -q
if errorlevel 1 goto basarisiz

echo.
echo KONTROL BASARILI
exit /b 0

:basarisiz
echo.
echo KONTROL BASARISIZ: yukaridaki ilk hatayi duzeltin.
exit /b 1
