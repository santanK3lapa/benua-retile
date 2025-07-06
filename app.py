
import streamlit as st

# === Tajuk & Pengenalan ===
st.set_page_config(page_title="BENUA Retile GUI", layout="wide")
st.title("🟢 BENUA Retile GUI (Demo Versi)")
st.markdown("""
Versi awal antaramuka untuk sistem **retile dan buffer** fail LAS/LAZ dengan penamaan `E####N####`.
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

    uploaded_file = st.file_uploader("📁 Muat naik fail dummy (CSV/LAS)", type=["csv", "las", "laz"])

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
    st.warning("❗ Tiada fail dimuat naik. Ini hanya demo GUI, tidak perlu fail sebenar.")

# === Butang Proses ===
if st.button("🚀 Jalankan Proses (Simulasi)"):
    st.info("🔧 Menjana tile koordinat... (simulasi)")
    st.success("✅ Selesai! 36 tiles dijana dengan buffer 20m.")
    st.download_button("📥 Muat turun shapefile (dummy)", "Shapefile_dummy_content", file_name="tiles_buffer_20m.zip")
