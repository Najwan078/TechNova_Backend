import re

# 1. Base Class (Superclass)
class Person:
    def __init__(self, nama):
        self._nama = nama  # Protected attribute (Enkapsulasi)

    # Polimorfisme: Method ini akan di-override di subclass
    def to_dict(self):
        return {"nama": self._nama}

# 2. Subclass (Pewarisan)
class Student(Person):
    def __init__(self, nim, nama, jurusan, semester, status, ipk):
        super().__init__(nama)
        self.__nim = nim  # Private attribute (Enkapsulasi ketat)
        self.jurusan = jurusan
        self.semester = semester
        self.status = status
        self.ipk = float(ipk)

    # Getter untuk property private
    def get_nim(self):
        return self.__nim

    # Polimorfisme: Overriding method dari Person
    def to_dict(self):
        data = super().to_dict()
        data.update({
            "nim": self.__nim,
            "jurusan": self.jurusan,
            "semester": self.semester,
            "status": self.status,
            "ipk": self.ipk
        })
        return data

    # Validasi Input menggunakan Regex
    @staticmethod
    def validasi_input(nim, nama):
        # NIM harus berawalan 2 huruf kapital diikuti 8 angka (misal: IT12345678)
        if not re.match(r"^[A-Z]{2}\d{8}$", nim):
            raise ValueError("Format NIM tidak valid! (Contoh: IT12345678)")
        # Nama hanya boleh berisi huruf dan spasi
        if not re.match(r"^[A-Za-z\s]+$", nama):
            raise ValueError("Nama hanya boleh berisi huruf dan spasi!")
        return True