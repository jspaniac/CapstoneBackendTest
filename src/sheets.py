import json
import os

from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from src.drive import Drive

from src.constants import (
    SKIPPED_SHEETS, MAX_ROWS, STORAGE_DIR, PARSED_JSON
)


class Sheets:
    @staticmethod
    def get_id_from_link(link):
        return link.split('/')[-2]

    def __init__(self, creds):
        self.drive = Drive(creds)
        self.service = build("sheets", "v4", credentials=creds)

    def get_sheets(self, spreadsheet_id):
        """
        Returns a map for title -> sheetId for all subsheets in the provided
        spreadsheet
        """
        result = (
            self.service.spreadsheets()
            .get(spreadsheetId=spreadsheet_id)
            .execute()
        )
        return [sheet['properties']['title'] for sheet in result['sheets']]

    def get_values(self, spreadsheet_id, range, sheet=None):
        """
        Returns 2d array of values from provided spreadsheet within the
        given range. None if there's an error
        """
        try:
            result = (
                self.service.spreadsheets()
                .values()
                .get(spreadsheetId=spreadsheet_id, range=range)
                .execute()
            )
            return result.get("values", [])
        except HttpError as error:
            print(f"An error occurred: {error}")
            return None

    # @staticmethod
    def convert_page_data(self, data):
        languages = data[0][1:]
        page_info = {
            "title": {languages[i]: data[1][1:][i] if i < len(data[1][1:]) else ""
                      for i in range(len(languages))},
            "content": [{
                "content-type": row[0],
                "content": self.copy_content_and_download(row, languages)
            } for row in data[2:]]
        }
        return page_info

    def copy_content_and_download(self, row, languages):
        content = {}
        for i in range(len(languages)):
            if 1 + i < len(row):
                if row[0] == "Image": # download image and write file name to json
                    link = row[1+i]
                    id = Drive.get_id_from_link(link)
                    name = self.drive.get_file_name(id)
                    self.drive.download_file(id, name)
                    content[languages[i]] = name
                else:
                    content[languages[i]] = row[1+i]
            else:
                content[languages[i]] = ""
        return content

    def parse_to_json(self, spreadsheet_id):
        # 1. Get all sheets
        sheets = self.get_sheets(spreadsheet_id)
        if "Languages" not in sheets:
            print("Provided sheet doesn't include 'Languages' page")
            return False

        # 2. Get expected languages
        languages = self.get_values(spreadsheet_id, "Languages!1:1")[0]
        json_data = {
            "languages": languages,
            "pages": []
        }

        # 3. Get data and parse
        for sheet in sheets:
            if sheet in SKIPPED_SHEETS:
                continue
            data = self.get_values(spreadsheet_id, f"{sheet}!1:{MAX_ROWS}")
            if data[0][1:] != languages:
                print("Provided sheet doesn't include columns for all 'Languages")
                return False
            json_data['pages'].append(self.convert_page_data(data))

        # 4. Save to file
        with open(PARSED_JSON, 'w') as f:
            json.dump(json_data, f)
