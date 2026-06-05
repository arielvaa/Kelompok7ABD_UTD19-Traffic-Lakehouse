# Scripts Documentation

Folder `scripts/` berisi seluruh proses ETL, validasi data, benchmarking, dan demonstrasi fitur Delta Lake yang digunakan dalam implementasi Lakehouse Architecture pada dataset UTD19.

---

# Benchmark

Folder: `scripts/benchmark/`

Digunakan untuk membandingkan performa Apache Parquet dan Delta Lake pada operasi analitik umum.

## benchmark_read_parquet.py

Mengukur waktu pembacaan dataset Silver Layer dalam format Parquet.

Output:

* Jumlah record dataset
* Waktu eksekusi pembacaan data (detik)

---

## benchmark_read_delta.py

Mengukur waktu pembacaan dataset Silver Layer dalam format Delta Lake.

Output:

* Jumlah record dataset
* Waktu eksekusi pembacaan data (detik)

---

## benchmark_filter_parquet.py

Mengukur performa operasi filtering pada dataset Parquet.

Contoh operasi:

* Filter berdasarkan kota tertentu
* Filter berdasarkan nilai flow

Output:

* Jumlah record hasil filter
* Waktu eksekusi filtering

---

## benchmark_filter_delta.py

Mengukur performa operasi filtering pada dataset Delta Lake.

Output:

* Jumlah record hasil filter
* Waktu eksekusi filtering

---

## benchmark_agg_parquet.py

Mengukur performa agregasi pada dataset Parquet.

Contoh operasi:

* AVG(flow)
* AVG(speed)
* GROUP BY city

Output:

* Hasil agregasi
* Waktu eksekusi agregasi

---

## benchmark_agg_delta.py

Mengukur performa agregasi pada dataset Delta Lake.

Output:

* Hasil agregasi
* Waktu eksekusi agregasi

---

# Bronze Layer

Folder: `scripts/bronze/`

Digunakan untuk eksplorasi dan evaluasi kualitas data mentah (raw data).

## data_quality.py

Memeriksa kualitas dataset sumber sebelum transformasi.

Output:

* Jumlah baris dataset
* Missing value per kolom
* Persentase missing value
* Tipe data setiap kolom

Contoh:

```text
Jumlah baris: 134380371

Missing value:
occ      : 3279527
error    : 59193481
speed    : 129750416
```

---

## bronze_profile.py

Melakukan profiling dataset secara deskriptif.

Output:

* Statistik numerik
* Informasi kolom
* Distribusi data
* Ringkasan dataset

File hasil:

* bronze_report.txt

---

## bronze_relationship.py

Menganalisis hubungan antar dataset.

Fokus:

* Relasi UTD19_u.csv dengan detectors_public.csv
* Validasi key detid
* Kecocokan hasil join

Output:

* Jumlah detector yang cocok
* Jumlah detector yang tidak cocok
* Statistik hasil join

---

# Delta Features

Folder: `scripts/delta_features/`

Berisi demonstrasi fitur-fitur khusus Delta Lake.

## cek_duplicate_detid.py

Memeriksa apakah terdapat duplikasi detid setelah proses transformasi.

Output:

* Total duplicate detid
* Status validasi

---

## cek_infinity.py

Memeriksa keberadaan nilai Infinity atau NaN ekstrem.

Output:

* Jumlah nilai Infinity
* Jumlah nilai tidak valid

---

## check_delta_schema.py

Membandingkan schema antar versi Delta Lake.

Output:

* Schema versi lama
* Schema versi terbaru
* Perubahan kolom

Contoh:

```text
VERSION 0
city
avg_flow
avg_speed
avg_occ
detector_count

LATEST VERSION
city
avg_flow
avg_speed
avg_occ
detector_count
congestion_index
```

---

## delta_history.py

Menampilkan histori transaksi Delta Lake.

Output:

* Version
* Timestamp
* Operation
* Operation metrics

Contoh:

```text
Version 1
Operation : WRITE
Rows      : 39
```

---

## delta_time_travel.py

Demonstrasi fitur Time Travel Delta Lake.

Output:

* Isi tabel versi lama
* Isi tabel versi terbaru
* Perbandingan perubahan data

---

## delta_update_demo.py

Demonstrasi Schema Evolution Delta Lake.

Aktivitas:

* Menambahkan kolom baru
* Menulis ulang tabel Delta

Output:

* Delta version bertambah
* Schema baru berhasil diterapkan

---

# Gold Layer

Folder: `scripts/gold/`

Membuat dataset analitik yang siap digunakan untuk dashboard dan visualisasi.

## gold_city_daily_parquet.py

Membuat agregasi harian per kota.

Output:

* city_daily.parquet

Kolom:

* city
* day
* avg_flow
* avg_speed
* avg_occ

---

## gold_city_summary_parquet.py

Membuat ringkasan lalu lintas setiap kota.

Output:

* city_summary.parquet

Kolom:

* city
* avg_flow
* avg_speed
* avg_occ
* detector_count

---

## gold_city_summary_delta.py

Menyimpan city summary dalam format Delta Lake.

Output:

* city_summary Delta Table

Digunakan untuk:

* Versioning
* Schema Evolution
* Time Travel

---

## gold_road_analysis_parquet.py

Membuat analisis berdasarkan klasifikasi jalan.

Output:

* road_analysis.parquet

Kolom:

* city
* fclass
* avg_flow
* avg_speed
* records

---

## export_gold_csv.py

Mengubah seluruh output Gold Layer menjadi CSV.

Output:

* city_summary.csv
* city_daily.csv
* road_analysis.csv

Digunakan untuk:

* GitHub repository
* Power BI
* Visualisasi

---

# Silver Layer

Folder: `scripts/silver/`

Melakukan transformasi dan integrasi data.

## silver_parquet.py

Membangun Silver Layer dalam format Parquet.

Proses:

1. Membaca UTD19_u.csv
2. Membaca detectors_public.csv
3. Join berdasarkan detid
4. Menyimpan hasil ke Parquet

Output:

* traffic_enriched (Parquet)

---

## silver_delta.py

Membangun Silver Layer dalam format Delta Lake.

Proses:

1. Join dataset
2. Menyimpan hasil ke Delta Lake
3. Membuat transaction log Delta

Output:

* traffic_enriched (Delta)

Catatan:

* Membutuhkan peningkatan storage VM dari sekitar 30 GB menjadi 64 GB agar proses selesai.
* Dataset hasil transformasi memiliki ukuran puluhan gigabyte.

---

## silver_links_parquet.py

Mengubah links.csv menjadi format Parquet.

Output:

* links.parquet

Catatan:

* Tidak digunakan dalam join utama karena berpotensi menyebabkan ledakan jumlah record (data explosion).

---

## silver_links_delta.py

Mengubah links.csv menjadi format Delta Lake.

Output:

* links Delta Table

---

# Validation

Folder: `scripts/validation/`

Digunakan untuk memastikan kualitas dan konsistensi data hasil transformasi.

## validasi_city.py

Memastikan seluruh kota tetap tersedia setelah proses join.

Output:

* Jumlah kota unik
* Daftar kota

---

## validasi_delta_count.py

Memvalidasi jumlah record Silver Delta.

Output:

* Total record
* Status validasi

---

## validasi_parquet_count.py

Memvalidasi jumlah record Silver Parquet.

Output:

* Total record
* Status validasi

---

## validasi_schema.py

Memvalidasi schema Silver Layer.

Output:

* Daftar kolom
* Tipe data

---

## validasi_missing.py

Memvalidasi missing value setelah transformasi.

Output:

* Missing value per kolom

---

## validasi_gold_count.py

Memvalidasi jumlah record seluruh dataset Gold.

Output:

* Total record city_summary
* Total record city_daily
* Total record road_analysis

---

## validasi_gold_schema.py

Memvalidasi schema seluruh dataset Gold.

Output:

* Struktur kolom
* Tipe data

---

## validasi_gold_sample.py

Menampilkan sampel data Gold Layer.

Output:

* 5 sampai 10 record pertama

---

## validasi_gold_missing.py

Memeriksa missing value pada Gold Layer.

Output:

* Missing value per kolom

---

## validasi_gold_duplicate.py

Memastikan tidak terdapat data duplikat.

Output:

* Jumlah duplicate row

---

## validasi_gold_logic.py

Memvalidasi logika bisnis hasil agregasi.

Pemeriksaan:

* Nilai flow tidak negatif
* Nilai speed tidak negatif
* Detector count valid

Output:

* PASS / FAIL

---

## validasi_gold_city.py

Memastikan seluruh kota tetap muncul pada output Gold Layer.

Output:

* Jumlah kota unik
* Status validasi

```

---

Dokumentasi ini menjelaskan seluruh script ETL, benchmarking, validasi, serta fitur Delta Lake yang digunakan dalam implementasi Lakehouse Architecture pada dataset UTD19.
```
