# Aryadana Agung Karama F5212510013

from unittest.mock import MagicMock, patch
from models.buku_model import BukuModel


def test_create_buku_berhasil():
    # Membuat koneksi database tiruan
    mock_connection = MagicMock()
    mock_cursor = MagicMock()

    mock_connection.cursor.return_value = mock_cursor

    # Mencegah koneksi ke MySQL asli
    with patch("models.buku_model.Database") as mock_database:
        mock_database.return_value.get_connection.return_value = (
            mock_connection
        )

        # Membuat Model
        model = BukuModel()

        # Menjalankan fungsi tambah buku
        hasil = model.create_buku(
            "Buku Testing",
            "Penulis QA",
            2026
        )

        # Memastikan fungsi berhasil
        assert hasil is True

        # Memastikan query dijalankan
        mock_cursor.execute.assert_called_once()

        # Memastikan perubahan disimpan
        mock_connection.commit.assert_called_once()


def test_get_all_buku_berhasil():
    # Menyiapkan data buku tiruan
    data_dummy = [
        {
            "id_buku": 1,
            "judul": "Pemrograman Python",
            "penulis": "Guido van Rossum",
            "tahun_terbit": 2023
        },
        {
            "id_buku": 2,
            "judul": "Belajar Database",
            "penulis": "Abdul Kadir",
            "tahun_terbit": 2024
        }
    ]

    # Membuat objek tiruan
    mock_cursor = MagicMock()
    mock_cursor.fetchall.return_value = data_dummy

    mock_connection = MagicMock()
    mock_connection.cursor.return_value = mock_cursor

    # Menggantikan Database asli dengan objek tiruan
    with patch("models.buku_model.Database") as mock_database:
        mock_database.return_value.get_connection.return_value = (
            mock_connection
        )

        # Membuat Model dan mengambil seluruh data buku
        model = BukuModel()
        hasil = model.get_all_buku()

        # Memastikan hasil sesuai dengan data yang disiapkan
        assert hasil == data_dummy

        # Memastikan cursor dibuat dalam mode dictionary
        mock_connection.cursor.assert_called_once_with(
            dictionary=True
        )

        # Memastikan query SELECT dijalankan
        mock_cursor.execute.assert_called_once_with(
            "SELECT * FROM buku"
        )

        # Memastikan cursor ditutup
        mock_cursor.close.assert_called_once()
