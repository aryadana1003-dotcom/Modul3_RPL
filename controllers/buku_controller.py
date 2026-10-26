# Aryadana Agung Karama F5212510013
import tkinter.messagebox as messagebox
from models.buku_model import BukuModel
from views.buku_view import BukuView

class BukuController:
    def __init__(self):
        # Inisialisasi Model dan View
        self.model = BukuModel()
        self.view = BukuView()
        
        # Binding (mengikat) tombol di View dengan fungsi di Controller
        self.view.btn_simpan.configure(command=self.simpan_data)
        
        # Memuat data ke tabel saat aplikasi pertama kali dijalankan
        self.muat_data_tabel()
        
    def muat_data_tabel(self):
        # Mengosongkan isi tabel di view terlebih dahulu
        for item in self.view.table.get_children():
            self.view.table.delete(item)
            
        # Mengambil data buku dari Database
        data_buku = self.model.get_all_buku()
        
        # Memasukkan data baru ke dalam tabel View
        for buku in data_buku:
            self.view.table.insert("", "end", values=(buku['id_buku'], buku['judul'], buku['penulis'], buku['tahun_terbit']))
            
    def simpan_data(self):
        # Mengambil teks dari inputan di View
        judul = self.view.entry_judul.get()
        penulis = self.view.entry_penulis.get()
        tahun = self.view.entry_tahun.get()
        
        # Validasi Form kosong
        if not judul or not penulis or not tahun:
            messagebox.showwarning("Peringatan", "Semua kolom form harus diisi!")
            return
            
        # Mengirim data ke Model untuk disimpan
        berhasil = self.model.create_buku(judul, penulis, tahun)
        
        if berhasil:
            messagebox.showinfo("Sukses", "Data buku berhasil disimpan!")
            # Bersihkan form input
            self.view.entry_judul.delete(0, 'end')
            self.view.entry_penulis.delete(0, 'end')
            self.view.entry_tahun.delete(0, 'end')
            # Muat ulang tabel agar selalu terbaru
            self.muat_data_tabel()
        else:
            messagebox.showerror("Error", "Terjadi kesalahan saat menyimpan data.")
            
    def run(self):
        self.view.mainloop()