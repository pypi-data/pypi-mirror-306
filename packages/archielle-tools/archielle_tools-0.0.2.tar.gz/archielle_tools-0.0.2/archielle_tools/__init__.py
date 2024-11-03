from .klaviyo import get_profiles_from_lists
from .perfexcrm import get_perfexcrm_leads
from .db_utils import insert_leads_into_db
from .utils import find_missing_leads
from .config import validate_token

# Initialize with user-provided token
def initialize(user_token):
    """Initialize the archielle-tools library with a user token."""
    validate_token(user_token)  # Validate the token
    global _initialized
    _initialized = True
    print("archielle-tools initialized successfully.")

# Wrapper to ensure functions are called only if the library is initialized
def require_initialization(func):
    def wrapper(*args, **kwargs):
        if not _initialized:
            raise ValueError("Library not initialized. Call `initialize(user_token)` with a valid token first.")
        return func(*args, **kwargs)
    return wrapper

# Mark library as not initialized by default
_initialized = False

# Decorate all public functions with the initialization requirement
get_profiles_from_lists = require_initialization(get_profiles_from_lists)
get_perfexcrm_leads = require_initialization(get_perfexcrm_leads)
insert_leads_into_db = require_initialization(insert_leads_into_db)
find_missing_leads = require_initialization(find_missing_leads)
