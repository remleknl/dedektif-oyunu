import sys
import os
import base64

# Ana dizini Python yoluna ekle (engine klasörünü bulabilmesi için)
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

import streamlit as st
from engine import clue_engine

def get_base64_of_bin_file(bin_file):
    """Yerel dosyayı base64 formatına çevirir."""
    with open(bin_file, 'rb') as f:
        data = f.read()
    return base64.b64encode(data).decode()

def apply_detective_theme(selected_room: str):
    """Seçilen odaya göre dinamik arka planı ve noir dedektif temasını uygular."""
    assets_dir = os.path.join(os.path.dirname(__file__), "..", "assets")
    
    room_backgrounds = {
        "Kütüphane": "room_kutuphane.jpg",
        "Çalışma Odası": "room_calisma.jpg",
        "Kış Bahçesi": "room_bahce.jpg",
        "Mahzen": "room_mahzen.jpg"
    }

    target_image_name = room_backgrounds.get(selected_room, "detective_room_bg.jpg")
    target_path = os.path.join(assets_dir, target_image_name)
    default_path = os.path.join(assets_dir, "detective_room_bg.jpg")

    active_path = None
    if os.path.exists(target_path):
        active_path = target_path
    elif os.path.exists(default_path):
        active_path = default_path

    if active_path:
        bin_str = get_base64_of_bin_file(active_path)
        bg_css = f"""
            background-image: linear-gradient(rgba(10, 13, 18, 0.84), rgba(8, 10, 14, 0.92)), url("data:image/jpg;base64,{bin_str}");
            background-size: cover;
            background-position: center;
            background-repeat: no-repeat;
            background-attachment: fixed;
        """
    else:
        bg_css = "background-color: #0b0e14;"

    st.markdown(f"""
        <style>
        @import url('https://fonts.googleapis.com/css2?family=Cinzel:wght@600;700&family=Inter:wght@400;500;600&display=swap');

        .stApp {{
            {bg_css}
            font-family: 'Inter', sans-serif;
            color: #e2e8f0;
            transition: background-image 0.4s ease-in-out;
        }}

        /* Sol Çanta Menüsü (Sidebar) */
        [data-testid="stSidebar"] {{
            background-color: rgba(26, 18, 12, 0.96) !important;
            border-right: 2px solid #d4af37 !important;
            box-shadow: 5px 0 15px rgba(0,0,0,0.7);
        }}
        .sidebar-title {{
            font-family: 'Cinzel', serif;
            color: #d4af37;
            font-size: 19px;
            font-weight: 700;
            text-align: center;
            border-bottom: 2px double rgba(212, 175, 55, 0.5);
            padding-bottom: 10px;
            margin-bottom: 12px;
        }}
        .sidebar-item {{
            background: rgba(255, 255, 255, 0.05);
            border: 1px solid rgba(212, 175, 55, 0.2);
            padding: 8px 12px;
            border-radius: 6px;
            margin-bottom: 8px;
            font-size: 13px;
        }}

        /* Üst Başlık Banner */
        .case-header {{
            background: linear-gradient(90deg, rgba(20, 24, 33, 0.95) 0%, rgba(30, 36, 48, 0.85) 100%);
            border: 1px solid rgba(212, 175, 55, 0.4);
            border-left: 6px solid #d4af37;
            border-radius: 10px;
            padding: 16px 22px;
            margin-bottom: 20px;
            box-shadow: 0 8px 24px rgba(0, 0, 0, 0.6);
        }}
        .case-header-title {{
            font-family: 'Cinzel', serif;
            font-size: 26px;
            font-weight: 700;
            color: #f6e05e;
            letter-spacing: 1.5px;
            margin-bottom: 4px;
        }}
        .case-header-sub {{
            color: #a0aec0;
            font-size: 14px;
        }}

        /* Mekan Gözlem Kutusu */
        .room-observation-box {{
            background: rgba(18, 22, 30, 0.88);
            border: 1px solid rgba(74, 85, 104, 0.6);
            border-left: 4px solid #4fd1c5;
            border-radius: 8px;
            padding: 12px 18px;
            color: #cbd5e0;
            font-size: 14px;
            height: 100%;
            display: flex;
            align-items: center;
        }}

        /* Delil Kartı */
        .clue-dossier-card {{
            background: linear-gradient(145deg, rgba(23, 28, 38, 0.92) 0%, rgba(14, 17, 24, 0.95) 100%);
            border: 1px solid rgba(212, 175, 55, 0.25);
            border-radius: 12px;
            padding: 18px 20px;
            box-shadow: 0 10px 25px rgba(0, 0, 0, 0.5);
            transition: all 0.3s ease;
            min-height: 185px;
            display: flex;
            flex-direction: column;
            justify-content: space-between;
        }}
        .clue-dossier-card:hover {{
            border-color: rgba(212, 175, 55, 0.65);
            box-shadow: 0 12px 30px rgba(212, 175, 55, 0.15);
            transform: translateY(-2px);
        }}

        .dossier-tag {{
            font-size: 11px;
            font-weight: 700;
            letter-spacing: 1.2px;
            color: #d4af37;
            text-transform: uppercase;
            margin-bottom: 6px;
        }}
        .clue-card-name {{
            font-family: 'Cinzel', serif;
            font-size: 18px;
            font-weight: 700;
            color: #ffffff;
            margin-bottom: 8px;
        }}
        .clue-card-desc {{
            font-size: 13px;
            color: #a0aec0;
            line-height: 1.5;
            margin-bottom: 12px;
        }}

        /* Rozetler */
        .badge-collected {{
            display: inline-block;
            background: rgba(39, 103, 73, 0.35);
            color: #68d391;
            border: 1px solid #38a169;
            padding: 4px 10px;
            border-radius: 6px;
            font-size: 12px;
            font-weight: 600;
        }}
        .badge-pending {{
            display: inline-block;
            background: rgba(156, 66, 33, 0.3);
            color: #fbd38d;
            border: 1px solid #dd6b20;
            padding: 4px 10px;
            border-radius: 6px;
            font-size: 12px;
            font-weight: 600;
        }}

        /* Buton Stilleri */
        .stButton > button {{
            background: linear-gradient(180deg, #2d3748 0%, #1a202c 100%) !important;
            color: #f7fafc !important;
            border: 1px solid rgba(212, 175, 55, 0.5) !important;
            border-radius: 6px !important;
            font-weight: 600 !important;
            transition: all 0.25s ease !important;
        }}
        .stButton > button:hover {{
            background: linear-gradient(180deg, #d4af37 0%, #b78a28 100%) !important;
            color: #1a202c !important;
            border-color: #f6e05e !important;
            box-shadow: 0 0 12px rgba(212, 175, 55, 0.4) !important;
        }}

        /* Pop-up (Dialog) */
        .case-file-popup {{
            background: #f7f3e9;
            color: #2b1f14;
            padding: 22px;
            border-radius: 8px;
            border: 8px double #4a3424;
            font-family: 'Courier New', Courier, monospace;
        }}
        .popup-title {{
            text-align: center;
            font-weight: bold;
            font-size: 20px;
            border-bottom: 2px dashed #4a3424;
            padding-bottom: 8px;
            margin-bottom: 14px;
            letter-spacing: 2px;
        }}
        </style>
    """, unsafe_allow_html=True)

def init_mock_database():
    """Arkadaşların motoru yazana kadar delilleri saklayacak yerel hafıza."""
    if "clues_db" not in st.session_state:
        st.session_state.clues_db = {
            "Kütüphane": [
                {
                    "id": "clue_kut_1",
                    "name": "Yırtık Zarf Parçası",
                    "description": "Üzerinde aceleyle karalanmış '23:15 Rıhtım' ibaresi ve silik bir mühür var.",
                    "details": "ÖZEL BİLGİ: Kağıt kalitesi yüksek ve köşesinde yabancı bir konsolosluğun mührü var. 'Sakın gecikme, her şeyi öğrenmiş' şeklinde panikle yazılmış bir not bulunuyor.",
                    "suspect_hint": "Lord Henry veya Uşak James bu mührü hemen tanıyacaktır.",
                    "collected": False
                },
                {
                    "id": "clue_kut_2",
                    "name": "Pirinç Çekmece Anahtarı",
                    "description": "Halı püsküllerinin arasına düşmüş, üzerinde 'Kasa-3' yazılı küçük antika anahtar.",
                    "details": "ÖZEL BİLGİ: Masif pirinçten dökülmüş, kurbanın gizli günlük çekmecesini açıyor olabilir. Üzerinde taze yağ lekeleri var.",
                    "suspect_hint": "Konağın anahtarları sadece Hizmetçi Mary'de durur.",
                    "collected": False
                }
            ],
            "Çalışma Odası": [
                {
                    "id": "clue_cal_1",
                    "name": "Devrilmiş Mürekkep Lekesi",
                    "description": "Hemen yanında bir mücadelenin yaşandığını gösteren tırnak çizikleri var.",
                    "details": "ÖZEL BİLGİ: Mürekkep tamamen kurumamış. Masa kenarında tırnak izleri ve yere saçılmış boş kağıtlar ani bir tartışmayı kanıtlıyor.",
                    "suspect_hint": "Katilin ellerinde veya manşetinde mürekkep izi kalmış olmalı.",
                    "collected": False
                },
                {
                    "id": "clue_cal_2",
                    "name": "Tehdit Mektubu Karalaması",
                    "description": "'Hisselerini devretmezsen her şeyi açıklarım' cümlesi güçlükle okunuyor.",
                    "details": "ÖZEL BİLGİ: Şöminede yakılmak istenmiş ama kurtarılmış. Sol alt köşesinde zarifçe karalanmış 'M' harfi göze çarpıyor.",
                    "suspect_hint": "Bu yazı tipini Bayan Margaret'a gösterip tepkisini ölçmelisiniz.",
                    "collected": False
                }
            ],
            "Kış Bahçesi": [
                {
                    "id": "clue_kis_1",
                    "name": "Kırık Cam Parçası",
                    "description": "Dışarıdan içeriye doğru kırılmış, üzerinde kumaş ipliği takılı.",
                    "details": "ÖZEL BİLGİ: Camın kenarında koyu kırmızı, kaba dokunmuş bir paltoya ait iplik parçaları kalmış.",
                    "suspect_hint": "Kırmızı palto giyen şüphelinin kıyafetlerini inceleyin.",
                    "collected": False
                }
            ],
            "Mahzen": [
                {
                    "id": "clue_mah_1",
                    "name": "Kayıp Şarap Şişesi",
                    "description": "Koleksiyondaki en değerli şişenin yeri boş, yerde taze ayak izi var.",
                    "details": "ÖZEL BİLGİ: 1884 rekoltesi şarabın yeri boş. Cinayet aleti olarak başa vurulmuş olma ihtimali çok yüksek.",
                    "suspect_hint": "Gece yarısı mahzene indiği görülen şüpheliyi sıkıştırın.",
                    "collected": False
                }
            ]
        }
    
    if "active_suspect_clue" not in st.session_state:
        st.session_state.active_suspect_clue = None

    if "audio_enabled" not in st.session_state:
        st.session_state.audio_enabled = True

@st.dialog("🔬 KRİMİNAL İNCELEME")
def show_clue_investigation(clue, room_name):
    """Büyüteç pop-up'ı ve Şüpheliye Sorma Aksiyonu."""
    st.markdown(f"""
        <div class="case-file-popup">
            <div class="popup-title">🔍 DETAYLI ANALİZ RAPORU</div>
            <p><strong>KANIT ADI:</strong> {clue['name']}</p>
            <p><strong>BULUNDUĞU YER:</strong> {room_name}</p>
            <hr style="border-top: 1px dashed #4a3424;">
            <p><strong>OLAY YERİ BULGULARI:</strong></p>
            <p style="font-style: italic; font-size: 14px;">"{clue['description']}"</p>
            <hr style="border-top: 1px dashed #4a3424;">
            <p><strong>KRİMİNAL NOTLAR VE DETAYLAR:</strong></p>
            <p style="line-height: 1.5; font-size: 14px;">{clue.get('details', '')}</p>
            <hr style="border-top: 1px dashed #4a3424;">
            <p><strong>💡 DEDEKTİF NOTU:</strong> <span style="color: #8c2d19; font-weight: bold;">{clue.get('suspect_hint', '')}</span></p>
        </div>
    """, unsafe_allow_html=True)
    
    st.write("")
    c1, c2, c3 = st.columns([1, 1.3, 1.4])
    
    with c1:
        if st.button("❌ Kapat", use_container_width=True):
            st.rerun()

    with c2:
        if st.button("💼 Çantaya Koy", use_container_width=True):
            for c in st.session_state.clues_db.get(room_name, []):
                if c["id"] == clue["id"]:
                    c["collected"] = True
            st.toast(f"'{clue.get('name')}' çantaya kaldırıldı!", icon="💼")
            st.rerun()

    with c3:
        if st.button("👥 Şüpheliye Sor", use_container_width=True):
            for c in st.session_state.clues_db.get(room_name, []):
                if c["id"] == clue["id"]:
                    c["collected"] = True
            st.session_state.active_suspect_clue = clue
            st.toast(f"'{clue.get('name')}' sorgu masasına alındı! Şüpheli odasına geçebilirsiniz.", icon="⚖️")
            st.rerun()

def play_ambient_audio(selected_room: str):
    """Yerel ses dosyalarını (assets/*.mp3) base64 ile kesintisiz ve sonsuz döngüde çalar."""
    assets_dir = os.path.join(os.path.dirname(__file__), "..", "assets")
    
    room_sound_files = {
        "Kış Bahçesi": "rain_ambient.mp3",
        "Çalışma Odası": "fireplace_ambient.mp3",
        "Kütüphane": "clock_ambient.mp3",
        "Mahzen": "cellar_ambient.mp3"
    }

    if st.session_state.audio_enabled:
        sound_file = room_sound_files.get(selected_room, "rain_ambient.mp3")
        sound_path = os.path.join(assets_dir, sound_file)

        if os.path.exists(sound_path):
            with open(sound_path, "rb") as f:
                audio_base64 = base64.b64encode(f.read()).decode()

            # Kütüphane gibi sessiz odalar için ses biraz daha hafif (%18), diğerleri %24
            volume_level = 0.18 if selected_room == "Kütüphane" else 0.24

            sound_html = f"""
            <audio id="noir-ambient" src="data:audio/mp3;base64,{audio_base64}" autoplay loop playsinline></audio>
            <script>
                (function() {{
                    var audio = document.getElementById("noir-ambient");
                    if (audio) {{
                        audio.volume = {volume_level};
                        audio.onended = function() {{
                            audio.currentTime = 0;
                            audio.play();
                        }};
                        var promise = audio.play();
                        if (promise !== undefined) {{
                            promise.catch(function() {{
                                document.addEventListener('click', function() {{
                                    audio.play();
                                }}, {{ once: true }});
                            }});
                        }}
                    }}
                }})();
            </script>
            """
            st.markdown(sound_html, unsafe_allow_html=True)

def render_sidebar(selected_room: str):
    """Sol menüdeki dedektif çantası ve arka planda görünmez çalan ambiyans kontrolü."""
    st.sidebar.markdown('<div class="sidebar-title">💼 DEDEKTİF ÇANTASI</div>', unsafe_allow_html=True)
    
    # Odalara göre ses dosyaları
    assets_dir = os.path.join(os.path.dirname(__file__), "..", "assets")
    room_sound_files = {
        "Kış Bahçesi": "rain_ambient.mp3",
        "Çalışma Odası": "fireplace_ambient.mp3",
        "Kütüphane": "clock_ambient.mp3",
        "Mahzen": "cellar_ambient.mp3"
    }

    # Sade açma/kapatma anahtarı (Çubuk/oynatıcı yok)
    audio_on = st.sidebar.toggle("📻 Olay Yeri Ambiyansı", value=st.session_state.audio_enabled)
    if audio_on != st.session_state.audio_enabled:
        st.session_state.audio_enabled = audio_on
        st.rerun()

    sound_file = room_sound_files.get(selected_room, "rain_ambient.mp3")
    sound_path = os.path.join(assets_dir, sound_file)

    if os.path.exists(sound_path):
        if st.session_state.audio_enabled:
            st.sidebar.caption(f"🎶 *{selected_room} havası çalıyor...*")
            with open(sound_path, "rb") as f:
                audio_base64 = base64.b64encode(f.read()).decode()

            target_volume = 0.05 if selected_room == "Kütüphane" else 0.08

            # 'controls' özelliği kaldırıldı, 'display:none' ile görsel çubuk tamamen gizlendi
            audio_player_html = f"""
            <audio id="ambient-player" src="data:audio/mp3;base64,{audio_base64}" autoplay loop style="display:none;"></audio>
            <script>
                var player = document.getElementById("ambient-player");
                if (player) {{
                    player.volume = {target_volume};
                    var promise = player.play();
                    if (promise !== undefined) {{
                        promise.catch(function() {{
                            document.addEventListener('click', function() {{
                                player.play();
                            }}, {{ once: true }});
                        }});
                    }}
                }}
            </script>
            """
            st.sidebar.markdown(audio_player_html, unsafe_allow_html=True)
        else:
            st.sidebar.caption("🔇 *Ambiyans kapatıldı.*")
    else:
        st.sidebar.warning(f"⚠️ `{sound_file}` dosyası bulunamadı!")

    st.sidebar.markdown("---")

    # Çantadaki delilleri listeleme
    collected_clues = []
    total_clues_count = 0
    for room, clues in st.session_state.clues_db.items():
        for clue in clues:
            total_clues_count += 1
            if clue.get("collected", False):
                collected_clues.append((clue, room))
                
    collected_count = len(collected_clues)
    
    st.sidebar.markdown(f"**Toplanan Kanıtlar ({collected_count} / {total_clues_count})**")
    progress = collected_count / total_clues_count if total_clues_count > 0 else 0
    st.sidebar.progress(progress)
    
    if st.session_state.active_suspect_clue:
        st.sidebar.success(f"🎯 **Sorgu Masasında:**\n\n*{st.session_state.active_suspect_clue['name']}*")

    st.sidebar.markdown("---")
    
    if not collected_clues:
        st.sidebar.info("💼 Çantanız henüz boş. Olay yerlerini dolaşıp ipuçları toplayın.")
    else:
        for clue, room in collected_clues:
            st.sidebar.markdown(f"""
                <div class="sidebar-item">
                    <strong>📜 {clue['name']}</strong><br>
                    <small>📍 {room}</small>
                </div>
            """, unsafe_allow_html=True)

def render_room_view(session_id: str):
    init_mock_database()

    room_details = {
        "Kütüphane": {
            "icon": "📚",
            "desc": "Tavandan tabana eski meşe raflar. Şömine külleri henüz ılık, yerde aceleyle yırtılmış bir sayfa var."
        },
        "Çalışma Odası": {
            "icon": "🖋️",
            "desc": "Kurbanın masası burada. Çekmeceler zorlanmış, antika mürekkep hokkası halıya dökülmüş."
        },
        "Kış Bahçesi": {
            "icon": "🌿",
            "desc": "Cam tavanlı nemli sera. Geniş yapraklı saksılardan birinde taze kazılmış bir çukur görünüyor."
        },
        "Mahzen": {
            "icon": "🍷",
            "desc": "Tozlu şişeler, kırık kadehler ve kilitli servis kapısına doğru giden ıslak ayak izleri."
        }
    }

    # 1. Oda Navigasyonu
    nav_c1, nav_c2 = st.columns([1.1, 2])
    with nav_c1:
        selected_room = st.selectbox(
            "İncelenecek Odayı Seçin:",
            list(room_details.keys()),
            format_func=lambda r: f"{room_details[r]['icon']} {r}"
        )

    apply_detective_theme(selected_room)
    play_ambient_audio(selected_room)
    render_sidebar(selected_room)

    # 2. Üst Banner
    st.markdown("""
        <div class="case-header">
            <div class="case-header-title">🕵️ VAKA SAHASI: OLAY YERİ DELİL ARAŞTIRMASI</div>
            <div class="case-header-sub">Konağın gizemini çözmek için odaları inceleyin, şüpheli nesneleri delil torbasına aktarın.</div>
        </div>
    """, unsafe_allow_html=True)

    with nav_c2:
        info = room_details[selected_room]
        st.markdown(f"""
            <div class="room-observation-box">
                <div><strong>📍 Mekan İntibası:</strong> {info['desc']}</div>
            </div>
        """, unsafe_allow_html=True)

    # 3. İpuçlarını Getir
    try:
        clues = clue_engine.get_room_clues(session_id, selected_room)
    except Exception:
        clues = st.session_state.clues_db.get(selected_room, [])

    room_total = len(clues)
    room_collected = sum(1 for c in clues if c.get("collected", False))

    st.markdown("<br>", unsafe_allow_html=True)
    
    col_stat1, col_stat2 = st.columns([3, 1])
    with col_stat1:
        st.markdown(f"#### 🔎 {selected_room} Delilleri")
    with col_stat2:
        st.markdown(f"**Oda Durumu:** `{room_collected} / {room_total} Toplandı`")

    if not clues:
        st.info("Bu mekanda gözden kaçan başka bir kanıt görünmüyor.")
        return

    # 4. Izgara (Grid) Düzeninde Kartlar
    for i in range(0, len(clues), 2):
        col_left, col_right = st.columns(2)
        
        with col_left:
            render_clue_card(clues[i], selected_room, index=i+1)

        if i + 1 < len(clues):
            with col_right:
                render_clue_card(clues[i + 1], selected_room, index=i+2)

def render_clue_card(clue, room_name, index):
    """Tek bir delil kartı."""
    is_collected = clue.get("collected", False)
    badge_html = '<span class="badge-collected">✓ Çantada / İncelendi</span>' if is_collected else '<span class="badge-pending">● İncelenmedi</span>'
    
    st.markdown(f"""
        <div class="clue-dossier-card">
            <div>
                <div class="dossier-tag">KANIT KÜTÜĞÜ #{index:02d}</div>
                <div class="clue-card-name">📜 {clue.get('name', 'Bilinmeyen Delil')}</div>
                <div class="clue-card-desc">{clue.get('description', '')}</div>
            </div>
            <div>{badge_html}</div>
        </div>
    """, unsafe_allow_html=True)
    
    st.write("")
    btn_text = "İncele (Çantada) 🔍" if is_collected else "İncele & Analiz Et 🔍"
    if st.button(btn_text, key=f"btn_investigate_{clue['id']}", use_container_width=True):
        show_clue_investigation(clue, room_name)
