import json
import logging
from pathlib import Path

from src.config import data_path


class Storage:
    def __init__(self, path):
        self.path = path
        self.projects, self.sessions = self.load_data()

    def load_data(self) -> tuple[dict, list]:
        """
        load data from json file
        :return: projects dictionary，sessions list
        """
        try:
            with open(self.path, 'r', encoding='utf-8') as f:
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

    def save_data(self):
        with open(self.path, 'w') as f:
            data = {'projects': self.projects, 'sessions': self.sessions}
            try:
                json.dump(data, f)
            except json.decoder.JSONDecodeError:
                logging.error("json decode error")

    def add_project(self, name, path):
        # add a new project into data
        # the data going to be dumped in json must be string
        if isinstance(path, Path):
            path = str(path.resolve())
        self.projects[name] = path
        self.save_data()

    def add_project_list(self, name_list, path_list):
        for name, path in zip(name_list, path_list):
            name = str(name) # get the last name as project name
            if isinstance(path, Path):
                path = str(path.resolve())
            self.projects[name] = path
        self.save_data()

    def add_session(self, session_dict):
        self.sessions.append(session_dict)
        self.save_data()

    def get_projects(self):
        return self.projects
