"""
This module contains configuration for different environments.
For every new website create new class with properties for all configs.
Also, it's necessary to create new instance for every new class and add it to __init__.py for convenient import
"""

import os
import dotenv


# load dotenv variables
dotenv.load_dotenv()


class ZooplusConfig:
    """Class contains configuration for Zooplus URLs"""
    PROD_URL = "https://www.zooplus.se/"
    STAGE_URL = "https://https://www.stage.zooplus.se/"
    DEV_URL = "https://https://www.dev.zooplus.se/"

    PROD_FILTERS = ['Märke', 'Hundstorlek', 'Smak', 'Pris', 'Hundens ålder', 'Specialfoder för hund']
    STAGE_FILTERS = ['Märke', 'Hundstorlek', 'Smak', 'Pris']
    DEV_FILTERS = ['Märke', 'Smak', 'Pris']

    PROD_USERNAME = os.environ.get('ZOOPLUS_USERNAME')
    PROD_PASSWORD = os.environ.get('ZOOPLUS_PASSWORD')
    STAGE_USERNAME = 'to_be_added'
    STAGE_PASSWORD = 'to_be_added'
    DEV_USERNAME = 'to_be_added'
    DEV_PASSWORD = 'to_be_added'

    @property
    def current_url(self):
        env = os.environ.get("TEST_ENV", 'prod')
        urls = {'prod': self.PROD_URL, 'stage': self.STAGE_URL, 'dev': self.DEV_URL}

        if env not in urls:
            raise ValueError(f"Unknown environment: {env}")
        return urls[env]

    @property
    def current_filters(self):
        env = os.environ.get("TEST_ENV", 'prod')
        filters = {'prod': self.PROD_FILTERS, 'stage': self.STAGE_FILTERS, 'dev': self.DEV_FILTERS}

        if env not in filters:
            raise ValueError(f"Unknown environment: {env}")
        return filters[env]

    @property
    def current_username(self):
        env = os.environ.get("TEST_ENV", 'prod')
        usernames = {'prod': self.PROD_USERNAME, 'stage': self.STAGE_USERNAME, 'dev': self.DEV_USERNAME}

        if env not in usernames:
            raise ValueError(f"Unknown environment: {env}")
        return usernames[env]

    @property
    def current_password(self):
        env = os.environ.get("TEST_ENV", 'prod')
        passwords = {'prod': self.PROD_PASSWORD, 'stage': self.STAGE_PASSWORD, 'dev': self.DEV_PASSWORD}

        if env not in passwords:
            raise ValueError(f"Unknown environment: {env}")
        return passwords[env]

# create config instance
zooplus_config = ZooplusConfig()