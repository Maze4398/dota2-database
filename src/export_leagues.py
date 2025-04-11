import os
import time
from datetime import datetime
import pandas as pd
import requests
from tqdm import tqdm
from config import Config

class LeagueExporter:
    def __init__(self):
        Config.ensure_dirs_exist()
        self.api_url = Config.OPENDOTA_API_URL
        self.rate_limit = Config.RATE_LIMIT
        self.last_request_time = 0
        
    def _make_api_request(self, endpoint):
        """Handle API requests with rate limiting"""
        now = time.time()
        elapsed = now - self.last_request_time
        min_interval = 60 / self.rate_limit
        
        if elapsed < min_interval:
            time.sleep(min_interval - elapsed)
            
        url = f"{self.api_url}/{endpoint}"
        response = requests.get(url)
        self.last_request_time = time.time()
        
        if response.status_code == 200:
            return response.json()
        else:
            print(f"API request failed: {response.status_code} - {response.text}")
            return None
            
    def get_all_leagues(self):
        """Fetch all leagues from OpenDota API"""
        print("Fetching leagues data...")
        leagues = self._make_api_request("leagues")
        
        if not leagues:
            print("Failed to fetch leagues")
            return None
            
        print(f"Successfully retrieved {len(leagues)} leagues")
        return leagues
        
    def export_to_excel(self, leagues, filename=None):
        """Export leagues data to Excel"""
        if not leagues:
            print("No data to export")
            return False
            
        if not filename:
            today = datetime.now().strftime("%Y%m%d_%H%M")
            filename = f"dota_leagues_{today}.xlsx"
            filename = os.path.join(Config.RAW_DATA_DIR, filename)
            
        try:
            df = pd.DataFrame(leagues)
            
            # Add useful calculated fields
            if 'start_timestamp' in df.columns:
                df['start_date'] = pd.to_datetime(df['start_timestamp'], unit='s')
            if 'end_timestamp' in df.columns:
                df['end_date'] = pd.to_datetime(df['end_timestamp'], unit='s')
            if 'start_date' in df.columns and 'end_date' in df.columns:
                df['duration_days'] = (df['end_date'] - df['start_date']).dt.days
                
            # Save to Excel
            df.to_excel(filename, index=False)
            print(f"Successfully exported data to {filename}")
            return True
            
        except Exception as e:
            print(f"Error exporting data: {str(e)}")
            return False
            
def main():
    exporter = LeagueExporter()
    leagues = exporter.get_all_leagues()
    if leagues:
        exporter.export_to_excel(leagues)

if __name__ == "__main__":
    main()