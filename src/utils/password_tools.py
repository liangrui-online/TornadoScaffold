import itsdangerous
from passlib.hash import pbkdf2_sha256

import config

token_helper = itsdangerous.TimedJSONWebSignatureSerializer(
    secret_key="de;lkokasdf,,z.xmcvadf", expires_in=config.user_token_ttl
)


# 生成用于存入数据库的用户密码
def gen_passwd(raw_password: str):
    return pbkdf2_sha256.hash(raw_password)


# 校验登陆密码是否与数据库中的密码吻合
def verify_passwd(raw_password: str, password_in_db: str):
    return pbkdf2_sha256.verify(raw_password, password_in_db)


# 生成登陆用的token
def gen_token(data):
    return token_helper.dumps(data).decode()


# 解析token
def parse_token(token):
    try:
        return token_helper.loads(token)
    except itsdangerous.exc.BadSignature:
        return {}
