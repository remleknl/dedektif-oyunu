-- ÖRNEK SENARYO: "Kara Köşk Cinayeti"
-- Kurban: Lord Aldric Kara — köşkünde ölü bulundu.
-- Katil: Dr. Numan Aslan (şantaj motiviyle)
-- Bu dosya senarist tarafından düzenlenecek şablon veridir.

PRAGMA foreign_keys = ON;

-- ── ODALAR ────────────────────────────────────────────────────────────────────
INSERT INTO rooms (id, name, description) VALUES
(1, 'Kütüphane',  'Eski kitaplarla dolu loş bir oda. Şöminede yarım kalmış bir mektup var.'),
(2, 'Mutfak',     'Gece yarısı kullanılmış izler taşıyan büyük bir mutfak.'),
(3, 'Bahçe',      'Köşkün arka bahçesi. Çamurlu toprakta ayak izleri seçiliyor.'),
(4, 'Çalışma',    'Lord''un özel odası. Kilitli çekmeceler, yarı açık bir kasa.'),
(5, 'Balo Salonu','Gece partinin yapıldığı salon. Yerde kırık bir kadeh.');

-- ── İPUÇLARI ──────────────────────────────────────────────────────────────────
INSERT INTO clues (id, room_id, name, description, clue_type, is_key_clue) VALUES
-- Kütüphane
(1,  1, 'Yarım Mektup',    'Lord''un adreslendiği, "...sırrını ifşa edeceğim" diye biten mektup parçası.', 'document', 1),
(2,  1, 'İlaç Şişesi',     'Şöminenin yanında düşmüş bir uyku ilacı şişesi. Reçete Dr. Aslan''a ait.', 'physical', 1),
-- Mutfak
(3,  2, 'Kırık Kadeh',     'Yerde kırık bir şarap kadehi. Kenarda dudak izi var.', 'physical', 0),
(4,  2, 'Servis Defteri',  'Uşağın gece 23:15''te mutfakta olduğunu gösteren not.', 'document', 0),
-- Bahçe
(5,  3, 'Ayak İzleri',     'Kasadan çıkan iki ayrı ayak izi: biri küçük, biri büyük numara.', 'physical', 1),
(6,  3, 'Düğme',           'Çalı dibinde siyah bir ceket düğmesi. Doktorun ceketindekiyle aynı model.', 'physical', 1),
-- Çalışma
(7,  4, 'Açık Kasa',       'Kasada para yok; içinde yalnızca bir fotoğraf zarfı kalmış.', 'physical', 0),
(8,  4, 'Şantaj Fotoğrafı','Lord''u suç ortaklığında gösteren fotoğraflar. Üstte Dr. Aslan''ın parmak izi.', 'document', 1),
-- Balo Salonu
(9,  5, 'Kırık Kadeh 2',   'Balkonda kırık ikinci kadeh. Üstünde uyku ilacı kalıntısı.', 'physical', 1),
(10, 5, 'Davet Listesi',   'Geceye katılan herkesin imzaladığı liste. Dr. Aslan saat 22:00''de giriş yapmış.', 'document', 0);

-- ── ŞÜPHELİLER ────────────────────────────────────────────────────────────────
INSERT INTO suspects (id, name, description, is_killer, motive, alibi) VALUES
(1, 'Dr. Numan Aslan',  'Lord''un uzun yıllık aile doktoru. Sakin ama gergin görünüyor.',
    1,
    'Lord onun tıbbi lisansını iptal ettirecek belgelere sahipti.',
    'Partide olduğunu söylüyor, ama saat 23:00–00:00 arası nerede olduğu belirsiz.'),
(2, 'Leyla Hanım',      'Lord''un yeğeni. Mirası bekliyor.',
    0,
    'Mirasçı olmak istiyor.',
    'Balo salonundaydı, birden fazla tanık var.'),
(3, 'Hasan Bey',        'Köşkün uşağı. Tüm gece hizmet etti.',
    0,
    'Bilinen bir motifi yok.',
    'Mutfak defteri gece 23:15''te orada olduğunu kanıtlıyor.'),
(4, 'Selin Yıldız',     'Lord''un iş ortağı. Aralarında mali anlaşmazlık var.',
    0,
    'Şirketteki pay anlaşmazlığı.',
    'İstanbul''daydı, uçak bileti var.');

-- ── İFADELER ──────────────────────────────────────────────────────────────────

-- Dr. Aslan
INSERT INTO statements (id, suspect_id, trigger_type, trigger_clue, content, is_lie) VALUES
(1, 1, 'initial',    NULL,
 'Bu trajedi beni derinden sarstı. Lord''la 20 yıllık dostluğumuz vardı.',
 0),
(2, 1, 'after_clue', 2,   -- ilaç şişesi tetikliyor
 'O ilaç şişesi benim, evet — ama hastama verdiğim bir şeydi. Kütüphanede ne işi var bilmiyorum.',
 1),  -- yalan: şişeyi kasıtlı bıraktı
(3, 1, 'after_clue', 8,   -- fotoğraf tetikliyor
 'O fotoğrafları ilk kez görüyorum. Parmak izim nasıl çıktı bilmiyorum.',
 1),
(4, 1, 'confronted', NULL,
 'Tamam... Lord beni mahvedecekti. Ama sadece konuşmak için gittim, yemin ederim.',
 0),
-- Leyla Hanım
(5, 2, 'initial',    NULL,
 'Amcam çok kötü bir insandı. Kimse ağlamayacak onun ardından.',
 0),
(6, 2, 'after_clue', 5,   -- ayak izleri tetikliyor
 'Bahçeye çıktım, evet — ama yalnızca hava almak için. Gece 23:30 civarıydı.',
 0),
-- Hasan Bey
(7, 3, 'initial',    NULL,
 'Gece boyunca misafirlere servis yaptım. Saatten önce hiçbir yerde değildim.',
 0),
(8, 3, 'after_clue', 4,   -- servis defteri tetikliyor
 'Evet, defteri ben tutuyorum. Saat 23:15''te mutfaktaydım, bunu kanıtlayabilirim.',
 0),
-- Selin Yıldız
(9, 4, 'initial',    NULL,
 'O gece İstanbul''daydım. Uçak biletim de var.',
 0);

-- ── ÇELİŞKİLER ────────────────────────────────────────────────────────────────
-- Çelişki 1: Dr. Aslan ilaç şişesinin nasıl orada olduğunu bilmediğini söylüyor,
--            ama bahçedeki düğme onun ceketine ait → gece köşkte dolaştı.
INSERT INTO contradictions (statement_id, clue_id, explanation) VALUES
(2, 6,
 'Dr. Aslan kütüphanede ne işi olduğunu bilmediğini söylüyor, ama bahçede bulunan düğme onun ceketiyle eşleşiyor — gece köşkte dolaştığını kanıtlıyor.');

-- Çelişki 2: Dr. Aslan şantaj fotoğraflarını ilk kez gördüğünü iddia ediyor,
--            ama fotoğrafın üstünde onun parmak izi var.
INSERT INTO contradictions (statement_id, clue_id, explanation) VALUES
(3, 8,
 'Dr. Aslan fotoğrafları tanımadığını söylüyor, ancak adli inceleme fotoğraf zarfında onun parmak izini tespit etti.');

-- Çelişki 3: Dr. Aslan ilaç şişesinin bir hastasına ait olduğunu söylüyor,
--            ama kadeh üzerindeki iz uyku ilacı kalıntısıyla uyuşuyor — ilacı içeceğe karıştırdı.
INSERT INTO contradictions (statement_id, clue_id, explanation) VALUES
(2, 9,
 'İlaç şişesinin başkasına ait olduğunu iddia ediyor; oysa balo salonundaki kadehin üzerinde aynı ilaçtan kalıntı bulundu.');
