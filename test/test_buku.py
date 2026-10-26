# Aryadana Agung Karama F5212510013
from unittest.mock import MagicMock
from models.buku_model import BukuModel

def test_create_buku_berhasil():
    # Menginisialisasi Model
    model = BukuModel()

    # Memanipulasi (Mock) koneksi database agar tidak mengotori data asli
    # Mocking akan menimpa self.conn yang tadinya None (jika MySQL mati) menjadi objek palsu
    model.conn = MagicMock()
    mock_cursor = MagicMock()
    model.conn.cursor.return_value = mock_cursor

    # Melakukan eksekusi fungsi yang ada di BukuModel
    # Pastikan parameter sesuai: judul, penulis, tahun_terbit
    hasil = model.create_buku("Buku Testing", "Penulis QA", 2026)

    # Memverifikasi apakah fungsi mengembalikan nilai True
    assert hasil is True
    
    # Memverifikasi apakah cursor.execute benar-benar dipanggil oleh fungsi create_buku
    mock_cursor.execute.assert_called_once()
    
    # Memverifikasi apakah perintah commit (simpan) dipanggil ke database
    model.conn.commit.assert_called_once()
    