"""
Modul API untuk manajemen VLAN di Cisco Nexus 9000
Berisi fungsi-fungsi CRUD (Create, Read, Update, Delete) untuk VLAN
"""

import requests
import json
import urllib3
from config import BASE_URL, HEADERS, NEXUS_USERNAME, NEXUS_PASSWORD, REQUEST_TIMEOUT, VERIFY_SSL

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)


def send_command(commands):
    """
    Mengirim perintah ke Cisco Nexus via NX-API

    Args:
        commands: String atau list dari perintah CLI

    Returns:
        Response dari API atau None jika gagal
    """
    if isinstance(commands, str):
        commands = [commands]

    payload = {
        "ins_api": {
            "version": "1.0",
            "type": "cli_show",
            "chunk": "0",
            "sid": "1",
            "input": ";".join(commands),
            "output_format": "json"
        }
    }

    try:
        response = requests.post(
            BASE_URL,
            auth=(NEXUS_USERNAME, NEXUS_PASSWORD),
            headers=HEADERS,
            data=json.dumps(payload),
            timeout=REQUEST_TIMEOUT,
            verify=VERIFY_SSL
        )

        if response.status_code == 200:
            return response.json()
        else:
            print(f"Error: HTTP {response.status_code}")
            return None

    except requests.exceptions.RequestException as e:
        print(f"Error koneksi: {e}")
        return None


def send_config_command(commands):
    """
    Mengirim perintah konfigurasi ke Cisco Nexus

    Args:
        commands: String atau list dari perintah konfigurasi

    Returns:
        True jika berhasil, False jika gagal
    """
    if isinstance(commands, str):
        commands = [commands]

    payload = {
        "ins_api": {
            "version": "1.0",
            "type": "cli_conf",
            "chunk": "0",
            "sid": "1",
            "input": ";".join(commands),
            "output_format": "json"
        }
    }

    try:
        response = requests.post(
            BASE_URL,
            auth=(NEXUS_USERNAME, NEXUS_PASSWORD),
            headers=HEADERS,
            data=json.dumps(payload),
            timeout=REQUEST_TIMEOUT,
            verify=VERIFY_SSL
        )

        if response.status_code == 200:
            # Check for errors in response body
            try:
                result = response.json()
                if 'ins_api' in result and 'outputs' in result['ins_api']:
                    output = result['ins_api']['outputs']['output']
                    if isinstance(output, list):
                        for out in output:
                            if 'code' in out and out['code'] != '200':
                                print(f"Error: {out.get('msg', 'Unknown error')}")
                                return False
                    elif isinstance(output, dict):
                        if 'code' in output and output['code'] != '200':
                            print(f"Error: {output.get('msg', 'Unknown error')}")
                            return False
            except:
                pass  # If parsing fails, assume success based on HTTP 200
            return True
        else:
            print(f"Error: HTTP {response.status_code}")
            print(f"Response: {response.text}")
            return False

    except requests.exceptions.RequestException as e:
        print(f"Error koneksi: {e}")
        return False


def test_authentication():
    """
    Test koneksi dan autentikasi ke Cisco Nexus

    Returns:
        True jika berhasil, False jika gagal
    """
    result = send_command("show version")
    if result:
        print("Authentication successful!")
        return True
    else:
        print("Authentication failed!")
        return False


def create_vlan(vlan_id, vlan_name):
    """
    Membuat VLAN baru

    Args:
        vlan_id: ID VLAN (1-4094)
        vlan_name: Nama VLAN

    Returns:
        True jika berhasil, False jika gagal
    """
    # Try with configure terminal first
    commands = [
        "configure terminal",
        f"vlan {vlan_id}",
        f"name {vlan_name}",
        "exit"
    ]

    if send_config_command(commands):
        print(f"Successfully created VLAN {vlan_id} with name '{vlan_name}'")
        return True
    else:
        print(f"Failed to create VLAN {vlan_id}")
        return False


def get_vlan_info(vlan_id=None):
    """
    Mendapatkan informasi VLAN

    Args:
        vlan_id: ID VLAN spesifik (optional). Jika None, menampilkan semua VLAN

    Returns:
        Dictionary berisi informasi VLAN atau None jika gagal
    """
    if vlan_id:
        command = f"show vlan id {vlan_id}"
    else:
        command = "show vlan brief"

    result = send_command(command)

    if result:
        try:
            # Parse response dari NX-API
            if 'ins_api' in result and 'outputs' in result['ins_api']:
                output = result['ins_api']['outputs']['output']
                if 'body' in output:
                    return output['body']
            return result
        except (KeyError, TypeError) as e:
            print(f"Error parsing response: {e}")
            return None
    return None


def get_all_vlans():
    """
    Mendapatkan daftar semua VLAN

    Returns:
        List dari VLAN atau None jika gagal
    """
    vlan_info = get_vlan_info()

    if not vlan_info:
        return []

    # Debug: print struktur response (uncomment untuk debugging)
    # print(f"DEBUG - Response structure: {json.dumps(vlan_info, indent=2)}")

    # Try different possible response structures
    if 'TABLE_vlanbriefxbrief' in vlan_info:
        vlans = vlan_info['TABLE_vlanbriefxbrief']['ROW_vlanbriefxbrief']
        # Pastikan hasilnya adalah list
        if isinstance(vlans, dict):
            return [vlans]
        return vlans
    elif 'TABLE_vlanbriefid' in vlan_info:
        vlans = vlan_info['TABLE_vlanbriefid']['ROW_vlanbriefid']
        # Pastikan hasilnya adalah list
        if isinstance(vlans, dict):
            return [vlans]
        return vlans
    elif 'TABLE_vlanbrief' in vlan_info:
        vlans = vlan_info['TABLE_vlanbrief']['ROW_vlanbrief']
        if isinstance(vlans, dict):
            return [vlans]
        return vlans

    # Jika tidak ada struktur yang cocok, print untuk debugging
    print(f"Warning: Unexpected response structure. Keys: {vlan_info.keys() if isinstance(vlan_info, dict) else type(vlan_info)}")
    return []


def count_vlans():
    """
    Menghitung jumlah VLAN yang ada

    Returns:
        Jumlah VLAN
    """
    vlans = get_all_vlans()
    return len(vlans) if vlans else 0


def update_vlan_port(vlan_id, interface, mode='access'):
    """
    Mengupdate port assignment untuk VLAN

    Args:
        vlan_id: ID VLAN
        interface: Nama interface (contoh: Ethernet1/1)
        mode: Mode switchport ('access' atau 'trunk')

    Returns:
        True jika berhasil, False jika gagal
    """
    commands = [
        f"interface {interface}",
        f"switchport mode {mode}"
    ]

    if mode == 'access':
        commands.append(f"switchport access vlan {vlan_id}")
    else:
        commands.append(f"switchport trunk allowed vlan add {vlan_id}")

    if send_config_command(commands):
        print(f"Successfully updated interface {interface} for VLAN {vlan_id}")
        return True
    else:
        print(f"Failed to update interface {interface}")
        return False


def delete_vlan(vlan_id):
    """
    Menghapus VLAN

    Args:
        vlan_id: ID VLAN yang akan dihapus

    Returns:
        True jika berhasil, False jika gagal
    """
    command = f"no vlan {vlan_id}"

    if send_config_command(command):
        print(f"Successfully deleted VLAN {vlan_id}")
        return True
    else:
        print(f"Failed to delete VLAN {vlan_id}")
        return False


def get_vlan_by_id(vlan_id):
    """
    Mendapatkan informasi VLAN berdasarkan ID

    Args:
        vlan_id: ID VLAN

    Returns:
        Dictionary informasi VLAN atau None
    """
    vlans = get_all_vlans()
    for vlan in vlans:
        if str(vlan.get('vlanshowbr-vlanid-utf', '')) == str(vlan_id):
            return vlan
    return None


def get_vlan_by_name(vlan_name):
    """
    Mendapatkan informasi VLAN berdasarkan nama

    Args:
        vlan_name: Nama VLAN

    Returns:
        List dari VLAN yang cocok
    """
    vlans = get_all_vlans()
    matching_vlans = []
    for vlan in vlans:
        if vlan_name.lower() in vlan.get('vlanshowbr-vlanname', '').lower():
            matching_vlans.append(vlan)
    return matching_vlans
