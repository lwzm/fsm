#!/usr/bin/env python3

import pathlib
from datetime import datetime
from pony.orm import Database, Required, Optional, Json


db = Database()


@db.on_connect(provider="sqlite")
def _home_sqliterc(_, conn):
    rc = pathlib.Path.home() / ".sqliterc"
    rc.exists() and conn.executescript(rc.read_text())


class Fsm(db.Entity):
    state = Required(str, 80)
    ts = Optional(datetime, default=datetime.now, index=True)
    data = Optional(Json)


if __name__ == '__main__':
    db.bind('sqlite', filename=':memory:')
    db.generate_mapping(create_tables=True)
