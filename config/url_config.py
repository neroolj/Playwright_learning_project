"""
This module contains configuration for different environments.
For every new website create new class with properties for all configs.
Also, it's necessary to create new instance for every new class and add it to __init__.py for convenient import
"""

import os


class ZooplusConfig:
    """Class contains configuration for Zooplus URLs"""
    PROD_URL = "https://www.zooplus.se/"
    STAGE_URL = "https://https://www.stage.zooplus.se/"
    DEV_URL = "https://https://www.dev.zooplus.se/"

    PROD_FILTERS = ['Märke', 'Hundstorlek', 'Smak', 'Pris', 'Hundens ålder', 'Specialfoder för hund']
    STAGE_FILTERS = ['Märke', 'Hundstorlek', 'Smak', 'Pris']
    DEV_FILTERS = ['Märke', 'Smak', 'Pris']

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

# create config instance
zooplus_config = ZooplusConfig()