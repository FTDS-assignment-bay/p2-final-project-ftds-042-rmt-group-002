## 📁 Struktur File Proyek Clusturn

Aplikasi ini terdiri dari beberapa komponen utama yang saling terintegrasi, baik untuk eksplorasi data, prediksi churn, klasterisasi, maupun visualisasi dengan Streamlit.

---

### 🧪 Script Utama

- `eda.py`  
  Menyediakan tampilan menu utama aplikasi yang berisi pengantar, penjelasan singkat, serta navigasi ke fitur-fitur lain seperti prediksi.

- `prediction.py`  
  Melakukan prediksi kemungkinan churn untuk satu pelanggan berdasarkan input fitur.

- `batch_prediction.py`  
  Melakukan prediksi churn dalam jumlah besar (batch), menggunakan file CSV berisi data banyak pelanggan.

- `streamlit_app.py`
  Merupakan titik masuk utama aplikasi Streamlit yang **menyatukan semua fitur** dari `eda.py`, `prediction.py`, dan `batch_prediction.py` ke dalam satu antarmuka interaktif.

---

### 🐳 Deployment

- `Dockerfile`  
  File konfigurasi Docker untuk menjadikan aplikasi dapat dijalankan secara terisolasi dan portabel di berbagai environment.

- `requirements.txt`  
  Daftar dependensi (library Python) yang dibutuhkan untuk menjalankan aplikasi. Akan otomatis diinstal saat build Docker.

---

### 📦 Model Machine Learning

- `churn_model.pkl`  
  File model prediksi churn (dalam format pickle), hasil dari proses training dengan data historis pelanggan.

- `kproto_bundle.pkl`  
  File model clustering pelanggan menggunakan algoritma K-Prototypes. Berguna untuk segmentasi pelanggan.

---

### 🔗 Akses Aplikasi Online

Aplikasi ini dapat diakses secara langsung melalui Hugging Face Spaces:  
👉 [Clusturn on Hugging Face](https://huggingface.co/spaces/azhar-muhammad/clusturn)

## 🧾 Metadata Hugging Face Spaces

Bagian di bawah ini merupakan metadata yang **wajib disertakan di bagian paling atas file `README.md`** jika kamu melakukan deployment aplikasi di [Hugging Face Spaces](https://huggingface.co/spaces). Metadata ini digunakan oleh platform untuk mengatur:

- Judul dan ikon aplikasi
- Warna latar kartu aplikasi
- SDK yang digunakan (misalnya Streamlit, Gradio, atau Docker)
- Port aplikasi
- Tag pencarian dan deskripsi singkat

Tanpa metadata ini, aplikasi mungkin tetap berjalan, tetapi tidak akan ditampilkan dengan benar di katalog Spaces.

```yaml
title: Clusturn
emoji: 🚀
colorFrom: red
colorTo: red
sdk: docker
app_port: 8501
tags:
  - streamlit
pinned: false
short_description: Streamlit template space
