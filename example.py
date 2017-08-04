# coding: utf-8
"""
Example
"""

from modestfactory import Factory
from modestfactory import Singleton
from modestfactory import Dependency

# Fake DB access class.
class UserDB(object):

    def __init__(self, env):
        self._database = u"database_{}".format(env)
        self._table = u"user"

    def do_query(self, database, query):
        # Shoulds implement some DB process. Just mocking.
        return [
            [1, u"dummy"]
        ]

    def list(self):
        return self.do_query(
            self._database, 
            u"SELECT * FROM {}".format(self._table)
        )

# Fake Api class.
class UserApi(object):

    def __init__(self, user_db):
        self._user_db = user_db

    def list(self):
        return self._user_db.list()

# App configuration.
APP_CONFIG = {
    u"env": u"staging"
}

# Note that all these should be in seperate files.
# Factory instance.
FACTORY = Factory({
    # Wrapping in Singleton ensure it will have only one instance.
    u"db": { 
        UserDB: Singleton({
            u"env": APP_CONFIG[u"env"]
        })
    },
    u"api": {
        UserApi: Singleton({
            u"user_db": Dependency(u"db.UserDB")
        })
    }
})

# Building the classes in a easy way.
user_api = FACTORY.build(u"api.UserApi")
result = user_api.list() # -> [1, u"dummy"]
print(result)
