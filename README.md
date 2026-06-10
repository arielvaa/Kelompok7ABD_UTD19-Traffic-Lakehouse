# Evaluasi Performa Format Parquet dan Delta Lake dalam Medallion Lakehouse: Studi Kasus Data Lalu Lintas Perkotaan (UTD19)

## Kelompok 7

### Mata Kuliah Analisis Big Data

Implementasi arsitektur Lakehouse menggunakan pendekatan Medallion Architecture untuk mengelola dataset lalu lintas perkotaan UTD19 serta melakukan evaluasi performa antara format Apache Parquet dan Delta Lake.

---

# Tema Proyek

**SDG 11 – Kota dan Komunitas Berkelanjutan**

Proyek ini berfokus pada pengolahan data lalu lintas perkotaan dari berbagai kota di dunia untuk menghasilkan informasi yang bisa digunakan dalam analisis mobilitas, kemacetan, dan perencanaan transportasi berkelanjutan.

---

# Anggota Kelompok

| No | Nama | NIM | GitHub |
|----|------|------|---------|
| 1 | Arielva Simon Siahaan | 123450105 | @arielvaa |
| 2 | Tobias David Manogari | 122450091 | @Tobias030 |
| 3 | Rahma Oktavia Albar | 123450003 | @rahmaoktaviaalbar003 |
| 4 | Khazanatil Ilmi | 123450053 | @khazanatililmi |
| 5 | Citra Agustin | 123450108 | @citraagustin10 |

---

# Deskripsi Proyek

Proyek ini membangun sebuah pipeline Lakehouse berbasis Apache Spark menggunakan pendekatan Medallion Architecture yang terdiri dari Bronze Layer, Silver Layer, dan Gold Layer.

Dataset utama berasal dari **UTD19 (Urban Traffic Data 2019)** yang berisi data lalu lintas dari 40 kota di dunia.

Selain membangun pipeline data, proyek ini juga melakukan evaluasi performa antara:

- Apache Parquet
- Delta Lake

Perbandingan dilakukan pada beberapa operasi analitik utama seperti:

- Read
- Filter
- Aggregation

Selain itu, proyek ini juga mengevaluasi fitur tambahan yang hanya dimiliki Delta Lake seperti:

- Transaction Log
- Versioning
- Time Travel
- Schema Evolution
- Data History

---

# Dataset

## Dataset Utama

### UTD19_u.csv

Dataset pengukuran lalu lintas perkotaan.

Informasi:

- Ukuran file: ± 6.49 GB
- Jumlah record: 134.380.371 baris
- Berisi data:
  - Flow
  - Occupancy
  - Speed
  - Error Indicator
  - Detector ID
  - Waktu pengamatan
  - Kota

---

### detectors_public.csv

Dataset metadata detector lalu lintas.

Informasi:

- Ukuran file: ± 2.46 MB
- Jumlah detector: 23.577
- Berisi:
  - Lokasi detector
  - Jumlah lajur
  - Functional road class
  - Link ID
  - Nama jalan
  - Batas kecepatan

---

### links.csv

Dataset geometri jaringan jalan.

Informasi:

- Ukuran file: ± 7.18 MB
- Jumlah record: 140.858
- Berisi koordinat setiap segmen jalan

Catatan:

Dataset ini tidak diikutsertakan dalam proses join utama karena berpotensi menyebabkan ledakan jumlah data (data explosion) akibat relasi one-to-many antara link dan detektor. Dataset tetap ditransformasikan ke format Parquet dan Delta Lake sebagai bagian dari implementasi Lakehouse secara lengkap.

---

# Arsitektur Medallion Lakehouse

## Bronze Layer

Tahap penyimpanan data mentah hasil ingest.

Data yang masuk:

- UTD19_u.csv
- detectors_public.csv
- links.csv

Aktivitas:

- Data profiling
- Data quality assessment
- Analisis hubungan antar dataset

Output:

- Bronze Report
- Statistik kualitas data
- Analisis relasi antar tabel

---

## Silver Layer

Tahap transformasi dan integrasi data.

### Transformasi Utama

Join dilakukan antara:

```
UTD19_u.csv
      +
detectors_public.csv
      ↓
traffic_enriched
```

Key yang digunakan:

```
detid
```

Output:

- traffic_enriched (Parquet)
- traffic_enriched (Delta)

Data hasil join berisi:

- city
- day
- interval
- flow
- occ
- speed
- error
- detid
- lanes
- fclass
- road
- limit
- latitude
- longitude

---

### Transformasi Dataset Links

Dataset links.csv tidak di-join ke traffic_enriched.

Alasan:

- Berpotensi menghasilkan miliaran baris data.
- Menyebabkan data explosion.
- Tidak diperlukan untuk kebutuhan analisis agregasi proyek.

Namun dataset tetap dikonversi menjadi:

- links.parquet
- links.delta

untuk menunjukkan implementasi Lakehouse secara lengkap.

---

## Gold Layer

Tahap penyajian data untuk analisis dan dashboard.

Menghasilkan tiga dataset analitik:

### City Summary

Ringkasan statistik setiap kota.

Kolom:

- city
- avg_flow
- avg_speed
- avg_occ
- detector_count

---

### City Daily

Ringkasan harian per kota.

Kolom:

- city
- day
- avg_flow
- avg_speed
- avg_occ

---

### Road Analysis

Analisis berdasarkan klasifikasi jalan.

Kolom:

- city
- fclass
- avg_flow
- avg_speed
- records

---

# Pipeline Proyek

```text
                    RAW DATA
─────────────────────────────────────────

UTD19_u.csv (6.49 GB)
detectors_public.csv (2.46 MB)
links.csv (7.18 MB)

             │
             ▼

─────────────────────────────────────────
BRONZE LAYER
─────────────────────────────────────────

data_quality.py

bronze_profile.py

bronze_relationship.py

             │
             ▼

─────────────────────────────────────────
SILVER LAYER
─────────────────────────────────────────

UTD19_u.csv
       +
detectors_public.csv
       │
       ▼

traffic_enriched

       ├── Parquet
       └── Delta Lake

links.csv
       │
       ▼

links.parquet
links.delta

             │
             ▼

─────────────────────────────────────────
GOLD LAYER
─────────────────────────────────────────

traffic_enriched

       ├── city_summary
       ├── city_daily
       └── road_analysis

             │
             ▼

CSV Export

city_summary.csv
city_daily.csv
road_analysis.csv

             │
             ▼

Power BI Dashboard
```

---

# Benchmark yang Dilakukan

Perbandingan performa dilakukan pada:

## Read Benchmark

Membandingkan waktu pembacaan:

- Parquet
- Delta Lake

---

## Filter Benchmark

Membandingkan waktu filtering data:

- Parquet
- Delta Lake

---

## Aggregation Benchmark

Membandingkan waktu agregasi data:

- Parquet
- Delta Lake

---

# Fitur Delta Lake yang Dievaluasi

## Transaction Log

Delta Lake menyimpan histori transaksi dalam folder:

```
_delta_log/
```

---

## Versioning

Setiap perubahan data menghasilkan versi baru secara otomatis.

Contoh:

| Version | Operasi |
|----------|----------|
| 0 | Initial Write |
| 1 | Schema Update |

---

## Time Travel

Memungkinkan pembacaan data pada versi tertentu.

Contoh:

```python
.option("versionAsOf", 0)
```

---

## Schema Evolution

Memungkinkan penambahan kolom baru tanpa perlu membuat ulang tabel.

Contoh:

```text
Sebelum:
city
avg_flow
avg_speed
avg_occ
detector_count

Sesudah:
city
avg_flow
avg_speed
avg_occ
detector_count
congestion_index
```

---

# Tantangan Implementasi

## Ukuran Dataset Sangat Besar

Dataset awal:

- 6.49 GB

Jumlah record:

- >169 juta baris

sehingga setiap tahap pemrosesan memerlukan manajemen resource yang cermat.

---

## Kebutuhan Storage

Implementasi Delta Lake memerlukan kapasitas penyimpanan lebih besar dibanding Parquet karena menyimpan:

- Data file
- Transaction log
- Metadata versi

Kapasitas virtual machine perlu ditingkatkan dari sekitar 30 GB menjadi 64 GB agar proses transformasi Delta Lake dapat diselesaikan sepenuhnya.

---

## Optimasi Partisi

Jumlah partisi Spark dibuat sangat kecil untuk:

- Mengurangi fragmentasi file
- Menghindari terlalu banyak small files
- Menyesuaikan keterbatasan resource virtual machine

---

# Tools dan Teknologi

- Apache Spark
- Delta Lake
- Apache Parquet
- Python
- Pandas
- PyArrow
- Power BI
- Ubuntu Linux
- Azure Virtual Machine

---

# Struktur Repository

```text
UTD19-Traffic-Lakehouse
│
├── data
├── scripts
│   ├── bronze
│   ├── silver
│   ├── gold
│   ├── benchmark
│   ├── validation
│   └── delta_features
│
├── docs
│   ├── architecture
│   ├── benchmark
│   └── dashboard
│
├── report
│   └── bronze_report.txt
│
├── requirements.txt
└── README.md
```

---
