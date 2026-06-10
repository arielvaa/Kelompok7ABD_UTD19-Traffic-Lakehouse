# Evaluasi dan Benchmark

## Lingkungan Pengujian

Seluruh pengujian dilakukan menggunakan lingkungan sebagai berikut:

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

Proses transformasi Silver Layer dilakukan dengan menggabungkan dataset lalu lintas (`utd19_u.csv`) dengan metadata detector (`detectors_public.csv`) menggunakan atribut `detid`.

Relasi dataset:

```text
utd19_u.csv
     |
   detid
     |
detectors_public.csv
```

Dataset `links.csv` tidak digunakan pada proses join utama karena satu `linkid` dapat memiliki banyak waypoint sehingga berpotensi menyebabkan data explosion dan menghasilkan miliaran record.

---

# Tantangan Infrastruktur

Pada proses implementasi ditemukan bahwa kapasitas storage awal Azure VM tidak mencukupi untuk menjalankan transformasi Delta Lake.

Kondisi awal:

```text
Storage ≈ 30 GB
```

Proses write Delta Lake membutuhkan ruang tambahan untuk:

* Temporary files
* Shuffle process
* Transaction log (_delta_log)

Sehingga kapasitas storage ditingkatkan menjadi:

```text
Storage = 64 GB
```

Setelah peningkatan kapasitas disk, seluruh proses transformasi berhasil diselesaikan.

---

# Optimasi Partisi

Pengujian menunjukkan bahwa penggunaan jumlah partisi yang besar menyebabkan:

* Small files problem
* Overhead write meningkat
* Konsumsi disk lebih besar
* Shuffle Spark menjadi lebih berat

Untuk menjaga kestabilan pipeline pada VM 2 vCPU dan RAM 8 GB digunakan:

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

Walaupun Delta Lake menyimpan transaction log dan metadata tambahan, ukuran akhir dataset pada eksperimen ini lebih kecil dibandingkan Apache Parquet.

---

# Benchmark Performa

Untuk meningkatkan reliabilitas hasil, setiap benchmark dijalankan sebanyak **3 iterasi**, kemudian digunakan nilai rata-rata sebagai hasil evaluasi.

## Hasil Benchmark Tiap Iterasi

| Metrik                       | Iterasi 1 | Iterasi 2 | Iterasi 3 |
| ---------------------------- | --------- | --------- | --------- |
| Read Time Parquet (s)        | 4.84      | 5.44      | 4.06      |
| Read Time Delta (s)          | 12.59     | 11.94     | 12.34     |
| Filter Time Parquet (s)      | 4.27      | 5.54      | 4.29      |
| Filter Time Delta (s)        | 19.87     | 17.73     | 18.19     |
| Aggregation Time Parquet (s) | 14.22     | 14.62     | 13.18     |
| Aggregation Time Delta (s)   | 24.72     | 24.24     | 24.91     |
| Write Time Parquet (s)       | 890.08    | 908.11    | 896.09    |
| Write Time Delta (s)         | 1029.65   | 1026.57   | 1003.32   |

---

# Hasil Rata-Rata Benchmark

| Metrik               | Parquet | Delta Lake | Unggul  |
| -------------------- | ------- | ---------- | ------- |
| Write Time (s)       | 898.09  | 1019.85    | Parquet |
| Read Time (s)        | 4.78    | 12.29      | Parquet |
| Filter Time (s)      | 4.70    | 18.60      | Parquet |
| Aggregation Time (s) | 14.01   | 24.62      | Parquet |

---

## Analisis Write Performance

Parquet:

```text
898.09 detik
```

Delta Lake:

```text
1019.85 detik
```

Selisih:

```text
121.76 detik
```

Delta Lake memerlukan waktu sekitar:

```text
13.56% lebih lama
```

karena harus membangun transaction log dan metadata tambahan.

---

## Analisis Read Performance

Parquet:

```text
4.78 detik
```

Delta Lake:

```text
12.29 detik
```

Selisih:

```text
7.51 detik
```

Delta Lake membutuhkan waktu sekitar:

```text
157.11% lebih lama
```

dibandingkan Parquet.

---

## Analisis Filter Performance

Parquet:

```text
4.70 detik
```

Delta Lake:

```text
18.60 detik
```

Selisih:

```text
13.90 detik
```

Delta Lake membutuhkan waktu sekitar:

```text
295.74% lebih lama
```

dibandingkan Parquet.

---

## Analisis Aggregation Performance

Parquet:

```text
14.01 detik
```

Delta Lake:

```text
24.62 detik
```

Selisih:

```text
10.61 detik
```

Delta Lake membutuhkan waktu sekitar:

```text
75.73% lebih lama
```

dibandingkan Parquet.

---

# Ringkasan Benchmark

| Metrik           | Parquet  | Delta Lake | Unggul     |
| ---------------- | -------- | ---------- | ---------- |
| Write Time       | 898.09 s | 1019.85 s  | Parquet    |
| Read Time        | 4.78 s   | 12.29 s    | Parquet    |
| Filter Time      | 4.70 s   | 18.60 s    | Parquet    |
| Aggregation Time | 14.01 s  | 24.62 s    | Parquet    |
| Storage          | 2.8 GB   | 2.5 GB     | Delta Lake |

Secara performa komputasi, Apache Parquet unggul pada seluruh operasi analitik yang diuji.

Delta Lake unggul pada efisiensi penyimpanan dan fitur manajemen data modern.

---

# Evaluasi Fitur Delta Lake

## Transaction Log

Delta Lake secara otomatis membuat folder:

```text
_delta_log/
```

yang menyimpan seluruh histori perubahan tabel.

| Version | Operation                 |
| ------- | ------------------------- |
| 0       | Initial Write             |
| 1       | Overwrite + Schema Update |

---

## Versioning

| Version | Kondisi               |
| ------- | --------------------- |
| 0       | Schema awal           |
| 1       | Schema setelah update |

Versioning memungkinkan pelacakan perubahan data secara historis.

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

Kolom baru berhasil ditambahkan tanpa membangun ulang tabel.

---

## Time Travel

Contoh penggunaan:

```python
.option("versionAsOf", 0)
```

Fitur ini memungkinkan:

* Audit historis
* Reproduksi eksperimen
* Rollback data
* Pelacakan perubahan

Kemampuan tersebut tidak tersedia pada Parquet standar.

---

# Kelebihan dan Kekurangan

## Apache Parquet

### Kelebihan

* Write lebih cepat
* Read lebih cepat
* Filter lebih cepat
* Aggregation lebih cepat
* Overhead metadata rendah
* Cocok untuk analisis dan dashboard

### Kekurangan

* Tidak memiliki transaction log
* Tidak memiliki versioning
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
* Membutuhkan resource tambahan untuk metadata dan transaction log

---

# Kesimpulan

Ini kesimpulannya, tinggal copy-paste ganti yang lama:

---

# Kesimpulan

Pada lingkungan Azure Virtual Machine dengan spesifikasi 2 vCPU dan RAM 8 GB, Apache Parquet terbukti memberikan performa yang lebih baik untuk workload analitik dan kebutuhan dashboard secara keseluruhan.

Di sisi lain, Delta Lake menawarkan kemampuan pengelolaan data yang jauh lebih lengkap melalui fitur transaction log, versioning, schema evolution, dan time travel — fitur-fitur yang menjadi kebutuhan mendasar dalam implementasi Lakehouse di lingkungan produksi.

Hasil penelitian ini menunjukkan bahwa pemilihan format penyimpanan tidak semata-mata ditentukan oleh kecepatan pemrosesan, melainkan juga harus mempertimbangkan kebutuhan pengelolaan, auditabilitas, dan governance data dalam jangka panjang.
