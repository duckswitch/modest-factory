# Description.


Simple Factory lib to create classes with a dependency injection like pattern.


# How to use.


## Install the lib.


Install it with pip.
```bash
pip install modestfactory
```


## Create a configuration & the factory.


```python
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


# Note that all these should be in separate files.


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
            # Using dependency is like calling Factory.build(u"db.UserDB")
            u"user_db": Dependency(u"db.UserDB")
        })
    }
})


```


## Build your classes.


```python
# Building the classes in an easy way.
USER_API = FACTORY.build(u"api.UserApi")
USER_API.list() # -> [1, u"dummy"]
```
