# Dedektif Oyunu

Tek kişilik, tarayıcıda oynanan cinayet çözme oyunu. Python + Streamlit + SQLite.

## Nasıl Çalıştırılır

```bash
pip install -r requirements.txt
streamlit run app.py
```

## Geliştirici Branch Kuralları

| Dal | Amaç |
|-----|------|
| `main` | Prodüksiyon — her hafta sonu merge edilir |
| `dev` | Günlük entegrasyon — feature'lar buraya merge olur |
| `feature/<isim>` | Yeni özellik — `dev`'den açılır, max 3 gün |
| `release/hafta-<N>` | Haftalık release adayı — QA test eder |
| `hotfix/<isim>` | Acil düzeltme — `main`'den açılır |

### Başlangıç

```bash
git clone https://github.com/remleknl/dedektif-oyunu
git checkout dev
git checkout -b feature/<benim-isim>
# çalış, commit'le
git push -u origin feature/<benim-isim>
# GitHub'dan dev'e PR aç
```

### Commit Mesajı Formatı (Conventional Commits)

```
feat: oda navigasyonu eklendi
fix: session yüklenemiyor hatası düzeltildi
chore: requirements.txt güncellendi
test: clue engine unit testleri eklendi
docs: db şeması README'ye eklendi
```

### Haftalık Takvim

```
Pazartesi   → dev'den feature/* dalları açılır
Perşembe    → feature/* → dev PR açılır, review yapılır
Cuma        → dev'den release/hafta-N açılır, QA test eder
Cuma akşamı → release/hafta-N → main, tag: v0.x.0
```
