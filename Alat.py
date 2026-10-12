class Alat:
    def __init__(self, kode_alat: str, nama_alat: str, kategori: str, kondisi: str = "Baik"):
        self.kode_alat = kode_alat
        self.nama_alat = nama_alat
        self.kategori = kategori
        self.kondisi = kondisi
        # Menggunakan penamaan 'tersedia' sesuai Dokumen Keputusan Desain
        self.tersedia = True if kondisi == "Baik" else False

    def update_kondisi(self, kondisi_baru: str):
        self.kondisi = kondisi_baru
        # Aturan 5: Jika rusak berat atau rusak ringan, alat tidak tersedia
        if kondisi_baru in ["Rusak Berat", "Rusak Ringan"]:
            self.tersedia = False
        elif kondisi_baru == "Baik":
            self.tersedia = True

    def set_tersedia(self, status: bool):
        self.tersedia = status