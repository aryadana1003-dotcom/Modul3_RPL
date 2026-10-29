import tkinter.messagebox as messagebox

from models.anggota_model import AnggotaModel
from views.anggota_view import AnggotaView


class AnggotaController:
    def __init__(self):
        # Inisialisasi Model dan View
        self.model = AnggotaModel()
        self.view = AnggotaView()

        # Hubungkan tombol simpan
        self.view.btn_simpan.configure(
            command=self.simpan_data
        )

        # Hubungkan tabel dengan fungsi pemilihan data
        self.view.table.bind(
            "<<TreeviewSelect>>",
            self.pilih_data
        )

        # Hubungkan tombol tambahan jika tersedia
        # dan Model sudah memiliki metodenya
        if (
            hasattr(self.view, "btn_update")
            and callable(getattr(self.model, "update_anggota", None))
        ):
            self.view.btn_update.configure(
                command=self.perbarui_data
            )

        if (
            hasattr(self.view, "btn_hapus")
            and callable(getattr(self.model, "delete_anggota", None))
        ):
            self.view.btn_hapus.configure(
                command=self.hapus_data
            )

        self.muat_data_tabel()

    def muat_data_tabel(self):
        # Mengambil data anggota dan menampilkannya di tabel."""

        for item in self.view.table.get_children():
            self.view.table.delete(item)

        data_anggota = self.model.get_all_anggota()

        for anggota in data_anggota:
            self.view.table.insert(
                "",
                "end",
                values=(
                    anggota["id_anggota"],
                    anggota["nama"],
                    anggota["alamat"]
                )
            )

    def ambil_baris_terpilih(self):
        # Mengambil baris anggota yang dipilih.

        selected = self.view.table.selection()

        if not selected:
            return None

        return self.view.table.item(
            selected[0], "values"
        )

    def pilih_data(self, event=None):
        # Menampilkan data anggota terpilih ke form.

        data = self.ambil_baris_terpilih()

        if not data:
            return

        self.view.entry_nama.delete(0, "end")
        self.view.entry_nama.insert(0, data[1])

        self.view.entry_alamat.delete(0, "end")
        self.view.entry_alamat.insert(0, data[2])

    def ambil_data_form(self):
        # Mengambil dan memvalidasi input anggota.

        nama = self.view.entry_nama.get().strip()
        alamat = self.view.entry_alamat.get().strip()

        if not nama or not alamat:
            messagebox.showwarning(
                "Peringatan",
                "Nama dan alamat anggota harus diisi!"
            )
            return None

        return nama, alamat

    def bersihkan_form(self):
        # Mengosongkan form anggota.

        self.view.entry_nama.delete(0, "end")
        self.view.entry_alamat.delete(0, "end")

    def simpan_data(self):
        # Menyimpan anggota baru ke database. 

        data = self.ambil_data_form()

        if data is None:
            return

        nama, alamat = data

        berhasil = self.model.create_anggota(
            nama, alamat
        )

        if berhasil:
            messagebox.showinfo(
                "Sukses",
                "Data anggota berhasil disimpan!"
            )
            self.bersihkan_form()
            self.muat_data_tabel()
        else:
            messagebox.showerror(
                "Error",
                "Data anggota gagal disimpan."
            )

    def perbarui_data(self):
        # Memperbarui anggota yang dipilih.

        data_terpilih = self.ambil_baris_terpilih()

        if not data_terpilih:
            messagebox.showwarning(
                "Peringatan",
                "Pilih anggota yang ingin diperbarui!"
            )
            return

        data_form = self.ambil_data_form()

        if data_form is None:
            return

        id_anggota = int(data_terpilih[0])
        nama, alamat = data_form

        berhasil = self.model.update_anggota(
            id_anggota, nama, alamat
        )

        if berhasil:
            messagebox.showinfo(
                "Sukses",
                "Data anggota berhasil diperbarui!"
            )
            self.bersihkan_form()
            self.muat_data_tabel()
        else:
            messagebox.showerror(
                "Error",
                "Data anggota gagal diperbarui."
            )

    def hapus_data(self):
        # Menghapus anggota yang dipilih.

        data_terpilih = self.ambil_baris_terpilih()

        if not data_terpilih:
            messagebox.showwarning(
                "Peringatan",
                "Pilih anggota yang ingin dihapus!"
            )
            return

        id_anggota = int(data_terpilih[0])

        konfirmasi = messagebox.askyesno(
            "Konfirmasi",
            f"Hapus data anggota ID {id_anggota}?"
        )

        if not konfirmasi:
            return

        berhasil = self.model.delete_anggota(id_anggota)

        if berhasil:
            messagebox.showinfo(
                "Sukses",
                "Data anggota berhasil dihapus!"
            )
            self.bersihkan_form()
            self.muat_data_tabel()
        else:
            messagebox.showerror(
                "Error",
                "Data anggota gagal dihapus."
            )

    def run(self):
        self.view.mainloop()