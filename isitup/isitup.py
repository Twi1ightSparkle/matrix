# Import modules
import ast
import configparser
import os

# Import other python files
from util import content
from util import http


if __name__ == "__main__":
    # Setup

    # Load config
    work_dir = os.path.dirname(os.path.realpath(__file__)) # Get the path for the directory this python file is stored in
    config = configparser.ConfigParser()
    config.read(os.path.join(work_dir, 'config.ini'))

    # Global
    pages = ast.literal_eval(config.get("Global", "pages"))
    db_file = config.get('Global', 'db_file')
    db_file = os.path.join(work_dir, db_file)

    # For each page
    for page in list(pages):
        # Load page config
        hostname = config.get(page, 'hostname')
        delegated_hostname = config.get(page, 'delegated_hostname')
        riot_domain = config.get(page, 'riot_domain')
        username = config.get(page, 'username')

        # Check #/welcome
        riot_welcome = http.download_something(riot_domain, '/#/welcome')
        if riot_welcome:
            list_of_errors, riot_welcome_base64 = content.b64(riot_welcome)
            
            # If an error
            if riot_welcome_base64 in list_of_errors:
                # TODO: add error to db
                pass
        
        # Check #/login
        
        # Check #/register

        # Check #/home

        # Check if monitoring user is created
            # Create
            # Accept terms
            # Create test room
        
        # Try sending a message to room
