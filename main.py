import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go
from scipy.signal import butter, filtfilt
from scipy import stats
import uuid
from datetime import datetime

class OceanSignalEngine:
    @staticmethod
    def calculate_sampling_rate(df, time_col):
        """Menghitung interval data (menit) dengan proteksi tipe data."""
        try:
            times = pd.to_datetime(df[time_col])
            if len(times) < 2: return 60.0
            delta = times.diff().dt.total_seconds().median()
            return max(0.1, delta / 60.0)
        except: return 1.0
    # Pembersihan data
    @staticmethod
    def get_cleaned_data(series, threshold=3.0):
        """Konversi data ke numerik, Interpolasi & Hapus Outlier"""
        s = pd.to_numeric(series, errors='coerce')
        cleaned = s.interpolate(method='linear').fillna(method='bfill').fillna(method='ffill')
        if cleaned.std() == 0: return cleaned
        z_scores = np.abs(stats.zscore(cleaned.fillna(cleaned.mean())))
        cleaned[z_scores > threshold] = np.nan
        return cleaned.interpolate(method='linear').fillna(method='bfill').fillna(method='ffill')

    #perhitungan lowpass filter
    @staticmethod
    def apply_low_pass(series, cutoff_hours, sr_min):
        if cutoff_hours <= 0: return pd.to_numeric(series, errors='coerce').values
        y = pd.to_numeric(series, errors='coerce').interpolate().fillna(method='ffill').fillna(method='bfill').values
        nyquist = 0.5 * (1.0 / (sr_min * 60.0))
        cutoff_hz = 1.0 / (cutoff_hours * 3600.0)
        wn = cutoff_hz / nyquist
        if wn >= 1.0: return y
        b, a = butter(N=4, Wn=wn, btype='low', analog=False)
        return filtfilt(b, a, y)
    # Perhitungan moving average
    @staticmethod
    def apply_moving_avg(series, window_hours, sr_min):
        s = pd.to_numeric(series, errors='coerce')
        if window_hours <= 0: return s.values
        pts = int((window_hours * 60.0) / sr_min)
        return s.rolling(window=max(1, pts), center=True, min_periods=1).mean().values
    #perhitungan nilai data
    @staticmethod
    def get_summary_stats(data, name):
        s = pd.Series(data).dropna()
        if len(s) == 0: return None
        return {
            "Label": name,
            "Min": float(s.min()),
            "Max": float(s.max()),
            "Mean": float(s.mean()),
            "Std Dev": float(s.std()),
            "Count": int(len(s))
        }

def apply_professional_theme():
    st.markdown("""
        <style>
        .stApp { background-color: #0e1117; color: #ffffff; }
        [data-testid="stSidebar"] { background-color: #161b22; border-right: 1px solid #30363d; }
        .stDataFrame, .chart-container { border: 1px solid #30363d; border-radius: 8px; }
        h1, h2, h3, p, label, .stMarkdown { color: #ffffff !important; }
        .stButton>button {
            border-radius: 5px; font-weight: bold; background-color: #21262d;
            color: white; border: 1px solid #30363d; width: 100%;
        }
        .stButton>button:hover { border-color: #ff4b4b; color: #ff4b4b; }
        .layer-control-box {
            background-color: #1c2128; padding: 12px; border-radius: 8px;
            border: 1px solid #30363d; margin-bottom: 10px;
            min-height: 100px;
        }
        </style>
    """, unsafe_allow_html=True)

# pengaturan warna
CHART_COLORS = ['#EF553B', '#00CC96', '#AB63FA', '#FFA15A', '#19D3F3', '#FF6692', '#B6E880']
def main():
    st.set_page_config(page_title="OceanData Pro Analytics", layout="wide", page_icon="🌊")
    apply_professional_theme()
    if 'layers' not in st.session_state:
        st.session_state.layers = []

    st.title("🌊 OceanData Pro: Dashboard Pengolahan Data Oseanografi")
    with st.sidebar:
        st.header("📂 Input Data")
        uploaded_file = st.file_uploader("Upload File (.csv,.xlsx)", type=['csv', 'xlsx'])
        if uploaded_file:
            if st.button("Reset Layer"):
                st.session_state.layers = []
                st.rerun()
    if not uploaded_file:
        st.info("Silakan menggungah file dataset")
        return
    try:
        df_raw = pd.read_csv(uploaded_file) if uploaded_file.name.endswith('.csv') else pd.read_excel(uploaded_file)
        time_col = next((c for c in df_raw.columns if any(x in c.lower() for x in ['time', 'date', 'timestamp'])), None)
        if not time_col:
            st.error("Gagal mendeteksi kolom waktu"); 
            return
        df_raw[time_col] = pd.to_datetime(df_raw[time_col], errors='coerce')
        df_raw = df_raw.dropna(subset=[time_col]).sort_values(time_col)
        sr = OceanSignalEngine.calculate_sampling_rate(df_raw, time_col)
        # Pengaturan tabel
        st.header("🔍 Tampilan Data")
        all_cols = df_raw.columns.tolist()
        selected_cols = st.multiselect("Pilih Kolom Tabel:", all_cols, default=all_cols[:8]) 
        c_t1, c_t2 = st.columns(2)
        start_d = c_t1.date_input("Mulai Waktu:", df_raw[time_col].min().date())
        end_d = c_t2.date_input("Selesai Waktu:", df_raw[time_col].max().date())
        mask = (df_raw[time_col].dt.date >= start_d) & (df_raw[time_col].dt.date <= end_d)
        df_filtered = df_raw.loc[mask, selected_cols].copy().reset_index(drop=True)
        st.dataframe(df_filtered.head(100), use_container_width=True)

        # Pengaturan konfigurasi grafik
        st.divider()
        st.header("📈 Konfigurasi Grafik")
        col_cfg1, col_cfg2, col_cfg3 = st.columns([2, 2, 2])
        with col_cfg1:
            numeric_cols = [c for c in df_filtered.columns if c != time_col]
            y_param = st.selectbox("Pilih Parameter Y:", numeric_cols)
            base_mode = st.radio("Pilih Tipe Data:", ["Raw Data", "Cleaned Data", "Raw + Cleaned"], horizontal=True)
        with col_cfg2:
            target_filters = st.multiselect("Pilih Jenis Filter:", 
                                          ["Moving Average", "Low Pass Filter", "Averaging (Resample)"])
        with col_cfg3:
            f_win = st.slider("Set Window Size (Jam):", 0, 48, 1)
            if st.button("Tambahkan"):
                for ft in target_filters:
                    layer_id = str(uuid.uuid4())
                    st.session_state.layers.append({
                        "id": layer_id, "type": ft, "win": f_win, "y": y_param, "base": base_mode
                    })
                st.rerun()
        # Perhitungan statistik
        global_stats = []
        raw_series = pd.to_numeric(df_filtered[y_param], errors='coerce')
        clean_series = OceanSignalEngine.get_cleaned_data(raw_series)
        global_stats.append(OceanSignalEngine.get_summary_stats(raw_series, f"Raw {y_param}"))
        global_stats.append(OceanSignalEngine.get_summary_stats(clean_series, f"Cleaned {y_param}"))

        # Merender bentuk grafik
        # Grafik data mentah
        st.subheader(f"📊 Grafik Data Raw (Mentah): {y_param}")
        fig_base = go.Figure()
        if "Raw" in base_mode:
            fig_base.add_trace(go.Scatter(x=df_filtered[time_col], y=raw_series, name="Raw", line=dict(color='gray', width=1), opacity=0.6))
        if "Cleaned" in base_mode:
            fig_base.add_trace(go.Scatter(x=df_filtered[time_col], y=clean_series, name="Cleaned", line=dict(color='#58a6ff', width=2)))
        fig_base.update_layout(template="plotly_dark", height=400, paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)", hovermode="x unified", xaxis=dict(rangeslider=dict(visible=True)))
        st.plotly_chart(fig_base, use_container_width=True)
        # Grafik Per Jenis Filter 
        current_active_types = sorted(list(set([l['type'] for l in st.session_state.layers])))
        for f_type in current_active_types:
            # pengaturan item spesifik 
            type_layers = [l for l in st.session_state.layers if l['type'] == f_type]
            # Jika tidak ada layer untuk tipe ini, lewati section ini sepenuhnya
            if not type_layers:
                continue
            st.divider()
            st.subheader(f"📈 Grafik Analisis: {f_type}")
            st.write(f"**Manajemen Layer {f_type}:**")
            # pengaturan tombol kontrol
            n_cols = 3
            for i in range(0, len(type_layers), n_cols):
                cols = st.columns(n_cols)
                for idx, aw in enumerate(type_layers[i:i+n_cols]):
                    color = CHART_COLORS[(i + idx) % len(CHART_COLORS)]
                    with cols[idx]:
                        st.markdown(f"""
                        <div class='layer-control-box'>
                            <span style='color:{color}; font-size:20px;'>●</span> 
                            <b>{aw['type']}</b><br>
                            <small>{aw['win']} Jam — {aw['y']}</small>
                        </div>
                        """, unsafe_allow_html=True)
                        if st.button(f"❌ Hapus Layer", key=aw['id']):
                            # Hapus data dari session_state
                            st.session_state.layers = [l for l in st.session_state.layers if l['id'] != aw['id']]
                            # Paksa rerun agar UI langsung terhapus
                            st.rerun()
            # Render perhitungan Grafik
            fig = go.Figure()
            y_ref = clean_series if "Cleaned" in base_mode else raw_series
            fig.add_trace(go.Scatter(x=df_filtered[time_col], y=y_ref, name="Reference", line=dict(color='gray', width=1), opacity=0.3))
            for i, aw in enumerate(type_layers):
                src = pd.to_numeric(df_filtered[aw['y']], errors='coerce')
                if "Cleaned" in aw['base']: src = OceanSignalEngine.get_cleaned_data(src)
                p_x, p_y = df_filtered[time_col], None
                label = f"{aw['win']} Jam"
                if f_type == "Moving Average":
                    p_y = OceanSignalEngine.apply_moving_avg(src, aw['win'], sr)
                elif f_type == "Low Pass Filter":
                    p_y = OceanSignalEngine.apply_low_pass(src, aw['win'], sr)
                elif f_type == "Averaging (Resample)":
                    res_df = df_filtered[[time_col]].copy()
                    res_df['val'] = src
                    res_df = res_df.set_index(time_col).resample(f"{aw['win']}H" if aw['win'] > 0 else "1T").mean().reset_index()
                    p_x, p_y = res_df[time_col], res_df['val']
                if p_y is not None:
                    fig.add_trace(go.Scatter(
                        x=p_x, y=p_y, name=label, 
                        line=dict(width=2.5, color=CHART_COLORS[i % len(CHART_COLORS)]),
                        mode='lines+markers' if "Averaging" in f_type else 'lines'
                    ))
                    global_stats.append(OceanSignalEngine.get_summary_stats(p_y, f"{f_type} ({label})"))

            fig.update_layout(template="plotly_dark", height=500, paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)", hovermode="x unified", xaxis=dict(rangeslider=dict(visible=True)))
            st.plotly_chart(fig, use_container_width=True)

        # Pengaturan tabel Statistik
        st.divider()
        st.header("🔢 Statistika Data")
        valid_stats = [s for s in global_stats if s is not None]
        if valid_stats:
            df_stats = pd.DataFrame(valid_stats).set_index("Label")
            st.table(df_stats.style.format("{:.3f}"))

    except Exception as e:
        st.error(f"Terjadi kesalahan: {e}")

if __name__ == "__main__":
    main()