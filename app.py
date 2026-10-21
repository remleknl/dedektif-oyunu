import streamlit as st
from db.db import init_db

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
    # TODO: K7 kazanma/kaybetme ekranını buraya ekler
    st.info("Oyun sonu ekranı henüz hazır değil.")
    if st.button("Yeniden Oyna"):
        st.session_state.page = "home"
        st.session_state.session_id = None
        st.rerun()


# ── Router ────────────────────────────────────────────────────────────────────
page = st.session_state.page

if page == "home":
    show_home()
elif page == "game":
    show_game()
elif page == "end":
    show_end()
