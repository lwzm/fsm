#!/usr/bin/env python3

from datetime import datetime
from pony.orm import Database, Required, Optional, Json


db = Database()


class Fsm(db.Entity):
    state = Required(str, 80)
    ts = Optional(datetime, default=datetime.now, index=True)
    data = Optional(Json)


if __name__ == '__main__':
    db.bind('sqlite', filename=':memory:')
    db.generate_mapping(create_tables=True)
