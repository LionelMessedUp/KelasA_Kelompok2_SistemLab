class Alat:
    def __init__(self, kode_alat: str, nama_alat: str, kategori: str, kondisi: str = "Baik"):
        self.kode_alat = kode_alat
        self.nama_alat = nama_alat
        self.kategori = kategori
        self.kondisi = kondisi
        self.tersedia = True if kondisi == "Baik" else False

    def update_kondisi(self, kondisi_baru: str):
        self.kondisi = kondisi_baru
        if kondisi_baru in ["Rusak Berat", "Rusak Ringan"]:
            self.tersedia = False
        elif kondisi_baru == "Baik":
            self.tersedia = True

    def set_tersedia(self, status: bool):
        self.tersedia = status
