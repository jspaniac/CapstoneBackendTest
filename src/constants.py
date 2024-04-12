import os

# Directories & Files
STORAGE_DIR = os.path.join(os.getcwd(), 'store')
DOWNLOADS_DIR = os.path.join(STORAGE_DIR, 'downloads')

# TODO: Update to use environment variable
CREDENTIALS_FILE = os.path.join(STORAGE_DIR, 'credentials.json')
PARSED_JSON = os.path.join(STORAGE_DIR, "pages.json")

# Sheets stuff
SKIPPED_SHEETS = {"Languages", "Base"}
MAX_ROWS = 1000
