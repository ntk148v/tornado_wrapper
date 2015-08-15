#!/usr/bin/python
# -*- coding: utf-8 -*-

from tornado.gen import coroutine, Return, Task
import shlex
import time
import tornado.ioloop
from tornado.process import Subprocess


class GeneralSubprocess:
    def __init__(self, id, cmd):
        self.pipe = None
        self.id = id
        self.cmd = cmd
        self.start = None
        self.end = None

    @coroutine
    def run_process(self):
        self.pipe = Subprocess(shlex.split(self.cmd),
                               stdout=Subprocess.STREAM,
                               stderr=Subprocess.STREAM)
        self.start = time.time()
        (out, err) = (yield [Task(self.pipe.stdout.read_until_close),
                             Task(self.pipe.stderr.read_until_close)])
        return (out, err)

    def stat(self):
        self.pipe.poll()
        if self.pipe.returncode is not None:
            self.end = time.time()
            print('Done time : %f', self.end - self.start)
        else:
            print('Not done yet')
