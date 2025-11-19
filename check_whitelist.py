from api.abuseipdb import AbuseIPDBClient
from config import Config

c = Config()
client = AbuseIPDBClient(c.ABUSEIPDB_API_KEY)

for ip in ['1.1.1.1', '8.8.8.8']:
    result = client.check_ip(ip)
    wl = result.get('data', {}).get('isWhitelisted')
    print(f"{ip}: Whitelisted = {wl}")
