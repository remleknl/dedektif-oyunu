import sys
import os

# Ana dizini Python yoluna ekle (engine klasörünü bulabilmesi için)
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

import streamlit as st


class NotebookUI:
    def __init__(self, engine=None):
        self.engine = engine

    def apply_notebook_styles(self):
        """room_view.py ile uyumlu noir dedektif teması için not defteri stilleri."""
        st.markdown("""
            <style>
            .notebook-banner {
                background: linear-gradient(90deg, rgba(20, 24, 33, 0.95) 0%, rgba(30, 36, 48, 0.85) 100%);
                border: 1px solid rgba(212, 175, 55, 0.4);
                border-left: 6px solid #d4af37;
                border-radius: 10px;
                padding: 14px 20px;
                margin-bottom: 16px;
                box-shadow: 0 6px 18px rgba(0, 0, 0, 0.5);
            }
            .notebook-banner-title {
                font-family: 'Cinzel', serif;
                font-size: 18px;
                font-weight: 700;
                color: #f6e05e;
                margin-bottom: 4px;
            }
            .notebook-banner-sub {
                font-size: 13px;
                color: #cbd5e0;
            }
            .clue-type-badge {
                display: inline-block;
                padding: 3px 10px;
                border-radius: 6px;
                font-size: 12px;
                font-weight: 600;
                letter-spacing: 0.4px;
            }
            </style>
        """, unsafe_allow_html=True)

    def get_clue_visuals(self, clue_type: str) -> dict:
        """İpucu türüne göre (physical / document / witness) ikon, etiket ve renk döner."""
        normalized_type = (clue_type or "").strip().lower()

        visuals_map = {
            "physical": {
                "icon": "🔍",
                "label": "Fiziksel Kanıt",
                "color": "#fbd38d",
                "bg_color": "rgba(156, 66, 33, 0.30)",
                "border_color": "#dd6b20",
            },
            "document": {
                "icon": "📜",
                "label": "Belge / Doküman",
                "color": "#90cdf4",
                "bg_color": "rgba(43, 108, 176, 0.30)",
                "border_color": "#3182ce",
            },
            "witness": {
                "icon": "🗣️",
                "label": "Tanık İfadesi",
                "color": "#d6bcfa",
                "bg_color": "rgba(107, 70, 193, 0.30)",
                "border_color": "#805ad5",
            },
        }

        return visuals_map.get(
            normalized_type,
            {
                "icon": "📌",
                "label": "Genel İpucu",
                "color": "#e2e8f0",
                "bg_color": "rgba(74, 85, 104, 0.35)",
                "border_color": "#718096",
            },
        )

    def show_key_clue_count(self, clues: list):
        """Toplanan ipuçları içindeki anahtar ipucu (is_key_clue) sayısını ve özetini gösterir."""
        self.apply_notebook_styles()

        clues = clues or []
        total_collected = len(clues)
        key_clues = [c for c in clues if c.get("is_key_clue", False)]
        key_count = len(key_clues)

        st.markdown(f"""
            <div class="notebook-banner">
                <div class="notebook-banner-title">🔑 KRİTİK DELİL ÖZETİ</div>
                <div class="notebook-banner-sub">
                    Toplam <strong>{total_collected}</strong> ipucundan
                    <strong style="color: #f6e05e;">{key_count}</strong> tanesi vakayı çözecek <strong>Anahtar İpucu</strong>.
                </div>
            </div>
        """, unsafe_allow_html=True)

        if total_collected == 0:
            st.info("Henüz toplanmış bir ipucu yok. Odaları inceleyerek kanıt toplamaya başlayabilirsiniz.")
        else:
            ratio = key_count / total_collected
            st.progress(ratio, text=f"Anahtar İpucu Oranı: {key_count} / {total_collected}")

    def show_collected_clues(self):
        # TODO (Hafta 2): Oyuncunun topladığı tüm ipuçlarını kart yapısıyla listele
        pass

    def list_caught_contradictions(self):
        # TODO (Hafta 3): Yakalanan çelişkileri listele
        pass