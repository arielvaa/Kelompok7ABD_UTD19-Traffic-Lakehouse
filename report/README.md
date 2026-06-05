# Evaluasi dan Benchmark

## Lingkungan Pengujian

Seluruh pengujian dilakukan menggunakan:

| Komponen                | Spesifikasi           |
| ----------------------- | --------------------- |
| Platform                | Azure Virtual Machine |
| CPU                     | 2 vCPU                |
| RAM                     | 8 GB                  |
| Storage Awal            | ±30 GB                |
| Storage Setelah Upgrade | 64 GB                 |
| Apache Spark            | 4.1.1                 |
| Delta Lake              | 4.2.0                 |

Dataset utama yang diproses:

| Dataset       | Ukuran      |
| ------------- | ----------- |
| utd19_u.csv   | 6.49 GB     |
| Jumlah Record | 134.380.371 |

---

# Hasil Transformasi Silver Layer

Proses transformasi Silver Layer dilakukan dengan menggabungkan data lalu lintas (`utd19_u.csv`) dengan metadata detector (`detectors_public.csv`) menggunakan atribut `detid`.

Relasi:

```text
utd19_u.csv
     |
   detid
     |
detectors_public.csv
```

Dataset `links.csv` tidak digunakan pada proses join utama karena satu `linkid` dapat memiliki banyak waypoint sehingga berpotensi menyebabkan data explosion dan menghasilkan miliaran record setelah join.

---

## Tantangan Infrastruktur

Selama pengujian ditemukan bahwa kapasitas storage awal Azure VM tidak cukup untuk menyelesaikan transformasi Silver Layer menggunakan Delta Lake.

Kondisi awal:

```text
Storage ≈ 30 GB
```

Proses write Delta Lake gagal diselesaikan karena kebutuhan ruang sementara (temporary files), shuffle, dan transaction log.

Storage kemudian ditingkatkan menjadi:

```text
Storage = 64 GB
```

Setelah peningkatan kapasitas disk, seluruh proses transformasi dapat berjalan hingga selesai.

---

## Optimasi Partisi

Pengujian menunjukkan bahwa penggunaan jumlah partisi besar menyebabkan:

* Banyak file kecil (small files problem)
* Overhead write yang tinggi
* Penggunaan disk yang meningkat
* Proses shuffle yang lebih berat

Untuk menjaga stabilitas pipeline pada VM 2 vCPU dan 8 GB RAM digunakan:

```python
repartition(2)
```

Pendekatan ini menghasilkan jumlah file output yang lebih sedikit dan penggunaan resource yang lebih stabil.

---

# Perbandingan Ukuran Penyimpanan

## Dataset Awal

| Dataset | Ukuran  |
| ------- | ------- |
| Raw CSV | 6.49 GB |

## Hasil Silver Layer

| Format     | Ukuran |
| ---------- | ------ |
| Parquet    | 2.8 GB |
| Delta Lake | 2.5 GB |

### Reduksi Ukuran Data

#### Parquet

```text
6.49 GB → 2.8 GB
```

Pengurangan ukuran:

```text
56.86%
```

#### Delta Lake

```text
6.49 GB → 2.5 GB
```

Pengurangan ukuran:

```text
61.48%
```

### Temuan

Walaupun Delta Lake menyimpan metadata tambahan melalui transaction log, ukuran akhir dataset justru lebih kecil dibanding Parquet pada eksperimen ini.

---

# Benchmark Performa

## Write Performance

Mengukur waktu penulisan hasil Silver Layer.

| Format     | Waktu      |
| ---------- | ---------- |
| Parquet    | 890 detik  |
| Delta Lake | 1029 detik |

Selisih:

```text
139 detik
```

Delta Lake membutuhkan waktu sekitar:

```text
15.62% lebih lama
```

karena harus membuat transaction log dan metadata tambahan.

---

## Read Performance

Mengukur waktu pembacaan dataset Silver.

| Format     | Waktu       |
| ---------- | ----------- |
| Parquet    | 4.84 detik  |
| Delta Lake | 12.59 detik |

Selisih:

```text
7.75 detik
```

Delta Lake membutuhkan waktu sekitar:

```text
160.12% lebih lama
```

dibanding Parquet pada pembacaan sederhana.

---

## Filter Performance

Pengujian operasi filter.

| Format     | Waktu       |
| ---------- | ----------- |
| Parquet    | 4.27 detik  |
| Delta Lake | 19.87 detik |

Selisih:

```text
15.60 detik
```

Delta Lake membutuhkan waktu sekitar:

```text
365.34% lebih lama
```

dibanding Parquet.

---

## Aggregation Performance

Pengujian operasi:

```python
groupBy()
agg()
```

| Format     | Waktu       |
| ---------- | ----------- |
| Parquet    | 14.22 detik |
| Delta Lake | 24.72 detik |

Selisih:

```text
10.50 detik
```

Delta Lake membutuhkan waktu sekitar:

```text
73.84% lebih lama
```

dibanding Parquet.

---

# Ringkasan Benchmark

| Metrik      | Parquet | Delta Lake | Unggul     |
| ----------- | ------- | ---------- | ---------- |
| Write       | 890 s   | 1029 s     | Parquet    |
| Read        | 4.84 s  | 12.59 s    | Parquet    |
| Filter      | 4.27 s  | 19.87 s    | Parquet    |
| Aggregation | 14.22 s | 24.72 s    | Parquet    |
| Storage     | 2.8 GB  | 2.5 GB     | Delta Lake |

Secara performa murni, Parquet unggul pada seluruh operasi analitik yang diuji.

Delta Lake hanya unggul pada efisiensi penyimpanan dan fitur manajemen data.

---

# Evaluasi Fitur Delta Lake

## Transaction Log

Delta Lake secara otomatis membuat folder:

```text
_delta_log/
```

yang menyimpan seluruh histori perubahan tabel.

History yang diperoleh:

| Version | Operation                 |
| ------- | ------------------------- |
| 0       | Initial Write             |
| 1       | Overwrite + Schema Update |

Setiap perubahan tabel tercatat secara permanen dan dapat diaudit kembali.

---

## Versioning

Delta Lake menyimpan beberapa versi tabel secara otomatis.

Hasil eksperimen:

| Version | Kondisi               |
| ------- | --------------------- |
| 0       | Schema awal           |
| 1       | Schema setelah update |

Dengan mekanisme ini pengguna dapat mengetahui kapan perubahan dilakukan dan versi apa yang digunakan dalam analisis tertentu.

---

## Schema Evolution

Schema awal:

```text
city
avg_flow
avg_speed
avg_occ
detector_count
```

Schema terbaru:

```text
city
avg_flow
avg_speed
avg_occ
detector_count
congestion_index
```

Kolom baru berhasil ditambahkan tanpa membuat ulang tabel.

Hal ini menunjukkan kemampuan Delta Lake untuk melakukan schema evolution secara langsung.

---

## Time Travel

Delta Lake memungkinkan pembacaan data berdasarkan versi tertentu.

Contoh:

```python
.option("versionAsOf", 0)
```

Kemampuan ini memungkinkan:

* Audit historis
* Reproduksi eksperimen
* Rollback data
* Pelacakan perubahan

Fitur ini tidak tersedia pada Parquet standar.

---

# Kelebihan dan Kekurangan

## Apache Parquet

### Kelebihan

* Performa baca lebih cepat
* Performa filter lebih cepat
* Performa agregasi lebih cepat
* Overhead metadata rendah
* Cocok untuk analisis dan dashboard

### Kekurangan

* Tidak memiliki versioning
* Tidak memiliki transaction log
* Tidak memiliki time travel
* Tidak mendukung schema evolution secara native

---

## Delta Lake

### Kelebihan

* Mendukung ACID Transaction
* Mendukung Versioning
* Mendukung Time Travel
* Mendukung Schema Evolution
* Mendukung Audit Trail
* Ukuran penyimpanan lebih kecil pada eksperimen ini

### Kekurangan

* Write lebih lambat
* Read lebih lambat
* Filter lebih lambat
* Aggregation lebih lambat
* Membutuhkan storage tambahan untuk metadata dan proses transaksi

---

# Kesimpulan

Pada lingkungan Azure VM dengan spesifikasi 2 vCPU dan 8 GB RAM, Apache Parquet memberikan performa terbaik untuk workload analitik dan dashboard.

Namun Delta Lake menawarkan kemampuan manajemen data yang jauh lebih lengkap melalui transaction log, versioning, schema evolution, dan time travel yang sangat penting pada implementasi Lakehouse skala produksi.

Hasil penelitian menunjukkan bahwa pemilihan format penyimpanan tidak hanya bergantung pada performa, tetapi juga pada kebutuhan pengelolaan dan governance data dalam jangka panjang.
