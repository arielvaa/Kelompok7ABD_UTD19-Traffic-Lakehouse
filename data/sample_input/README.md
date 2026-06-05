## Dataset

Proyek ini menggunakan **UTD19 (Urban Traffic Data 2019)** yang dikembangkan oleh Loder et al. dari ETH Zurich. Dataset ini berisi data lalu lintas perkotaan dari **40 kota di berbagai negara** yang dikumpulkan melalui berbagai jenis sensor lalu lintas seperti inductive loop detectors, camera detectors, ultrasonic detectors, dan sensor sejenis.

Dataset digunakan untuk membangun arsitektur **Lakehouse berbasis Medallion Architecture (Bronze-Silver-Gold)** serta melakukan perbandingan performa antara **Apache Parquet** dan **Delta Lake**.

### File Dataset

| File                 | Ukuran  | Deskripsi                             |
| -------------------- | ------- | ------------------------------------- |
| utd19_u.csv          | 6.49 GB | Data pengukuran lalu lintas utama     |
| links.csv            | 7.18 MB | Informasi geometri dan jaringan jalan |
| detectors_public.csv | 2.46 MB | Informasi lokasi dan atribut detector |

### 1. UTD19 Traffic Measurements

File utama:

```text
utd19_u.csv
```

Berisi data pengukuran lalu lintas yang direkam oleh detector pada interval waktu tertentu.

**Jumlah record:**

```text
134.380.371 baris
```

**Variabel:**

| Kolom    | Deskripsi                                    |
| -------- | -------------------------------------------- |
| city     | Nama kota                                    |
| detid    | ID detector                                  |
| day      | Tanggal pengamatan                           |
| interval | Interval waktu dalam detik dari tengah malam |
| flow     | Arus kendaraan (veh/hour/lane)               |
| occ      | Occupancy detector                           |
| speed    | Kecepatan rata-rata (km/jam)                 |
| error    | Indikator error dari sensor                  |

### Profiling Dataset Traffic

Jumlah missing value pada dataset utama:

| Kolom    | Missing Value |
| -------- | ------------- |
| day      | 0             |
| interval | 0             |
| detid    | 0             |
| flow     | 0             |
| occ      | 3.279.527     |
| error    | 59.193.481    |
| city     | 0             |
| speed    | 129.750.416   |

Temuan penting:

* Variabel **speed** memiliki jumlah missing value yang sangat besar karena tidak semua detector menyediakan informasi kecepatan.
* Variabel **occ (occupancy)** tidak tersedia pada seluruh detector.
* Variabel **error** hanya terisi ketika sistem mendeteksi kesalahan sensor.
* Kondisi ini sesuai dengan dokumentasi resmi UTD19 yang menyebutkan bahwa setiap kota menggunakan jenis sensor yang berbeda sehingga tidak semua variabel tersedia pada setiap lokasi dan interval waktu.

---

### 2. Detector Information

File:

```text
detectors_public.csv
```

Berisi informasi lokasi detector beserta atribut jalan yang diperoleh dari OpenStreetMap.

**Jumlah record:**

```text
23.577 detector
```

**Variabel utama:**

| Kolom    | Deskripsi                        |
| -------- | -------------------------------- |
| detid    | ID detector                      |
| citycode | Nama kota                        |
| length   | Panjang lajur yang diamati       |
| pos      | Jarak ke persimpangan berikutnya |
| long     | Longitude                        |
| lat      | Latitude                         |
| lanes    | Jumlah lajur                     |
| linkid   | ID link jalan                    |
| fclass   | Kelas jalan                      |
| road     | Nama jalan                       |
| limit    | Batas kecepatan                  |

---

### 3. Link Information

File:

```text
links.csv
```

Berisi representasi geometri setiap ruas jalan yang dipantau detector.

**Jumlah record:**

```text
140.858 record
```

**Variabel utama:**

| Kolom    | Deskripsi           |
| -------- | ------------------- |
| citycode | Nama kota           |
| linkid   | ID link jalan       |
| order    | Urutan waypoint     |
| piece    | Nomor segmen        |
| group    | Nomor grup geometri |
| long     | Longitude           |
| lat      | Latitude            |

---

### Relasi Antar Dataset

Hubungan antar dataset menggunakan kunci utama berikut:

```text
UTD19 Traffic
      |
    detid
      |
Detector Information
      |
    linkid
      |
Link Information
```

* `detid` digunakan untuk menghubungkan data lalu lintas dengan informasi detector.
* `linkid` digunakan untuk menghubungkan detector dengan informasi jaringan jalan.

Relasi ini digunakan pada proses enrichment di Silver Layer untuk menghasilkan dataset analitik pada Gold Layer.

### Referensi

Loder, A., Ambühl, L., Menendez, M., & Axhausen, K. W. (2020). *UTD19: Urban Traffic Data from 40 Cities*. Institute for Transport Planning and Systems (IVT), ETH Zurich.
