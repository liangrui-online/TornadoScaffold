import os

# server
debug = os.environ.get("example", False)
port = os.environ.get("port", 8200)
user_token_ttl = os.environ.get("user_token_ttl", 24 * 60 * 60)

# mongodb
mongo_uri = os.environ.get("mongo_uri")


# aliyun
aliyun_sms_ak = os.environ.get("aliyun_sms_ak")
aliyun_sms_sk = os.environ.get("aliyun_sms_sk")


#
