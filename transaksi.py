from datetime import date, timedelta
from mahasiswa import Mahasiswa
from Alat import Alat
from DetailPeminjaman import DetailPeminjaman

class Transaksi:
    def __init__(self, id_transaksi: str, mahasiswa: Mahasiswa, tanggal_pinjam: date = None):
        self.id_transaksi = id_transaksi
        self.mahasiswa = mahasiswa
        self.daftar_detail = []  
        self.tanggal_pinjam = tanggal_pinjam if tanggal_pinjam else date.today()
        self.batas_kembali = self.tanggal_pinjam + timedelta(days=7)
        self.status = "Dipinjam"

    def tambah_detail(self, alat: Alat):
        detail = DetailPeminjaman(alat)
        self.daftar_detail.append(detail)
        alat.set_tersedia(False)

    def cari_detail(self, kode_alat: str) -> DetailPeminjaman:
        for detail in self.daftar_detail:
            if detail.alat.kode_alat == kode_alat:
                return detail
        return None

    def semua_dikembalikan(self) -> bool:
        if not self.daftar_detail:
            return False
        for detail in self.daftar_detail:
            if not detail.status_dikembalikan:
                return False
        return True

    def hitung_terlambat(self, tgl: date = None) -> int:
        if tgl is None:
            tgl = date.today()
        selisih = (tgl - self.batas_kembali).days
        return selisih if selisih > 0 else 0

    def cek_status_transaksi(self) -> str:
        if self.semua_dikembalikan():
            self.status = "Selesai"
            self.mahasiswa.kurangi_transaksi_aktif()
        return self.status