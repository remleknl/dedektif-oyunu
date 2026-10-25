"""
ui/accusation_view.py — Suçlama ekranı (Issue #9)

Bu ekran:
  1. Tüm şüphelileri kart olarak gösterir (ad, açıklama, alibi),
  2. Oyuncu bir şüpheli seçip "Suçla" butonuna basınca
     engine.session.finish_game() fonksiyonunu çağırır,
  3. Sonucu kaydedip st.session_state.page = "end" ile bitiş ekranına geçer.

Oyuncu oyunun herhangi bir anında suçlama yapabilir; hiçbir engel yoktur.

Kullanım (app.py içinden, K7 bağlayacak):
    from ui.accusation_view import show_accusation
    show_accusation()
"""

import sys
from pathlib import Path

import streamlit as st

# Proje ana klasörünü Python'un arama yoluna ekle.
# (app.py'den çalışırken zaten ekli, tek başına test ederken gerekli.)
ROOT = Path(__file__).resolve().parent.parent
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from db import db                      # şüphelileri veritabanından okumak için
from engine.session import finish_game  # suçlamayı sonuçlandıran engine fonksiyonu


# ── Yardımcı fonksiyon ────────────────────────────────────────────────────────
def _alan(satir, adaylar, varsayilan="—"):
    """
    Veritabanı satırından, verilen sütun adlarından ilk bulunanı döner.

    schema.sql'deki sütun adlarını kesin bilmediğimiz için birkaç olası
    isim deniyoruz (örn. 'name' ya da 'ad'). Hiçbiri yoksa varsayılan döner.
    """
    for ad in adaylar:
        if ad in satir.keys() and satir[ad]:
            return satir[ad]
    return varsayilan


# ── Ana ekran fonksiyonu ──────────────────────────────────────────────────────
def show_accusation():
    """Suçlama ekranını çizer."""

    # Oturum yoksa suçlama yapılamaz (oyun başlamamış demektir).
    session_id = st.session_state.get("session_id")
    if session_id is None:
        st.warning("Aktif bir oyun oturumu yok. Önce oyunu başlatın.")
        return

    # Seçili şüphelinin id'sini tutmak için session_state'te yer aç.
    if "accused_suspect_id" not in st.session_state:
        st.session_state.accused_suspect_id = None

    st.title("Suçlama")
    st.write("Katilin kim olduğunu düşünüyorsun? Bir şüpheli seç ve suçla.")

    # Tüm şüphelileri veritabanından çek.
    suspects = db.get_all_suspects()
    if not suspects:
        st.warning("Veritabanında şüpheli bulunamadı.")
        return

    # ── Şüpheli kartları (satır başına 3 kart) ───────────────────────────────
    KART_SAYISI_SATIR = 3
    for baslangic in range(0, len(suspects), KART_SAYISI_SATIR):
        satir_suspects = suspects[baslangic:baslangic + KART_SAYISI_SATIR]
        kolonlar = st.columns(KART_SAYISI_SATIR)

        for kolon, suspect in zip(kolonlar, satir_suspects):
            with kolon:
                secili_mi = st.session_state.accused_suspect_id == suspect["id"]

                # border=True kart görünümü verir.
                with st.container(border=True):
                    isim = _alan(suspect, ["name", "ad", "isim"], "İsimsiz")
                    aciklama = _alan(suspect, ["description", "aciklama", "bio"])
                    alibi = _alan(suspect, ["alibi"])

                    st.subheader(isim)
                    st.write(aciklama)
                    st.caption(f"**Alibi:** {alibi}")

                    # Seçili kartta buton "primary" (vurgulu) olur.
                    etiket = "✓ Seçildi" if secili_mi else "Seç"
                    tur = "primary" if secili_mi else "secondary"
                    if st.button(
                        etiket,
                        key=f"sec_{suspect['id']}",
                        type=tur,
                        use_container_width=True,
                    ):
                        st.session_state.accused_suspect_id = suspect["id"]
                        st.rerun()

    st.divider()

    # ── Suçla butonu ─────────────────────────────────────────────────────────
    secilen_id = st.session_state.accused_suspect_id

    if secilen_id is None:
        st.info("Suçlamak için yukarıdan bir şüpheli seç.")

    # Şüpheli seçilmediyse buton pasif; seçildiyse her zaman aktif (engel yok).
    if st.button("Suçla", type="primary", disabled=secilen_id is None):
        # Engine'e suçlamayı yaptır: kazandıysa True, kaybettiyse False döner.
        kazandi = finish_game(session_id, secilen_id)

        # Bitiş ekranı (K7) sonucu gösterebilsin diye sakla.
        st.session_state.accusation_won = kazandi
        st.session_state.accusation_suspect_id = secilen_id

        # Bir sonraki oyun için seçimi temizle ve bitiş ekranına geç.
        st.session_state.accused_suspect_id = None
        st.session_state.page = "end"
        st.rerun()


# ── Tek başına test modu ──────────────────────────────────────────────────────
# `streamlit run ui/accusation_view.py` ile çalıştırınca burası devreye girer.
# app.py üzerinden import edildiğinde çalışmaz.
if __name__ == "__main__":
    from engine.session import start_game

    db.init_db(seed=False)
    st.set_page_config(page_title="Suçlama (test)", layout="wide")

    if st.session_state.get("page") == "end":
        st.success("Bitiş ekranına yönlendirildi (page = 'end').")
        st.write("Sonuç (kazandı mı?):", st.session_state.get("accusation_won"))
        if st.button("Testi sıfırla"):
            st.session_state.page = "game"
            st.session_state.session_id = None
            st.rerun()
    else:
        if st.session_state.get("session_id") is None:
            st.session_state.session_id = start_game("Test Oyuncusu")
        show_accusation()