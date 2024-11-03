import requests
import pandas as pd
from .config import validate_token

def get_perfexcrm_leads(api_key, user_token):
    validate_token(user_token)  # Validate the user's token
    
    url = "https://crm.archielle.com/crm/api/leads"
    headers = {
        'Authtoken': api_key
    }
    response = requests.get(url, headers=headers)

    if response.status_code == 200:
        data = response.json()
        df = pd.json_normalize(data)
        df = df.explode('customfields')
        customfields_flat = pd.json_normalize(df['customfields']).add_prefix('customfields_')
        return pd.concat([df.drop(columns=['customfields']), customfields_flat], axis=1)
    else:
        print(f"Request failed with status code {response.status_code}")
        return None
