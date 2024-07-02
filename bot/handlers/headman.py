import settings
from aiogram import Bot, F, Router, types
from aiogram.filters import Command, CommandStart, StateFilter, or_f
from filters.chat_types import ChatTypeFilter
from jinja2 import Environment, FileSystemLoader



headman_router = Router()
headman_router.message.filter(ChatTypeFilter(["private"]))

env = Environment(loader=FileSystemLoader("bot/templates/"), lstrip_blocks=True)