import csv

# Baca dataset
file_path = "data.csv"
data_harga_rumah = []

with open(file_path, newline='') as file:
    data_harga_rumah = [row for row in csv.reader(file)]

# Buat variabel tampungan list harga rumah dengan nama harga_rumah
key_harga_rumah = data_harga_rumah[0]
harga_rumah = []

for baris_harga_rumah in data_harga_rumah[1:]:
    dict_harga_rumah = dict()
    for i in range(len(baris_harga_rumah)):
        dict_harga_rumah[key_harga_rumah[i]] = baris_harga_rumah[i]
    harga_rumah.append(dict_harga_rumah)

# Fungsi baca_spesifik_atribut untuk membuat sebuah list yang berisikan seluruh 
# atribut dengan kunci (key) yang spesifik. 
def baca_spesifik_atribut(data, atribut):
 list_atribut = []
 for data in data:
  hasil = data[atribut]
  list_atribut.append(hasil)
 return list_atribut

# fungsi nilai minimal untuk mendapatkan nilai terkecil dalam dataset
def nilai_minimal(list_atribut):
 min_atribut = 9999
 for atribut in list_atribut:
  if int(atribut) < min_atribut:
   min_atribut = int(atribut)
 return min_atribut

# fungsi max value untuk mendapatkan nilai terbesar dalam dataset
def nilai_maksimal(list_atribut):
 max_atribut = -9999
 for atribut in list_atribut:
  if int(atribut) > max_atribut:
   max_atribut = int(atribut)
 return max_atribut

# fungsi nilai_transformasi untuk mendapatkan nilai transformasi
def nilai_transformasi(atribut, nilai_maksimal, nilai_minimal):
 nilai = (atribut - nilai_minimal) / (nilai_maksimal - nilai_minimal)
 return nilai

# fungsi transformasi_data yang yang memproses hasil dari
# transformasi data dari dataset dan atribut.
def transformasi_data(dataset, list_atribut):
 info_atribut = {}
 for nama_atribut in list_atribut:
  spesifik_atribut = baca_spesifik_atribut(dataset, nama_atribut)
  max_atribut = nilai_maksimal(spesifik_atribut)
  min_atribut = nilai_minimal(spesifik_atribut)
  info_atribut[nama_atribut] = {'max': max_atribut, 'min': min_atribut}
  indeks_data = 0
  while(indeks_data < len(dataset)):
   dataset[indeks_data][nama_atribut] = nilai_transformasi(int(dataset[indeks_data][nama_atribut]), max_atribut, min_atribut)
   indeks_data += 1
 return dataset, info_atribut

# fungsi transformasi_data_prediksi yang yang memproses hasil dari
# transformasi data dari hasil transformasi data sebelumnya dan info atribut.
def transformasi_data_prediksi(data_transformasi, info_atribut):
 for nama_atribut in data_transformasi.keys():
  data_transformasi[nama_atribut] = (data_transformasi[nama_atribut] - info_atribut[nama_atribut]['min']) / (
                    info_atribut[nama_atribut]['max'] - info_atribut[nama_atribut]['min'])
 return data_transformasi

# fungsi untuk mengubah nilai menjadi nilai absolut dari 
# nilai data atribut untuk prediksi
def nilai_absolut(nilai):
	if nilai < 0:
		return -nilai
	else:
		return nilai

# fungsi untuk memprediksi harga rumah dengan membandingkan dari kemiripan atribut 
def proses_prediksi_harga_rumah(data_prediksi, dataset):
	prediksi_harga = 0
	perbedaan_terkecil = 999
	for nilai_atribut in dataset:
		perbedaan= nilai_absolut(data_prediksi['tanah'] - nilai_atribut['tanah'])
		perbedaan+= nilai_absolut(data_prediksi['bangunan'] - nilai_atribut['bangunan'])
		perbedaan+= nilai_absolut(data_prediksi['jarak_ke_pusat'] - nilai_atribut['jarak_ke_pusat'])
		if perbedaan < perbedaan_terkecil:
			prediksi_harga = nilai_atribut['harga']
			perbedaan_terkecil = perbedaan
	return prediksi_harga

# melakukan transformasi data awal 
harga_rumah, attr_info = transformasi_data(harga_rumah ,['tanah','bangunan','jarak_ke_pusat'])

# inputan untuk memprediksi harga rumah 
input_atribut_prediksi = {'tanah': 80, 'bangunan': 80, 'jarak_ke_pusat': 35}

# melakukan transformasi data untuk prediksi 
data = transformasi_data_prediksi(input_atribut_prediksi, attr_info)

# melakukan proses prediksi 
harga = proses_prediksi_harga_rumah(data, harga_rumah)

# menampilkan harga prediksi rumah 
print("Prediksi harga rumah: ", "Rp.", harga)