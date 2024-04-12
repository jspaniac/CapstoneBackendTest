import io
import os
import json

from googleapiclient.discovery import build
from googleapiclient.http import MediaIoBaseDownload
from googleapiclient.errors import HttpError

from src.constants import DOWNLOADS_DIR


class Drive:
    @staticmethod
    def get_id_from_link(link):
        """
        Returns the file id for the file from the provided drive share 'link'
        """
        return link.split('/')[-2]

    def __init__(self, creds):
        """
        Constructs a new interface with the drive API from the provided 'creds'
        """
        self.service = build("drive", "v3", credentials=creds)

    def get_file_name(self, file_id):
        """
        Returns the file name for the provided 'file_id'
        Throws HttpError if error occurs on fetch
        """

        file_metadata = self.service.files().get(
            fileId=file_id, fields='name'
        ).execute()
        return file_metadata['name']

    def get_file_bytes(self, file_id):
        """
        Returns the bytes for the provided 'file_id'
        Throws HttpError if error occurs on fetch
        """
        request = self.service.files().get_media(fileId=file_id)

        file = io.BytesIO()
        downloader = MediaIoBaseDownload(file, request)

        done = False
        while done is False:
            _, done = downloader.next_chunk()

        return file.getvalue()

    def download_file(self, file_id, new_name=None):
        """
        Downloads the provided 'file_id', placing the result in DOWNLOADS_DIR
            Named 'new_name' if provided, otherwise will be the original name
        Returns whether or not the download was successful
        """
        try:
            if new_name is None:
                new_name = self.get_file_name(file_id)

            file_bytes = self.get_file_bytes(file_id)
            with open(os.path.join(DOWNLOADS_DIR, new_name), 'wb') as f:
                f.write(file_bytes)

            return True
        except HttpError as error:
            print(f"An error occurred: {error}")
            return False

    def download_files(self):
        #read json file
        f = open('store/pages.json', 'r+')
        data = json.load(f)

        for i in range(len(data["pages"])):
            page = data["pages"][i]
            for j in range(len(page["content"])):
                row = page["content"][j]
                if row["content-type"] == "Image":
                    # download each image
                    for lang,link in row["content"].items():
                        id = Drive.get_id_from_link(link)
                        name = self.get_file_name(id)
                        self.download_file(id, name)

                        # change json content to match downloaded file name
                        data["pages"][i]["content"][j]["content"][lang] = name

        # rewrite json file
        f.seek(0)
        json.dump(data, f)
        f.truncate()

