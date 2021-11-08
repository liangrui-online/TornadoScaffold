from src.views.example.hello_world import HelloWorldHandler
from src.views.ws import WsHandler


routes = [
    (r"/example/hello-world", HelloWorldHandler),
    (r"/ws", WsHandler),  # websocket

]
