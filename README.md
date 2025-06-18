# Clusturn – Predicting & Clustering Churn Customers

**Clusturn** adalah sebuah sistem berbasis machine learning yang dirancang untuk mengatasi tantangan customer churn di industri telekomunikasi. Dengan mengintegrasikan model prediksi risiko dan segmentasi perilaku, sistem ini memberikan insight bagi perusahaan untuk menjalankan strategi retensi yang proaktif, personal, dan efisien, sehingga dapat meningkatkan loyalitas pelanggan

## 📌 Project Overview
Proyek ini bertujuan untuk membantu perusahaan telekomunikasi dalam **mengidentifikasi pelanggan yang berisiko churn** serta **memahami karakteristik pelanggan churn** melalui dua pendekatan utama:

1. **Model klasifikasi churn** menggunakan algoritma model klasifikasi.
2. **Segmentasi pelanggan churn** menggunakan algoritma K-Prototypes.

Dengan pendekatan ini, perusahaan dapat merancang strategi retensi yang lebih efektif dan efisien.

---

## 🎯 Business Problem

Dalam industri telekomunikasi yang sangat kompetitif, *customer churn* (pelanggan berhenti berlangganan) adalah tantangan utama yang menggerus profitabilitas. Riset dari Bain & Company menunjukkan bahwa biaya akuisisi pelanggan baru bisa 5 hingga 25 kali lebih mahal daripada biaya mempertahankan pelanggan yang sudah ada. Proyek ini bertujuan membangun sistem peringatan dini yang proaktif untuk mengidentifikasi pelanggan berisiko tinggi sebelum mereka pergi, memungkinkan intervensi yang strategis dan dipersonalisasi.

---

## Objectives
* Membangun model klasifikasi supervised untuk memprediksi probabilitas setiap pelanggan akan berhenti berlangganan, dengan fokus pada metrik Recall dan F1-Score.

* Membangun model clustering unsupervised untuk mengelompokkan pelanggan churn ke dalam segmen-segmen yang bermakna berdasarkan pola perilaku dan nilai mereka.

---

## 🗂️ Dataset

Dataset yang digunakan adalah "Iranian Churn Dataset" dari UCI Machine Learning Repository.
- **Sumber**: [https://archive.ics.uci.edu/dataset/563/iranian+churn+dataset](https://archive.ics.uci.edu/dataset/563/iranian+churn+dataset)
- **Jumlah data**: 3.150 pelanggan
- **Fitur**: Campuran numerik dan kategorikal seperti:
  - Subscription Length
  - Number of Complaints
  - Age
  - Call Failures
  - Customer Value
  - dsb.
- **Target**: `Churn` (1 = churn, 0 = tidak)

---

## ⚙️ Teknologi & Library

* **Analisis & Pemodelan**: `Python`, `Pandas`, `NumPy`, `Scikit-learn`, `imblearn`, `kmodes`, `feature-engine`
* **Visualisasi**: `Matplotlib`, `Seaborn`
* **Deployment**: `Streamlit`
* **Serialisasi Model**: `Pickle`, `Joblib`

---

## 🔍 Methodology

Proyek ini dibagi menjadi dua alur pemodelan utama yang berjalan secara paralel setelah tahap eksplorasi data.

1.  **ETL Pipeline**: Fetch dataset dari PostgresQL
2. **Data Loading & Cleaning**: Memuat dataset, menangani nilai duplikat, dan memastikan tipe data sudah benar.
3.  **Exploratory Data Analysis (EDA)**: Menganalisis data untuk memahami distribusi, korelasi, dan mendapatkan insight awal mengenai karakteristik pelanggan yang churn.
4.  **Feature Engineering**: Melakukan pra-pemrosesan data seperti:
    * **Penanganan Outlier**: Menggunakan `Winsorizer` untuk membatasi nilai-nilai ekstrim.
    * **Seleksi Fitur**: Menggunakan VIF (Variance Inflation Factor) untuk mendeteksi dan mengurangi multikolinearitas.
5.  **Pemodelan Churn (Supervised)**:
    * Membagi data menjadi set latih dan uji untuk validasi yang akurat.
    * Menggunakan `imblearn.pipeline` untuk menggabungkan pra-pemrosesan (`StandardScaler`, `Encoder`) dengan penanganan data tidak seimbang menggunakan `SMOTENC`.
    * Melakukan *hyperparameter tuning* pada model `RandomForestClassifier` dengan `RandomizedSearchCV` untuk memaksimalkan `recall`.
6.  **Pemodelan Clustering (Unsupervised)**:
    * Menggunakan keseluruhan data fitur untuk menemukan segmen yang representatif.
    * Menerapkan pra-pemrosesan (capping dan scaling) secara berurutan.
    * Melatih model `K-Prototypes` yang dirancang khusus untuk data campuran (numerik & kategorikal).
    * Menentukan jumlah klaster optimal menggunakan *Elbow Method*.
7.  **Penyimpanan & Deployment**:
    * Menyimpan semua komponen yang telah dilatih (model, scaler, capper, daftar kolom) ke dalam satu file "bundle" menggunakan `pickle`.
    * Membangun aplikasi web interaktif dengan **Streamlit** yang memuat bundle tersebut untuk melakukan inferensi pada data baru.

---

## Results & Insights
| Model | Recall | F1-Score |
|-------|--------|----------|
| Random Forest | Tinggi | Baik (Detail dapat dilihat di notebook) |

- Beberapa cluster pelanggan churn teridentifikasi, masing-masing dengan karakteristik unik.
- Visualisasi PCA menunjukkan pemisahan segmen yang cukup jelas.
- Pelanggan churn terdiri dari beberapa kelompok berbeda: berdasarkan usia, penggunaan layanan, keluhan, dsb.
- Segmentasi membantu membangun strategi retensi yang lebih spesifik dan tepat sasaran.
- Model klasifikasi memungkinkan fokus kampanye retensi pada pelanggan yang benar-benar berisiko tinggi.

---

## Recommendations
- Gunakan model prediksi churn untuk menyusun daftar pelanggan prioritas retensi.
- Terapkan strategi berbeda untuk tiap segmen churn (misal: bonus, perbaikan layanan, komunikasi personal).
- Lanjutkan iterasi model dan monitoring performa seiring waktu.

---

## 👥 Team Members
- [Azhar Muhammad](https://github.com/azharmuhammad-3124)
- [Nathanael August Zefanya](https://github.com/nathanaelzefanya)
- [Pradita Ajeng Wiguna](https://github.com/praditaw)

---
