# 5. CLASS SISTEM LABORATORIUM 
# ==========================================
class SistemLaboratorium:
    def __init__(self):
        self.data_mahasiswa = {}  # {nim: Mahasiswa}
        self.data_alat = {}       # {kode_alat: Alat}
        self.data_transaksi = []  # [Transaksi]
        self.nomor_transaksi = 0  # Counter ID otomatis sesuai Dokumen Desain
        
        # Memuat data awal untuk pengujian
        self.muat_data_dummy()

    def muat_data_dummy(self):
        # Data Mahasiswa
        m1 = Mahasiswa("MHS001", "Budi Santoso", "081234567890")
        m2 = Mahasiswa("MHS002", "Siti Rahma", "089876543210")
        self.data_mahasiswa = {m1.nim: m1, m2.nim: m2}

        # Data Alat
        a1 = Alat("ALT001", "Laptop Dell XPS", "Perangkat Komputasi", "Baik")
        a2 = Alat("ALT002", "Switch Cisco 24 Port", "Perangkat Jaringan", "Baik")
        a3 = Alat("ALT003", "Kamera Canon EOS", "Perangkat Multimedia", "Baik")
        a4 = Alat("ALT004", "Proyektor Epson", "Perangkat Multimedia", "Rusak Ringan")
        self.data_alat = {a1.kode_alat: a1, a2.kode_alat: a2, a3.kode_alat: a3, a4.kode_alat: a4}

        # Dummy Transaksi Peminjaman Awal
        self.nomor_transaksi += 1
        id_trx = f"TRX{self.nomor_transaksi:03d}"
        tgl_pinjam = date.today() - timedelta(days=2)
        
        trx = Transaksi(id_trx, m1, tgl_pinjam)
        trx.tambah_detail(a1)
        trx.tambah_detail(a2)
        m1.tambah_transaksi_aktif()
        self.data_transaksi.append(trx)

    # --- KELOLA DATA MAHASISWA (CRUD) ---
    def tambah_mahasiswa(self):
        print("\n--- Tambah Mahasiswa ---")
        nim = input("Masukkan NIM: ").strip()
        if nim in self.data_mahasiswa:
            print("[X] Gagal: NIM sudah terdaftar!")
            return
        nama = input("Masukkan Nama: ").strip()
        no_hp = input("Masukkan No. HP: ").strip()
        self.data_mahasiswa[nim] = Mahasiswa(nim, nama, no_hp)
        print("[V] Data mahasiswa berhasil ditambahkan.")

    def edit_mahasiswa(self):
        print("\n--- Edit Mahasiswa ---")
        nim = input("Masukkan NIM Mahasiswa: ").strip()
        mhs = self.cari_mahasiswa(nim)
        if mhs:
            mhs.nama = input(f"Nama Baru ({mhs.nama}): ").strip() or mhs.nama
            mhs.no_hp = input(f"No. HP Baru ({mhs.no_hp}): ").strip() or mhs.no_hp
            print("[V] Data mahasiswa berhasil diperbarui.")

    def hapus_mahasiswa(self):
        print("\n--- Hapus Mahasiswa ---")
        nim = input("Masukkan NIM: ").strip()
        mhs = self.cari_mahasiswa(nim)
        if not mhs:
            return
        # Aturan 6: Tidak boleh dihapus jika masih ada transaksi aktif
        if mhs.jumlah_transaksi_aktif > 0:
            print("[X] Gagal: Mahasiswa masih memiliki transaksi peminjaman aktif!")
            return
        del self.data_mahasiswa[nim]
        print("[V] Data mahasiswa berhasil dihapus.")

    def cari_mahasiswa(self, nim: str) -> Mahasiswa:
        mhs = self.data_mahasiswa.get(nim)
        if mhs:
            print(f"-> NIM: {mhs.nim} | Nama: {mhs.nama} | HP: {mhs.no_hp} | Trx Aktif: {mhs.jumlah_transaksi_aktif}")
            return mhs
        else:
            print("[X] Data mahasiswa tidak ditemukan.")
            return None

    # --- KELOLA DATA ALAT (CRUD) ---
    def tambah_alat(self):
        print("\n--- Tambah Alat ---")
        kode = input("Masukkan Kode Alat: ").strip()
        if kode in self.data_alat:
            print("[X] Gagal: Kode alat sudah terdaftar!")
            return
        nama = input("Masukkan Nama Alat: ").strip()
        kategori = input("Masukkan Kategori: ").strip()
        self.data_alat[kode] = Alat(kode, nama, kategori)
        print("[V] Data alat berhasil ditambahkan.")

    def edit_alat(self):
        print("\n--- Edit Alat ---")
        kode = input("Masukkan Kode Alat: ").strip()
        alat = self.cari_alat(kode)
        if alat:
            alat.nama_alat = input(f"Nama Baru ({alat.nama_alat}): ").strip() or alat.nama_alat
            alat.kategori = input(f"Kategori Baru ({alat.kategori}): ").strip() or alat.kategori
            print("[V] Data alat berhasil diperbarui.")

    def hapus_alat(self):
        print("\n--- Hapus Alat ---")
        kode = input("Masukkan Kode Alat: ").strip()
        alat = self.cari_alat(kode)
        if not alat:
            return
        # Aturan 6: Tidak boleh dihapus jika masih ada dalam transaksi aktif
        for trx in self.data_transaksi:
            if trx.status != "Selesai":
                detail = trx.cari_detail(kode)
                if detail and not detail.status_dikembalikan:
                    print("[X] Gagal: Alat sedang tercatat dalam transaksi aktif!")
                    return
        del self.data_alat[kode]
        print("[V] Data alat berhasil dihapus.")

    def cari_alat(self, kode: str) -> Alat:
        alat = self.data_alat.get(kode)
        if alat:
            stok = "Tersedia" if alat.tersedia else "Tidak Tersedia"
            print(f"-> Kode: {alat.kode_alat} | Nama: {alat.nama_alat} | Kategori: {alat.kategori} | Kondisi: {alat.kondisi} | Status: {stok}")
            return alat
        else:
            print("[X] Data alat tidak ditemukan.")
            return None

    # --- TRANSAKSI PEMINJAMAN & PENGEMBALIAN ---
    def buat_transaksi_peminjaman(self):
        print("\n--- Buat Transaksi Peminjaman ---")
        nim = input("Masukkan NIM Mahasiswa: ").strip()
        mhs = self.data_mahasiswa.get(nim)
        if not mhs:
            print("[X] Gagal: NIM belum terdaftar!")
            return

        # Aturan 2: Cek batas peminjaman aktif
        if not mhs.bisa_pinjam():
            print("[X] Gagal: Mahasiswa sudah mencapai batas maksimal 2 transaksi aktif!")
            return

        pilihan_alat = []
        while True:
            kode = input("Masukkan Kode Alat (ketik 'selesai' untuk mengakhiri): ").strip()
            if kode.lower() == 'selesai':
                break
            alat = self.data_alat.get(kode)
            if not alat:
                print("[X] Kode alat tidak ditemukan.")
                continue
            # Aturan 1: Cek ketersediaan alat
            if not alat.tersedia:
                print(f"[X] Alat '{alat.nama_alat}' sedang tidak tersedia/dipinjam/rusak!")
                continue
            if alat in pilihan_alat:
                print("[X] Alat sudah ditambahkan ke daftar peminjaman ini.")
                continue

            pilihan_alat.append(alat)
            print(f"[V] '{alat.nama_alat}' berhasil ditambahkan ke daftar.")

        if not pilihan_alat:
            print("[X] Transaksi dibatalkan karena tidak ada alat yang dipinjam.")
            return

        # Penomoran otomatis menggunakan nomor_transaksi
        self.nomor_transaksi += 1
        id_trx = f"TRX{self.nomor_transaksi:03d}"
        tgl_sekarang = date.today()

        trx_baru = Transaksi(id_trx, mhs, tgl_sekarang)
        for a in pilihan_alat:
            trx_baru.tambah_detail(a)
        
        mhs.tambah_transaksi_aktif()
        self.data_transaksi.append(trx_baru)

        print(f"\n[V] Transaksi Berhasil Dibuat!")
        print(f"ID Transaksi : {trx_baru.id_transaksi}")
        print(f"Peminjam     : {mhs.nama}")
        print(f"Tenggat      : {trx_baru.batas_kembali}")

    def proses_pengembalian_alat(self):
        print("\n--- Proses Pengembalian Alat ---")
        id_trx = input("Masukkan ID Transaksi: ").strip()
        trx = self.cari_transaksi(id_trx)
        
        if not trx:
            return
        if trx.status == "Selesai":
            print("[!] Transaksi ini sudah selesai.")
            return

        print(f"\nDaftar Alat Dipinjam dalam {trx.id_transaksi}:")
        for idx, detail in enumerate(trx.daftar_detail, 1):
            st = f"Sudah Kembali ({detail.kondisi_kembali})" if detail.status_dikembalikan else "Masih Dipinjam"
            print(f"{idx}. [{detail.alat.kode_alat}] {detail.alat.nama_alat} - Status: {st}")

        kode_alat = input("\nMasukkan Kode Alat yang ingin dikembalikan: ").strip()
        detail_terpilih = trx.cari_detail(kode_alat)

        if not detail_terpilih:
            print("[X] Alat tersebut tidak ada dalam transaksi ini.")
            return
        if detail_terpilih.status_dikembalikan:
            print("[!] Alat ini sudah dikembalikan sebelumnya.")
            return

        print("\nPilih Kondisi Alat Saat Dikembalikan:")
        print("1. Baik")
        print("2. Rusak Ringan")
        print("3. Rusak Berat")
        opsi_kondisi = input("Pilihan (1/2/3): ").strip()
        map_kondisi = {"1": "Baik", "2": "Rusak Ringan", "3": "Rusak Berat"}
        kondisi_akhir = map_kondisi.get(opsi_kondisi, "Baik")

        tgl_sekarang = date.today()
        detail_terpilih.proses_kembali(kondisi_akhir, tgl_sekarang)

        # Hitung keterlambatan
        terlambat = trx.hitung_terlambat(tgl_sekarang)
        if terlambat > 0:
            print(f"[!] PERHATIAN: Pengembalian terlambat {terlambat} hari dari batas waktu!")

        status_terbaru = trx.cek_status_transaksi()
        print(f"[V] Pengembalian berhasil dicatat!")
        print(f"Status Transaksi Saat Ini: {status_terbaru}")

    def cari_transaksi(self, id_transaksi: str) -> Transaksi:
        for trx in self.data_transaksi:
            if trx.id_transaksi == id_transaksi:
                return trx
        print("[X] ID Transaksi tidak ditemukan.")
        return None

    # --- LAPORAN & RIWAYAT ---
    def laporan_alat_tersedia(self):
        print("\n--- Laporan Alat Tersedia ---")
        tersedia = [a for a in self.data_alat.values() if a.tersedia]
        if not tersedia:
            print("Tidak ada alat yang tersedia saat ini.")
            return
        for a in tersedia:
            print(f"[{a.kode_alat}] {a.nama_alat} | Kategori: {a.kategori} | Kondisi: {a.kondisi}")

    def laporan_alat_dipinjam(self):
        print("\n--- Laporan Alat yang Sedang Dipinjam ---")
        dipinjam = []
        for trx in self.data_transaksi:
            if trx.status != "Selesai":
                for detail in trx.daftar_detail:
                    if not detail.status_dikembalikan:
                        dipinjam.append((detail.alat, trx.mahasiswa.nama, trx.id_transaksi))

        if not dipinjam:
            print("Tidak ada alat yang sedang dipinjam saat ini.")
            return
        for alat, peminjam, id_trx in dipinjam:
            print(f"[{alat.kode_alat}] {alat.nama_alat} | Dipinjam oleh: {peminjam} (ID: {id_trx})")

    def laporan_alat_rusak(self):
        print("\n--- Laporan Alat Rusak ---")
        rusak = [a for a in self.data_alat.values() if a.kondisi in ["Rusak Ringan", "Rusak Berat"]]
        if not rusak:
            print("Tidak ada alat yang rusak saat ini.")
            return
        for a in rusak:
            print(f"[{a.kode_alat}] {a.nama_alat} | Kondisi: {a.kondisi} | Status Tersedia: {a.tersedia}")

    def riwayat_peminjaman_mahasiswa(self, nim: str = None):
        if not nim:
            nim = input("Masukkan NIM Mahasiswa: ").strip()
        mhs = self.data_mahasiswa.get(nim)
        if not mhs:
            print("[X] Data mahasiswa tidak ditemukan.")
            return

        print(f"\n--- Riwayat Peminjaman: {mhs.nama} ({mhs.nim}) ---")
        riwayat = [t for t in self.data_transaksi if t.mahasiswa.nim == nim]
        if not riwayat:
            print("Belum ada riwayat transaksi peminjaman.")
            return

        for trx in riwayat:
            print(f"\nID Transaksi : {trx.id_transaksi}")
            print(f"Tgl Pinjam   : {trx.tanggal_pinjam} | Batas Kembali: {trx.batas_kembali}")
            print(f"Status       : {trx.status}")
            print("Item Dipinjam:")
            for d in trx.daftar_detail:
                st = f"Dikembalikan tgl {d.tanggal_kembali} [{d.kondisi_kembali}]" if d.status_dikembalikan else "Belum dikembalikan"
                print(f" - {d.alat.nama_alat} : {st}")

    # --- MENU UTAMA PROGRAM ---
    def menu_utama(self):
        while True:
            print("\n==============================================")
            print("    SISTEM LAB PEMINJAMAN PERALATAN (OOP)     ")
            print("==============================================")
            print("1.  Kelola Data Mahasiswa (Tambah/Edit/Hapus/Cari)")
            print("2.  Kelola Data Alat (Tambah/Edit/Hapus/Cari)")
            print("3.  Buat Transaksi Peminjaman")
            print("4.  Proses Pengembalian Alat")
            print("5.  Cari Transaksi")
            print("6.  Tampilkan Alat yang Tersedia")
            print("7.  Tampilkan Alat yang Sedang Dipinjam")
            print("8.  Tampilkan Alat yang Rusak")
            print("9.  Tampilkan Riwayat Peminjaman Mahasiswa")
            print("0.  Keluar dari Program")
            print("==============================================")
            pilihan = input("Pilih menu (0-9): ").strip()

            if pilihan == "1":
                print("\n[ Submenu Mahasiswa ]")
                print("a. Tambah | b. Edit | c. Hapus | d. Cari")
                sub = input("Pilih: ").lower()
                if sub == 'a': self.tambah_mahasiswa()
                elif sub == 'b': self.edit_mahasiswa()
                elif sub == 'c': self.hapus_mahasiswa()
                elif sub == 'd': self.cari_mahasiswa(input("NIM: "))
            elif pilihan == "2":
                print("\n[ Submenu Alat ]")
                print("a. Tambah | b. Edit | c. Hapus | d. Cari")
                sub = input("Pilih: ").lower()
                if sub == 'a': self.tambah_alat()
                elif sub == 'b': self.edit_alat()
                elif sub == 'c': self.hapus_alat()
                elif sub == 'd': self.cari_alat(input("Kode Alat: "))
            elif pilihan == "3":
                self.buat_transaksi_peminjaman()
            elif pilihan == "4":
                self.proses_pengembalian_alat()
            elif pilihan == "5":
                id_t = input("Masukkan ID Transaksi: ").strip()
                t = self.cari_transaksi(id_t)
                if t:
                    print(f"ID: {t.id_transaksi} | Peminjam: {t.mahasiswa.nama} | Status: {t.status}")
            elif pilihan == "6":
                self.laporan_alat_tersedia()
            elif pilihan == "7":
                self.laporan_alat_dipinjam()
            elif pilihan == "8":
                self.laporan_alat_rusak()
            elif pilihan == "9":
                self.riwayat_peminjaman_mahasiswa()
            elif pilihan == "0":
                print("\nTerima kasih telah menggunakan Sistem Peminjaman Laboratorium.")
                break
            else:
                print("\n[X] Pilihan menu tidak valid!")# 5. CLASS SISTEM LABORATORIUM 
# ==========================================
class SistemLaboratorium:
    def __init__(self):
        self.data_mahasiswa = {}  # {nim: Mahasiswa}
        self.data_alat = {}       # {kode_alat: Alat}
        self.data_transaksi = []  # [Transaksi]
        self.nomor_transaksi = 0  # Counter ID otomatis sesuai Dokumen Desain
        
        # Memuat data awal untuk pengujian
        self.muat_data_dummy()

    def muat_data_dummy(self):
        # Data Mahasiswa
        m1 = Mahasiswa("MHS001", "Budi Santoso", "081234567890")
        m2 = Mahasiswa("MHS002", "Siti Rahma", "089876543210")
        self.data_mahasiswa = {m1.nim: m1, m2.nim: m2}

        # Data Alat
        a1 = Alat("ALT001", "Laptop Dell XPS", "Perangkat Komputasi", "Baik")
        a2 = Alat("ALT002", "Switch Cisco 24 Port", "Perangkat Jaringan", "Baik")
        a3 = Alat("ALT003", "Kamera Canon EOS", "Perangkat Multimedia", "Baik")
        a4 = Alat("ALT004", "Proyektor Epson", "Perangkat Multimedia", "Rusak Ringan")
        self.data_alat = {a1.kode_alat: a1, a2.kode_alat: a2, a3.kode_alat: a3, a4.kode_alat: a4}

        # Dummy Transaksi Peminjaman Awal
        self.nomor_transaksi += 1
        id_trx = f"TRX{self.nomor_transaksi:03d}"
        tgl_pinjam = date.today() - timedelta(days=2)
        
        trx = Transaksi(id_trx, m1, tgl_pinjam)
        trx.tambah_detail(a1)
        trx.tambah_detail(a2)
        m1.tambah_transaksi_aktif()
        self.data_transaksi.append(trx)

    # --- KELOLA DATA MAHASISWA (CRUD) ---
    def tambah_mahasiswa(self):
        print("\n--- Tambah Mahasiswa ---")
        nim = input("Masukkan NIM: ").strip()
        if nim in self.data_mahasiswa:
            print("[X] Gagal: NIM sudah terdaftar!")
            return
        nama = input("Masukkan Nama: ").strip()
        no_hp = input("Masukkan No. HP: ").strip()
        self.data_mahasiswa[nim] = Mahasiswa(nim, nama, no_hp)
        print("[V] Data mahasiswa berhasil ditambahkan.")

    def edit_mahasiswa(self):
        print("\n--- Edit Mahasiswa ---")
        nim = input("Masukkan NIM Mahasiswa: ").strip()
        mhs = self.cari_mahasiswa(nim)
        if mhs:
            mhs.nama = input(f"Nama Baru ({mhs.nama}): ").strip() or mhs.nama
            mhs.no_hp = input(f"No. HP Baru ({mhs.no_hp}): ").strip() or mhs.no_hp
            print("[V] Data mahasiswa berhasil diperbarui.")

    def hapus_mahasiswa(self):
        print("\n--- Hapus Mahasiswa ---")
        nim = input("Masukkan NIM: ").strip()
        mhs = self.cari_mahasiswa(nim)
        if not mhs:
            return
        # Aturan 6: Tidak boleh dihapus jika masih ada transaksi aktif
        if mhs.jumlah_transaksi_aktif > 0:
            print("[X] Gagal: Mahasiswa masih memiliki transaksi peminjaman aktif!")
            return
        del self.data_mahasiswa[nim]
        print("[V] Data mahasiswa berhasil dihapus.")

    def cari_mahasiswa(self, nim: str) -> Mahasiswa:
        mhs = self.data_mahasiswa.get(nim)
        if mhs:
            print(f"-> NIM: {mhs.nim} | Nama: {mhs.nama} | HP: {mhs.no_hp} | Trx Aktif: {mhs.jumlah_transaksi_aktif}")
            return mhs
        else:
            print("[X] Data mahasiswa tidak ditemukan.")
            return None

    # --- KELOLA DATA ALAT (CRUD) ---
    def tambah_alat(self):
        print("\n--- Tambah Alat ---")
        kode = input("Masukkan Kode Alat: ").strip()
        if kode in self.data_alat:
            print("[X] Gagal: Kode alat sudah terdaftar!")
            return
        nama = input("Masukkan Nama Alat: ").strip()
        kategori = input("Masukkan Kategori: ").strip()
        self.data_alat[kode] = Alat(kode, nama, kategori)
        print("[V] Data alat berhasil ditambahkan.")

    def edit_alat(self):
        print("\n--- Edit Alat ---")
        kode = input("Masukkan Kode Alat: ").strip()
        alat = self.cari_alat(kode)
        if alat:
            alat.nama_alat = input(f"Nama Baru ({alat.nama_alat}): ").strip() or alat.nama_alat
            alat.kategori = input(f"Kategori Baru ({alat.kategori}): ").strip() or alat.kategori
            print("[V] Data alat berhasil diperbarui.")

    def hapus_alat(self):
        print("\n--- Hapus Alat ---")
        kode = input("Masukkan Kode Alat: ").strip()
        alat = self.cari_alat(kode)
        if not alat:
            return
        # Aturan 6: Tidak boleh dihapus jika masih ada dalam transaksi aktif
        for trx in self.data_transaksi:
            if trx.status != "Selesai":
                detail = trx.cari_detail(kode)
                if detail and not detail.status_dikembalikan:
                    print("[X] Gagal: Alat sedang tercatat dalam transaksi aktif!")
                    return
        del self.data_alat[kode]
        print("[V] Data alat berhasil dihapus.")

    def cari_alat(self, kode: str) -> Alat:
        alat = self.data_alat.get(kode)
        if alat:
            stok = "Tersedia" if alat.tersedia else "Tidak Tersedia"
            print(f"-> Kode: {alat.kode_alat} | Nama: {alat.nama_alat} | Kategori: {alat.kategori} | Kondisi: {alat.kondisi} | Status: {stok}")
            return alat
        else:
            print("[X] Data alat tidak ditemukan.")
            return None

    # --- TRANSAKSI PEMINJAMAN & PENGEMBALIAN ---
    def buat_transaksi_peminjaman(self):
        print("\n--- Buat Transaksi Peminjaman ---")
        nim = input("Masukkan NIM Mahasiswa: ").strip()
        mhs = self.data_mahasiswa.get(nim)
        if not mhs:
            print("[X] Gagal: NIM belum terdaftar!")
            return

        # Aturan 2: Cek batas peminjaman aktif
        if not mhs.bisa_pinjam():
            print("[X] Gagal: Mahasiswa sudah mencapai batas maksimal 2 transaksi aktif!")
            return

        pilihan_alat = []
        while True:
            kode = input("Masukkan Kode Alat (ketik 'selesai' untuk mengakhiri): ").strip()
            if kode.lower() == 'selesai':
                break
            alat = self.data_alat.get(kode)
            if not alat:
                print("[X] Kode alat tidak ditemukan.")
                continue
            # Aturan 1: Cek ketersediaan alat
            if not alat.tersedia:
                print(f"[X] Alat '{alat.nama_alat}' sedang tidak tersedia/dipinjam/rusak!")
                continue
            if alat in pilihan_alat:
                print("[X] Alat sudah ditambahkan ke daftar peminjaman ini.")
                continue

            pilihan_alat.append(alat)
            print(f"[V] '{alat.nama_alat}' berhasil ditambahkan ke daftar.")

        if not pilihan_alat:
            print("[X] Transaksi dibatalkan karena tidak ada alat yang dipinjam.")
            return

        # Penomoran otomatis menggunakan nomor_transaksi
        self.nomor_transaksi += 1
        id_trx = f"TRX{self.nomor_transaksi:03d}"
        tgl_sekarang = date.today()

        trx_baru = Transaksi(id_trx, mhs, tgl_sekarang)
        for a in pilihan_alat:
            trx_baru.tambah_detail(a)
        
        mhs.tambah_transaksi_aktif()
        self.data_transaksi.append(trx_baru)

        print(f"\n[V] Transaksi Berhasil Dibuat!")
        print(f"ID Transaksi : {trx_baru.id_transaksi}")
        print(f"Peminjam     : {mhs.nama}")
        print(f"Tenggat      : {trx_baru.batas_kembali}")

    def proses_pengembalian_alat(self):
        print("\n--- Proses Pengembalian Alat ---")
        id_trx = input("Masukkan ID Transaksi: ").strip()
        trx = self.cari_transaksi(id_trx)
        
        if not trx:
            return
        if trx.status == "Selesai":
            print("[!] Transaksi ini sudah selesai.")
            return

        print(f"\nDaftar Alat Dipinjam dalam {trx.id_transaksi}:")
        for idx, detail in enumerate(trx.daftar_detail, 1):
            st = f"Sudah Kembali ({detail.kondisi_kembali})" if detail.status_dikembalikan else "Masih Dipinjam"
            print(f"{idx}. [{detail.alat.kode_alat}] {detail.alat.nama_alat} - Status: {st}")

        kode_alat = input("\nMasukkan Kode Alat yang ingin dikembalikan: ").strip()
        detail_terpilih = trx.cari_detail(kode_alat)

        if not detail_terpilih:
            print("[X] Alat tersebut tidak ada dalam transaksi ini.")
            return
        if detail_terpilih.status_dikembalikan:
            print("[!] Alat ini sudah dikembalikan sebelumnya.")
            return

        print("\nPilih Kondisi Alat Saat Dikembalikan:")
        print("1. Baik")
        print("2. Rusak Ringan")
        print("3. Rusak Berat")
        opsi_kondisi = input("Pilihan (1/2/3): ").strip()
        map_kondisi = {"1": "Baik", "2": "Rusak Ringan", "3": "Rusak Berat"}
        kondisi_akhir = map_kondisi.get(opsi_kondisi, "Baik")

        tgl_sekarang = date.today()
        detail_terpilih.proses_kembali(kondisi_akhir, tgl_sekarang)

        # Hitung keterlambatan
        terlambat = trx.hitung_terlambat(tgl_sekarang)
        if terlambat > 0:
            print(f"[!] PERHATIAN: Pengembalian terlambat {terlambat} hari dari batas waktu!")

        status_terbaru = trx.cek_status_transaksi()
        print(f"[V] Pengembalian berhasil dicatat!")
        print(f"Status Transaksi Saat Ini: {status_terbaru}")

    def cari_transaksi(self, id_transaksi: str) -> Transaksi:
        for trx in self.data_transaksi:
            if trx.id_transaksi == id_transaksi:
                return trx
        print("[X] ID Transaksi tidak ditemukan.")
        return None

    # --- LAPORAN & RIWAYAT ---
    def laporan_alat_tersedia(self):
        print("\n--- Laporan Alat Tersedia ---")
        tersedia = [a for a in self.data_alat.values() if a.tersedia]
        if not tersedia:
            print("Tidak ada alat yang tersedia saat ini.")
            return
        for a in tersedia:
            print(f"[{a.kode_alat}] {a.nama_alat} | Kategori: {a.kategori} | Kondisi: {a.kondisi}")

    def laporan_alat_dipinjam(self):
        print("\n--- Laporan Alat yang Sedang Dipinjam ---")
        dipinjam = []
        for trx in self.data_transaksi:
            if trx.status != "Selesai":
                for detail in trx.daftar_detail:
                    if not detail.status_dikembalikan:
                        dipinjam.append((detail.alat, trx.mahasiswa.nama, trx.id_transaksi))

        if not dipinjam:
            print("Tidak ada alat yang sedang dipinjam saat ini.")
            return
        for alat, peminjam, id_trx in dipinjam:
            print(f"[{alat.kode_alat}] {alat.nama_alat} | Dipinjam oleh: {peminjam} (ID: {id_trx})")

    def laporan_alat_rusak(self):
        print("\n--- Laporan Alat Rusak ---")
        rusak = [a for a in self.data_alat.values() if a.kondisi in ["Rusak Ringan", "Rusak Berat"]]
        if not rusak:
            print("Tidak ada alat yang rusak saat ini.")
            return
        for a in rusak:
            print(f"[{a.kode_alat}] {a.nama_alat} | Kondisi: {a.kondisi} | Status Tersedia: {a.tersedia}")

    def riwayat_peminjaman_mahasiswa(self, nim: str = None):
        if not nim:
            nim = input("Masukkan NIM Mahasiswa: ").strip()
        mhs = self.data_mahasiswa.get(nim)
        if not mhs:
            print("[X] Data mahasiswa tidak ditemukan.")
            return

        print(f"\n--- Riwayat Peminjaman: {mhs.nama} ({mhs.nim}) ---")
        riwayat = [t for t in self.data_transaksi if t.mahasiswa.nim == nim]
        if not riwayat:
            print("Belum ada riwayat transaksi peminjaman.")
            return

        for trx in riwayat:
            print(f"\nID Transaksi : {trx.id_transaksi}")
            print(f"Tgl Pinjam   : {trx.tanggal_pinjam} | Batas Kembali: {trx.batas_kembali}")
            print(f"Status       : {trx.status}")
            print("Item Dipinjam:")
            for d in trx.daftar_detail:
                st = f"Dikembalikan tgl {d.tanggal_kembali} [{d.kondisi_kembali}]" if d.status_dikembalikan else "Belum dikembalikan"
                print(f" - {d.alat.nama_alat} : {st}")

    # --- MENU UTAMA PROGRAM ---
    def menu_utama(self):
        while True:
            print("\n==============================================")
            print("    SISTEM LAB PEMINJAMAN PERALATAN (OOP)     ")
            print("==============================================")
            print("1.  Kelola Data Mahasiswa (Tambah/Edit/Hapus/Cari)")
            print("2.  Kelola Data Alat (Tambah/Edit/Hapus/Cari)")
            print("3.  Buat Transaksi Peminjaman")
            print("4.  Proses Pengembalian Alat")
            print("5.  Cari Transaksi")
            print("6.  Tampilkan Alat yang Tersedia")
            print("7.  Tampilkan Alat yang Sedang Dipinjam")
            print("8.  Tampilkan Alat yang Rusak")
            print("9.  Tampilkan Riwayat Peminjaman Mahasiswa")
            print("0.  Keluar dari Program")
            print("==============================================")
            pilihan = input("Pilih menu (0-9): ").strip()

            if pilihan == "1":
                print("\n[ Submenu Mahasiswa ]")
                print("a. Tambah | b. Edit | c. Hapus | d. Cari")
                sub = input("Pilih: ").lower()
                if sub == 'a': self.tambah_mahasiswa()
                elif sub == 'b': self.edit_mahasiswa()
                elif sub == 'c': self.hapus_mahasiswa()
                elif sub == 'd': self.cari_mahasiswa(input("NIM: "))
            elif pilihan == "2":
                print("\n[ Submenu Alat ]")
                print("a. Tambah | b. Edit | c. Hapus | d. Cari")
                sub = input("Pilih: ").lower()
                if sub == 'a': self.tambah_alat()
                elif sub == 'b': self.edit_alat()
                elif sub == 'c': self.hapus_alat()
                elif sub == 'd': self.cari_alat(input("Kode Alat: "))
            elif pilihan == "3":
                self.buat_transaksi_peminjaman()
            elif pilihan == "4":
                self.proses_pengembalian_alat()
            elif pilihan == "5":
                id_t = input("Masukkan ID Transaksi: ").strip()
                t = self.cari_transaksi(id_t)
                if t:
                    print(f"ID: {t.id_transaksi} | Peminjam: {t.mahasiswa.nama} | Status: {t.status}")
            elif pilihan == "6":
                self.laporan_alat_tersedia()
            elif pilihan == "7":
                self.laporan_alat_dipinjam()
            elif pilihan == "8":
                self.laporan_alat_rusak()
            elif pilihan == "9":
                self.riwayat_peminjaman_mahasiswa()
            elif pilihan == "0":
                print("\nTerima kasih telah menggunakan Sistem Peminjaman Laboratorium.")
                break
            else:
                print("\n[X] Pilihan menu tidak valid!")