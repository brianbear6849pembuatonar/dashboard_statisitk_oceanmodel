# 🌊 OceanData Pro Analysis
**Dashboard  Signal Analysis & Comparative Visualization Ocean Data**

Ocean OceanData Pro Analysis adalah platform analitik berbasis web yang dirancang untuk pengolahan sinyal deret waktu (time-series) pada data observasi oseanografi. Platform ini memungkinkan peneliti untuk melakukan transformasi sinyal secara multi-skala dan perbandingan metrik statistik dalam satu antarmuka *enterprise*.

## 🛠️ Key Scientific Modules

### 1. Anomaly Mitigation Engine
Menggunakan algoritma **Z-Score Outlier Removal** dan **Linear Interpolation** untuk membersihkan sinyal dari noise ekstrem tanpa merusak integritas tren data utama. Menghasilkan *Pre-processed Baseline* yang stabil untuk analisis lebih lanjut.

### 2. Digital Signal Transformation kernels
Platform ini menyediakan tiga metode transformasi utama:
* **Butterworth Digital Signal Filter**: Filter *low-pass* orde-4 untuk ekstraksi sinyal frekuensi rendah (seperti komponen pasut).
* **Temporal Moving Average (SMA)**: perata-rataan sinyal berbasis waktu untuk penghalusan tren menengah.
* **Discrete Interval Aggregation**: Resampling data otomatis menggunakan metode agregat rata-rata pada jendela waktu diskrit.

### 3. Observational Horizon Scoping
Fitur pencarian data dinamis yang memungkinkan pengguna menentukan **Attribute Vector** (parameter Y) dan batasan temporal (rentang waktu) secara presisi sebelum melakukan komitmen transformasi.

---

## Installation & Local Deployment

### Prerequisites
- Python 3.9+
- Pip (Python Package Manager)

## Module Description 
1. Core Module (Scientific Analytics Engine)
Modul utama yang menangani seluruh kalkulasi matematis dan algoritma pemrosesan sinyal:
###processor.py: Mengelola mitigasi anomali sinyal (Anomaly Mitigation), pembersihan data dari outlier menggunakan metode Z-Score, serta melakukan interpolasi data yang hilang.
###signal_logic.py: Implementasi algoritma transformasi sinyal utama, mencakup Butterworth Digital Filter orde-4 dan konvolusi temporal melalui Simple Moving Average (SMA).
###stats.py: Berfungsi menghitung metrik statistik deskriptif komparatif (Mean, Std Dev, Min/Max) untuk setiap analisis.

2. UI Module (Interface & Visualization)
Modul yang bertanggung jawab terhadap seluruh elemen visual dan interaksi pengguna. Adapun file data sebagai berikut:
###styles.py: kustomisasi CSS, tema web, dan interface (antarmuka) web.
###plots.py: Logika visualisasi deret waktu menggunakan Plotly, termasuk pengaturan palet warna dan pengaturan temporal.
###components.py: Komponen modular UI seperti KPI Metrics Cards, manajemen Operational Layer, dan navigasi kontrol di atas grafik.

3. Utils Module (Operational Support)
Sebagai fungsi pendukung untuk operasional sistem stabil. Adapun file data sebagai berikut:
###file_handler.py: Menangani akuisisi data observasi (Observational Data Acquisition) untuk format .csv dan .xlsx, serta validasi kolom waktu.
###helpers.py: Fungsi utilitas tambahan seperti pembuatan ID unik (UUID) untuk setiap lapisan grafik dan manajemen transisi antar Session State.

## Plaintext
ocean_analyzer_pro/
├── core/                
│   ├── __init__.py
│   ├── processor.py     
│   ├── signal_logic.py  
│   └── stats.py         
├── ui/                  
│   ├── __init__.py
│   ├── components.py    
│   ├── plots.py         
│   └── styles.py        
├── utils/               
│   ├── __init__.py
│   ├── file_handler.py  
│   └── helpers.py       
└── main.py

