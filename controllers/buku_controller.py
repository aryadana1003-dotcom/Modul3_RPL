# Aryadana Agung Karama F5212510013
import tkinter.messagebox as messagebox
from models.buku_model import BukuModel
from views.buku_view import BukuView

class BukuController:
    def __init__(self, user_role="anggota"):
        self.user_role = user_role
        self.model = BukuModel()
        self.view = BukuView()
        self.view.title(f"Sistem Manajemen Perpustakaan - Mode: {self.user_role.upper()}")
        
        # Variabel untuk melacak data mana yang sedang diklik di tabel
        self.id_buku_terpilih = None 
        
        self.view.btn_simpan.configure(command=self.simpan_data)
        if hasattr(self.view, 'btn_logout'):
            self.view.btn_logout.configure(command=self.logout)
            
        # Hubungkan event klik baris tabel dengan fungsi pilih_data
        if hasattr(self.view, 'tabel'):
            self.view.tabel.bind("<ButtonRelease-1>", self.pilih_data_tabel)
            
        # Hubungkan tombol update dan hapus
        if hasattr(self.view, 'btn_update'):
            self.view.btn_update.configure(command=self.update_data)
        if hasattr(self.view, 'btn_hapus'):
            self.view.btn_hapus.configure(command=self.hapus_data)
        
        # Otorisasi tombol Simpan, Update, dan Hapus
        if self.user_role != "admin":
            try:
                teks_terkunci = "Akses Terkunci (Khusus Admin)"
                self.view.btn_simpan.configure(state="disabled", text=teks_terkunci)
                self.view.btn_update.configure(state="disabled", text=teks_terkunci)
                self.view.btn_hapus.configure(state="disabled", text=teks_terkunci)
                
                self.view.entry_judul.configure(state="disabled")
                self.view.entry_penulis.configure(state="disabled")
                self.view.entry_tahun.configure(state="disabled")
            except Exception as e:
                pass
                
        self.muat_data_tabel()

    def muat_data_tabel(self):
        for item in self.view.tabel.get_children():
            self.view.tabel.delete(item)
        data_buku = self.model.get_all_buku()
        for buku in data_buku:
            self.view.tabel.insert("", "end", values=(buku["id_buku"], buku["judul"], buku["penulis"], buku["tahun_terbit"]))

    def simpan_data(self):
        # Proteksi di controller
        if self.user_role != "admin":
            messagebox.showerror("Akses Ditolak", "Anda tidak memiliki izin untuk menambah data!")
            return

        judul = self.view.entry_judul.get()
        penulis = self.view.entry_penulis.get()
        tahun = self.view.entry_tahun.get()

        if not judul or not penulis or not tahun:
            messagebox.showwarning("Peringatan", "Semua kolom form harus diisi!")
            return

        if self.model.create_buku(judul, penulis, tahun):
            messagebox.showinfo("Sukses", "Data buku berhasil disimpan!")
            self.view.entry_judul.delete(0, 'end')
            self.view.entry_penulis.delete(0, 'end')
            self.view.entry_tahun.delete(0, 'end')
            self.muat_data_tabel()
        else:
            messagebox.showerror("Error", "Gagal menyimpan data.")

    def pilih_data_tabel(self, event):
        # Abaikan jika bukan admin karena formnya terkunci
        if self.user_role != "admin":
            return
            
        item_terpilih = self.view.tabel.selection()
        if item_terpilih:
            item = self.view.tabel.item(item_terpilih)
            nilai = item['values']

            self.id_buku_terpilih = nilai[0] # Simpan ID Buku

            # Tampilkan data ke form
            self.view.entry_judul.delete(0, 'end')
            self.view.entry_judul.insert(0, nilai[1])
            
            self.view.entry_penulis.delete(0, 'end')
            self.view.entry_penulis.insert(0, nilai[2])
            
            self.view.entry_tahun.delete(0, 'end')
            self.view.entry_tahun.insert(0, str(nilai[3]))

    def update_data(self):
        if self.user_role != "admin":
            return

        if not self.id_buku_terpilih:
            messagebox.showwarning("Peringatan", "Pilih data di tabel terlebih dahulu!")
            return

        judul = self.view.entry_judul.get()
        penulis = self.view.entry_penulis.get()
        tahun = self.view.entry_tahun.get()

        if not judul or not penulis or not tahun:
            messagebox.showwarning("Peringatan", "Form tidak boleh kosong!")
            return

        if self.model.update_buku(self.id_buku_terpilih, judul, penulis, tahun):
            messagebox.showinfo("Sukses", "Data buku berhasil diperbarui!")
            self.bersihkan_form()
            self.muat_data_tabel()
        else:
            messagebox.showerror("Error", "Gagal memperbarui data.")

    def hapus_data(self):
        if self.user_role != "admin":
            return

        if not self.id_buku_terpilih:
            messagebox.showwarning("Peringatan", "Pilih data di tabel terlebih dahulu!")
            return

        konfirmasi = messagebox.askyesno("Konfirmasi", "Yakin ingin menghapus data buku ini?")
        if konfirmasi:
            if self.model.delete_buku(self.id_buku_terpilih):
                messagebox.showinfo("Sukses", "Data buku berhasil dihapus!")
                self.bersihkan_form()
                self.muat_data_tabel()
            else:
                messagebox.showerror("Error", "Gagal menghapus data.")

    def bersihkan_form(self):
        self.id_buku_terpilih = None
        self.view.entry_judul.delete(0, 'end')
        self.view.entry_penulis.delete(0, 'end')
        self.view.entry_tahun.delete(0, 'end')
    
    def logout(self):
        # Tutup jendela utama perpustakaan
        self.view.destroy()
        
        # Panggil kembali jendela Login
        from controllers.auth_controller import AuthController
        app_login = AuthController()
        app_login.run()
    
    def run(self):
        self.view.mainloop()
