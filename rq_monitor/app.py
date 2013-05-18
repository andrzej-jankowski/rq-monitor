#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals

import argparse
import os
import threading
import time

from random import randint

import tornado.ioloop
import tornado.web
import tornado.websocket

from redis import Redis
from rq import Queue, Worker


class SocketHandler(tornado.websocket.WebSocketHandler):
    waiters = set()
    cache = {'workers': [], 'queues': []}

    def open(self):
        SocketHandler.waiters.add(self)

    def on_close(self):
        SocketHandler.waiters.remove(self)

    @classmethod
    def update_cache(cls, state):
        cls.cache = state

    @classmethod
    def send_updates(cls, state):
        for waiter in cls.waiters:
            waiter.write_message(state)


class BaseHandler(tornado.web.RequestHandler):
    pass


class IndexHandler(BaseHandler):
    def get(self):
        self.render('index.html', state=SocketHandler.cache)


class RQMonitorThread(threading.Thread):
    def __init__(self, host, port=6379, db=0, password=None, *args, **kwargs):
        super(RQMonitorThread, self).__init__(*args, **kwargs)
        self.registered_queues_names = set()
        self.redis_connection = Redis(
            host=host,
            port=port,
            db=db,
            password=password,
        )

    def _get_workers_info(self):
        return sorted(
            [{
                'state': worker.state,
                'name': worker.name,
                'queue_names': ', '.join(worker.queue_names()),
            } for worker in Worker.all(connection=self.redis_connection)],
            key=lambda worker: worker["name"],
        )

    def _get_queues_info(self):
        queues = []
        current_queues_names = set()
        for queue in Queue.all(connection=self.redis_connection):
            queues.append({
                'name': queue.name,
                'jobs_count': len(queue.jobs),
            })
            current_queues_names.add(queue.name)
            self.registered_queues_names.add(queue.name)
        for queue_name in self.registered_queues_names:
            if queue_name not in current_queues_names:
                queues.append({'name': queue_name, 'jobs_count': 0})
        return sorted(queues, key=lambda queue: queue["name"])

    def _get_rq_state(self):
        return {
            'workers': self._get_workers_info(),
            'queues': self._get_queues_info(),
        }

    def run(self):
        while True:
            state = self._get_rq_state()
            SocketHandler.update_cache(state)
            SocketHandler.send_updates(state)
            time.sleep(randint(1, 2))


def _args_parser():
    parser = argparse.ArgumentParser()
    parser.add_argument(
        '--redis-host',
        help='Redis host (default: 127.0.0.1)',
        default='127.0.0.1',
        dest='redis_host',
    )
    parser.add_argument(
        '--redis-port',
        help='Redis port (default: 6379)',
        default=6379,
        dest='redis_port',
        type=int,
    )
    parser.add_argument(
        '--redis-db',
        help='Redis DB number (default: 0)',
        default=0,
        dest='redis_db',
        type=int,
    )
    parser.add_argument(
        '--redis-password',
        help='Redis password',
        default=None,
        dest='redis_password',
    )
    parser.add_argument(
        '--bind-address',
        help='start application on the given address (default: 127.0.0.1)',
        default='127.0.0.1',
        dest='bind_address',
    )
    parser.add_argument(
        '--bind-port',
        help='start application on the given port (default: 7272)',
        default=7272,
        dest='bind_port',
        type=int,
    )
    return parser.parse_args()


def main():
    args = _args_parser()
    app = tornado.web.Application(
        [
            (r"/", IndexHandler),
            (r"/websocket", SocketHandler),
        ],
        template_path=os.path.join(os.path.dirname(__file__), "templates"),
        static_path=os.path.join(os.path.dirname(__file__), "static"),
        debug=False,
    )
    app.listen(args.bind_port, address=args.bind_address)
    monitor = RQMonitorThread(
        name="RQMonitorThread",
        host=args.redis_host,
        port=args.redis_port,
        db=args.redis_db,
        password=args.redis_password,
    )
    monitor.daemon = True
    monitor.start()
    tornado.ioloop.IOLoop.instance().start()


if __name__ == "__main__":
    main()
