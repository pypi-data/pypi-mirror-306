import pandas as pd
from .config import validate_token

def find_missing_leads(df_profiles, df_leads, user_token):
    """Compare Klaviyo profiles with PerfexCRM leads and return missing leads."""

    validate_token(user_token)  # Validate the user's token

    # Check for required columns in df_profiles before creating 'full_name'
    if 'first_name' not in df_profiles.columns or 'last_name' not in df_profiles.columns:
        raise KeyError("The `df_profiles` DataFrame must contain 'first_name' and 'last_name' columns.")
    
    # Create 'full_name' in df_profiles by combining 'first_name' and 'last_name'
    df_profiles['full_name'] = df_profiles['first_name'].str.strip() + " " + df_profiles['last_name'].str.strip()

    # Check for required column in df_leads before creating 'full_name'
    if 'name' not in df_leads.columns:
        raise KeyError("The `df_leads` DataFrame must contain a 'name' column representing the full name.")

    # Create 'full_name' in df_leads by trimming 'name' if necessary
    df_leads['full_name'] = df_leads['name'].str.strip()

    # Find profiles in df_profiles that are not in df_leads based on 'full_name'
    missing_leads = df_profiles[~df_profiles['full_name'].isin(df_leads['full_name'])]

    return missing_leads

