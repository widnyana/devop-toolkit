# -*- coding: utf-8 -*-
import logging

import MySQLdb
from MySQLdb.cursors import DictCursor


class SphinxConnector(object):
    """SphinxConnector

    a simple SphinxQL client

    usage:
    $ pip install MySQL-python

    >>> connection = SphinxConnector(host=Sphinx_HOST, port=Sphinx_PORT)
    >>> cursor = connection.execute("SELECT * FROM indexname WHERE MATCH('keyword');")
    >>> #: return number of row for given query
    >>> print cursor.rowcount
    >>> #: this will provide a list of dict since the connection use MySQLdb.cursors.DictCursor
    >>> print cursor.fetchall()


    """
    CONNECTED = False

    def __init__(self, host, port=9306, autoconnect=False):
        self.conn = None
        self.cur = None
        self.log = logging.getLogger(__name__)

        self.host = host
        self.port = port
        self.charset = "utf8"

        if autoconnect:
            self.connect()

    def connect(self):
        try:
            self.conn = MySQLdb.connect(
                host=self.host,
                port=self.port,
                cursorclass=DictCursor
            )
            self.conn.set_character_set(self.charset)
            self.cur = self.conn.cursor()

            self.CONNECTED = True
        except MySQLdb.Error as e:
            self.log.exception("Sphinx Error %d: %s" % (e.args[0], e.args[1]))
            raise

    def rowcount(self):
        if not self.CONNECTED:
            return None

        return self.cur.rowcount

    def commit(self):
        if not self.CONNECTED:
            return None

        self.conn.commit()

    def close(self):
        if not self.CONNECTED:
            return False

        self.cur.close()
        self.conn.close()

    @property
    def last_executed(self):
        if not self.CONNECTED:
            return ""

        # noinspection PyProtectedMember
        return self.cur._last_executed

    def execute(self, query, args=()):
        """Execute raw query and return the cursor.

        :param query: SphinxQL query to execute
        :param args: tuple of arguments need to be passed towards SphinxQL query. Conditional
        :return: MySQLdb DictCursor
        :rtype: DictCursor
        """
        if not self.CONNECTED:
            self.connect()

        if not args:
            self.cur.execute(query)
        else:
            self.cur.execute(query, args)

        return self.cur
