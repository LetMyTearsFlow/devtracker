import json
import logging

data_path = './data.json'


def load_data() -> tuple[dict, list]:
    """
    load data from json file
    :return: projects dictionary，sessions list
    """
    try:
        with open(data_path, 'r') as f:
            data = json.load(f)
            projects = data['projects']
            sessions = data['sessions']
            logging.info("successfully load data")
        return projects, sessions
    except FileNotFoundError:
        # file not found, maybe the first time or deleted, return empty data
        logging.error("file not found")
        return {}, []
    except json.decoder.JSONDecodeError:
        # illegal format
        logging.error("json decode error")
        return {}, []
    except KeyError:
        # the data file may be modified maliciously, don't use it
        logging.error("key error")
        return {}, []

