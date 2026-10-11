Class Mahasiswa:
    def__init__(self, nim: str, nama: str, no_hp: str):
        self.nim = nim
        self.nama= nama
        self.no_hp= no_hp
        self.jumlah_transaksi_aktif = 0

    def bisa_pinjam(self) -> bool:
        #maksimal 2 transaksi peminjaman aktif
        return self.jumlah_transaksi_aktif < 2

    def tambah_transaksi_aktif(self):
        self.jumlah_transaksi_aktif += 1

    def kurangi_transaksi_aktif(self):
        if self.jumlah_transaksi_aktif > 0:
            self.jumlah_transaksi_aktif -= 1
