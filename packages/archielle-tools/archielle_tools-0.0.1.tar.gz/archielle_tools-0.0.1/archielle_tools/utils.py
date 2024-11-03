import pandas as pd
from .config import validate_token

def find_missing_leads(df_profiles, df_leads, user_token):
    """Compare Klaviyo profiles with PerfexCRM leads and return missing leads."""
    validate_token(user_token)  # Validate the user's token

    df_profiles['full_name'] = df_profiles['first_name'].str.strip() + " " + df_profiles['last_name'].str.strip()
    missing_leads = df_profiles[~df_profiles['full_name'].isin(df_leads['full_name'])]
    return missing_leads
