import json
import logging
from config import data_path

def load_data(path) -> tuple[dict, list]:
    """
    load data from json file
    :return: projects dictionary，sessions list
    """
    try:
        with open(path, 'r') as f:
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

def save_data(projects, sessions):
    with open(data_path, 'w') as f:
        data = {'projects': projects, 'sessions': sessions}
        try:
            json.dump(data, f)
        except json.decoder.JSONDecodeError:
            logging.error("json decode error")

def add_project(name, path):
    projects, sessions = load_data(data_path)
    # add a new project into data
    projects[name] = path
    save_data(projects, sessions)

def add_session(session_dict):
    projects, sessions = load_data(data_path)
    sessions.append(session_dict)
    save_data(projects,sessions)
