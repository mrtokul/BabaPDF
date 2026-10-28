# Baba PDF — kaynak kodu

PDF görüntüleme, düzenleme, birleştirme, bölme, sıkıştırma, OCR, şifreleme ve dijital imza programı; ayrıca EPUB, MOBI, AZW3, IBA, RTF, FB2, XPS, CBZ ve SVG belgelerini okur (Windows, Tkinter + PyMuPDF).
Belgeler bilgisayardan çıkmaz; program kendiliğinden ağa bağlanmaz.

**Lisans:** AGPL-3.0 (`LICENSE.txt`, `NOTICE.txt`). PyMuPDF AGPL olduğu için program da AGPL ile dağıtılır.
Değiştirilmiş sürümü başkalarına sunarsanız kaynak kodunu da aynı lisansla sunmalısınız.

## Klasör yapısı

| Yol | Ne işe yarar |
|---|---|
| `pdf_gui.py` | Programın tamamı (arayüz + PDF işlemleri) |
| `pdf_gui.spec`, `build_exe.bat` | PyInstaller ile klasör (onedir) paketi üretimi: `dist\Baba_PDF\` (eski tek dosya için `PDF_GUI_ONEFILE=1`) |
| `build_tek_exe.bat` | Bağımsız tek dosya EXE üretir: `dist\Baba_PDF.exe` (başka klasöre/bilgisayara tek başına kopyalanabilir; açılış ≈ 14 sn) |
| `kontrol.bat` | Tek komutlu kalite kapısı: sözdizimi + pyflakes + testler (sürümden önce) |
| `requirements-build.txt` | Derleme için sabitlenmiş paket sürümleri |
| `requirements-dev.txt` | Derleme paketleri + `pytest` + `pyflakes` |
| `tests/` | Çekirdek işlev ve paket bütünlüğü testleri (arayüz açmaz) |
| `kurulum/BabaPDF.iss` | Inno Setup kurulum betiği (lisans sayfası, eski kurulumu kaldırma, PDF işleyici kaydı) |
| `kurulum/imzala_ve_paketle.ps1` | EXE’yi imzalar, kurulum paketini derler ve imzalar |
| `kurulum/BabaPDF-yayinci.cer` | Yalnızca ortak sertifika (özel anahtar burada **yoktur**) |

## Araçlar menüsü (çekirdek işlevler `PDFProcessor` içinde, testli)

Menü ilkesi: her işlev tek yerde, göreve göre gruplanır. **Dosya ▸ Dışa Aktar:** yeni dosya üreten her şey (metin, resim, sayfa aralığı, kitapçık, çok sayfalı düzen, tek uzun sayfa). **Düzenle ▸ Sayfalar** (döndür, otomatik döndür, sil, boş sayfa sil, ekle/böl/birleştir, boyut, kırp, üst-alt bilgi); **Filigran, Damga ve Bindirme**; **Açıklamalar** (düzleştirme dahil); **Yer İmleri** (ekle; göster/düzenle/sil tek pencerede). **Güvenlik ve İmza:** şifre, izin, kalıcı karartma, gizli veri ve belge bilgisi temizliği, imza. **Araçlar:** küçült, doğrula, onar, belge bilgisi/metadata, görseller, iki PDF karşılaştırma, gömülü ekler. Düzenle ▸ Komut Ara (Ctrl+K) tüm menü komutlarını arar. Açılış sayfasında (belge yokken) belgeye bağlı öğeler kapalıdır; yalnızca PDF Aç, Birleştir, Toplu Metin, Komut Ara, Görünüm ve Yardım açıktır. 1.4.0'da yinelenen üç öğe silindi (Metadata Temizle ⊂ Gizli Verileri Temizle; Yer İmlerini Göster ve Son Yer İmini Sil ⊂ yer imi düzenleyici). Fikirler Stirling PDF'nin araç listesinden alınmıştır (kod kopyalanmamıştır).

**Görünüm, gezinti ve yeni araçlar:** sayfadaki bağlantılara tek tıkla gidilir (iç bağlantılar sayfaya/noktaya atlar; dış bağlantılar yalnızca http/https/mailto ve onayla açılır; üzerine gelince hedef balonda görünür). *Alt+←/→* bağlantıdan önceki/sonraki konuma döner. *Görünüm ▸ İçindekiler Paneli* (F4, araç çubuğunda 📑) yer imi ağacını gösterir. *Görünüm ▸ Katmanlar…* PDF katmanlarını açıp kapatır. *Dosya ▸ Dışa Aktar ▸ Resimlerden PDF Oluştur…* resimleri sıralayıp tek PDF yapar (açılış sayfasında kartı ve duyuru şeridi vardır; resim sürükleyip bırakmak da açar). Sayfa sıralama panelinde (☰) sürükle-bırak ekleme çizgisi, kenarda otomatik kaydırma ve çoklu seçili sayfaları birlikte taşıma vardır.

**Kırpma, sayfa ekleme/silme:** *Düzenle ▸ Sayfalar ▸ Alan Seçerek Kırp* (araç çubuğunda ✂) sayfada tutulacak alanı sürükleyerek seçtirir (bu sayfa ya da tüm sayfalar); *Kırpmayı Kaldır* kırpma kutusunu eski haline getirir (içerik silinmediği için kayıpsızdır); *Boş Sayfa Ekle* ve *Sayfa Aralığını Sil* (örn. `1-3, 5`) sayfaları ekler/siler. Hepsi Ctrl+Z ile geri alınır.

**Office biçiminde kaydet (Dosya ▸ Office Biçiminde Kaydet):** Word (.docx; metin, kalın/italik/punto ve resimler düzenlenebilir ya da sayfa başına tek resim), Excel (.xlsx; sayfalardaki tablolar ayrı sayfalara, tablo yoksa metin satır satır) ve PowerPoint (.pptx; sayfa başına slayt, düzenlenebilir metin kutuları ya da tek resim; metin notlarda). Tarama (metinsiz) sayfalar Word'de resim olarak konur; OCR için önce *OCR ile Metin* kullanın. Kütüphaneler: python-docx, openpyxl, python-pptx (`requirements-build.txt`).

**Açılış sayfası:** menülerdeki her özelliğin kartı ya da düğmesi vardır; liste `_welcome_feature_groups` içindedir ve `tests/test_acilis_ozellikleri.py` yeni bir menü komutu eklenip buraya konmazsa başarısız olur.

## Desteklenen biçimler

| Biçim | Nasıl açılır |
|---|---|
| PDF | Doğrudan (PyMuPDF) |
| EPUB, FB2 | PyMuPDF akışlı belgeyi sayfalara dizer, sayfalı PDF üretir |
| XPS/OXPS, CBZ, SVG | Sabit sayfalıdır; PyMuPDF olduğu gibi PDF'e dönüştürür (yazı/sayfa boyutu ayarı etkilemez) |
| MOBI, AZW3 (.azw) | `mobi` paketi (KindleUnpack) EPUB'a açar, sonra EPUB ile aynı yol; DRM'li kitaplar açılmaz |
| RTF | Kendi okuyucumuz (`rtf_to_html`): paragraf, kalın/italik/altı çizili, hizalama, tablo, PNG/JPEG resim, Unicode ve Windows kod sayfaları (Türkçe dahil) |
| IBA (iBooks Author) | Kendi okuyucumuz (`iba_to_html`): paketteki `index.xml(.gz)` paragrafları ve `Data/` resimleri; widget/etkileşimli öğeler okunmaz |

PDF olmayan her biçim sayfalı PDF'e çevrilir (kitabın yanına `ad.pdf`, EPUB dışındakiler için `ad_mobi.pdf`, `ad_rtf.pdf` vb.; ayar kapalıysa uygulama klasörüne). Yazı ve sayfa boyutu *Görünüm ▸ E-Kitap Okuma Ayarları*'ndan seçilir. Açılış sayfasında her biçim için ayrı bir kutu vardır.

## Derleme ve test

Önkoşul: Python 3.12, Tesseract OCR (`C:\Program Files\Tesseract-OCR`, İngilizce + Türkçe dil verisi; EXE’nin içine alınır).

```bat
python -m pip install -r requirements-dev.txt
kontrol.bat
build_exe.bat
```

Kurulum paketi için ayrıca Inno Setup 6 ve Windows SDK `signtool` gerekir:

```powershell
powershell -ExecutionPolicy Bypass -File kurulum\imzala_ve_paketle.ps1 -SertifikaOlustur
```

Çıktı: `dist\BabaPDF-Kurulum-<sürüm>.exe`. Dağıtım için yalnızca bu dosya yeterlidir; tek başına `Baba_PDF.exe` lisans, kaynak ve kaldırıcı içermez.

## Sürüm yükseltirken

**Kural:** her EXE derlemesinden önce sürüm uygun şekilde yükseltilir (yeni özellik → MINOR, düzeltme → PATCH, büyük/uyumsuz değişiklik → MAJOR) ve `SURUM_NOTLARI.md` güncellenir.

1. `pdf_gui.py` içinde `APP_VERSION` / `APP_DATE` değerlerini değiştirin (kurulum betiği sürümü buradan okur).
2. Paket sürümlerini ancak `requirements-build.txt` içinde değiştirip derlemeyi ve açılış sayfasını doğrulayarak yükseltin.
3. Testleri çalıştırın, EXE’yi temiz bir kullanıcı profilinde Türkçe karakterli bir PDF ile açın.

## Bilinen tuzaklar (yaşanmış)

- **Türkçe karakter:** Yerleşik Helvetica ğ/ı çizemez; metin `insert_text_tr` ile Arial/Segoe dosyasından gömülür. Geçici PDF önbelleği dosya adında sürümlenir (`_v2`).
- **Koordinatlar:** PyMuPDF metin/arama konumları döndürülmemiş sayfa uzayındadır; ekrana çizerken `page.rotation_matrix`, tıklamayı sayfaya çevirirken tersi uygulanır.
- **Kaydetme:** Önce geçici dosya, ilk kayıtta `.yedek.pdf`, sonra `os.replace` (kısa yeniden denemeli). Hata olursa düzenlemeler bellekte kalır.
- **Betikle toplu düzenleme:** Çıpa metninin `count == 1` olduğunu doğrulayın; sonra `python -m pip install pyflakes` sonrası `python -m pyflakes pdf_gui.py` gibi bir eksik-ad denetimi çalıştırın (silinmiş `def` / tanımsız ad yakalanır).
- **Kurulum:** `SetupMutex` aynı anda tek sihirbaza izin verir; uygulama `BabaPDFCalisiyorMutex` açar. Eski kurulum varsa onay alınıp kaldırılır. Uygulamayı kapattıktan hemen sonra sessiz kaldırma vazgeçebilir: süreç bitene kadar bekleyin.
- **Windows izleri:** Kaldırma sonrası `AppListBackup`, `CloudStore` ve `Start\TileProperties` altında uygulama izi kalabilir; temizlerken önce `reg export` yedeği alın.
- **İmza:** Kendinden imzalı sertifika SmartScreen uyarısını başka bilgisayarlarda kaldırmaz; herkese açık dağıtım için tanınmış bir otoriteden sertifika gerekir. Özel anahtarı depoya koymayın.

## Tek kopya koruması

Başlat menüsünden ya da EXE'ye tek/çift/art arda tıklanınca, ilk kopyanın açılışı sürerken gelen başlatmalar yok sayılır. Açılış bitince (pencere görününce) süre ölçülüp `%LOCALAPPDATA%\BabaPDFaslatma.json` içine yazılır ve sonraki başlatmalar yeni kopya açabilir. Karar, kullanıcının tıklama anına (tek dosya EXE'de önyükleyici sürecin oluşturulma zamanı) göre verilir; farklı bir PDF açma isteği engellenmez; çöken ilk kopya kilit bırakmaz. Ölçülen (aynı makine): tek dosya EXE ≈ 14 sn; klasör paketi ≈ 2 sn (ısınmış). Yeni imzalanmış/kopyalanmış dosyanın ilk açılışı Windows taraması yüzünden ≈ 17–20 sn sürebilir. Klasör modunda üst süreç önyükleyici değildir; tıklama anı yalnızca üst süreç aynı EXE ise ondan alınır.

## Güncelleme denetimi

Yardım ▸ Güncellemeleri Denetle, yalnızca kullanıcı seçince çalışır. Adres `BABA_PDF_UPDATE_URL` ortam değişkeninden ya da `%APPDATA%\BabaPDF\guncelleme_adresi.txt` dosyasından okunur (https zorunlu, varsayılan yok).
Beklenen JSON: `{"version": "1.2.0", "url": "https://.../indir", "notes": "Kısa not"}`.
