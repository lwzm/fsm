#!/usr/bin/env python3

import json

from datetime import datetime, timedelta

from pony import orm
from entities import Fsm, db


class NotFound(Warning): pass
class NotAllowed(Warning): pass


@orm.db_session
def new(state, data={}):
    Fsm(state=state, data=data)


@orm.db_session
def lock(state):
    ts = datetime.now() - timedelta(days=1)
    i = orm.select(i for i in Fsm if i.state ==
                   state and i.ts > ts).for_update().first()
    if not i:
        raise NotFound(state)
    i.state = f"locked-{i.state}"
    return i.to_dict()


@orm.db_session
def transit(id, state, data_patch=None):
    i = Fsm.get_for_update(id=id)
    if not i:
        raise NotFound(id)
    if not i.state.startswith("locked-"):
        raise NotAllowed(id, i.state, state)
    i.state = state
    i.ts = datetime.now()
    if data_patch:
        i.data.update(data_patch)


if __name__ == '__main__':
    db.bind('sqlite', filename=':memory:')
    db.generate_mapping(create_tables=True)
    new('a', {"v": 5})
    try:
        print(lock('-'))
    except Warning:
        pass
    o = lock('a')
    print(o)
    transit(o['id'], 'b', {"v": 'q', 'x': 'ok'})
    print(lock('b'))
else:
    import yaml
    db.bind(**yaml.safe_load(open("database.yaml")))
    db.generate_mapping(create_tables=True)
