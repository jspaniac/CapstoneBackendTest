from google.oauth2 import service_account

from src.drive import Drive
from src.sheets import Sheets
from src.constants import CREDENTIALS_FILE


def load_credentials(scopes):
    return service_account.Credentials.from_service_account_file(
        CREDENTIALS_FILE,
        scopes=scopes
    )


def main():
    creds = load_credentials([
        'https://www.googleapis.com/auth/drive',
        'https://www.googleapis.com/auth/spreadsheets'
    ])

    # image_link = "https://drive.google.com/file/d/1Wm0b8FnM79pzSjmnvrvABJ1Rsvro68uL/view?usp=drive_link"
    spreadsheet_link = "https://docs.google.com/spreadsheets/d/1tu5G4pl6Wn2uOx3CbrUiJHEZy2e_8F2bPn8Ry6HJYJ4/edit#gid=1392834485"

    # Drive(creds).download_file(file_id=Drive.get_id_from_link(image_link))
    Sheets(creds).parse_to_json(Sheets.get_id_from_link(spreadsheet_link))
    Drive(creds).download_files()


if __name__ == "__main__":
    main()