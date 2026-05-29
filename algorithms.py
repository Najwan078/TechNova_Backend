# --- ALGORITMA PENGURUTAN (SORTING) ---

# 1. Bubble Sort (Berdasarkan IPK Descending)
# Time Complexity: O(n^2) Worst case, O(n) Best case
def bubble_sort_ipk(data):
    """
    Mengurutkan data mahasiswa dengan membandingkan elemen yang bersebelahan.
    
    Estimasi Time Complexity:
    - Best Case: O(n) (Jika data sudah dalam keadaan terurut)
    - Worst/Average Case: O(n^2)
    """
    langkah = 0 # 🧮 Variabel penghitung dimulai
    n = len(data)
    for i in range(n):
        for j in range(0, n-i-1):
            langkah += 1 # 🧮 Tambah 1 setiap kali membandingkan data
            if data[j]['ipk'] < data[j+1]['ipk']:
                data[j], data[j+1] = data[j+1], data[j]
    return data, langkah # 🚀  Mengembalikan 2 nilai (data dan jumlah langkah)

# 2. Selection Sort (Berdasarkan NIM Ascending)
# Time Complexity: O(n^2) untuk semua kasus
def selection_sort_nim(data):
    """
    Mengurutkan data dengan mencari nilai minimum dari sisa array.
    
    Estimasi Time Complexity:
    - Best, Average, & Worst Case: O(n^2)
    """
    langkah = 0 # 🧮 Variabel penghitung dimulai
    n = len(data)
    for i in range(n):
        min_idx = i
        for j in range(i+1, n):
            langkah += 1 # 🧮 Tambah 1 setiap kali mencari nilai minimum
            if data[j]['nim'] < data[min_idx]['nim']:
                min_idx = j
        data[i], data[min_idx] = data[min_idx], data[i]
    return data, langkah


# --- ALGORITMA PENCARIAN (SEARCHING) ---

# 1. Linear Search (Mencari Nama)
# Time Complexity: O(n)
def linear_search_nama(data, target_nama):
    """
    Mencari mahasiswa berdasarkan Nama dengan mengecek satu per satu.
    
    Estimasi Time Complexity:
    - Best Case: O(1) (Jika target ada di urutan paling pertama)
    - Worst/Average Case: O(n)
    """
    langkah = 0 # 🧮 Variabel penghitung dimulai
    hasil = []
    target = target_nama.lower()
    for mhs in data:
        langkah += 1 # 🧮 Tambah 1 setiap kali mengecek nama mahasiswa
        if target in mhs['nama'].lower():
            hasil.append(mhs)
    return hasil, langkah

# 2. Binary Search (Mencari NIM Eksak)
# Time Complexity: O(log n)
def binary_search_nim(data, target_nim):
    """
    Mencari mahasiswa dengan membagi dua area pencarian pada data terurut.
    
    Estimasi Time Complexity:
    - Pencarian Inti (Binary Search): O(log n)
    - Persiapan Pengurutan (Selection Sort): O(n^2)
    """
    langkah_search = 0
    
    data_sorted, langkah_sort = selection_sort_nim(data.copy())
    
    low = 0
    high = len(data_sorted) - 1

    while low <= high:
        langkah_search += 1 # 🧮 Tambah 1 setiap kali membelah data
        mid = (low + high) // 2
        if data_sorted[mid]['nim'] == target_nim:
            return [data_sorted[mid]], langkah_search
        elif data_sorted[mid]['nim'] < target_nim:
            low = mid + 1
        else:
            high = mid - 1
    return [], langkah_search

# 3. Sequential Search (Linear Search) - Mencari berdasarkan Jurusan
# Time Complexity: O(n)
def sequential_search_jurusan(data, target_jurusan):
    """
    Mencari data mahasiswa secara berurutan (sekuensial) berdasarkan Jurusan.
    
    Estimasi Time Complexity:
    - Best Case: O(1) (Jika target ditemukan pada pengecekan pertama)
    - Worst/Average Case: O(n)
    """
    langkah = 0 # 🧮 Variabel penghitung dimulai
    hasil = []
    target = target_jurusan.lower()
    for mhs in data:
        langkah += 1 # 🧮 Tambah 1 setiap kali mengecek jurusan
        if target in mhs['jurusan'].lower():
            hasil.append(mhs)
    return hasil, langkah