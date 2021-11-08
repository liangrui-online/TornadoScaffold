import json
import traceback
from typing import Any, Optional, Union

import tornado.web
import tornado.httputil

from src.utils.log_tools import logger
from src.utils.password_tools import parse_token


class EasyHandler(tornado.web.RequestHandler):
    def __init__(
        self,
        application: tornado.web.Application,
        request: tornado.httputil.HTTPServerRequest,
        **kwargs: Any,
    ):
        super().__init__(application, request, **kwargs)

    async def prepare(self):
        logger.debug(
            f"[HttpRequest] {self.request.remote_ip} {self.request.method} {self.request.uri}"
        )

        if self.request.query_arguments:
            logger.debug(f"[HttpRequestQueryArgs] {self.request.query_arguments}")

        if self.request.body and "json" in self.request.headers.get("Content-Type", ""):
            logger.debug(f"[HttpRequestBody] {json.loads(self.request.body)}")

    def data_received(self, chunk):
        pass

    def write_error(self, status_code: int, **kwargs):
        if "exc_info" in kwargs:
            e_type, e_value, tb = kwargs["exc_info"]

            self.set_status(status_code=400)
            if "status_code" in e_value.__dict__.keys() and e_value.status_code in (
                401,
                403,
                404,
                405,
                400,
            ):
                self.set_status(status_code=status_code)

            if isinstance(e_value, AssertionError):
                err_data = {
                    "code": 400,
                    "message": e_value.args[0],
                }
            else:
                error_message = (
                    f"{traceback.format_exception(etype=e_type, value=e_value, tb=tb)}"
                )
                err_data = {
                    "code": 500,
                    "message": "未知错误",
                    "errorMessage": error_message,
                }
                logger.warning(
                    traceback.format_exception(etype=e_type, value=e_value, tb=tb)
                )

            self.write(err_data)
        super().write_error(status_code, **kwargs)

    @logger.catch
    def get_json_params(self):
        """获取json参数并转化为dict"""
        assert self.request.headers.get("Content-Type", "").startswith(
            "application/json"
        ), "请求内容非json格式"
        request_body = self.request.body or "{}"
        return json.loads(request_body)

    @property
    def json_params(self):
        if not hasattr(self, "_json_params"):
            self._json_params = self.get_json_params()
        return self._json_params

    def write_response(
        self,
        status_code: int,
        body: Union[str, bytes, dict, None] = None,
        reason: Optional[str] = None,
        update_headers: dict = None,
    ):
        # 设置响应状态
        self.set_status(status_code=status_code, reason=reason)

        # 设置请求头
        if update_headers and isinstance(update_headers, dict):
            for n, v in update_headers.items():
                self.set_header(n, v)

        # 写响应体
        self.finish(body)

    def write_json_response(self, status_code, body: dict, reason=None):
        assert body and isinstance(body, dict)
        if status_code >= 400:
            body = body or {}
            if not body.get("data", None):
                body["data"] = {}
            if not isinstance(body["data"], dict):
                body["data"] = {"detail": body["data"]}
        self.write_response(
            status_code,
            reason=reason,
            body=body,
            update_headers={"Content-Type": "application/json"},
        )

    def set_default_headers(self):
        """
        config.headers['Locale'] = getLocale();
         :return:
        """
        headers = (
            "Authorization, Content-Type, Depth, User-Agent, X-File-Size, X-Requested-With, X-Requested-By,"
            "If-Modified-Since, X-File-Name, X-File-Type, Cache-Control, Origin, Locale, "
            "Access-Control-Allow-Headers, access-control-request-headers, Accept, "
            "Access-Control-Request-Method, Access-Control-Request-Headers, "
            "authorization, Access-Control-Allow-Credentials, X-Auth-Token, X-Accept-Charset, X-Accept, "
            "x-lins-merchantid, X-LINS-MERCHANTID, *"
        )
        origin = (
            self.request.headers.get("origin")
            or self.request.headers.get("Origin")
            or self.request.headers.get("ORIGIN")
        )

        self.set_header("Access-Control-Allow-Credentials", "true")
        self.set_header("Access-Control-Allow-Origin", origin or "*")
        self.set_header("Access-Control-Allow-Headers", headers)
        self.set_header(
            "Access-Control-Allow-Methods", "POST, GET, OPTIONS, PUT, DELETE"
        )

    def options(self, *args, **kwargs):
        """

        :param args:
        :param kwargs:
        :return:
        """
        self.set_status(204)
        self.finish()

    def write_200_json_response(self, body=None):
        """200 Ok 返回给前端的数据

        :param body: 返回给前端的数据
        :return:
        """
        if body is None:
            body = {}

        if not all(["code" in body, "message" in body]):
            body = {
                "code": 0,
                "message": "ok",
                "data": body,
            }
        self.write_json_response(status_code=200, body=body)

    def write_400_json_response(self, code=400, message=None, body=None):
        self.write_json_response(
            status_code=400,
            reason=message,
            body={"code": code, "message": message, "data": body},
        )

    def write_401_json_response(self, code=401, message="登陆状态已失效，请重新登陆！"):
        self.write_json_response(
            status_code=401, body={"code": code, "message": message}
        )

    def write_403_json_response(self, code=403, message=None):
        message = message or "暂无权限，请联系管理员!"
        self.write_json_response(
            status_code=403, body={"code": code, "message": message}
        )

    def write_404_json_response(self, code=404, message=None):
        message = message or "资源不存在"
        self.write_json_response(
            status_code=403, body={"code": code, "message": message}
        )

    def write_500_json_response(self, code=500, message="未知错误，请刷新后重试！"):
        self.write_json_response(
            status_code=500,
            reason=message,
            body={
                "code": code,
                "message": message,
            },
        )


# class AuthBaseHandler(EasyHandler):
#     def get_current_user(self) -> Any:
#         token = self.request.headers.get("Authorization", "")
#         m = re.match(r"^Bearer (.*)$", token)
#         if not m:
#             return None
#         token = m.group(1)
#         payload = parse_token(token)
#         if payload.get("role") == UserStatus.DISABLED:
#             logger.warning(f"禁用用户{payload['username']}尝试登陆，已阻止")
#             return None
#         # FIXME: 这里其实需要查数据库判断用户信息是否有变更
#         return payload
#
#     def get_login_url(self) -> str:
#         return "/api/users/loginRequest"
