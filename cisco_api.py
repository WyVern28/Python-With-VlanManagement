"""
Modul API untuk manajemen VLAN di Cisco Nexus 9000
Updated: Menggunakan Unified Request Handler untuk cli_show dan cli_conf
"""

import requests
import json
import urllib3
from config import BASE_URL, HEADERS, NEXUS_USERNAME, NEXUS_PASSWORD, REQUEST_TIMEOUT, VERIFY_SSL

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

def send_nexus_request(commands, mode='cli_show'):
    """
    Fungsi Master untuk mengirim request ke Cisco Nexus
    
    Args:
        commands: String atau list perintah
        mode: 'cli_show' untuk read-only, 'cli_conf' untuk konfigurasi
    """
    if isinstance(commands, str):
        commands = [commands]

    payload = {
        "ins_api": {
            "version": "1.0",
            "type": mode,  
            "chunk": "0",
            "sid": "1",
            "input": " ; ".join(commands), 
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
            result = response.json()
            
            if 'ins_api' in result and 'outputs' in result['ins_api']:
                output = result['ins_api']['outputs']['output']
                
                if isinstance(output, list):
                    for out in output:
                        if 'code' in out and out['code'] != '200':
                            print(f"Nexus Error: {out.get('msg', 'Unknown Error')}")
                            return None
                elif isinstance(output, dict):
                    if 'code' in output and output['code'] != '200':
                        print(f"Nexus Error: {output.get('msg', 'Unknown Error')}")
                        return None
            
            return result
        else:
            print(f"HTTP Error {response.status_code}: {response.text}")
            return None

    except requests.exceptions.RequestException as e:
        print(f"Connection Error: {e}")
        return None


def test_authentication():
    print("Mencoba menghubungkan ke Sandbox...")
    result = send_nexus_request("show version", mode='cli_show')
    if result:
        print("Authentication successful!")
        return True
    else:
        print("Authentication failed!")
        return False

def get_all_vlans():
    command = "show vlan brief"
    result = send_nexus_request(command, mode='cli_show')

    if result:
        try:
            if 'ins_api' in result and 'outputs' in result['ins_api']:
                output = result['ins_api']['outputs']['output']
                if 'body' in output:
                    body = output['body']
                    if 'TABLE_vlanbriefxbrief' in body:
                        vlans = body['TABLE_vlanbriefxbrief']['ROW_vlanbriefxbrief']
                    elif 'TABLE_vlanbrief' in body:
                        vlans = body['TABLE_vlanbrief']['ROW_vlanbrief']
                    else:
                        return []

                    if isinstance(vlans, dict):
                        return [vlans]
                    return vlans
        except Exception as e:
            print(f"Error parsing VLAN data: {e}")
            return []
    return []

def create_vlan(vlan_id, vlan_name):
    commands = [
        f"vlan {vlan_id}",
        f"name {vlan_name}",
        "exit"
    ]
    if send_nexus_request(commands, mode='cli_conf'):
        print(f"Successfully created VLAN {vlan_id} ({vlan_name})")
        return True
    else:
        print(f"Failed to create VLAN {vlan_id}")
        return False

def delete_vlan(vlan_id):
    """Menghapus VLAN menggunakan mode cli_conf"""
    command = f"no vlan {vlan_id}"

    if send_nexus_request(command, mode='cli_conf'):
        print(f"Successfully deleted VLAN {vlan_id}")
        return True
    else:
        print(f"Failed to delete VLAN {vlan_id}")
        return False

def update_vlan_port(vlan_id, interface, mode='access'):
    commands = [
        f"interface {interface}",
        f"switchport mode {mode}"
    ]

    if mode == 'access':
        commands.append(f"switchport access vlan {vlan_id}")
    else:
        commands.append(f"switchport trunk allowed vlan add {vlan_id}")

    if send_nexus_request(commands, mode='cli_conf'):
        print(f"Successfully updated interface {interface}")
        return True
    else:
        print(f"Failed to update interface")
        return False

def count_vlans():
    vlans = get_all_vlans()
    return len(vlans)

def get_vlan_by_id(vlan_id):
    vlans = get_all_vlans()
    for vlan in vlans:
        vid = vlan.get('vlanshowbr-vlanid-utf', vlan.get('vlanshowbr-vlanid'))
        if str(vid) == str(vlan_id):
            return vlan
    return None

def get_vlan_by_name(vlan_name):
    vlans = get_all_vlans()
    matching = []
    for vlan in vlans:
        name = vlan.get('vlanshowbr-vlanname', '')
        if vlan_name.lower() in name.lower():
            matching.append(vlan)
    return matching