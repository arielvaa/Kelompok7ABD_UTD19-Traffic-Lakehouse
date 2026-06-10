# Data Directory

Folder ini berisi contoh output hasil pemrosesan serta dokumentasi dataset yang digunakan dalam proyek.

## Struktur Folder

```text
data/
├── sample_input/
│   ├── dataset.pdf
│   └── README.md
│
└── sample_output/
    ├── city_summary.csv
    ├── city_daily.csv
    ├── road_analysis.csv
    └── README.md
```

---

# Sample Input

Folder `sample_input` tidak menyertakan dataset mentah asli karena ukuran file yang sangat besar dan melebihi batas praktis penyimpanan GitHub.

File yang tersedia:

| File        | Deskripsi                                      |
| ----------- | ---------------------------------------------- |
| dataset.pdf | Dokumentasi resmi UTD19 dari ETH Zurich        |
| README.md   | Penjelasan dataset yang digunakan dalam proyek |

## Dataset yang Digunakan

Proyek ini menggunakan dataset **UTD19 (Urban Traffic Data from 40 Cities)**.

Dataset asli yang digunakan selama proses pembangunan Lakehouse:

| File                 | Ukuran  |
| -------------------- | ------- |
| utd19_u.csv          | 6.49 GB |
| detectors_public.csv | 2.46 MB |
| links.csv            | 7.18 MB |

### Dataset Utama

File utama yang diproses adalah:

```text
utd19_u.csv
```

Dataset ini berisi:

* 134.380.371 record lalu lintas
* Data dari 40 kota
* Informasi flow, speed, occupancy, detector, dan waktu pengamatan

### Detector Metadata

File:

```text
detectors_public.csv
```

Digunakan untuk:

* Menambahkan informasi lokasi detector
* Menambahkan atribut jalan
* Menambahkan jumlah lajur
* Menghubungkan detector dengan informasi jaringan jalan

Proses enrichment pada Silver Layer menggunakan relasi:

```text
utd19_u.csv
     |
   detid
     |
detectors_public.csv
```

### Link Dataset

File:

```text
links.csv
```

Berisi informasi geometri jaringan jalan dalam bentuk waypoint dan koordinat spasial.

Dataset ini **tidak digunakan dalam proses join utama** pada pipeline karena karakteristik datanya dapat menyebabkan ledakan jumlah record (data explosion).

Setiap `linkid` dapat memiliki banyak waypoint sehingga ketika dilakukan join langsung dengan dataset traffic yang berisi lebih dari 134 juta record, jumlah baris hasil join dapat meningkat menjadi miliaran record dan tidak sesuai dengan tujuan analisis proyek.

Oleh karena itu:

* `links.csv` digunakan untuk eksplorasi dan pemahaman struktur jaringan jalan.
* Join utama hanya dilakukan antara `utd19_u.csv` dan `detectors_public.csv`.
* Pendekatan ini menjaga efisiensi pemrosesan pada lingkungan Azure VM dengan spesifikasi terbatas (2 vCPU, 8 GB RAM).

---

# Sample Output

Folder `sample_output` berisi contoh dataset hasil akhir dari Gold Layer.

Dataset ini merupakan hasil agregasi dari lebih dari 134 juta record data mentah menjadi dataset analitik yang siap digunakan untuk dashboard dan Business Intelligence.

| File              | Ukuran  | Jumlah Baris |
| ----------------- | ------- | ------------ |
| city_summary.csv  | 1.54 KB | 39           |
| city_daily.csv    | 59 KB   | 1.378        |
| road_analysis.csv | 14.4 KB | 315          |

Deskripsi masing-masing outputnya dapat dilihat pada file:

```text
sample_output/README.md
```

---

# Catatan

Karena ukuran dataset asli mencapai beberapa gigabyte, file mentah tidak disertakan dalam repository ini.

Pengguna yang ingin mereproduksi pipeline secara menyeluruh dapat mengunduh dataset UTD19 langsung dari sumber resminya dan mengikuti panduan yang telah dijelaskan pada README utama proyek.
