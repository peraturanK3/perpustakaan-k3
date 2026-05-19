import streamlit as st
import requests
from bs4 import BeautifulSoup
import re

st.set_page_config(page_title="Perpustakaan K3 Indonesia", layout="wide")

st.markdown("""
<style>
.stApp {
    background-color: #f4f1ea;
    font-family: 'Georgia', serif;
}
h1 {
    text-align: center;
    border-bottom: 3px double #8b7355;
    padding-bottom: 15px;
    color: #5c4a32;
}
.card {
    background: white;
    padding: 20px;
    border-radius: 8px;
    box-shadow: 0 2px 5px rgba(0,0,0,0.1);
    margin-bottom: 15px;
}
.card h3 {
    color: #5c4a32;
    margin-top: 0;
}
.download-btn {
    display: inline-block;
    background-color: #8b7355;
    color: white !important;
    padding: 8px 16px;
    border-radius: 5px;
    text-decoration: none;
}
</style>
""", unsafe_allow_html=True)

st.title("📚 Perpustakaan Digital K3 Indonesia")
st.markdown("*Kumpulan lengkap Peraturan Keselamatan dan Kesehatan Kerja terbaru*")

def get_kemnaker_links():
    try:
        url = "https://bskkpnaker.kemnaker.go.id/hasil"
        r = requests.get(url, timeout=30)
        soup = BeautifulSoup(r.text, "lxml")
        links = []
        for a in soup.find_all("a", href=re.compile(r"\.zip$", re.I)):
            judul = a.text.strip()
            link = a['href']
            if not link.startswith("http"):
                link = requests.compat.urljoin(url, link)
            links.append({"judul": judul, "link": link})
        return links
    except:
        return []

tab1, tab2 = st.tabs(["🔍 Cari Peraturan", "📖 Daftar Lengkap"])

with tab1:
    keyword = st.text_input("Cari berdasarkan judul atau tahun:", 
                            placeholder="Contoh: APD, 2023, Listrik")
    
    if st.button("Cari", type="primary"):
        with st.spinner("Mencari di database Kemnaker..."):
            data = get_kemnaker_links()
            if not data:
                st.error("Gagal mengambil data dari Kemnaker")
            else:
                hasil = [d for d in data if keyword.lower() in d["judul"].lower()] if keyword else data
                if not hasil:
                    st.warning("Tidak ditemukan peraturan dengan keyword tersebut")
                else:
                    st.success(f"Ditemukan {len(hasil)} peraturan")
                    for item in hasil:
                        st.markdown(f"""
                        <div class="card">
                            <h3>{item['judul']}</h3>
                            <a href="{item['link']}" target="_blank" class="download-btn">⬇️ Download ZIP</a>
                        </div>
                        """, unsafe_allow_html=True)

with tab2:
    st.info("Memuat semua peraturan K3 dari Kemnaker...")
    with st.spinner("Mengambil data..."):
        data = get_kemnaker_links()
        if not data:
            st.error("Gagal mengambil data dari Kemnaker")
        else:
            st.success(f"Total {len(data)} peraturan tersedia")
            for item in data:
                st.markdown(f"""
                <div class="card">
                    <h3>{item['judul']}</h3>
                    <a href="{item['link']}" target="_blank" class="download-btn">⬇️ Download ZIP</a>
                </div>
                """, unsafe_allow_html=True)

st.markdown("---")
st.caption("Data diambil langsung dari https://bskkpnaker.kemnaker.go.id")