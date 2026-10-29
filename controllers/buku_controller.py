# # Aryadana Agung Karama F5212510013

import tkinter.messagebox as messagebox

from models.buku_model import BukuModel
from views.buku_view import BukuView


class BukuController:
    def __init__(self):
        # Inisialisasi Model dan View
        self.model = BukuModel()
        self.view = BukuView()

        # Hubungkan tombol dengan fungsi Controller
        self.view.btn_simpan.configure(
            command=self.simpan_data
        )
        self.view.btn_update.configure(
            command=self.perbarui_data
        )
        self.view.btn_hapus.configure(
            command=self.hapus_data
        )

        # Ketika baris tabel dipilih, tampilkan datanya di form
        self.view.table.bind(
            "<<TreeviewSelect>>",
            self.pilih_data
        )

        # Tampilkan data buku dari database
        self.muat_data_tabel()

    def muat_data_tabel(self):
        # Mengambil data dari Model dan menampilkannya di tabel.

        # Bersihkan isi tabel terlebih dahulu
        for item in self.view.table.get_children():
            self.view.table.delete(item)

        data_buku = self.model.get_all_buku()

        for buku in data_buku:
            self.view.table.insert(
                "",
                "end",
                values=(
                    buku["id_buku"],
                    buku["judul"],
                    buku["penulis"],
                    buku["tahun_terbit"]
                )
            )

    def ambil_baris_terpilih(self):
        # Mengambil data baris yang dipilih pengguna.

        selected = self.view.table.selection()

        if not selected:
            return None

        return self.view.table.item(
            selected[0], "values"
        )

    def pilih_data(self, event=None):
        # Memindahkan data dari tabel ke form input.

        data = self.ambil_baris_terpilih()

        if not data:
            return

        # Indeks 0 = ID, 1 = Judul, 2 = Penulis, 3 = Tahun
        self.view.entry_judul.delete(0, "end")
        self.view.entry_judul.insert(0, data[1])

        self.view.entry_penulis.delete(0, "end")
        self.view.entry_penulis.insert(0, data[2])

        self.view.entry_tahun.delete(0, "end")
        self.view.entry_tahun.insert(0, data[3])

    def ambil_data_form(self):
        # Membaca dan memvalidasi data dari form.

        judul = self.view.entry_judul.get().strip()
        penulis = self.view.entry_penulis.get().strip()
        tahun = self.view.entry_tahun.get().strip()

        if not judul or not penulis or not tahun:
            messagebox.showwarning(
                "Peringatan",
                "Semua kolom form harus diisi!"
            )
            return None

        try:
            tahun = int(tahun)
        except ValueError:
            messagebox.showwarning(
                "Peringatan",
                "Tahun terbit harus berupa angka!"
            )
            return None

        return judul, penulis, tahun

    def bersihkan_form(self):
        # Mengosongkan seluruh form input.

        self.view.entry_judul.delete(0, "end")
        self.view.entry_penulis.delete(0, "end")
        self.view.entry_tahun.delete(0, "end")

    def simpan_data(self):
        # Menyimpan data buku baru.

        data = self.ambil_data_form()

        if data is None:
            return

        judul, penulis, tahun = data
        berhasil = self.model.create_buku(
            judul, penulis, tahun
        )

        if berhasil:
            messagebox.showinfo(
                "Sukses",
                "Data buku berhasil disimpan!"
            )
            self.bersihkan_form()
            self.muat_data_tabel()
        else:
            messagebox.showerror(
                "Error",
                "Data buku gagal disimpan."
            )

    def perbarui_data(self):
        # Memperbarui buku yang dipilih dari tabel.

        data_terpilih = self.ambil_baris_terpilih()

        if not data_terpilih:
            messagebox.showwarning(
                "Peringatan",
                "Pilih baris buku yang ingin diperbarui!"
            )
            return

        data_form = self.ambil_data_form()

        if data_form is None:
            return

        # ID diambil dari baris tabel yang dipilih
        id_buku = int(data_terpilih[0])
        judul, penulis, tahun = data_form

        berhasil = self.model.update_buku(
            id_buku, judul, penulis, tahun
        )

        if berhasil:
            messagebox.showinfo(
                "Sukses",
                "Data buku berhasil diperbarui!"
            )
            self.bersihkan_form()
            self.muat_data_tabel()
        else:
            messagebox.showwarning(
                "Peringatan",
                "Data tidak ditemukan atau tidak mengalami perubahan."
            )

    def hapus_data(self):
        # Menghapus buku yang dipilih dari tabel.

        data_terpilih = self.ambil_baris_terpilih()

        if not data_terpilih:
            messagebox.showwarning(
                "Peringatan",
                "Pilih baris buku yang ingin dihapus!"
            )
            return

        # Ambil id_buku dari kolom pertama tabel
        id_buku = int(data_terpilih[0])

        konfirmasi = messagebox.askyesno(
            "Konfirmasi",
            f"Apakah kamu yakin ingin menghapus buku ID {id_buku}?"
        )

        if not konfirmasi:
            return

        berhasil = self.model.delete_buku(id_buku)

        if berhasil:
            messagebox.showinfo(
                "Sukses",
                "Data buku berhasil dihapus!"
            )
            self.bersihkan_form()
            self.muat_data_tabel()
        else:
            messagebox.showerror(
                "Error",
                "Data buku gagal dihapus."
            )

    def run(self):
        self.view.mainloop()