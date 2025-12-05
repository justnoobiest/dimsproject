🌍 Global Health, Nutrition & Economics Explorer

Aplikasi ini adalah dashboard interaktif berbasis Streamlit yang digunakan untuk mengeksplorasi keterkaitan antara kesehatan, gizi, demografi, dan ekonomi di berbagai negara dan tahun.

Dibangun sebagai tugas praktikum big data / visualisasi data oleh:

Nama : Muhammad Dimas Sudirman

NIM : 021002404001

Link aplikasi yang sudah dideploy di Streamlit Cloud:
👉 https://dimsproject.streamlit.app/

📦 Dataset

Aplikasi ini menggunakan dataset:

“Global Health, Nutrition, Mortality & Economic Data” – Miguel Roca

Sumber resmi dataset (Kaggle):
➡️ https://www.kaggle.com/datasets/miguelroca/global-health-nutrition-mortality-economic-data

File yang dipakai di aplikasi ini sudah digabung dalam satu file utama:

UnifiedDataset.csv

yang berisi berbagai indikator, antara lain:

Kesehatan & Mortalitas
Life expectancy, infant mortality rate, under-5 mortality, cardiovascular deaths, suicide rate, alcohol abuse, unsafe WASH mortality, poisoning mortality, injury deaths, death rate, birth rate, dll.

Polusi Udara & Penyakit Tidak Menular (NCD)
Air pollution death rate (stroke, IHD, COPD, LRI, lung cancer) serta versi age-standardized.

Demografi & Populasi
Struktur umur (% age 0–14, 15–64, 65+, dst), total population.

Kesehatan Ibu & Anak
Maternal mortality, neonatal mortality, skilled birth attendance, malaria incidence, TB incidence, hepatitis B, adolescent birth rate, reproductive-age women.

Sistem Kesehatan
Universal health coverage, jumlah dokter, perawat & bidan, dokter gigi, apoteker, intervensi NTDs, road traffic deaths.

WASH & Energi Bersih
Akses air minum dasar, sanitasi dasar (total/urban/rural), safely managed sanitation, fasilitas cuci tangan, clean fuel and technology.

Ekonomi & Kemiskinan
GDP per capita, income per capita, GNI per capita, belanja pemerintah untuk edukasi, militer, kesehatan; persentase penduduk di bawah garis $1.90, $3.20, $5.50 per hari.

Konflik & Keamanan
Conflict and terrorism deaths, homicide rate, battle-related deaths.

Pola Makan & Gizi
Komposisi diet (sugar, fats, meat, dairy & eggs, fruits & vegetables, starchy roots, pulses, cereals & grains) serta kalori dari animal protein, plant protein, fat, dan carbohydrates.
Ditambah detail konsumsi buah & sereal (bananas, apples, citrus, grapes, rice, wheat, maize, dll).

🧭 Struktur Halaman Aplikasi

Aplikasi terdiri dari beberapa halaman utama (sesuai menu di sidebar):

1. 🏠 Home

Menampilkan judul aplikasi dan identitas pengembang:

Muhammad Dimas Sudirman – 021002404001.

Menjelaskan tujuan aplikasi:

Menghubungkan indikator kesehatan, gizi, demografi, ekonomi, kemiskinan, WASH, dan konflik.

Menampilkan ringkasan dataset:

Jumlah negara, rentang tahun, total observasi.

Tabel contoh data (head) untuk memberikan gambaran struktur kolom.

2. 🌍 Global Map

Peta dunia interaktif berbasis choropleth.

Filter:

Tahun (Year)

Gender (Gender) – misal: Both sexes, Male, Female jika tersedia di dataset.

Indikator yang bisa dipilih (hanya yang punya data untuk kombinasi tahun & gender tersebut), misalnya:

Life Expectancy

Infant Mortality Rate

Death Rate

GDP per Capita

dll.

Jika tidak ada data untuk kombinasi filter tertentu, aplikasi akan menampilkan pesan yang informatif.

Dilengkapi histogram + boxplot untuk melihat distribusi indikator yang sama di seluruh negara.

3. 📋 Country Profile

Profil lengkap untuk satu negara (dan gender tertentu), dengan beberapa tab:

🩺 Health
Tren life expectancy, infant mortality, under-5 mortality, death rate per tahun.

💨 Air Pollution
Tren air pollution death rate (total & age-standardized) untuk beberapa penyebab (stroke, IHD, LRI, COPD, lung cancers).

👨‍👩‍👧 Demography & Maternal

Struktur umur dalam bentuk area chart (% penduduk per kelompok umur).

Tren maternal mortality, neonatal mortality, dan % births attended by skilled personnel.

💰 Economics & Poverty
Tren GDP per capita, income per capita, GNI per capita, dan persentase penduduk di bawah garis kemiskinan (1.90 / 3.20 / 5.50 USD).

🍽 Nutrition & Diet

Menampilkan tahun terakhir yang memiliki data diet lengkap untuk negara tersebut.

Bar chart komposisi diet (share kalori dari berbagai kelompok makanan).

Bar chart kalori dari animal protein, plant protein, fat, dan carbohydrates.

4. 📈 Compare Countries

Membandingkan beberapa negara sekaligus berdasarkan indikator yang sama.

Filter:

Daftar negara (multiselect)

Gender

Rentang tahun

Visualisasi:

Line chart: tren indikator (misal life expectancy atau GDP per capita) untuk beberapa negara sekaligus.

Bar chart: snapshot per tahun tertentu untuk membandingkan nilai antar negara.

5. 🥦 Nutrition & Diet

Fokus pada hubungan indikator gizi/pola makan dengan indikator kesehatan/ekonomi.

Filter:

Tahun (dibatasi hanya pada tahun yang memiliki data diet).

Gender.

Opsional: filter negara tertentu.

Pilih:

X axis: indikator diet (misalnya Diet Composition Sugar, Diet Composition Meat, dll).

Y axis: indikator health/economic (misalnya Life Expectancy, GDP per Capita).

Scatter plot interaktif dengan bubble size opsional (GDP per Capita) dan outlier ekstrim dibersihkan (1–99th percentile).

6. 🚰 Demography & WASH

Menampilkan kombinasi struktur penduduk, indikator SDGs populasi, serta cakupan layanan WASH & clean fuel.

Dibagi menjadi dua tab:

Demografi & SDGs – area chart struktur umur; line chart indikator populasi SDG.

WASH & Clean Fuel – bar chart cakupan air minum, sanitasi, cuci tangan, dan akses energi bersih untuk tahun terakhir yang tersedia.

7. 💰 Economics & Poverty

Halaman khusus untuk indikator ekonomi makro, kemiskinan, dan konflik.

Visualisasi:

Line chart belanja pemerintah (education, military, health).

Line chart persentase penduduk di bawah garis kemiskinan.

Line chart indikator konflik (conflict & terrorism deaths, homicide rate, battle-related deaths) jika datanya tersedia.

8. 📊 Correlation Explorer

Memungkinkan pengguna memilih subset indikator numerik dan melihat:

Correlation matrix (heatmap korelasi).

Scatter plot antara dua indikator yang dipilih.

Filter:

Tahun

Gender

(Opsional) subset negara

Variabel default mencakup kombinasi health, economic, dan diet (misal Life Expectancy, Death Rate, GDP per Capita, Diet Calories Fat, dll).

9. 📑 Data & Download

Halaman untuk filter dan mengunduh subset data.

Filter:

Rentang tahun

Gender (All / spesifik)

Daftar negara

Pengguna memilih sendiri kolom apa saja yang ingin ditampilkan.

Subset data dapat diunduh dalam format CSV untuk analisis lanjutan (Excel, Jupyter, Stata, dsb).

🛠️ Teknologi yang Digunakan

Python

Streamlit – untuk membangun web app interaktif.

Pandas & NumPy – manipulasi dan pembersihan data.

Plotly Express – visualisasi interaktif (line, bar, area, scatter, choropleth, heatmap).