# Import libraries
import configparser
import sqlite3



def initialize_db():
    """Initialize db if needed

    TODO:
        - Create tables
            auth:
                id
                server
                username
                password
                token
            static_pages:
                id
                url
                b64_page_content
            media
                id
                url
                sha512
            status:
                id
                server
                timestamp
                status
    """
    pass


def connect_db():
    config = configparser.ConfigParser()
    config.read(os.path.join(work_dir, '../config.ini'))
    db_file = os.path.join(work_dir, db_file)


def select_media(url):
    