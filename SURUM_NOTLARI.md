# Baba PDF — sürüm notları

Sürüm numarası `MAJOR.MINOR.PATCH` biçimindedir ve `pdf_gui.py` içindeki `APP_VERSION` / `APP_DATE` değerlerinden okunur
(kurulum betiği de buradan alır). **Her EXE derlemesinden önce** uygun şekilde yükseltilir:

- **MAJOR** — dosya/ayar uyumluluğunu bozan ya da programı kökten değiştiren büyük değişiklik.
- **MINOR** — yeni özellik eklenen sürüm (mevcut özellikler korunur).
- **PATCH** — yalnızca hata düzeltme, metin/görünüm ince ayarı, paket sürümü güncellemesi.

## 1.12.10 — 28.10.2026
Düzeltilen
- Satır genişliği ölçümü (1.12.9) Windows dışı ortamlarda ve testlerde gömülü Helvetica ile yapılıyordu; bu yazı tipinde ş, ğ, ı gibi Türkçe harflerin genişliği 0 sayıldığından satırlar %20–30 fazla genişletiliyordu. Windows yazı tipi yoksa artık ölçü uyumlu Liberation yazı tipleri kullanılır. Windows'ta davranış değişmedi (gerçek Arial/Times/Courier).
Ölçüm (LibreOffice, A3 ABB kılavuzu, özgün PDF ile sözcük konumu farkı ≤ 3 pt): sayfa 1'de sözcüklerin %40 → %90'ı, sayfa 2'de %84 → %96'sı; ortalama yatay sapma 5,3 / 2,4 pt → 1,1 / 1,1 pt.

## 1.12.9 — 28.10.2026
Düzeltilen (PDF → Word, sabit konumlu sayfa; gerçek Word'de A3 ABB kılavuzu ile ölçüldü)
- Her satırın genişliği Word'de yerine konan yazı tipinin gerçek ölçüsüne (Arial TTF) göre PDF'teki genişliğe eşitlenir (satır başına yatay ölçek); önceki yazı tipi başına tek ölçek yerine.
- Numaralı/maddeli listelerde ikinci ve sonraki satırlar birinci satırdan içerideydi, Word hepsini sola yaslıyordu (≈12 pt kayma): asılı girinti uygulanır; satır başlangıçları karışıksa satır başına paragraf.
- Asılı girintili madde «ortalı» sanılıyor ve kutu yanlış yere konuyordu (bir madde Word'de kayboluyordu).
- Taban çizgisi aralığı düzensiz bloklar (logo çizgisi + küçük başlık + başlık) ve iri gösterge rakamı + küçük etiket ayrı kutulara bölünür (üstü kesiliyor ve 4–7 pt aşağı kayıyordu); üst üste binen yazı (rakam üstü ondalık nokta) ayrı blok olur.
- Sabit genişlikli yazı tipinde baştaki boşlukla hizalanmış etiketler gerçek yazının başına konur.
- Altı çizili tespiti sıkılaştırıldı (LCD çerçeve çizgisi altı çizgi sanılıyordu).
Ölçüm (özgün PDF ile Word'den geri çevrilen PDF, sözcük merkezi farkı): sayfa 1'de 3 pt içinde sözcük 704 → 1608 / 1760, sayfa 2'de 1154 → 1339 / 1383; ortalama düşey fark 0,36 → 0,07 pt.

## 1.12.8 — 28.10.2026
Düzeltilen
- Word dosyası açılırken çıkabilecek uyarılar giderildi: «Uyumluluk Modu» (Word 2010 kipi) yerine Word 2013+ kipi; belge özellikleri şablondan kalan «python-docx», 2013 tarihi ve şablon önizleme resmi yerine «Baba PDF» ve gerçek tarih; tablo ve hücre özellikleri şema sırasında yazılır (sırası bozuk öğe Word'de «okunamayan içerik» onarımına yol açabilir).
- Word'deki web bağlantıları: metin kutusunu taşıyan dış öğe bağlantı sayılıyordu (3 bağlantı yanlış yere yazılıyordu); artık bağlantı kutunun içindeki yazıya uygulanır.
- Sayfa dışına taşan (negatif konumlu) metin kutuları sayfa kenarına çekilir.
- Test: Word dosyasının yapı denetimi (kimlik benzersizliği, tablo özellik sırası, uyumluluk kipi, şablon artıkları).

## 1.12.7 — 28.10.2026
Düzeltilen
- Word/PowerPoint, karmaşık sayfa: Arial, Helvetica, Times gibi Office'te gerçek karşılığı olan yazı tiplerine artık yatay ölçek uygulanmaz (önceden yazılar %4–11 genişletilip komşu yazıların üstüne taşabiliyordu). Genişlik ölçümü iki yana yaslı satırları saymaz (boşlukları gerilmiş olduğundan ölçü şişiyordu).
- Döndürülmüş yan yazılı sayfa: görünür alan dışında kalan metin artık kesilmiyor (kaynak sayfanın dönüklüğü önce kaldırılıyor).
- Testler: bilinen yazı tipi ölçeği ve yan yazılı döndürülmüş sayfa.

## 1.12.6 — 28.10.2026
Düzeltilen
- Excel: tablo dışı yazı (başlık, açıklama, madde metni, tablosuz sayfalar) artık «Metin» sayfasına `[sayfa, satır]` olarak yazılır. A3 ABB kılavuzunda sözcük kaybı büyük ölçüde kapandı (önce ≈936/3177 sözcük; şimdi tüm sözcükler var, sayılar hücrede sayı olarak durduğu için metin sayımında eksik görünür).
- Word, karmaşık sayfa: metin kutuları `wrap="none"`; iki yana yaslı bloklar sola hizalanır (Word sert satır sonlu satırları kutu genişliğine geriyordu). Gerçek Word'de denenmedi.
- Test eklendi: `test_excel_tablo_disi_baslik_metin_sayfasina_yazilir`.

## 1.12.5 — 28.10.2026
Düzeltilen
- Word'de karmaşık sayfalarda yazıların bozulması/karışması: sabit konumlu yazılar Word çerçevesi (framePr) yerine metin kutusu olarak yazılır. Word çerçeveleri üst üste bindiğinde kayıyor; metin kutuları birbirinden bağımsızdır. Çizim kimlikleri benzersiz yapıldı. LibreOffice'te konum farkı değişmedi (yaklaşık −0,5 pt dikey); Word'de görünüm sizin denemenize bağlıdır.

## 1.12.4 — 28.10.2026
Yeni
- Word'e kaydet: PDF'teki web bağlantıları Word bağlantısı olarak korunur.
- Word'e kaydet: düzenlenebilir seçilince «Sayfa düzeni» sorusu: otomatik (karmaşık sayfalar görünüme sadık) ya da tümü akışlı metin (düzenlemesi kolay).

## 1.12.3 — 28.10.2026
Düzeltilen
- Office'e kaydet: döndürülmüş (/Rotate) sayfalar artık doğru okunur; önceden Word çıktısı 1 sayfadan 4'e şişiyor, PowerPoint'te metin kutusu hiç oluşmuyordu. Yatay yazılı içerikte sayfanın dönüklüğü kaldırılır, yan yazılı (görünüşte dik) içerikte sayfa görünen yönüyle yeniden kurulur.
- PowerPoint: karışık boyutlu sayfalarda her sayfa slayda oranı bozulmadan ortalanarak sığdırılır (önceden yatay sayfa sıkışıyordu).

## 1.12.2 — 28.10.2026
Değişen
- Word (karmaşık/broşür sayfalar): harf büyüklükleri artık özgün boyutta kalır; yazı tipi yerine konunca genişlik farkı, harf boyunu küçültmek yerine her yazı tipi için sayfa düzeyinde tek bir yatay ölçekle (Word «ölçek %») giderilir. Böylece tablo hücreleri ve satırlar arasında boyut tutarsızlığı kalmaz. Tek satırlık yazılar için satır yüksekliği doğal değere yakın tutuldu (Word ile LibreOffice arası dikey kayma azalır); madde imi gibi iri simgeler satır aralığını şişirmez.
- Kenar boşlukları: sabit konumlu sayfalarda sıfır kenar boşluğu yerine sayfadaki içerik boşluğu (en az 14, en çok 36 nokta) kullanılır.
- Arka plan resmi: yazı silme işlemi saydamlık maskeli resimleri (ör. simgeler) karartıyordu; yazı yalnızca yazı kutularının içinde silinir, kalan alan özgün görüntüdür. Dosya da küçüldü.
- PowerPoint aynı arka planı ve yatay ölçeği (en çok %12 daralma ile) kullanır.

## 1.12.1 — 28.10.2026
Değişen
- Word dışa aktarma: yoğun/broşür düzenli sayfalar (3+ yan yana sütun ya da çok resimli) artık sayfa görünümünü bozmaz: çizgi, şekil ve resimler arka plan resmi olur, her yazı bloğu sayfada aynı yere sabitlenmiş düzenlenebilir yazı çerçevesi olur (A3 kılavuz örneğinde 2 sayfa → 2 sayfa; önceki sürümde 6 sayfa). Satır sonları korunur; bilgisayarda olmayan özel yazı tipleri Arial/Times'a çevrilir ve gerekirse küçültülür.
- Aynı satırdaki tablo hücreleri ve madde imi + metin ayrı/birleşik doğru ele alınır; madde imi ve simge yazı tiplerinin özel karakterleri kutu olarak görünmez. PowerPoint da aynı blok ayrıştırmasını kullanır.
- Önceki sürüm 1.12.0 yalnızca akışlı düzeni yapıyordu; 1.12.1 ona karmaşık sayfa kipini ekler.

## 1.12.0 — 28.10.2026
Değişen
- Word/Excel/PowerPoint olarak kaydet baştan yazıldı; çıktı girdi PDF ile yan yana karşılaştırılarak düzeltildi.
- Word: sayfa boyutu ve kenar boşlukları PDF'ten alınır; yazı tipi, boyut, kalın/italik/altı çizili, renk, hizalama (sola/ortaya/sağa/iki yana), girinti ve satır aralığı korunur; madde imleri tek satırda kalır; tablolar gerçek Word tablosu olur (birleşik hücre, zemin rengi, sağa yaslı sayılar); resimler ve çizimler yerinde durur; iki sütunlu sayfalarda sütun düzeni korunur. Taranmış sayfa resim olarak konur.
- PowerPoint: yazılar yazı tipi/renk/hizasıyla kendi yerinde düzenlenebilir kutu olur; tablo hücreleri ayrı kutu; çizgiler, şekiller ve resimler yazısız arka plan resmidir (üst üste binme biter).
- Excel: tablolar gerçek hücre olur; sayılar (Türkçe biçim, yüzde dahil) sayı olarak yazılır; yazı biçimi, hizalama, zemin rengi, kenarlık, birleşik hücre, sütun genişliği ve satır yüksekliği korunur; çizgisiz sütunlu tablolar da bulunur; sayfaya bölünmüş tablo tek sayfada birleşir.
- Yeni testler eklendi. Windows'ta Word/PowerPoint ile gerçek dosya üzerinde elle denenmesi önerilir.

## 1.11.1 — 28.10.2026
Değişen
- Paket küçültüldü: programın kullanmadığı cv2 (OpenCV), onnxruntime, numpy, pandas, matplotlib, scipy, networkx ve pymupdf4llm/pymupdf-layout `pdf_gui.spec` içinde dışarıda bırakıldı (pymupdf 2.0 bağımlılıkları olarak pakete giriyordu; ~200 MB). Tek dosya EXE'nin açıkça daha hızlı açılması beklenir; yeni «Son açılış süresi» Hakkında penceresinde görünür. İlk derlemede OCR, Word/Excel/PPT dışa aktarma, şifreli PDF açma ve yazı ekleme elle denenmelidir.

## 1.11.0 — 28.10.2026
Kaldırılan
- Dijital imza işlevlerinin tümü kaldırıldı: «PDF'yi Dijital Olarak İmzala», «Dijital İmzaları Doğrula», «İmza Raporunu TXT Olarak Kaydet», «Sertifikayı Kontrol Et» ve açılış sayfasındaki «Dijital İmza» kartı. «Güvenlik ve İmza» menüsü «Güvenlik» oldu. Resim yerleştirme (imza resmi dahil) durur.
- pyHanko, xsdata ve toposort paketleri artık gerekmez (EXE küçülür, açılış hızlanır). Kurulum paketinin kendi imzası (`kurulum\imzala_ve_paketle.ps1`) değişmedi.

## 1.10.1 — 28.10.2026
Değişen
- Yazı ekleme artık doğrudan açık sayfada yapılır: yazı sayfa üzerinde çerçeve içinde görünür, sayfada sürüklenir (boş yere tıklayınca oraya gelir; ok tuşları 1 nokta, Shift ile 10 nokta). Ayrı büyük önizleme penceresi kaldırıldı; yalnızca küçük bir «Yazı biçimi» paneli açılır (biçim ayarları, «Onayla ve ekle» / İptal). Yakınlaştırma ve kaydırma düzenleme sürerken de çalışır; başka araca geçilirse düzenleme iptal edilir.

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
