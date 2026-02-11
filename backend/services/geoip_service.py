import geoip2.database
import os

class GeoIPService:
    def __init__(self, db_path="backend/database/GeoLite2-City.mmdb"):
        self.reader = None
        if os.path.exists(db_path):
            try:
                self.reader = geoip2.database.Reader(db_path)
                print(f"GeoIP Database loaded from {db_path}")
            except Exception as e:
                print(f"Error loading GeoIP database: {e}")
        else:
            print(f"GeoIP Database not found at {db_path}. GeoIP features will be disabled.")

    def get_country(self, ip):
        if not self.reader:
            return "Unknown"
        
        try:
            response = self.reader.city(ip)
            return response.country.name or "Unknown"
        except Exception:
            return "Unknown"

    def close(self):
        if self.reader:
            self.reader.close()

# Singleton instance
geoip_service = GeoIPService()
