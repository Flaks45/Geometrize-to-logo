import json
import pyperclip
import time


def get_file_path_json(file_path: str = None):
    """
    Function to get information of a JSON as a dict.
    :param file_path: File path of the JSON
    :return: JSON data
    :rtype: dict
    """
    try:
        with open(file_path) as j_file:
            file_data_raw = j_file.read()
            file_data = json.loads(file_data_raw)

    except FileNotFoundError:
        file_data = {}

    return file_data


def dict_to_json_file(dictionary: dict, file_path: str):
    """
    Function to turn dict into JSON file and save it in set directory
    :param dictionary: Dictionary with data to parse
    :param file_path: Directory to save file into
    """
    with open(f"{file_path}", "w") as outfile:
        json.dump(dictionary, outfile, indent=4)


def copy_text(text: str = ""):
    """
    Function to copy text to clipboard
    :param text: Text to copy
    """
    pyperclip.copy(text)
