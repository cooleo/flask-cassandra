# -*- coding: utf-8 -*-

import os
import imp

from pip import logger
from redis import StrictRedis

from cassandra.cqlengine import connection
from cassandra.cqlengine.management import sync_table
from cassandra.cqlengine.management import sync_type
from cassandra.cqlengine.management import drop_table

from app.models import ShoppingList,User
from app.models.app import Feed
from app.models.category import Category
from app.models.feed import Image, FeedPhoto
from app.models.news import News, NewsPhoto
from app.models.photo import Photo
from app.models.profile import Profile
from app.models.video import Video


def _get_default_config_path():
    for name in ("prod.py", "dev.py"):
        path = "config/{}".format(name)
        if os.path.exists(path):
            return path
    else:
        logger.error("Couldn't locate the files in config/")
        exit(1)


def load_config():
    """Load config object for workers.

    Look the environment variable called `WORKER_CONFIG`. If present
    load the python file else look for `prod.py`, `dev.py` in the order.
    If both are missing quit.

    `WORKER_CONFIG` can be of form `config/prod.py` or `config.prod.py`.
    """
    path = os.environ.get('WORKER_CONFIG')
    if not path:
        path = _get_default_config_path()

    mod_name, file_ext = os.path.splitext(os.path.split(path)[-1])
    config = imp.load_source(mod_name, path)
    return config

def _set_env_vars(config):
    for k, v in config.__dict__.items():
        if isinstance(v, (int, str)):
            os.environ[k] = str(v)

def _setup_cassandra(hosts, keyspace):
    """Setup connection to cassandra nodes.

    This function needs to be called before making any queries.

    :param hosts `list`: list of hosts to connect to.
    :param keyspace `unicode`: name of the keyspace to connect.
    """
    if not isinstance(hosts, list):
        raise ValueError("hosts only accepts list of ips.")
    connection.setup(hosts=hosts, default_keyspace=keyspace,
                     protocol_version=3)

def setup_connections(config):
    """Set connection to Cassandra
    """
    keyspace = config.CASSANDRA_KEYSPACE
    hosts = config.CASSANDRA_HOSTS
    _setup_cassandra(hosts=hosts, keyspace=keyspace)
    _set_env_vars(config)
    sync_tables()


def get_redis_client(host='localhost', port=6379, db=0):
    """Create Redis Client connection.
    """
    host = os.environ.get('REDIS_HOST') or host
    port = os.environ.get('REDIS_PORT') or port
    return StrictRedis(host=host, port=port, db=db)


# Helper methods for tests
def sync_tables():
    """Sync all models to tables.
    """
    sync_table(ShoppingList)
    sync_table(User)
    sync_table(Category)
    sync_table(Feed)
    sync_table(News)
    sync_table(Photo)
    sync_table(Profile)
    sync_table(Video)
    sync_type(FeedPhoto)
    sync_type(NewsPhoto)


def drop_tables():
    """Drop all tables in the keyspace.

    Note: Use this with care!.
    """
    drop_table(ShoppingList)
    drop_table(User)
    drop_table(Category)
