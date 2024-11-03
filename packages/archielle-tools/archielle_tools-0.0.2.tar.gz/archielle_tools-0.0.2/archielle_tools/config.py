REQUIRED_TOKEN = 'fjslkaslkdbiovweoivjkelsa'

def validate_token(user_token):
    if user_token != REQUIRED_TOKEN:
        raise ValueError("Invalid token. Access to archielle-tools is restricted.")
