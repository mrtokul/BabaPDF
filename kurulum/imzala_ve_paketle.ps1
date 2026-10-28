# Baba PDF: EXE'yi imzalar, kurulum paketini derler ve kurulum paketini imzalar.
# Önkoşul: dist\Baba_PDF.exe (build_exe.bat), Inno Setup 6, Windows SDK signtool.
# İmza sertifikası "CN=Baba PDF" konusuyla Cert:\CurrentUser\My içinde aranır; yoksa -SertifikaOlustur ile kendinden imzalı
# sertifika üretilir. Özel anahtar dışa aktarılmaz ve bu klasöre/depoya yazılmaz.
param([switch]$SertifikaOlustur)
$ErrorActionPreference = "Stop"
$kok = Split-Path -Parent $PSScriptRoot
$konu = "CN=Baba PDF, O=Baba PDF"

$sert = Get-ChildItem Cert:\CurrentUser\My -CodeSigningCert | Where-Object { $_.Subject -eq $konu -and $_.NotAfter -gt (Get-Date) } |
    Sort-Object NotAfter -Descending | Select-Object -First 1
if (-not $sert) {
    if (-not $SertifikaOlustur) { throw "İmza sertifikası yok. -SertifikaOlustur ile çalıştırın." }
    $sert = New-SelfSignedCertificate -Type CodeSigningCert -Subject $konu -KeyUsage DigitalSignature -KeyAlgorithm RSA `
        -KeyLength 3072 -HashAlgorithm SHA256 -CertStoreLocation Cert:\CurrentUser\My -NotAfter (Get-Date).AddYears(5)
}
Export-Certificate -Cert $sert -FilePath (Join-Path $PSScriptRoot "BabaPDF-yayinci.cer") | Out-Null

$signtool = Get-ChildItem "${env:ProgramFiles(x86)}\Windows Kits\10\bin" -Recurse -Filter signtool.exe -ErrorAction SilentlyContinue |
    Where-Object { $_.FullName -match "\\x64\\" } | Sort-Object FullName -Descending | Select-Object -First 1
if (-not $signtool) { throw "signtool.exe bulunamadı (Windows SDK)." }
$iscc = @("${env:ProgramFiles(x86)}\Inno Setup 6\ISCC.exe", "$env:ProgramFiles\Inno Setup 6\ISCC.exe", "$env:LOCALAPPDATA\Programs\Inno Setup 6\ISCC.exe") |
    Where-Object { Test-Path $_ } | Select-Object -First 1
if (-not $iscc) { throw "Inno Setup 6 (ISCC.exe) bulunamadı." }

$exe = Join-Path $kok "dist\Baba_PDF\Baba_PDF.exe"
$tek = Join-Path $kok "dist\Baba_PDF.exe"
if (-not (Test-Path $exe) -and (Test-Path $tek)) {
    # Klasör (onedir) paketi yok ama tek dosya EXE var: kurulum paketi için klasöre koy.
    New-Item -ItemType Directory -Force -Path (Split-Path $exe) | Out-Null
    Copy-Item $tek $exe -Force
    Write-Host "Tek dosya EXE dist\Baba_PDF\ klasörüne kopyalandı."
}
if (-not (Test-Path $exe)) { throw "dist\Baba_PDF\Baba_PDF.exe yok; önce build_exe.bat çalıştırın." }
$surum = (Select-String -Path (Join-Path $kok "pdf_gui.py") -Pattern '^APP_VERSION = "([^"]+)"').Matches[0].Groups[1].Value

& $signtool.FullName sign /sha1 $sert.Thumbprint /fd SHA256 /d "Baba PDF" $exe
if ($LASTEXITCODE) { throw "EXE imzalanamadı." }

& $iscc "/DAppVersion=$surum" "/DCertThumb=$($sert.Thumbprint)" (Join-Path $PSScriptRoot "BabaPDF.iss")
if ($LASTEXITCODE) { throw "Kurulum paketi derlenemedi." }

$kurulum = Join-Path $kok "dist\BabaPDF-Kurulum-$surum.exe"
& $signtool.FullName sign /sha1 $sert.Thumbprint /fd SHA256 /d "Baba PDF Kurulum" $kurulum
if ($LASTEXITCODE) { throw "Kurulum paketi imzalanamadı." }
Get-AuthenticodeSignature $exe, $kurulum | Select-Object Path, Status, @{n="Imzalayan";e={$_.SignerCertificate.Subject}} | Format-Table -AutoSize
Write-Host "Hazır: $kurulum"
