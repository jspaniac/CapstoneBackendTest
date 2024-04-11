from google.oauth2 import service_account

from src.drive import Drive
from src.constants import CREDENTIALS_FILE


def load_credentials(scopes):
    return service_account.Credentials.from_service_account_file(
        CREDENTIALS_FILE,
        scopes=scopes
    )


def main():
    creds = load_credentials(['https://www.googleapis.com/auth/drive'])

    link = "https://drive.google.com/file/d/1Wm0b8FnM79pzSjmnvrvABJ1Rsvro68uL/view?usp=drive_link"
    Drive(creds).download_file(file_id=Drive.get_id_from_link(link))


if __name__ == "__main__":
    main()