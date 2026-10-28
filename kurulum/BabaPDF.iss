; Baba PDF kurulum betiği (Inno Setup 6). Derleme: kurulum\imzala_ve_paketle.ps1
; Kullanıcı bazlı kurulum: yönetici hakkı gerekmez, yalnızca bu Windows hesabını etkiler.
#ifndef AppVersion
  #define AppVersion "1.0.0"
#endif
#ifndef CertThumb
  #define CertThumb ""
#endif

[Setup]
AppId={{8A1D3C52-4D0A-4F6B-9E21-BABA00F00001}
AppName=Baba PDF
AppVersion={#AppVersion}
AppPublisher=Baba PDF
DefaultDirName={autopf}\Baba PDF
DefaultGroupName=Baba PDF
PrivilegesRequired=lowest
LicenseFile=..\LICENSE.txt
InfoBeforeFile=..\NOTICE.txt
OutputDir=..\dist
OutputBaseFilename=BabaPDF-Kurulum-{#AppVersion}
SetupIconFile=..\app_icon.ico
UninstallDisplayIcon={app}\Baba_PDF.exe
Compression=lzma2
SolidCompression=yes
WizardStyle=modern
ChangesAssociations=yes
SetupMutex=BabaPDFKurulumMutex,Global\BabaPDFKurulumMutex
AppMutex=BabaPDFCalisiyorMutex
ArchitecturesInstallIn64BitMode=x64compatible
; İmza, imzala_ve_paketle.ps1 tarafından ayrıca atılır.

[Languages]
Name: "turkish"; MessagesFile: "compiler:Languages\Turkish.isl"

[Tasks]
Name: "desktopicon"; Description: "Masaüstü kısayolu oluştur"; GroupDescription: "Kısayollar:"
Name: "pdfassoc"; Description: "Baba PDF'i PDF ve e-kitap (EPUB, MOBI, AZW3, IBA, RTF) dosyaları için varsayılan program yapmak istiyor musunuz?"; GroupDescription: "PDF ve e-kitap dosyaları:"; Flags: unchecked
#if CertThumb != ""
Name: "trustcert"; Description: "Yayıncıyı (Baba PDF) bu kullanıcı hesabı için güvenilir say (kendinden imzalı sertifika; Windows bir onay penceresi gösterebilir)"; GroupDescription: "Güven:"
#endif

[Files]
; Klasör (onedir) paketi: Baba_PDF.exe + _internal\ ; açılışta dosya çıkarılmadığı için tek dosya EXE'den çok daha hızlı açılır.
Source: "..\dist\Baba_PDF\*"; DestDir: "{app}"; Flags: ignoreversion recursesubdirs createallsubdirs
Source: "..\LICENSE.txt"; DestDir: "{app}"; Flags: ignoreversion
Source: "..\NOTICE.txt"; DestDir: "{app}"; Flags: ignoreversion
Source: "BabaPDF-yayinci.cer"; DestDir: "{app}"; Flags: ignoreversion
Source: "BabaPDF-yayinci.cer"; DestDir: "{app}\kaynak\kurulum"; Flags: ignoreversion
; AGPL-3.0 kaynak kodu sunumu: kaynak ve derleme betikleri programla birlikte kurulur.
Source: "..\pdf_gui.py"; DestDir: "{app}\kaynak"; Flags: ignoreversion
Source: "..\pdf_gui.spec"; DestDir: "{app}\kaynak"; Flags: ignoreversion
Source: "..\build_exe.bat"; DestDir: "{app}\kaynak"; Flags: ignoreversion
Source: "..\kontrol.bat"; DestDir: "{app}\kaynak"; Flags: ignoreversion
Source: "..\requirements-build.txt"; DestDir: "{app}\kaynak"; Flags: ignoreversion
Source: "..\requirements-dev.txt"; DestDir: "{app}\kaynak"; Flags: ignoreversion
Source: "..\app_icon.ico"; DestDir: "{app}\kaynak"; Flags: ignoreversion
Source: "..\app_icon.png"; DestDir: "{app}\kaynak"; Flags: ignoreversion
Source: "..\LICENSE.txt"; DestDir: "{app}\kaynak"; Flags: ignoreversion
Source: "..\README.md"; DestDir: "{app}\kaynak"; Flags: ignoreversion
Source: "..\.gitignore"; DestDir: "{app}\kaynak"; Flags: ignoreversion
Source: "..\NOTICE.txt"; DestDir: "{app}\kaynak"; Flags: ignoreversion
Source: "..\tests\*.py"; DestDir: "{app}\kaynak\tests"; Flags: ignoreversion
Source: "BabaPDF.iss"; DestDir: "{app}\kaynak\kurulum"; Flags: ignoreversion
Source: "imzala_ve_paketle.ps1"; DestDir: "{app}\kaynak\kurulum"; Flags: ignoreversion

[Icons]
Name: "{group}\Baba PDF"; Filename: "{app}\Baba_PDF.exe"
Name: "{group}\Kaynak kodu (AGPL-3.0)"; Filename: "{app}\kaynak"
Name: "{group}\Baba PDF'i kaldır"; Filename: "{uninstallexe}"
Name: "{autodesktop}\Baba PDF"; Filename: "{app}\Baba_PDF.exe"; Tasks: desktopicon

[Registry]
; PDF işleyicisi olarak kayıt (yalnızca bu kullanıcı). Varsayılan seçimi Windows'ta kullanıcı onaylar.
Root: HKCU; Subkey: "Software\Classes\BabaPDF.Document"; ValueType: string; ValueData: "PDF Belgesi (Baba PDF)"; Flags: uninsdeletekey; Tasks: pdfassoc
Root: HKCU; Subkey: "Software\Classes\BabaPDF.Document\DefaultIcon"; ValueType: string; ValueData: "{app}\Baba_PDF.exe,0"; Tasks: pdfassoc
Root: HKCU; Subkey: "Software\Classes\BabaPDF.Document\shell\open\command"; ValueType: string; ValueData: """{app}\Baba_PDF.exe"" ""%1"""; Tasks: pdfassoc
Root: HKCU; Subkey: "Software\Classes\.pdf\OpenWithProgids"; ValueType: none; ValueName: "BabaPDF.Document"; ValueData: ""; Flags: uninsdeletevalue; Tasks: pdfassoc
Root: HKCU; Subkey: "Software\Classes\BabaPDF.Epub"; ValueType: string; ValueData: "EPUB Kitabı (Baba PDF)"; Flags: uninsdeletekey; Tasks: pdfassoc
Root: HKCU; Subkey: "Software\Classes\BabaPDF.Epub\DefaultIcon"; ValueType: string; ValueData: "{app}\Baba_PDF.exe,0"; Tasks: pdfassoc
Root: HKCU; Subkey: "Software\Classes\BabaPDF.Epub\shell\open\command"; ValueType: string; ValueData: """{app}\Baba_PDF.exe"" ""%1"""; Tasks: pdfassoc
Root: HKCU; Subkey: "Software\Classes\.epub\OpenWithProgids"; ValueType: none; ValueName: "BabaPDF.Epub"; ValueData: ""; Flags: uninsdeletevalue; Tasks: pdfassoc
Root: HKCU; Subkey: "Software\BabaPDF"; ValueType: none; Flags: uninsdeletekey; Tasks: pdfassoc
Root: HKCU; Subkey: "Software\BabaPDF\Capabilities"; ValueType: string; ValueName: "ApplicationName"; ValueData: "Baba PDF"; Tasks: pdfassoc
Root: HKCU; Subkey: "Software\BabaPDF\Capabilities"; ValueType: string; ValueName: "ApplicationDescription"; ValueData: "PDF ve e-kitap görüntüleme, PDF düzenleme"; Tasks: pdfassoc
Root: HKCU; Subkey: "Software\BabaPDF\Capabilities\FileAssociations"; ValueType: string; ValueName: ".pdf"; ValueData: "BabaPDF.Document"; Tasks: pdfassoc
Root: HKCU; Subkey: "Software\BabaPDF\Capabilities\FileAssociations"; ValueType: string; ValueName: ".epub"; ValueData: "BabaPDF.Epub"; Tasks: pdfassoc
Root: HKCU; Subkey: "Software\Classes\BabaPDF.Book"; ValueType: string; ValueData: "E-Kitap / Belge (Baba PDF)"; Flags: uninsdeletekey; Tasks: pdfassoc
Root: HKCU; Subkey: "Software\Classes\BabaPDF.Book\DefaultIcon"; ValueType: string; ValueData: "{app}\Baba_PDF.exe,0"; Tasks: pdfassoc
Root: HKCU; Subkey: "Software\Classes\BabaPDF.Book\shell\open\command"; ValueType: string; ValueData: """{app}\Baba_PDF.exe"" ""%1"""; Tasks: pdfassoc
Root: HKCU; Subkey: "Software\Classes\.mobi\OpenWithProgids"; ValueType: none; ValueName: "BabaPDF.Book"; ValueData: ""; Flags: uninsdeletevalue; Tasks: pdfassoc
Root: HKCU; Subkey: "Software\Classes\.azw3\OpenWithProgids"; ValueType: none; ValueName: "BabaPDF.Book"; ValueData: ""; Flags: uninsdeletevalue; Tasks: pdfassoc
Root: HKCU; Subkey: "Software\Classes\.azw\OpenWithProgids"; ValueType: none; ValueName: "BabaPDF.Book"; ValueData: ""; Flags: uninsdeletevalue; Tasks: pdfassoc
Root: HKCU; Subkey: "Software\Classes\.iba\OpenWithProgids"; ValueType: none; ValueName: "BabaPDF.Book"; ValueData: ""; Flags: uninsdeletevalue; Tasks: pdfassoc
Root: HKCU; Subkey: "Software\Classes\.rtf\OpenWithProgids"; ValueType: none; ValueName: "BabaPDF.Book"; ValueData: ""; Flags: uninsdeletevalue; Tasks: pdfassoc
Root: HKCU; Subkey: "Software\BabaPDF\Capabilities\FileAssociations"; ValueType: string; ValueName: ".mobi"; ValueData: "BabaPDF.Book"; Tasks: pdfassoc
Root: HKCU; Subkey: "Software\BabaPDF\Capabilities\FileAssociations"; ValueType: string; ValueName: ".azw3"; ValueData: "BabaPDF.Book"; Tasks: pdfassoc
Root: HKCU; Subkey: "Software\BabaPDF\Capabilities\FileAssociations"; ValueType: string; ValueName: ".azw"; ValueData: "BabaPDF.Book"; Tasks: pdfassoc
Root: HKCU; Subkey: "Software\BabaPDF\Capabilities\FileAssociations"; ValueType: string; ValueName: ".iba"; ValueData: "BabaPDF.Book"; Tasks: pdfassoc
Root: HKCU; Subkey: "Software\BabaPDF\Capabilities\FileAssociations"; ValueType: string; ValueName: ".rtf"; ValueData: "BabaPDF.Book"; Tasks: pdfassoc
Root: HKCU; Subkey: "Software\RegisteredApplications"; ValueType: string; ValueName: "BabaPDF"; ValueData: "Software\BabaPDF\Capabilities"; Flags: uninsdeletevalue; Tasks: pdfassoc

[Run]
#if CertThumb != ""
Filename: "powershell.exe"; Parameters: "-NoProfile -ExecutionPolicy Bypass -Command ""$c='{app}\BabaPDF-yayinci.cer'; Import-Certificate -FilePath $c -CertStoreLocation Cert:\CurrentUser\TrustedPublisher | Out-Null; Import-Certificate -FilePath $c -CertStoreLocation Cert:\CurrentUser\Root | Out-Null"""; Flags: runhidden waituntilterminated; Tasks: trustcert; StatusMsg: "Yayıncı sertifikası güvenilir olarak ekleniyor..."
#endif
; Windows varsayılan programı sessizce değiştirmeye izin vermez: Varsayılan uygulamalar ekranını açar.
Filename: "ms-settings:defaultapps"; Flags: shellexec nowait postinstall skipifsilent; Tasks: pdfassoc; Description: "Windows'ta PDF ve e-kitap dosyaları için Baba PDF'i seçmek üzere Varsayılan uygulamalar ekranını aç"
Filename: "{app}\Baba_PDF.exe"; Flags: nowait postinstall skipifsilent; Description: "Baba PDF'i başlat"

[UninstallRun]
#if CertThumb != ""
Filename: "powershell.exe"; Parameters: "-NoProfile -ExecutionPolicy Bypass -Command ""Remove-Item 'Cert:\CurrentUser\TrustedPublisher\{#CertThumb}','Cert:\CurrentUser\Root\{#CertThumb}' -ErrorAction SilentlyContinue"""; Flags: runhidden waituntilterminated; RunOnceId: "BabaPdfSertifikaKaldir"
#endif

[Code]
const
  UninstKey = 'Software\Microsoft\Windows\CurrentVersion\Uninstall\{8A1D3C52-4D0A-4F6B-9E21-BABA00F00001}_is1';

// Kayıtlı (veya varsayılan klasördeki) önceki kurulumun kaldırıcısını bulur.
function FindOldUninstaller(var Cmd: String; var Ver: String): Boolean;
begin
  Cmd := '';
  Ver := '';
  if not RegQueryStringValue(HKCU, UninstKey, 'UninstallString', Cmd) then
    if not RegQueryStringValue(HKLM, UninstKey, 'UninstallString', Cmd) then
      Cmd := '';
  if Cmd <> '' then
  begin
    Cmd := RemoveQuotes(Cmd);
    if not RegQueryStringValue(HKCU, UninstKey, 'DisplayVersion', Ver) then
      RegQueryStringValue(HKLM, UninstKey, 'DisplayVersion', Ver);
  end
  else if FileExists(ExpandConstant('{autopf}\Baba PDF\unins000.exe')) then
    Cmd := ExpandConstant('{autopf}\Baba PDF\unins000.exe');
  Result := (Cmd <> '') and FileExists(Cmd);
end;

function InitializeSetup(): Boolean;
var
  Cmd, Ver, Info: String;
  Code, I: Integer;
begin
  Result := True;
  if not FindOldUninstaller(Cmd, Ver) then
    Exit;
  if Ver <> '' then
    Info := ' (sürüm ' + Ver + ')'
  else
    Info := '';
  if SuppressibleMsgBox('Baba PDF bu bilgisayarda zaten kurulu' + Info + '.' + #13#10#13#10 +
       'Yeni sürümü kurmadan önce eski kurulum kaldırılacak. Ayarlarınız ve belgeleriniz silinmez.' + #13#10#13#10 +
       'Eski kurulumu kaldırıp yenisini kurmak istiyor musunuz?', mbConfirmation, MB_YESNO, IDYES) <> IDYES then
  begin
    Result := False;
    Exit;
  end;
  if not Exec(Cmd, '/SILENT /NORESTART', '', SW_SHOW, ewWaitUntilTerminated, Code) or (Code <> 0) then
  begin
    SuppressibleMsgBox('Eski kurulum kaldırılamadı. Kurulum durduruldu; Windows ayarlarından Baba PDF''i kaldırıp tekrar deneyin.', mbError, MB_OK, IDOK);
    Result := False;
    Exit;
  end;
  // Inno kaldırıcısı kendini geçici kopyayla yeniden başlatıp çıkabilir: bitene kadar bekle (en çok 60 sn).
  for I := 1 to 120 do
  begin
    if not FileExists(Cmd) then
      Break;
    Sleep(500);
  end;
  if FileExists(Cmd) then
  begin
    SuppressibleMsgBox('Eski kurulum 60 saniyede kaldırılamadı. Kurulum durduruldu.', mbError, MB_OK, IDOK);
    Result := False;
  end;
end;
