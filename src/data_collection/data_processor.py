# data_processor.py
import pandas as pd
import numpy as np
from datetime import datetime
import time
import sys
sys.path.append('../thingspeak_integration')
from config import WRITE_API_KEY
import requests

class WeatherDataProcessor:
    def __init__(self, file_path):
        self.data = None
        self.file_path = file_path
    
    def load_data(self):
        """Load and initially process the dataset"""
        print("Loading dataset...")
        self.data = pd.read_csv(self.file_path)
        print(f"Loaded {len(self.data)} records")
        
        # Convert datetime
        self.data['Date Time'] = pd.to_datetime(self.data['Date Time'])
        
        # Select relevant columns
        self.processed_data = self.data[[
            'Date Time',
            'p (mbar)',      # Pressure
            'T (degC)',      # Temperature
            'rh (%)'         # Humidity
        ]].copy()
        
        # Rename columns for clarity
        self.processed_data.columns = ['timestamp', 'pressure', 'temperature', 'humidity']
        
        print("Data processing completed")
        return self.processed_data

    def simulate_rain_status(self, humidity_threshold=90):
        """Simple rain simulation based on humidity"""
        return 1 if humidity_threshold <= 90 else 0

    def send_to_thingspeak(self, row):
        """Send a single row of data to ThingSpeak"""
        url = 'https://api.thingspeak.com/update'
        
        payload = {
            'api_key': WRITE_API_KEY,
            'field1': row['temperature'],
            'field2': row['humidity'],
            'field3': row['pressure'],
            'field4': self.simulate_rain_status(row['humidity'])
        }
        
        try:
            response = requests.get(url, params=payload)
            if response.status_code == 200:
                print(f"Data sent successfully: Temp={row['temperature']:.1f}°C, "
                      f"Humidity={row['humidity']:.1f}%, "
                      f"Pressure={row['pressure']:.1f}mbar")
                return True
            else:
                print(f"Failed to send data: {response.status_code}")
                return False
        except Exception as e:
            print(f"Error sending data: {e}")
            return False

def main():
    # Initialize processor
    processor = WeatherDataProcessor('../../data/weather_dataset/max_planck_weather.csv')
    
    # Load and process data
    processed_data = processor.load_data()
    
    print("\nStarting data simulation...")
    
    # Simulate real-time data sending (first 100 records)
    for index, row in processed_data.head(100).iterrows():
        processor.send_to_thingspeak(row)
        time.sleep(15)  # ThingSpeak free tier requires 15s interval
        
if __name__ == "__main__":
    main()