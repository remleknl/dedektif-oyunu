import streamlit as st
from db.db import init_db
import db.db as db
from engine.clue_engine import get_collected_clues

st.set_page_config(page_title="Dedektif Oyunu", layout="wide")

init_db(seed=False)

# ── Session state başlangıç değerleri ─────────────────────────────────────────
if "session_id" not in st.session_state:
    st.session_state.session_id = None

if "page" not in st.session_state:
    st.session_state.page = "home"   # "home" | "game" | "end"


# ── Sayfa yönlendirme ─────────────────────────────────────────────────────────
def show_home():
    st.title("Dedektif Oyunu")
    st.subheader("Kara Köşk Cinayeti")
    player_name = st.text_input("Adınız")
    if st.button("Oyunu Başlat", disabled=not player_name):
        from engine.session import start_game
        st.session_state.session_id = start_game(player_name)
        st.session_state.page = "game"
        st.rerun()


def show_game():
    # TODO: K5 (ui/room_view.py) ve K6 (ui/suspect_view.py) hazır olunca buraya eklenir
    st.info("Oyun ekranı henüz hazır değil — UI modülleri tamamlandıktan sonra buraya bağlanacak.")
    if st.button("Ana Menüye Dön"):
        st.session_state.page = "home"
        st.session_state.session_id = None
        st.rerun()


def show_end():
    session_id = st.session_state.get("session_id")
    
    # Oturum ve sonuç bilgilerini DB'den al
    session_data = db.get_session(session_id) if session_id else {}
    is_won = session_data.get("is_won", False) if session_data else False
    accused_suspect = session_data.get("accused_suspect", "Bilinmiyor") if session_data else "Bilinmiyor"

    st.markdown("<h1 style='text-align: center;'>📋 Vaka Raporu ve Soruşturma Sonu</h1>", unsafe_allow_html=True)
    st.divider()

    # 1. Tebrik / Kaybetme Durum Mesajları
    if is_won:
        st.balloons()
        st.success("🎉 **TEBRİKLER DEDEKTİF, DAVAYI ÇÖZDÜNÜZ!**")
        st.markdown(
            f"""
            ### ⚖️ Adalet Yerini Buldu!
            Doğru kişiyi (**{accused_suspect}**) suçladınız.
            
            **Katilin İtirafı ve Olay Örgüsü:**
            Aylin Karaca, babasının kendisini mirastan menedeceğini öğrendiğinde kasadaki mektubu yok etmek istedi. 
            Mutfaktaki böcek ilacını (siyanür türevi) babasının gece kahvesine karıştırarak cinayeti işledi. 
            Şoför Murat ise sadece kargaşadan faydalanıp kasanın açık olduğunu görünce broşu çalmıştı. 
            Topladığınız deliller ve yakaladığınız çelişkiler sayesinde Aylin daha fazla inkar edemedi ve teslim oldu!
            """
        )
    else:
        st.error("❌ **YANLIŞ SUÇLAMA! GERÇEK KATİL KAÇMAYI BAŞARDI.**")
        st.markdown(
            f"""
            ### 🌧️ Masum Biri Parmaklıklar Ardında...
            Suçladığınız kişi: **{accused_suspect}**. Ancak mahkemede sunulan kanıtlar yetersiz kaldı!
            
            **Gerçekte Ne Olmuştu? (Gerçek Katil ve Motifi):**
            * **Gerçek Katil:** **Aylin Karaca (Kurbanın Kızı)**
            * **Cinayet Motifi:** Selim Karaca'nın yazdığı gizli vasiyetnamede kızını mirastan tamamen çıkardığı ortaya çıktı. 
              Aylin bu mektubu yırtıp yok etmeye çalıştı ve babasını akşam kahvesine zehir katarak öldürdü.
            * **Diğerlerinin Durumu:** Şoför Murat sadece tarihi broşu çalan bir fırsatçıydı, kahya Banu'nun ise cinayetle hiçbir ilgisi yoktu. 
              Yanlış kişiyi suçladığınız için Aylin malikaneden kaçmayı başardı.
            """
        )

    st.write("")
    st.subheader("📊 Soruşturma Özeti")

    # 2. Toplanan İpuçları ve Yakalanan Çelişkilerin Özeti
    col1, col2 = st.columns(2)

    with col1:
        st.markdown("#### 🔍 Toplanan Deliller")
        collected_clues = get_collected_clues(session_id) if session_id else []
        if collected_clues:
            for clue in collected_clues:
                clue_name = clue.get("name", "Bilinmeyen İpucu")
                clue_desc = clue.get("description", "")
                st.markdown(f"- **{clue_name}:** *{clue_desc}*")
        else:
            st.info("Hiç ipucu toplanmadı.")

    with col2:
        st.markdown("#### ⚡ Yakalanan Çelişkiler")
        contradiction_ids = db.get_caught_contradiction_ids(session_id) if session_id else []
        if contradiction_ids:
            for c_id in contradiction_ids:
                contradiction = db.get_contradiction(c_id)
                explanation = contradiction.get("explanation", "Çelişki çözüldü.") if contradiction else "Detay yok"
                st.markdown(f"- ⚠️ {explanation}")
        else:
            st.warning("Hiçbir çelişki yakalanmadı.")

    st.divider()

    # 3. Yeniden Oyna Butonu (Session ve Page Sıfırlama)
    col_center1, col_center2, col_center3 = st.columns([1, 2, 1])
    with col_center2:
        if st.button("🔄 Yeniden Oyna", use_container_width=True, type="primary"):
            st.session_state.session_id = None
            st.session_state.page = "home"
            st.rerun()


# ── Router ────────────────────────────────────────────────────────────────────
page = st.session_state.page

if page == "home":
    show_home()
elif page == "game":
    show_game()
elif page == "end":
    show_end()
