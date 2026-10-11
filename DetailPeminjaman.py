class DetailPeminjaman:
    def __init__(self, alat: Alat):
        self.alat = alat  # Merujuk ke objek Alat
        self.status_dikembalikan = False
        self.tanggal_kembali = None
        self.kondisi_kembali = None  # Menyimpan kondisi fisik saat dikembalikan

    def proses_kembali(self, kondisi: str, tgl: date):
        self.status_dikembalikan = True
        self.tanggal_kembali = tgl
        self.kondisi_kembali = kondisi
        # Update kondisi fisik dan ketersediaan pada objek Alat
        self.alat.update_kondisi(kondisi)
