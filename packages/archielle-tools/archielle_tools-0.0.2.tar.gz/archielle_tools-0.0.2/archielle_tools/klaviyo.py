import requests
import pandas as pd
from .config import validate_token

def get_profiles_from_lists(list_ids, api_key, user_token):
    validate_token(user_token)  # Validate the user's token
    all_profiles = []
    
    for list_id in list_ids:
        url = f"https://a.klaviyo.com/api/lists/{list_id}/profiles"
        headers = {
            "accept": "application/vnd.api+json",
            "revision": "2024-10-15",
            "Authorization": f"Klaviyo-API-Key {api_key}"
        }
        response = requests.get(url, headers=headers)
        
        if response.status_code == 200:
            profiles_data = response.json()
            
            for profile in profiles_data['data']:
                all_profiles.append({
                    "id": profile['id'],
                    "email": profile['attributes'].get('email', None),
                    "first_name": profile['attributes'].get('first_name', None),
                    "last_name": profile['attributes'].get('last_name', None),
                    "phone": profile['attributes'].get('phone_number', None),
                    "location": profile['attributes'].get('location', None),
                    "properties": profile['attributes'].get('properties', None),
                    "joined_group_at": profile['attributes'].get('joined_group_at', None),
                    "created": profile['attributes'].get('created', None),
                    "updated": profile['attributes'].get('updated', None),
                    "title": profile['attributes'].get('title', None)
                })
        else:
            print(f"Failed to fetch profiles for list {list_id}. Status code: {response.status_code}")
    
    return pd.DataFrame(all_profiles)
