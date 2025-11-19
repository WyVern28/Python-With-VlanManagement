"""
Program Manajemen VLAN Cisco Nexus 9000
Main menu dan interface interaksi dengan user
"""

import os
import sys
import csv
from cisco_api import (
    test_authentication,
    create_vlan,
    get_all_vlans,
    get_vlan_by_id,
    get_vlan_by_name,
    update_vlan_port,
    delete_vlan,
    count_vlans
)


def clear_screen():
    """Membersihkan layar terminal"""
    os.system('cls' if os.name == 'nt' else 'clear')


def print_header(title):
    """Mencetak header menu"""
    print("=" * 30)
    print(title)
    print("=" * 30)


def display_vlan_table(vlans, show_mode='all'):
    """
    Menampilkan VLAN dalam format tabel

    Args:
        vlans: List dari VLAN
        show_mode: Mode tampilan ('all', 'id', 'name')
    """
    if not vlans:
        print("Tidak ada VLAN ditemukan")
        return

    print("\nDaftar Semua VLAN:")
    print("-" * 70)

    if show_mode == 'all':
        print(f"{'VLAN ID':<20} {'Name':<35} {'Status':<15}")
        print("-" * 70)
        for vlan in vlans:
            vlan_id = vlan.get('vlanshowbr-vlanid-utf', vlan.get('vlanshowbr-vlanid', 'N/A'))
            vlan_name = vlan.get('vlanshowbr-vlanname', 'N/A')
            status = vlan.get('vlanshowbr-vlanstate', 'N/A')
            print(f"{vlan_id:<20} {vlan_name:<35} {status:<15}")

    elif show_mode == 'name':
        print(f"{'VLAN Name':<35} {'State':<20} {'Shut state':<15}")
        print("-" * 70)
        for vlan in vlans:
            vlan_name = vlan.get('vlanshowbr-vlanname', 'N/A')
            state = vlan.get('vlanshowbr-vlanstate', 'N/A')
            shut_state = vlan.get('vlanshowbr-shutstate', 'N/A')
            print(f"{vlan_name:<35} {state:<20} {shut_state:<15}")

    elif show_mode == 'id':
        print(f"{'VLAN ID':<20} {'State':<20} {'Shut state':<15}")
        print("-" * 70)
        for vlan in vlans:
            vlan_id = vlan.get('vlanshowbr-vlanid-utf', vlan.get('vlanshowbr-vlanid', 'N/A'))
            state = vlan.get('vlanshowbr-vlanstate', 'N/A')
            shut_state = vlan.get('vlanshowbr-shutstate', 'N/A')
            print(f"{vlan_id:<20} {state:<20} {shut_state:<15}")

    print("-" * 70)


def export_vlan_to_csv():
    """Mengekspor daftar VLAN ke file CSV"""
    vlans = get_all_vlans()

    if not vlans:
        print("Tidak ada VLAN untuk diekspor")
        return

    filename = input("Masukkan nama file CSV (tanpa ekstensi): ").strip()
    if not filename:
        filename = "vlan_export"

    filename = f"{filename}.csv"

    try:
        with open(filename, 'w', newline='', encoding='utf-8') as csvfile:
            fieldnames = ['VLAN_ID', 'VLAN_Name', 'Status', 'Shut_State']
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

            writer.writeheader()
            for vlan in vlans:
                writer.writerow({
                    'VLAN_ID': vlan.get('vlanshowbr-vlanid-utf', ''),
                    'VLAN_Name': vlan.get('vlanshowbr-vlanname', ''),
                    'Status': vlan.get('vlanshowbr-vlanstate', ''),
                    'Shut_State': vlan.get('vlanshowbr-shutstate', '')
                })

        print(f"\nData VLAN berhasil diekspor ke {filename}")

    except Exception as e:
        print(f"Error saat mengekspor ke CSV: {e}")


def menu_read():
    """Menu untuk operasi Read VLAN"""
    while True:
        print_header("Interface Brief Menu")
        print("1.  Show All")
        print("2.  Show Vlan-name")
        print("3.  Show Vlan-id")
        print("4.  Count vlans")
        print("5.  Exit")
        print("=" * 30)

        choice = input("Enter options    : ").strip()

        if choice == '1':
            vlans = get_all_vlans()
            display_vlan_table(vlans, 'all')
            input("\nTekan Enter untuk melanjutkan...")

        elif choice == '2':
            print("\nDaftar VLAN Name:")
            vlans = get_all_vlans()
            display_vlan_table(vlans, 'name')
            input("\nTekan Enter untuk melanjutkan...")

        elif choice == '3':
            print("\nDaftar VLAN ID:")
            vlans = get_all_vlans()
            display_vlan_table(vlans, 'id')
            input("\nTekan Enter untuk melanjutkan...")

        elif choice == '4':
            total = count_vlans()
            print(f"\nThere are {total} VLAN connected")
            input("\nTekan Enter untuk melanjutkan...")

        elif choice == '5':
            break

        else:
            print("Pilihan tidak valid!")
            input("\nTekan Enter untuk melanjutkan...")


def menu_create_update():
    """Menu untuk operasi Create/Update VLAN"""
    print_header("Cisco NX-API Menu")
    print("1.  Read")
    print("2.  Create/Update")
    print("3.  Delete")
    print("4.  Exit")
    print("=" * 30)

    print("Enter your choice (1-4) : 2")

    if not test_authentication():
        print("Gagal melakukan autentikasi!")
        input("\nTekan Enter untuk melanjutkan...")
        return

    vlan_id = input("Enter VLAN ID   : ").strip()
    if not vlan_id.isdigit():
        print("VLAN ID harus berupa angka!")
        input("\nTekan Enter untuk melanjutkan...")
        return

    vlan_id = int(vlan_id)
    if vlan_id < 1 or vlan_id > 4094:
        print("VLAN ID harus antara 1-4094!")
        input("\nTekan Enter untuk melanjutkan...")
        return

    vlan_name = input("Enter VLAN Name : ").strip()
    if not vlan_name:
        print("VLAN Name tidak boleh kosong!")
        input("\nTekan Enter untuk melanjutkan...")
        return

    create_vlan(vlan_id, vlan_name)
    input("\nTekan Enter untuk melanjutkan...")


def menu_delete():
    """Menu untuk operasi Delete VLAN"""
    print_header("Cisco NX-API Menu")
    print("1.  Read")
    print("2.  Create/Update")
    print("3.  Delete")
    print("4.  Exit")
    print("=" * 30)

    print("Enter your choice (1-4) : 3")
    print()

    print("List all VLAN:")
    vlans = get_all_vlans()
    display_vlan_table(vlans, 'all')

    vlan_id = input("\nEnter the ID you want to delete: ").strip()

    if not vlan_id.isdigit():
        print("VLAN ID harus berupa angka!")
        input("\nTekan Enter untuk melanjutkan...")
        return

    vlan_id = int(vlan_id)

    confirm = input(f"Apakah Anda yakin ingin menghapus VLAN {vlan_id}? (y/n): ").strip().lower()
    if confirm == 'y':
        delete_vlan(vlan_id)
    else:
        print("Penghapusan dibatalkan")

    input("\nTekan Enter untuk melanjutkan...")


def main_menu():
    """Menu utama program"""
    while True:
        print_header("Cisco NX-API Menu")
        print("1.  Read")
        print("2.  Create/Update")
        print("3.  Delete")
        print("4.  Export to CSV")
        print("5.  Exit")
        print("=" * 30)

        choice = input("Enter your choice (1-5) : ").strip()

        if choice == '1':
            menu_read()

        elif choice == '2':
            menu_create_update()

        elif choice == '3':
            menu_delete()

        elif choice == '4':
            export_vlan_to_csv()
            input("\nTekan Enter untuk melanjutkan...")

        elif choice == '5':
            print("\nTerima kasih telah menggunakan program ini!")
            print("Program selesai.")
            sys.exit(0)

        else:
            print("Pilihan tidak valid! Silakan pilih 1-5")
            input("\nTekan Enter untuk melanjutkan...")


if __name__ == "__main__":
    try:
        print("=" * 30)
        print("Program Manajemen VLAN")
        print("Cisco Nexus 9000 Sandbox")
        print("=" * 30)
        print()
        input("Tekan Enter untuk memulai...")
        main_menu()

    except KeyboardInterrupt:
        print("\n\nProgram dihentikan oleh user")
        sys.exit(0)
    except Exception as e:
        print(f"\nError: {e}")
        sys.exit(1)
