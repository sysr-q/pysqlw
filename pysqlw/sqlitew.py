# -*- coding: utf-8 -*-
from sqltype import sqltype


class sqlitew(sqltype):
    @property
    def required(self):
        return ['db_path']

    def connect(self):
        try:
            import sqlite3
            self.dbc = sqlite3.connect(self.args.get('db_path'))
            self.dbc.row_factory = self._sqlite_dict_factory
            self.cursor = self.dbc.cursor()
        except Exception as e:
            return False
        return True

    def format(self, item):
        return '?'

    def _sqlite_dict_factory(self, cursor, row):
        d = {}
        for idx, col in enumerate(cursor.description):
            d[col[0]] = row[idx]
        return d
