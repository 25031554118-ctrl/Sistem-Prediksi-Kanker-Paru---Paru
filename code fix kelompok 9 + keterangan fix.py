# 1. DEFINISI KELAS (Blueprint untuk setiap titik dalam pohon)
class Node:
    def __init__(self, pertanyaan=None, hasil=None):
        self.pertanyaan = pertanyaan   # Menyimpan teks pertanyaan (jika node ini adalah persimpangan)
        self.hasil = hasil            # Menyimpan kesimpulan (jika node ini adalah ujung pohon/leaf)
        self.cabang = {}              # Kamus (dictionary) untuk memetakan jawaban ke node berikutnya

    def tambah_cabang(self, nilai_input, node_tujuan):
        # Menghubungkan satu node ke node lain berdasarkan jawaban tertentu
        # Contoh: Jika jawabannya "ya", maka lanjut ke node_X
        self.cabang[nilai_input.lower()] = node_tujuan 

# FUNGSI INTI: Logic Penelusuran (Traversing)
# Ini adalah "mesin" yang menggerakkan program dari pertanyaan ke pertanyaan
def telusuri_pohon(node):
    # BASIS REKURSI: Jika node memiliki 'hasil', berarti perjalanan selesai
    if node.hasil is not None:
        print(f"\n=== HASIL KEPUTUSAN ===")
        print(f"Keputusan: {node.hasil}")
        return

    # Tampilkan pertanyaan kepada pengguna
    print(f"\n> {node.pertanyaan}")
    pilihan = input("Jawaban: ").lower()

    # LOGIKA KHUSUS: Penanganan input numerik untuk Nilai NO
    if node.pertanyaan == "Masukkan nilai NO":
        try:
            nilai_no = float(pilihan)
            if nilai_no > 54.5: # Percabangan berdasarkan perbandingan angka
                telusuri_pohon(node.cabang["> 54.5"])
            else:
                telusuri_pohon(node.cabang["<= 54.5"])
        except ValueError:
            print("Input tidak valid! Harap masukkan angka untuk nilai NO.")
            telusuri_pohon(node)
    # Logika umum untuk pilihan teks
    elif pilihan in node.cabang:
        # Memanggil fungsi ini kembali (rekursif) dengan node tujuan sesuai jawaban
        telusuri_pohon(node.cabang[pilihan]) 
    else:
        print("Input tidak valid. Silakan coba lagi.")
        telusuri_pohon(node)

# 2. MEMBANGUN STRUKTUR POHON (Decision Tree Construction)

# A. Leaf Nodes (Ujung Pohon): Berisi hasil akhir/kesimpulan
tidak = Node(hasil="Tidak")
ya = Node(hasil="Ya")
tidak2 = Node(hasil="(Kemungkinan tidak terkena lebih tinggi)")
ya2 = Node(hasil="(Kemungkinan terkena lebih tinggi)")

# B. Internal Nodes (Persimpangan): Berisi pertanyaan

# Jalur untuk perokok PASIF
node_alkohol_kanan = Node(pertanyaan="Konsumsi alkohol (jarang/sering)?")
node_alkohol_kanan.tambah_cabang("jarang", tidak2)
node_alkohol_kanan.tambah_cabang("sering", ya2)

node_usia = Node(pertanyaan="Usia (muda/tua)?")
node_usia.tambah_cabang("tua", ya)
node_usia.tambah_cabang("muda", node_alkohol_kanan) # Menyambung ke pertanyaan alkohol

node_begadang = Node(pertanyaan="Apakah sering begadang (ya/tidak)?")
node_begadang.tambah_cabang("ya", ya)
node_begadang.tambah_cabang("tidak", node_usia) # Menyambung ke pertanyaan usia

# Jalur untuk perokok AKTIF
node_no = Node(pertanyaan="Masukkan nilai NO")
node_no.tambah_cabang("> 54.5", tidak2)
node_no.tambah_cabang("<= 54.5", ya)

node_alkohol_kiri = Node(pertanyaan="Konsumsi alkohol (jarang/sering)?")
node_alkohol_kiri.tambah_cabang("jarang", tidak2)
node_alkohol_kiri.tambah_cabang("sering", node_no) # Menyambung ke input nilai NO

node_jari = Node(pertanyaan="Apakah jari kuning (ada/tidak)?")
node_jari.tambah_cabang("tidak", tidak)
node_jari.tambah_cabang("ada", node_alkohol_kiri) # Menyambung ke pertanyaan alkohol

node_jk = Node(pertanyaan="Jenis kelamin (pria/wanita)?")
node_jk.tambah_cabang("pria", tidak)
node_jk.tambah_cabang("wanita", node_jari) # Menyambung ke pertanyaan jari kuning

node_penyakit = Node(pertanyaan="Apakah memiliki penyakit bawaan (ada/tidak)?")
node_penyakit.tambah_cabang("tidak", tidak)
node_penyakit.tambah_cabang("ada", node_jk) # Menyambung ke pertanyaan jenis kelamin

# C. ROOT NODE (Pintu Masuk Utama)
# Dari sini program mulai menentukan apakah akan lari ke cabang Aktif atau Pasif
root_node = Node(pertanyaan="Status merokok (aktif/pasif)?")
root_node.tambah_cabang("aktif", node_penyakit) # Menyambung ke jalur Aktif
root_node.tambah_cabang("pasif", node_begadang)  # Menyambung ke jalur Pasif

# 3. EKSEKUSI PROGRAM
if __name__ == "__main__":
    print("=== PROGRAM PREDIKSI RISIKO KANKER PARU-PARU ===")
    # Memulai program dari Root Node yang sudah didefinisikan di atas
    telusuri_pohon(root_node) 