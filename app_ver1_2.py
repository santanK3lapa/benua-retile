
import streamlit as st
import laspy
import numpy as np
from io import BytesIO

# === Tajuk & Pengenalan ===
st.set_page_config(page_title="BENUA Retile GUI", layout="wide")
st.title("🟢 BENUA Retile GUI (Demo Versi)")
st.markdown("""
Versi antaramuka untuk sistem **retile dan buffer** fail LAS dengan sampling dan penyimpanan semula.
""")

# === Sidebar Input ===
with st.sidebar:
    st.header("⚙️ Parameter Tiling")

    tile_size = st.selectbox("📏 Saiz Tile (meter)", [500, 1000, 2000], index=1)
    rounding = st.selectbox("📐 Bundar koordinat ke", [100, 1000], index=1)
    buffer_dist = st.selectbox("📦 Saiz Buffer (meter)", [0, 10, 20, 50], index=2)

    crs = st.selectbox("🌐 Sistem Koordinat (EPSG)", [
        "WGS84 / UTM Zone 47N (EPSG:32647)",
        "WGS84 / UTM Zone 48N (EPSG:32648)",
        "WGS84 / UTM Zone 49N (EPSG:32649)",
        "WGS84 / UTM Zone 50N (EPSG:32650)",
        "WGS84 (LatLong) (EPSG:4326)",
        "Cassini Malaysia (EPSG:33801)",
        "Unknown / Manual EPSG"
    ], index=1)

    if "Unknown" in crs:
        epsg_code = st.number_input("Masukkan EPSG secara manual", value=4326)
    else:
        epsg_code = int(crs.split(":")[-1].replace(")", ""))

    uploaded_file = st.file_uploader("📁 Muat naik fail LAS sahaja", type=["las"])

# === Kandungan Utama ===
st.subheader("📊 Ringkasan Parameter")

st.markdown(f"""
- **Saiz Tile**: `{tile_size} meter`
- **Pembundaran Koordinat**: `{rounding}`
- **Buffer**: `{buffer_dist} meter`
- **EPSG Code**: `{epsg_code}`
""")

if uploaded_file:
    st.success(f"Fail `{uploaded_file.name}` dimuat naik!")
else:
    st.warning("❗ Tiada fail dimuat naik.")

# === Sampling dan Simpan .las ===
def sample_and_save_las(uploaded_file, interval):
    las = laspy.read(uploaded_file)
    mask = np.arange(0, len(las.x), interval)

    new_las = laspy.LasData(las.header)
    for dim in las.point_format.dimension_names:
        if hasattr(las, dim):
            setattr(new_las, dim, getattr(las, dim)[mask])

    output = BytesIO()
    new_las.write(output)
    output.seek(0)

    base = uploaded_file.name.rsplit('.', 1)[0]
    filename = f"{base}_deci_{interval}.las"
    return output, filename

# === Pilih Interval dan Proses ===
if uploaded_file and uploaded_file.name.endswith(".las"):
    interval = st.selectbox("🔄 Sampling setiap berapa point?", [100, 1000, 10000])

    if st.button("📤 Simpan sebagai .las (disampel)"):
        with st.spinner("Sedang memproses dan menjana fail..."):
            output, filename = sample_and_save_las(uploaded_file, interval)
            st.success(f"✅ Fail {filename} telah dijana.")
            st.download_button("📥 Muat Turun Fail .las", output, file_name=filename, mime="application/octet-stream")
