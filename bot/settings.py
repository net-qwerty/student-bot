# -*- coding: utf-8 -*-

from environs import Env

env = Env()
env.read_env()

with env.prefixed("BOT_"):
    TOKEN = env.str("TOKEN", default="")