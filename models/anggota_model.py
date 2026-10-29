# Aryadana Agung Karama F5212510013

from config.database import Database

class AnggotaModel:
    def __init__(self):
        # Membuat koneksi ke database
        self.db = Database()
        self.conn = self.db.get_connection()
        self.table_name = "anggota"

    def get_all_anggota(self):
        # Mengambil seluruh data anggota.
        if not self.conn:
            return []

        cursor = None

        try:
            cursor = self.conn.cursor(dictionary=True)

            query = f"SELECT * FROM {self.table_name}"
            cursor.execute(query)

            result = cursor.fetchall()
            return result

        except Exception as error:
            print(f"Gagal mengambil data anggota: {error}")
            return []

        finally:
            if cursor is not None:
                cursor.close()

    def create_anggota(self, nama, alamat):
        # Menambahkan data anggota baru.
        if not self.conn:
            return False

        cursor = None

        try:
            cursor = self.conn.cursor()

            query = (
                f"INSERT INTO {self.table_name} (nama, alamat) "
                "VALUES (%s, %s)"
            )

            cursor.execute(query, (nama, alamat))
            self.conn.commit()

            return cursor.rowcount > 0

        except Exception as error:
            self.conn.rollback()
            print(f"Gagal menambahkan anggota: {error}")
            return False

        finally:
            if cursor is not None:
                cursor.close()

    
    def update_anggota(self, id_anggota, nama, alamat):
        # Memperbarui data anggota berdasarkan ID.

        if not self.conn:
            return False

        cursor = None

        try:
            cursor = self.conn.cursor()

            query = (
                "UPDATE anggota "
                "SET nama = %s, alamat = %s "
                "WHERE id_anggota = %s"
            )

            cursor.execute(
                query,
                (nama, alamat, id_anggota)
            )

            jumlah_diubah = cursor.rowcount
            self.conn.commit()

            # Jika ada data yang berubah, pembaruan berhasil
            if jumlah_diubah > 0:
                return True

            # Jika tidak ada perubahan, periksa apakah ID-nya ada
            cursor.execute(
                "SELECT id_anggota FROM anggota "
                "WHERE id_anggota = %s",
                (id_anggota,)
            )

            data_anggota = cursor.fetchone()

            # ID ditemukan berarti data anggota memang ada
            return data_anggota is not None

        except Exception as error:
            self.conn.rollback()
            print(f"Gagal memperbarui anggota: {error}")
            return False

        finally:
            if cursor is not None:
                cursor.close()

    def delete_anggota(self, id_anggota):
        # Menghapus data anggota berdasarkan ID.
        if not self.conn:
            return False

        cursor = None

        try:
            cursor = self.conn.cursor()

            query = (
                f"DELETE FROM {self.table_name} "
                "WHERE id_anggota = %s"
            )

            cursor.execute(query, (id_anggota,))
            self.conn.commit()

            return cursor.rowcount > 0

        except Exception as error:
            self.conn.rollback()
            print(f"Gagal menghapus anggota: {error}")
            return False

        finally:
            if cursor is not None:
                cursor.close()
