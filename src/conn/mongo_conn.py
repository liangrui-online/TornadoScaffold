import motor

import config

mongo_client = motor.motor_tornado.MotorClient(config.mongo_uri)
