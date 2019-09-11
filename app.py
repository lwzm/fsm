#!/usr/bin/env python3

import json

from falcon import Request, Response, API, HTTPNotFound, HTTPForbidden

from core import new, lock, transit, NotFound, NotAllowed


class InitNew:
    def on_post(self, req: Request, resp: Response, state):
        data = json.load(req.stream) if req.content_length else {}
        new(state, data)


class LockOne:
    def on_post(self, req: Request, resp: Response, state):
        try:
            item = lock(state)
        except NotFound:
            raise HTTPNotFound
        resp.body = json.dumps(item, default=str)


class TransitLocked:
    def on_post(self, req: Request, resp: Response, id, state):
        data = json.load(req.stream) if req.content_length else None
        try:
            transit(id, state, data)
        except NotFound:
            raise HTTPNotFound
        except NotAllowed as e:
            raise HTTPForbidden(description=e.args)


application = API()
application.add_route('/new/{state}', InitNew())
application.add_route('/lock/{state}', LockOne())
application.add_route('/transit/{id:int}/{state}', TransitLocked())


if __name__ == '__main__':
    import bjoern
    bjoern.run(application, "", 8000)
