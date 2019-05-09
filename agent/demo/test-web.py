import web
import sys


urls = (
  '/', 'index',
  '/add', 'add',
  '/echo/(.*)', 'echo',
  '/webhooks/topic/(.*)/', 'webhooks'
)


class index:
    def GET(self):
        return "Hello, world!"


class add:
    def POST(self):
        i = web.input()
        n = db.insert('todo', title=i.title)
        raise web.seeother('/')


class echo:
    def GET(self, name): return name


class webhooks:
    def GET(self, topic):
        return "Hello, GET! " + topic

    def POST(self):
        return "Hello, POST! " + topic


if __name__ == "__main__": 
    print(len(sys.argv), sys.argv)
    print(globals())
    app = web.application(urls, globals())
    app.run()  

