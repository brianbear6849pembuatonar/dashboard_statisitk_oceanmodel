import streamlit as st
#Pengaturan UI/Ux Web
class UIComponents:
    @staticmethod
    def render_header():
        st.title("🌊 OceanData Pro Analysis")
        st.caption("Professional Signal Processing for Oceanographic & Meteorological Data")

    @staticmethod
    def render_welcome_screen():
        st.info("Selamat datang. Silakan unggah file data di sidebar untuk memulai pencarian dan analisis.")

    @staticmethod
    def render_stats_cards(stats):
        cols = st.columns(len(stats))
        for i, (k, v) in enumerate(stats.items()):
            cols[i].metric(label=k, value=v)