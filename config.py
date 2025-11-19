"""
Konfigurasi untuk koneksi ke Cisco Nexus 9000 Sandbox
File ini berisi kredensial dan endpoint untuk API Cisco NX-API
"""

NEXUS_HOST = "sbx-nxos-mgmt.cisco.com"
NEXUS_PORT = 443
NEXUS_USERNAME = "admin"
NEXUS_PASSWORD = "Admin_1234!"

BASE_URL = f"https://{NEXUS_HOST}:{NEXUS_PORT}/ins"

HEADERS = {
    'content-type': 'application/json'
}

REQUEST_TIMEOUT = 30

VERIFY_SSL = False
