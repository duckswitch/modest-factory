# coding: utf-8
"""
This module contains tests for the class Factory
"""

from mock import Mock
from pytest import fixture
from simplefactory.factory import Factory, Singleton, Dependency


class StorageIO(object):
    def __init__(self, storage):
        self._storage = storage


class Builder(object):

    def __init__(self, service_account_json):
        self._service_account_json = service_account_json

    def build_cloud_storage_client(self):
        return u"storage.Client"


class Dummy(object):
    def __init__(self, storage, dummy_arg):
        self._storage = storage
        self._dummy_arg = dummy_arg


STORAGE_DEP = Dependency(u"service.Builder", u"build_cloud_storage_client")


@fixture(scope=u"function")
def test_config():
    return {
        u"service": {
            Builder: Singleton({
                u"service_account_json": u"dummy_file.json"
            }),
            StorageIO: {
                u"storage": STORAGE_DEP
            }
        },
        Dummy: Singleton({
            u"storage": STORAGE_DEP
        })
    }


@fixture(scope=u"function")
def factory(test_config):
    return Factory(config=test_config)


def test_find(factory):
    class_def, kwargs = factory.find(factory._config, u"service.StorageIO")
    assert class_def == StorageIO
    assert kwargs == {u"storage": STORAGE_DEP}


def test_interpret_params(factory):
    conf = {
        u"service_account_json": u"dummy_file.json"
    }

    params, is_singleton = factory.interpret_params(Singleton(conf))
    assert params == conf
    assert is_singleton

    params, is_singleton = factory.interpret_params(conf)
    assert params == conf
    assert not is_singleton


def test_interpret_params_with_dependency(factory):
    conf = {
        u"storage": STORAGE_DEP
    }

    params, is_singleton = factory.interpret_params(Singleton(conf))
    assert params == conf
    assert conf[u"storage"] == u"storage.Client"


def test_build_singleton(factory):
    builder1 = factory.build(u"service.Builder")
    builder2 = factory.build(u"service.Builder")

    assert builder1 and builder2
    assert builder1 == builder2


def test_build_not_singleton(factory):
    storage1 = factory.build(u"service.StorageIO")
    storage2 = factory.build(u"service.StorageIO")

    assert storage1 and storage2
    assert storage1 != storage2


def test_build_with_args(factory):
    dummy_instance = factory.build(u"Dummy", dummy_arg=u"dummyValue")
    assert dummy_instance._dummy_arg == u"dummyValue"

