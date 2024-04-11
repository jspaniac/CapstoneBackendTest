import os

STORAGE_DIR = os.path.join(os.getcwd(), 'store')
DOWNLOADS_DIR = os.path.join(STORAGE_DIR, 'downloads')

# TODO: Update to use environment variable
CREDENTIALS_FILE = os.path.join(STORAGE_DIR, 'credentials.json')
