import requests
from requests.auth import HTTPBasicAuth
import pandas as pd

class PIDataFetcher:
    def __init__(self, api_url, username, password):
        """
        Initializes the PIDataFetcher with the API URL, username, and password.
        
        Parameters:
        - api_url: str, the PI Web API URL
        - username: str, PI System username
        - password: str, PI System password
        """
        self.api_url = api_url
        self.auth = HTTPBasicAuth(username, password)
    
    def get_web_id(self, tag):
        """
        Retrieves the WebID for a given PI tag.
        
        Parameters:
        - tag: str, the PI tag in the format \\ServerName\TagName
        
        Returns:
        - str, the WebID of the specified tag
        """
        search_url = f"{self.api_url}/points?path={tag}"
        response = requests.get(search_url, auth=self.auth, headers={"Content-Type": "application/json"}, verify=False)
        if response.status_code == 200:
            return response.json().get('WebId')
        else:
            raise Exception(f"Error {response.status_code}: {response.text}")

    def fetch_historical_data(self, web_id, start_time, end_time, interval="1h"):
        """
        Fetches historical data for a specified WebID.
        
        Parameters:
        - web_id: str, the WebID of the tag
        - start_time: str, the start time in ISO format
        - end_time: str, the end time in ISO format
        - interval: str, the interval time, default is "1h"
        
        Returns:
        - DataFrame with columns: Timestamp, Value
        """
        data_url = f"{self.api_url}/streams/{web_id}/interpolated"
        params = {
            'startTime': start_time,
            'endTime': end_time,
            'interval': interval
        }
        response = requests.get(data_url, auth=self.auth, params=params, verify=False)
        if response.status_code == 200:
            items = response.json()['Items']
            timestamps = [item['Timestamp'] for item in items]
            values = [item['Value'] for item in items]
            return pd.DataFrame({"Timestamp": timestamps, "Value": values})
        else:
            raise Exception(f"Error {response.status_code}: {response.text}")

    def fetch_multiple_tags_data(self, tags, start_time, end_time, interval="1h"):
        """
        Fetches historical data for multiple tags simultaneously.
        
        Parameters:
        - tags: list of str, list of PI tags to fetch data from
        - start_time: str, the start time in ISO format
        - end_time: str, the end time in ISO format
        - interval: str, the interval time, default is "1h"
        
        Returns:
        - DataFrame with columns: Timestamp, Tag, Value
        """
        all_data = []
        
        for tag in tags:
            try:
                # Get the WebID for each tag
                web_id = self.get_web_id(tag)
                # Fetch historical data for the WebID
                data = self.fetch_historical_data(web_id, start_time, end_time, interval)
                data['Tag'] = tag  # Add the tag column for identification
                all_data.append(data)
            except Exception as e:
                print(f"Error fetching data for tag {tag}: {e}")
        
        # Combine all data into one DataFrame
        if all_data:
            return pd.concat(all_data, ignore_index=True)
        else:
            return pd.DataFrame(columns=["Timestamp", "Tag", "Value"])
