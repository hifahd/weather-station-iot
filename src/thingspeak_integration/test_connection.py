# test_connection.py
import requests
import time
from datetime import datetime
from config import CHANNEL_ID, WRITE_API_KEY

def send_test_data():
    # Base URL for ThingSpeak API
    url = 'https://api.thingspeak.com/update'
    
    # Test data
    test_data = {
        'api_key': WRITE_API_KEY,
        'field1': 25.5,  # Temperature
        'field2': 60,    # Humidity
        'field3': 1013,  # Pressure
        'field4': 0      # Rain Status (0 = No Rain)
    }
    
    try:
        response = requests.get(url, params=test_data)
        if response.status_code == 200:
            print(f"Data sent successfully at {datetime.now()}")
            print(f"Response: {response.text}")
        else:
            print(f"Failed to send data: {response.status_code}")
    except Exception as e:
        print(f"Error sending data: {e}")

if __name__ == "__main__":
    print("Testing ThingSpeak connection...")
    send_test_data()