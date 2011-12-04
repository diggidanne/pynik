import json
import inspect
import websocket
import plugins.commands

import plugin_handler
plugin_handler.plugins_on_load()

class WebSocketBot(object):
    def __init__(self, url, port, nick):
        self.url = url
        self.port = port
        self.nick = nick

    def on_message(self, ws, data):
        # Loop through plugins
        dictdata = json.loads(data)
        message = dictdata["MESSAGE"]
        if not message.startswith("."):
            return
        if dictdata["SENDER"] == self.nick:
            return
        trigger = message.split(" ")[0][1:]
        args = " ".join(message.split(" ")[1:])
        method_name = "trig_"+trigger.lower()
        for command in plugins.commands.Command.__subclasses__():
            methods = inspect.getmembers(command.instance)
            methodmatches = [m for m in methods if m[0] == method_name]
            if len(methodmatches) == 1:
                method = command.instance.__getattribute__(method_name)
                d = method.__call__("bot", "source", "target", trigger, args)
                ws.send(d)


    def on_error(self, ws, error):
        print "Error", error

    def on_close(self, ws):
        print "close"

    def on_open(self, ws):
        self.ws.send("/name " + self.nick)

    def run(self):
        hostname = "ws://%s:%s/chat" % (self.url, self.port)
        self.ws = websocket.WebSocketApp(hostname,
                                         on_message = self.on_message,
                                         on_error = self.on_error,
                                         on_close = self.on_close,
                                         on_open = self.on_open)
        self.ws.run_forever()
