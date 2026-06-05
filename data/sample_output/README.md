## Output Gold Layer

Gold Layer berisi dataset analitik yang telah melalui proses pembersihan, transformasi, dan agregasi pada Silver Layer. Dataset pada layer ini dirancang untuk kebutuhan analisis bisnis, visualisasi dashboard, dan benchmarking.

### 1. City Summary

File:

```text
city_summary.csv
```

Berisi ringkasan statistik lalu lintas pada tingkat kota.

#### Struktur Data

| Kolom          | Deskripsi                              |
| -------------- | -------------------------------------- |
| city           | Nama kota                              |
| avg_flow       | Rata-rata flow kendaraan               |
| avg_speed      | Rata-rata kecepatan kendaraan (km/jam) |
| avg_occ        | Rata-rata occupancy detector           |
| detector_count | Jumlah detector aktif                  |

#### Statistik Dataset

| Metrik              | Nilai   |
| ------------------- | ------- |
| Jumlah Baris        | 39      |
| Jumlah Kolom        | 5       |
| Ukuran File         | 1.54 KB |
| Total Missing Value | 37      |
| Persentase Missing  | 18.97%  |

#### Missing Value

| Kolom     | Missing |
| --------- | ------- |
| avg_speed | 30      |
| avg_occ   | 7       |

#### Penjelasan Missing Value

Missing value pada kolom `avg_speed` dan `avg_occ` berasal dari karakteristik asli dataset UTD19. Tidak semua detector menyediakan informasi kecepatan dan occupancy sehingga nilai tersebut memang tidak tersedia pada sumber data.

---

### 2. City Daily

File:

```text
city_daily.csv
```

Berisi agregasi harian lalu lintas pada setiap kota.

#### Struktur Data

| Kolom     | Deskripsi                  |
| --------- | -------------------------- |
| city      | Nama kota                  |
| day       | Tanggal pengamatan         |
| avg_flow  | Rata-rata flow harian      |
| avg_speed | Rata-rata kecepatan harian |
| avg_occ   | Rata-rata occupancy harian |

#### Statistik Dataset

| Metrik              | Nilai  |
| ------------------- | ------ |
| Jumlah Baris        | 1.378  |
| Jumlah Kolom        | 5      |
| Ukuran File         | 59 KB  |
| Total Missing Value | 1.321  |
| Persentase Missing  | 19.17% |

#### Missing Value

| Kolom     | Missing |
| --------- | ------- |
| avg_speed | 1.231   |
| avg_occ   | 90      |

#### Penjelasan Missing Value

Nilai `avg_speed` dan `avg_occ` tidak tersedia pada seluruh detector karena setiap kota menggunakan jenis sensor yang berbeda. Missing value dipertahankan untuk menjaga representasi kondisi asli data lalu lintas.

---

### 3. Road Analysis

File:

```text
road_analysis.csv
```

Berisi agregasi lalu lintas berdasarkan klasifikasi jalan (OpenStreetMap Functional Road Class).

#### Struktur Data

| Kolom     | Deskripsi                                   |
| --------- | ------------------------------------------- |
| city      | Nama kota                                   |
| fclass    | Kategori jalan                              |
| avg_flow  | Rata-rata flow kendaraan                    |
| avg_speed | Rata-rata kecepatan kendaraan               |
| records   | Jumlah record yang digunakan dalam agregasi |

#### Statistik Dataset

| Metrik              | Nilai   |
| ------------------- | ------- |
| Jumlah Baris        | 315     |
| Jumlah Kolom        | 5       |
| Ukuran File         | 14.4 KB |
| Total Missing Value | 261     |
| Persentase Missing  | 16.57%  |

#### Missing Value

| Kolom     | Missing |
| --------- | ------- |
| avg_speed | 261     |

#### Penjelasan Missing Value

Missing value pada `avg_speed` muncul karena sebagian kelompok jalan tidak memiliki detector yang melaporkan kecepatan kendaraan. Nilai flow tetap tersedia sehingga agregasi masih valid untuk analisis.

---

## Efisiensi Reduksi Data

Salah satu tujuan Medallion Architecture adalah mengubah data mentah berukuran besar menjadi dataset analitik yang ringkas dan siap digunakan.

| Layer  | Dataset           | Ukuran  |
| ------ | ----------------- | ------- |
| Bronze | utd19_u.csv       | 6.49 GB |
| Gold   | city_summary.csv  | 1.54 KB |
| Gold   | city_daily.csv    | 59 KB   |
| Gold   | road_analysis.csv | 14.4 KB |

Melalui proses transformasi dan agregasi, dataset mentah yang berisi lebih dari 134 juta record berhasil direduksi menjadi dataset analitik yang ringan, sehingga dapat digunakan secara efisien pada dashboard Power BI dan kebutuhan Business Intelligence lainnya.
