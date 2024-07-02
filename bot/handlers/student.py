import settings
from aiogram import Bot, F, Router, types
from aiogram.filters import Command, CommandStart, StateFilter, or_f
from filters.chat_types import ChatTypeFilter, IsStudent
from jinja2 import Environment, FileSystemLoader

student_router = Router()
student_router.message.filter(ChatTypeFilter(["private"]), IsStudent())


env = Environment(loader=FileSystemLoader("bot/templates/"), lstrip_blocks=True)
