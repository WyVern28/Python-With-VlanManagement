# Program Manajemen VLAN Cisco Nexus 9000

Program berbasis Python untuk melakukan manajemen VLAN secara otomatis pada perangkat jaringan Cisco Nexus 9000 melalui Sandbox.

## Deskripsi

Program ini berfungsi sebagai Client Interface yang menghubungkan pengguna dengan Cisco Nexus Sandbox (Switch virtual Cisco yang tersedia di cloud) untuk melakukan operasi CRUD (Create, Read, Update, Delete) pada konfigurasi VLAN.

## Fitur Utama

### Operasi CRUD VLAN

| Operasi | Fungsi Python | Perintah Jaringan |
|---------|---------------|-------------------|
| **Create** | `create_vlan(vlan_id, vlan_name)` | `vlan [ID], name [NAMA]` |
| **Read** | `get_vlan_info(vlan_id=None)` | `show vlan brief` atau `show running-config` |
| **Update** | `update_vlan_port(vlan_id, interface, mode='access')` | `interface [INT], switchport access vlan [ID]` |
| **Delete** | `delete_vlan(vlan_id)` | `no vlan [ID]` |

### Fitur Bonus

- **Export to CSV**: Mengekspor daftar VLAN ke file CSV untuk dokumentasi dan analisis

## Struktur File

```
TR_AST_DPJ/
├── main.py              # Menu utama dan interaksi dengan user
├── cisco_api.py         # Fungsi-fungsi untuk request API (CRUD VLAN)
├── config.py            # Konfigurasi koneksi ke Cisco Nexus Sandbox
├── requirements.txt     # Dependencies Python
└── README.md            # Dokumentasi program
```

## Instalasi

### Prasyarat

- Python 3.7 atau lebih tinggi
- Koneksi internet untuk mengakses Cisco Nexus Sandbox
- pip (Python package manager)

### Langkah Instalasi

1. Clone atau download repository ini

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Pastikan file `config.py` memiliki kredensial yang benar untuk Cisco Nexus Sandbox

## Cara Menggunakan

### Menjalankan Program

```bash
python main.py
```

### Menu Utama

Program memiliki menu utama dengan pilihan:

```
Cisco NX-API Menu
============================
1.  Read
2.  Create/Update
3.  Delete
4.  Export to CSV
5.  Exit
============================
```

### 1. Menu Read

Submenu untuk melihat informasi VLAN:

- **Show All**: Menampilkan semua VLAN dengan ID, Name, dan Status
- **Show Vlan-name**: Menampilkan VLAN berdasarkan nama
- **Show Vlan-id**: Menampilkan VLAN berdasarkan ID
- **Count vlans**: Menghitung total VLAN yang terdaftar

### 2. Menu Create/Update

Untuk membuat VLAN baru:

1. Pilih opsi 2 dari menu utama
2. Masukkan VLAN ID (1-4094)
3. Masukkan VLAN Name
4. Program akan membuat VLAN baru dengan ID dan nama yang diberikan

### 3. Menu Delete

Untuk menghapus VLAN:

1. Pilih opsi 3 dari menu utama
2. Program akan menampilkan semua VLAN yang ada
3. Masukkan ID VLAN yang ingin dihapus
4. Konfirmasi penghapusan

### 4. Export to CSV

Fitur bonus untuk mengekspor data VLAN:

1. Pilih opsi 4 dari menu utama
2. Masukkan nama file (tanpa ekstensi .csv)
3. File CSV akan disimpan di direktori yang sama dengan program

## Konfigurasi

File `config.py` berisi konfigurasi koneksi ke Cisco Nexus Sandbox:

```python
NEXUS_HOST = "sandbox-nxos-1.cisco.com"
NEXUS_PORT = 443
NEXUS_USERNAME = "admin"
NEXUS_PASSWORD = "Admin_1234!"
```

**Catatan**: Kredensial di atas adalah default untuk Cisco DevNet Sandbox. Sesuaikan dengan kredensial yang Anda miliki.

## Teknologi yang Digunakan

- **Python 3**: Bahasa pemrograman utama
- **requests**: Library untuk HTTP requests ke NX-API
- **urllib3**: Untuk handling SSL/TLS connections
- **csv**: Untuk export data ke format CSV
- **Cisco NX-API**: REST API dari Cisco Nexus untuk manajemen perangkat

## Troubleshooting

### Gagal Koneksi

Jika mendapat error koneksi:
1. Pastikan Cisco Nexus Sandbox dapat diakses
2. Periksa kredensial di `config.py`
3. Pastikan koneksi internet stabil

### SSL Certificate Error

Program sudah dikonfigurasi untuk menonaktifkan SSL verification (cocok untuk sandbox environment). Jika menggunakan di production, enable SSL verification di `config.py`.

### VLAN ID Invalid

- VLAN ID harus antara 1-4094
- Beberapa VLAN ID reserved untuk sistem (1, 1002-1005)

## Contoh Penggunaan

### Membuat VLAN Baru

```
Enter your choice (1-5) : 2
Authentication successful!
Enter VLAN ID   : 100
Enter VLAN Name : VLAN_IT
Successfully created VLAN 100 with name 'VLAN_IT'
```

### Melihat Semua VLAN

```
Enter your choice (1-5) : 1
Enter options    : 1

Daftar Semua VLAN:
------------------------------------------------------------
VLAN ID         Name                           Status
------------------------------------------------------------
1               default                        active
100             VLAN_IT                        active
125             VLAN125                        active
------------------------------------------------------------
```

### Menghapus VLAN

```
Enter your choice (1-5) : 3
List all VLAN:
[daftar VLAN ditampilkan]

Enter the ID you want to delete: 100
Apakah Anda yakin ingin menghapus VLAN 100? (y/n): y
Successfully deleted VLAN 100
```

## Catatan Penting

1. Program ini menggunakan Cisco NX-API yang merupakan REST API dari Cisco Nexus
2. Pastikan device mendukung NX-API (Cisco Nexus 9000 series)
3. Beberapa VLAN (seperti VLAN 1) adalah default VLAN dan tidak bisa dihapus
4. Selalu backup konfigurasi sebelum melakukan perubahan pada production environment

## Lisensi

Program ini dibuat untuk keperluan tugas akademik TR ASDOS DPJ H.

## Kontributor

[Nama Kelompok dan Anggota]

---

**Selamat Berkarya, Tuhan Memberkati**
