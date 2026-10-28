# Baba PDF — sürüm notları

Sürüm numarası `MAJOR.MINOR.PATCH` biçimindedir ve `pdf_gui.py` içindeki `APP_VERSION` / `APP_DATE` değerlerinden okunur
(kurulum betiği de buradan alır). **Her EXE derlemesinden önce** uygun şekilde yükseltilir:

- **MAJOR** — dosya/ayar uyumluluğunu bozan ya da programı kökten değiştiren büyük değişiklik.
- **MINOR** — yeni özellik eklenen sürüm (mevcut özellikler korunur).
- **PATCH** — yalnızca hata düzeltme, metin/görünüm ince ayarı, paket sürümü güncellemesi.

## 1.10.0 — 28.10.2026
Yeni
- Yazı aracı artık önizlemeli: yazı tipi, boyut, kalın, italik, altı çizili, üstü çizili, renk, saydamlık, hizalama, satır aralığı ve açı seçilir; yazı sayfa önizlemesinde çerçeve içinde görünür, sürüklenerek ya da ok tuşlarıyla (Shift = 10 nokta) istenen yere kaydırılır; yazı yalnız «Onayla ve ekle» ile sayfaya işlenir (İptal sayfaya dokunmaz). Eklenen yazı seçilebilir/aranabilir gerçek yazıdır; Ctrl+Z ile geri alınır.

## 1.9.5 — 25.10.2026
Düzelen
- Silgi artık seçilen alanın çevresindeki zemin rengini örnekleyip silinen yeri o renkle doldurur (renkli/kırık beyaz kâğıtlarda leke kalmaz).
- Silgi çizimlere (arka plan kutuları, çizgiler) dokunmaz; geniş bir alan seçilince tüm sayfanın gitmesi giderildi.

## 1.9.4 — 25.10.2026
Düzelen
- Silgi: resim pikselleri silinemeyen resim türlerinde (maske, JBIG2 gibi) alan artık beyaz bir kapakla örtülür; silme sonrası alanın gerçekten boşaldığı denetlenir.

## 1.9.3 — 25.10.2026
Düzelen
- Silgi, yalnızca resimden oluşan (taranmış) sayfalarda da çalışır: seçilen alandaki resim pikselleri beyaza boyanır.

## 1.9.2 — 25.10.2026
Değişen
- Açılış sayfası daha hızlı açılır: çekmecedeki düğmeler başlık ilk açıldığında üretilir, kitaplık kartları (kapak üretimi) sayfa göründükten sonra tek tek eklenir.

## 1.9.1 — 25.10.2026
Değişen
- Açılış sayfasındaki özellik düğmeleri (Dışa aktarma, Sayfalar, Filigran/açıklama, Güvenlik, Denetim, Görünüm, Yardım) sayfadan kaldırıldı; sol üstteki "☰ Özellikler" çekmecesinde başlık başlık açılır.

## 1.9.0 — 25.10.2026
Yeni
- Silgi aracı (araç çubuğu ve Düzenle ▸ Açıklamalar): sürükleyerek seçtiğin alandaki yazı sayfadan silinir, yerine beyaz zemin kalır. Resimlere dokunmaz, Ctrl+Z ile geri alınır. Siyah kutu isteyen için "Gizle" aracı durur.

## 1.8.0 — 25.10.2026
Yeni
- Açıklama araçları: metnin üstünü çizme, dalgalı alt çizgi (sürükleyerek), serbest kalem (araç çubuğu ve Düzenle ▸ Açıklamalar).
- "Metni Ara ve Üstünü Çiz" ve "Metni Ara ve Dalgalı Altını Çiz".
- Yeni açılan biçimler: FB2, XPS/OXPS, CBZ (çizgi roman), SVG; açılış sayfasında her biri için kart. Sayfalı PDF'e çevrilerek açılır.

Düzelen
- "Metni Ara ve Vurgula" ile "Altını Çiz" menüleri PyMuPDF'de olmayan bir yöntemi (`add_highlight`) çağırdığı için hata veriyordu; düzeltildi. Metin bulunamazsa artık sessiz kalmaz, bildirim gösterir.

## 1.7.0 — 25.10.2026
Yeni
- Resimlerden PDF oluşturma (sıralama, sayfa boyutu, sürükle-bırak).
- Bağlantılara tıklama (iç/dış, dış bağlantıda onay), bağlantı üzerinde hedef balonu, Alt+←/→ gezinti geçmişi.
- İçindekiler paneli (F4), katmanlar penceresi.
- Alan seçerek kırpma, kırpmayı kaldırma, boş sayfa ekleme, sayfa aralığı silme.
- Word (.docx), Excel (.xlsx) ve PowerPoint (.pptx) olarak kaydetme.
- Açılış sayfasında her özellik için kart/düğme; sayfa kaydırılabilir.
- Sayfa sıralama panelinde ekleme çizgisi, kenarda otomatik kaydırma, çoklu seçili sayfaları birlikte taşıma.

Değişen / düzelen
- PyMuPDF 1.28.2 → 2.0 (MuPDF 1.28.5).
- "Kenarları Kırp" daha önce kırpılmış sayfada kayma yapıyordu; düzeltildi.
- Yeni paketler: python-docx 1.2.0, openpyxl 3.1.5, python-pptx 1.0.2.

## 1.6.0 — 22.10.2026
- Önceki kararlı sürüm (ayrıntı için README).
