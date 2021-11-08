from src.utils.req_handler_tools import EasyHandler


class HelloWorldHandler(EasyHandler):
    async def get(self):
        self.write_200_json_response({"text": "hello world"})
