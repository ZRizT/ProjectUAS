import json
import os
import re
from abc import ABC, abstractmethod

# --- OOP CONCEPT ---

class Person(ABC):
    def __init__(self, nama, email):
        self.nama = nama
        self.email = email

    @abstractmethod
    def display_info(self):
        pass

class Student(Person):
    def __init__(self, nim, nama, email, jurusan, ipk):
        super().__init__(nama, email)
        self.__nim = nim       # Encapsulation
        self.jurusan = jurusan
        self.__ipk = ipk       # Encapsulation

    def get_nim(self):
        return self.__nim

    def get_ipk(self):
        return self.__ipk

    def set_ipk(self, new_ipk):
        if 0.0 <= new_ipk <= 4.0:
            self.__ipk = new_ipk
        else:
            raise ValueError("IPK harus antara 0.0 dan 4.0")

    def display_info(self):
        return f"{self.nama} ({self.__nim}) - {self.jurusan}"

    def to_dict(self):
        return {
            "nim": self.__nim,
            "nama": self.nama,
            "email": self.email,
            "jurusan": self.jurusan,
            "ipk": self.__ipk
        }

# --- DATA MANAGER ---

class StudentManager:
    def __init__(self, filename="data_mahasiswa.json"):
        self.filename = filename
        self.students = []
        self.load_data()

    def load_data(self):
        if not os.path.exists(self.filename):
            self.save_data()
        try:
            with open(self.filename, "r") as f:
                data = json.load(f)
                self.students = [Student(**item) for item in data]
        except:
            self.students = []

    def save_data(self):
        data = [s.to_dict() for s in self.students]
        with open(self.filename, "w") as f:
            json.dump(data, f, indent=4)

    def add_student(self, student):
        for s in self.students:
            if s.get_nim() == student.get_nim():
                raise ValueError("NIM sudah terdaftar!")
        self.students.append(student)
        self.save_data()

    def delete_student(self, nim):
        original = len(self.students)
        self.students = [s for s in self.students if s.get_nim() != nim]
        if len(self.students) == original:
            raise ValueError("Data tidak ditemukan")
        self.save_data()

    def get_all_data(self):
        return [s.to_dict() for s in self.students]