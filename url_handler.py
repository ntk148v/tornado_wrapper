from tornado.web import RequestHandler
from general_subprocess import GeneralSubprocess
from tornado.gen import coroutine, Task, Return
import tornado.web

tasks = {}


class ConfigHandler(RequestHandler):
    # def initialize(self):
    #     self.id = 0

    def get(self, id):
        # self.id = self.id + 1
        self.render("config.html", id=id)


class StartHandler(RequestHandler):
    def initialize(self):
        self.process = None

    @coroutine
    def post(self, id):
        # id = self.get_argument('id')
        cmd = self.get_argument('cmd').strip() + ' ' + self.get_argument('option').strip() \
              + ' ' + self.get_argument('file').strip()
        self.process = GeneralSubprocess(1, cmd)
        global tasks
        tasks[id] = self.process.run_process()
        self.render("start.html", id=id)


class DoneHandler(RequestHandler):
    @coroutine
    def get(self, id):
        if id:
            out, err = '',''
            task_run_process = tasks.get(id, False)
            if task_run_process.done():
                out, err = yield task_run_process
                stat = "Process Done"
            else:
                stat = "Process Not Done Yet"
            self.render("done.html", id=id, stat=stat, out=out, err=err)
        else:
            raise tornado.web.HTTPError(404)
