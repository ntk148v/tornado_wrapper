from url_handler import StartHandler, DoneHandler, ConfigHandler
import tornado.httpserver
import tornado.web
import setting


class Application(tornado.web.Application):
    def __init__(self):
        handlers = [
            (r"/config/([0-9]+)", ConfigHandler),
            (r"/start/([0-9]+)", StartHandler),
            (r"/done/([0-9]+)", DoneHandler),
        ]

        settings = {
            "template_path": setting.TEMPLATE_PATH,
            "static_path": setting.STATIC_PATH,
            "debug": setting.DEBUG,
        }

        tornado.web.Application.__init__(self, handlers, **settings)


def main():
    app = Application()

    http_server = tornado.httpserver.HTTPServer(app)
    http_server.listen(8888)
    tornado.ioloop.IOLoop.instance().start()


if __name__ == '__main__':
    main()
