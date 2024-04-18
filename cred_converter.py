import json


def main():
    creds = {}
    print(json.dumps(creds).replace('\\', r'\\').replace('"', r'\"'))


if __name__ == "__main__":
    main()
