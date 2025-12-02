"""
Konfigurasi untuk koneksi ke Cisco Nexus 9000 Sandbox
File ini berisi kredensial dan endpoint untuk API Cisco NX-API
"""

NEXUS_HOST = "https://sbx-nxos-mgmt.cisco.com"
NEXUS_USERNAME = "admin"
NEXUS_PASSWORD = "Admin_1234!"

BASE_URL = f"{NEXUS_HOST}/ins"

HEADERS = {
    'content-type': 'application/json'
}

REQUEST_TIMEOUT = 30

VERIFY_SSL = False
